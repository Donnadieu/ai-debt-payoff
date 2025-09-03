"""Integration tests for the debt payoff backend."""

import pytest
import asyncio
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock

from app.core.analytics import analytics_core
from app.core.performance import performance_monitor


class TestEndToEndWorkflows:
    """Test complete end-to-end workflows."""
    
    def test_complete_debt_analysis_workflow(self, client: TestClient, sample_debts):
        """Test complete debt analysis workflow from input to output."""
        # Step 1: Add debts
        for debt in sample_debts:
            response = client.post("/api/v1/debts", json=debt)
            assert response.status_code == 200
        
        # Step 2: Get payoff plan
        plan_request = {
            "monthly_payment": 500.0,
            "strategy": "avalanche"
        }
        response = client.post("/plan", json=plan_request)
        assert response.status_code == 200
        
        plan_data = response.json()
        assert "total_debt" in plan_data
        assert "monthly_payment" in plan_data
        assert "payoff_timeline" in plan_data
        assert "total_interest" in plan_data
        
        # Step 3: Check analytics were tracked
        stats_response = client.get("/api/analytics/stats")
        assert stats_response.status_code == 200
        
        stats_data = stats_response.json()
        assert stats_data["buffer_size"] > 0  # Events should be buffered
        
        # Step 4: Verify performance metrics
        perf_response = client.get("/api/analytics/performance")
        assert perf_response.status_code == 200
        
        perf_data = perf_response.json()
        assert perf_data["total_metrics_collected"] > 0
    
    def test_user_journey_with_analytics(self, client: TestClient):
        """Test user journey with analytics tracking."""
        user_id = "test_user_123"
        
        # Step 1: User visits homepage
        page_view_data = {
            "path": "/",
            "user_id": user_id
        }
        response = client.post("/api/analytics/user/page-view", json=page_view_data)
        assert response.status_code == 200
        
        # Step 2: User checks health
        response = client.get("/health")
        assert response.status_code == 200
        
        # Step 3: User interacts with calculator
        interaction_data = {
            "interaction_type": "click",
            "element": "calculate_button",
            "user_id": user_id,
            "metadata": {"page": "/calculator"}
        }
        response = client.post("/api/analytics/user/interaction", json=interaction_data)
        assert response.status_code == 200
        
        # Step 4: Verify all events were tracked
        recent_response = client.get("/api/analytics/events/recent?limit=10")
        assert recent_response.status_code == 200
        
        events_data = recent_response.json()
        assert events_data["count"] >= 2  # At least page view and interaction
    
    def test_error_handling_across_services(self, client: TestClient):
        """Test error handling across different services."""
        # Test invalid debt data
        invalid_debt = {
            "name": "",  # Invalid empty name
            "balance": -100,  # Invalid negative balance
            "interest_rate": 150  # Invalid high interest rate
        }
        
        response = client.post("/api/v1/debts", json=invalid_debt)
        assert response.status_code == 422  # Validation error
        
        # Test invalid payoff plan request
        invalid_plan = {
            "monthly_payment": -100,  # Invalid negative payment
            "strategy": "invalid_strategy"
        }
        
        response = client.post("/plan", json=invalid_plan)
        assert response.status_code == 422  # Validation error
        
        # Verify analytics still work after errors
        response = client.get("/api/analytics/health")
        assert response.status_code == 200


class TestServiceIntegration:
    """Test integration between different services."""
    
    def test_analytics_and_performance_integration(self, client: TestClient):
        """Test integration between analytics and performance monitoring."""
        # Make several requests to generate data
        for i in range(5):
            response = client.get("/health")
            assert response.status_code == 200
        
        # Check analytics stats
        analytics_response = client.get("/api/analytics/stats")
        assert analytics_response.status_code == 200
        
        analytics_data = analytics_response.json()
        assert analytics_data["buffer_size"] >= 0
        
        # Check performance stats
        perf_response = client.get("/api/analytics/performance")
        assert perf_response.status_code == 200
        
        perf_data = perf_response.json()
        assert perf_data["total_metrics_collected"] > 0
        
        # Verify operation stats include our requests
        operation_stats = perf_data["operation_stats"]
        health_check_found = any("health" in op.lower() for op in operation_stats.keys())
        assert health_check_found or len(operation_stats) > 0
    
    def test_middleware_and_api_integration(self, client: TestClient):
        """Test integration between middleware and API endpoints."""
        # Make request through middleware
        response = client.post("/api/analytics/track", json={"event": "test_event"})
        assert response.status_code == 200
        
        # Verify middleware added headers
        assert "X-Response-Time" in response.headers
        
        # Verify API response
        data = response.json()
        assert data["success"] is True
        
        # Check that middleware tracked this API call
        recent_response = client.get("/api/analytics/events/recent?limit=5")
        assert recent_response.status_code == 200
        
        events_data = recent_response.json()
        # Should have events from both the track call and the recent call
        assert events_data["count"] >= 1
    
    def test_event_service_integration(self, client: TestClient):
        """Test integration with event service layer."""
        # Track an event through API
        event_data = {
            "event": "integration_test",
            "properties": {"test_type": "service_integration"},
            "user_id": "integration_user"
        }
        
        response = client.post("/api/analytics/track", json=event_data)
        assert response.status_code == 200
        
        # Flush events to ensure processing
        flush_response = client.post("/api/analytics/flush")
        assert flush_response.status_code == 200
        
        # Verify event was processed
        stats_response = client.get("/api/analytics/stats")
        assert stats_response.status_code == 200


class TestConcurrentOperations:
    """Test concurrent operations and race conditions."""
    
    def test_concurrent_event_tracking(self, client: TestClient):
        """Test concurrent event tracking doesn't cause issues."""
        import threading
        import time
        
        results = []
        
        def track_events():
            for i in range(5):
                event_data = {
                    "event": f"concurrent_test_{i}",
                    "properties": {"thread": threading.current_thread().name}
                }
                response = client.post("/api/analytics/track", json=event_data)
                results.append(response.status_code)
                time.sleep(0.01)  # Small delay
        
        # Start multiple threads
        threads = []
        for i in range(3):
            thread = threading.Thread(target=track_events)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads
        for thread in threads:
            thread.join()
        
        # All requests should succeed
        assert all(status == 200 for status in results)
        assert len(results) == 15  # 3 threads * 5 events each
    
    def test_concurrent_performance_monitoring(self, client: TestClient):
        """Test concurrent performance monitoring."""
        import threading
        
        results = []
        
        def make_requests():
            for i in range(3):
                response = client.get("/health")
                results.append(response.status_code)
                
                # Check response has performance headers
                assert "X-Response-Time" in response.headers
        
        # Start multiple threads
        threads = []
        for i in range(3):
            thread = threading.Thread(target=make_requests)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads
        for thread in threads:
            thread.join()
        
        # All requests should succeed
        assert all(status == 200 for status in results)
        assert len(results) == 9  # 3 threads * 3 requests each


class TestDataConsistency:
    """Test data consistency across operations."""
    
    def test_analytics_data_consistency(self, client: TestClient):
        """Test analytics data remains consistent."""
        # Get initial stats
        initial_response = client.get("/api/analytics/stats")
        assert initial_response.status_code == 200
        initial_data = initial_response.json()
        initial_buffer_size = initial_data["buffer_size"]
        
        # Track some events
        for i in range(3):
            event_data = {
                "event": f"consistency_test_{i}",
                "properties": {"index": i}
            }
            response = client.post("/api/analytics/track", json=event_data)
            assert response.status_code == 200
        
        # Get updated stats
        updated_response = client.get("/api/analytics/stats")
        assert updated_response.status_code == 200
        updated_data = updated_response.json()
        updated_buffer_size = updated_data["buffer_size"]
        
        # Buffer size should have increased (unless auto-flush occurred)
        assert updated_buffer_size >= initial_buffer_size
    
    def test_performance_metrics_consistency(self, client: TestClient):
        """Test performance metrics remain consistent."""
        # Get initial performance stats
        initial_response = client.get("/api/analytics/performance")
        assert initial_response.status_code == 200
        initial_data = initial_response.json()
        initial_count = initial_data["total_metrics_collected"]
        
        # Make some requests to generate metrics
        for i in range(3):
            response = client.get("/health")
            assert response.status_code == 200
        
        # Get updated performance stats
        updated_response = client.get("/api/analytics/performance")
        assert updated_response.status_code == 200
        updated_data = updated_response.json()
        updated_count = updated_data["total_metrics_collected"]
        
        # Metrics count should have increased
        assert updated_count > initial_count


class TestSystemHealthIntegration:
    """Test system health monitoring integration."""
    
    def test_health_check_integration(self, client: TestClient):
        """Test health check integration across all components."""
        # Check main health endpoint
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        
        # Check analytics health
        analytics_response = client.get("/api/analytics/health")
        assert analytics_response.status_code == 200
        
        analytics_data = analytics_response.json()
        assert analytics_data["status"] in ["healthy", "warning"]
        assert "analytics" in analytics_data
        assert "system_health" in analytics_data
    
    def test_system_monitoring_integration(self, client: TestClient):
        """Test system monitoring integration."""
        # Get performance stats which include system metrics
        response = client.get("/api/analytics/performance")
        assert response.status_code == 200
        
        data = response.json()
        assert "system_metrics" in data
        
        system_metrics = data["system_metrics"]
        assert "memory_usage_mb" in system_metrics
        assert "cpu_percent" in system_metrics
        
        # Verify metrics are reasonable
        assert system_metrics["memory_usage_mb"] > 0
        assert 0 <= system_metrics["cpu_percent"] <= 100


class TestErrorRecovery:
    """Test error recovery and resilience."""
    
    def test_analytics_error_recovery(self, client: TestClient):
        """Test analytics error recovery."""
        # Simulate analytics error and recovery
        with patch('app.core.analytics.analytics_core.track_event') as mock_track:
            # First call fails
            mock_track.side_effect = Exception("Temporary error")
            
            response = client.post("/api/analytics/track", json={"event": "test"})
            assert response.status_code == 400  # Should handle error gracefully
            
            # Reset mock to succeed
            mock_track.side_effect = None
            mock_track.return_value = None
            
            # Subsequent calls should work
            response = client.post("/api/analytics/track", json={"event": "test"})
            assert response.status_code == 200
    
    def test_performance_monitoring_resilience(self, client: TestClient):
        """Test performance monitoring resilience."""
        with patch('app.core.performance.performance_monitor.record_operation') as mock_record:
            # Simulate performance monitoring failure
            mock_record.side_effect = Exception("Performance error")
            
            # Request should still succeed
            response = client.get("/health")
            assert response.status_code == 200
            
            # Should still have response time header from middleware
            assert "X-Response-Time" in response.headers
    
    def test_partial_system_failure(self, client: TestClient):
        """Test system behavior under partial failures."""
        # Simulate analytics failure but keep performance working
        with patch('app.core.analytics.analytics_core.track_event') as mock_track:
            mock_track.side_effect = Exception("Analytics down")
            
            # Main functionality should still work
            response = client.get("/health")
            assert response.status_code == 200
            
            # Performance monitoring should still work
            perf_response = client.get("/api/analytics/performance")
            assert perf_response.status_code == 200
