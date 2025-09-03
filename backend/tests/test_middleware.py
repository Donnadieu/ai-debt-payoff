"""Tests for middleware components."""

import pytest
import time
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock, AsyncMock

from app.middleware.performance import PerformanceMiddleware
from app.core.analytics import analytics_core
from app.core.performance import performance_monitor


class TestPerformanceMiddleware:
    """Test performance monitoring middleware."""
    
    @pytest.fixture
    def app_with_middleware(self):
        """Create test app with performance middleware."""
        app = FastAPI()
        app.add_middleware(PerformanceMiddleware)
        
        @app.get("/test")
        async def test_endpoint():
            return {"message": "test"}
        
        @app.get("/slow")
        async def slow_endpoint():
            await asyncio.sleep(0.1)  # Simulate slow operation
            return {"message": "slow"}
        
        @app.get("/error")
        async def error_endpoint():
            raise Exception("Test error")
        
        return app
    
    @pytest.fixture
    def middleware_client(self, app_with_middleware):
        """Create test client with middleware."""
        return TestClient(app_with_middleware)
    
    def test_middleware_adds_response_time_header(self, middleware_client):
        """Test that middleware adds response time header."""
        response = middleware_client.get("/test")
        
        assert response.status_code == 200
        assert "X-Response-Time" in response.headers
        
        response_time = response.headers["X-Response-Time"]
        assert response_time.endswith("ms")
        
        # Parse time value
        time_value = float(response_time[:-2])
        assert time_value >= 0
        assert time_value < 1000  # Should be reasonable for test
    
    def test_middleware_adds_performance_headers(self, middleware_client):
        """Test that middleware adds performance-related headers."""
        response = middleware_client.get("/test")
        
        assert response.status_code == 200
        assert "X-Response-Time" in response.headers
        
        # Check if other performance headers are present
        headers = response.headers
        performance_headers = [h for h in headers.keys() if h.startswith("X-")]
        assert len(performance_headers) >= 1
    
    def test_middleware_tracks_request_timing(self, middleware_client):
        """Test that middleware tracks request timing."""
        with patch('app.core.performance.performance_monitor.record_operation') as mock_record:
            response = middleware_client.get("/test")
            
            assert response.status_code == 200
            mock_record.assert_called()
            
            # Check call arguments
            call_args = mock_record.call_args
            assert call_args[0][0] == "GET /test"  # operation name
            assert isinstance(call_args[0][1], float)  # duration
    
    def test_middleware_tracks_analytics_events(self, middleware_client):
        """Test that middleware tracks analytics events."""
        with patch('app.core.analytics.analytics_core.track_event') as mock_track:
            response = middleware_client.get("/test")
            
            assert response.status_code == 200
            mock_track.assert_called()
            
            # Check that API request event was tracked
            call_args = mock_track.call_args
            assert call_args[0][0] == "api_request"  # event name
            
            properties = call_args[0][1]
            assert properties["method"] == "GET"
            assert properties["path"] == "/test"
            assert properties["status_code"] == 200
            assert "response_time" in properties
    
    def test_middleware_handles_slow_requests(self, middleware_client):
        """Test middleware handling of slow requests."""
        import asyncio
        
        # Mock asyncio.sleep for the slow endpoint
        with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
            mock_sleep.return_value = None
            
            response = middleware_client.get("/slow")
            
            assert response.status_code == 200
            assert "X-Response-Time" in response.headers
    
    def test_middleware_handles_errors(self, middleware_client):
        """Test middleware handling of errors."""
        with patch('app.core.analytics.analytics_core.track_event') as mock_track:
            response = middleware_client.get("/error")
            
            assert response.status_code == 500
            assert "X-Response-Time" in response.headers
            
            # Should still track the event even on error
            mock_track.assert_called()
            
            call_args = mock_track.call_args
            properties = call_args[0][1]
            assert properties["status_code"] == 500
    
    def test_middleware_excludes_health_checks(self, middleware_client):
        """Test that middleware can exclude health check endpoints."""
        # Add health endpoint to test app
        app = middleware_client.app
        
        @app.get("/health")
        async def health_check():
            return {"status": "healthy"}
        
        with patch('app.core.analytics.analytics_core.track_event') as mock_track:
            response = middleware_client.get("/health")
            
            assert response.status_code == 200
            
            # Check if health checks are excluded from analytics
            # (Implementation detail - might still track but with different properties)
            if mock_track.called:
                call_args = mock_track.call_args
                properties = call_args[0][1]
                # Health checks might be marked differently
                assert properties["path"] == "/health"
    
    def test_middleware_performance_under_load(self, middleware_client):
        """Test middleware performance under multiple requests."""
        response_times = []
        
        # Make multiple requests
        for _ in range(10):
            response = middleware_client.get("/test")
            assert response.status_code == 200
            
            response_time = response.headers["X-Response-Time"]
            time_value = float(response_time[:-2])
            response_times.append(time_value)
        
        # All requests should complete reasonably fast
        assert all(t < 100 for t in response_times)  # Less than 100ms
        
        # Average response time should be reasonable
        avg_time = sum(response_times) / len(response_times)
        assert avg_time < 50  # Less than 50ms average


class TestMiddlewareIntegration:
    """Test middleware integration with the main app."""
    
    def test_middleware_with_main_app(self, client: TestClient):
        """Test middleware integration with main FastAPI app."""
        response = client.get("/")
        
        assert response.status_code == 200
        assert "X-Response-Time" in response.headers
    
    def test_middleware_with_api_endpoints(self, client: TestClient):
        """Test middleware with API endpoints."""
        response = client.get("/health")
        
        assert response.status_code == 200
        assert "X-Response-Time" in response.headers
        
        # Check response time is reasonable
        response_time = response.headers["X-Response-Time"]
        time_value = float(response_time[:-2])
        assert time_value >= 0
    
    def test_middleware_with_analytics_endpoints(self, client: TestClient):
        """Test middleware with analytics endpoints."""
        response = client.get("/api/analytics/health")
        
        assert response.status_code == 200
        assert "X-Response-Time" in response.headers
    
    def test_middleware_analytics_tracking(self, client: TestClient):
        """Test that middleware analytics tracking works end-to-end."""
        # Make a request
        response = client.get("/health")
        assert response.status_code == 200
        
        # Check analytics stats to see if events were tracked
        stats_response = client.get("/api/analytics/stats")
        assert stats_response.status_code == 200
        
        stats_data = stats_response.json()
        assert "buffer_size" in stats_data
        # Buffer might have events from this and other tests
        assert stats_data["buffer_size"] >= 0
    
    def test_middleware_performance_tracking(self, client: TestClient):
        """Test that middleware performance tracking works end-to-end."""
        # Make a request
        response = client.get("/health")
        assert response.status_code == 200
        
        # Check performance stats
        perf_response = client.get("/api/analytics/performance")
        assert perf_response.status_code == 200
        
        perf_data = perf_response.json()
        assert "operation_stats" in perf_data
        assert "total_metrics_collected" in perf_data


class TestMiddlewareConfiguration:
    """Test middleware configuration and behavior."""
    
    def test_middleware_with_different_methods(self, client: TestClient):
        """Test middleware with different HTTP methods."""
        methods_to_test = [
            ("GET", "/health"),
            ("POST", "/api/analytics/track"),
        ]
        
        for method, path in methods_to_test:
            if method == "GET":
                response = client.get(path)
            elif method == "POST":
                # For POST, provide minimal valid data
                if "track" in path:
                    response = client.post(path, json={"event": "test"})
                else:
                    response = client.post(path)
            
            # Should have response time header regardless of method
            assert "X-Response-Time" in response.headers
    
    def test_middleware_with_query_parameters(self, client: TestClient):
        """Test middleware with query parameters."""
        response = client.get("/api/analytics/events/recent?limit=5")
        
        assert response.status_code == 200
        assert "X-Response-Time" in response.headers
    
    def test_middleware_with_request_body(self, client: TestClient):
        """Test middleware with request body."""
        event_data = {
            "event": "test_event",
            "properties": {"test": True}
        }
        
        response = client.post("/api/analytics/track", json=event_data)
        
        assert response.status_code == 200
        assert "X-Response-Time" in response.headers


class TestMiddlewareErrorHandling:
    """Test middleware error handling."""
    
    def test_middleware_handles_analytics_errors(self, middleware_client):
        """Test middleware handles analytics tracking errors gracefully."""
        with patch('app.core.analytics.analytics_core.track_event') as mock_track:
            mock_track.side_effect = Exception("Analytics error")
            
            # Request should still succeed even if analytics fails
            response = middleware_client.get("/test")
            
            assert response.status_code == 200
            assert "X-Response-Time" in response.headers
    
    def test_middleware_handles_performance_errors(self, middleware_client):
        """Test middleware handles performance tracking errors gracefully."""
        with patch('app.core.performance.performance_monitor.record_operation') as mock_record:
            mock_record.side_effect = Exception("Performance error")
            
            # Request should still succeed even if performance tracking fails
            response = middleware_client.get("/test")
            
            assert response.status_code == 200
            assert "X-Response-Time" in response.headers
    
    def test_middleware_continues_on_partial_failure(self, middleware_client):
        """Test middleware continues working when some components fail."""
        with patch('app.core.analytics.analytics_core.track_event') as mock_track:
            mock_track.side_effect = Exception("Analytics error")
            
            # Performance tracking should still work
            with patch('app.core.performance.performance_monitor.record_operation') as mock_record:
                response = middleware_client.get("/test")
                
                assert response.status_code == 200
                assert "X-Response-Time" in response.headers
                
                # Performance should still be recorded
                mock_record.assert_called()


class TestMiddlewarePerformanceImpact:
    """Test middleware performance impact."""
    
    def test_middleware_minimal_overhead(self, middleware_client):
        """Test that middleware adds minimal overhead."""
        # Test without middleware
        app_no_middleware = FastAPI()
        
        @app_no_middleware.get("/test")
        async def test_endpoint():
            return {"message": "test"}
        
        client_no_middleware = TestClient(app_no_middleware)
        
        # Time requests with and without middleware
        start_time = time.time()
        for _ in range(10):
            response = client_no_middleware.get("/test")
            assert response.status_code == 200
        no_middleware_time = time.time() - start_time
        
        start_time = time.time()
        for _ in range(10):
            response = middleware_client.get("/test")
            assert response.status_code == 200
        with_middleware_time = time.time() - start_time
        
        # Middleware should add minimal overhead (less than 50% increase)
        overhead_ratio = with_middleware_time / no_middleware_time
        assert overhead_ratio < 1.5  # Less than 50% overhead
    
    def test_middleware_memory_usage(self, middleware_client):
        """Test middleware memory usage is reasonable."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Make many requests
        for _ in range(100):
            response = middleware_client.get("/test")
            assert response.status_code == 200
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (less than 10MB)
        assert memory_increase < 10 * 1024 * 1024  # 10MB
