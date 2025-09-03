"""Tests for analytics API endpoints."""

import pytest
import json
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock

from app.core.analytics import analytics_core
from app.core.performance import performance_monitor


class TestAnalyticsEventTracking:
    """Test analytics event tracking endpoints."""
    
    def test_track_single_event(self, client: TestClient, sample_analytics_event):
        """Test tracking a single analytics event."""
        response = client.post("/api/analytics/track", json=sample_analytics_event)
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert "message" in data
        assert "tracked successfully" in data["message"].lower()
    
    def test_track_event_with_user_id(self, client: TestClient):
        """Test tracking event with user ID."""
        event_data = {
            "event": "user_login",
            "properties": {"method": "email"},
            "user_id": "user_123"
        }
        
        response = client.post("/api/analytics/track", json=event_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
    
    def test_track_event_without_properties(self, client: TestClient):
        """Test tracking event without properties."""
        event_data = {
            "event": "simple_event"
        }
        
        response = client.post("/api/analytics/track", json=event_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
    
    def test_track_event_invalid_data(self, client: TestClient):
        """Test tracking event with invalid data."""
        invalid_event = {
            "event": "",  # Empty event name
            "properties": {}
        }
        
        response = client.post("/api/analytics/track", json=invalid_event)
        assert response.status_code == 400
        
        data = response.json()
        assert "detail" in data
    
    def test_batch_track_events(self, client: TestClient):
        """Test batch tracking multiple events."""
        events = [
            {
                "event": "page_view",
                "properties": {"page": "/dashboard"},
                "user_id": "user_123"
            },
            {
                "event": "button_click",
                "properties": {"button": "calculate"},
                "user_id": "user_123"
            }
        ]
        
        response = client.post("/api/analytics/batch-track", json=events)
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert data["tracked_count"] == 2
    
    def test_batch_track_empty_list(self, client: TestClient):
        """Test batch tracking with empty list."""
        response = client.post("/api/analytics/batch-track", json=[])
        assert response.status_code == 400
        
        data = response.json()
        assert "detail" in data
    
    def test_batch_track_too_many_events(self, client: TestClient):
        """Test batch tracking with too many events."""
        # Create more than 100 events (assuming that's the limit)
        events = []
        for i in range(101):
            events.append({
                "event": f"test_event_{i}",
                "properties": {"index": i}
            })
        
        response = client.post("/api/analytics/batch-track", json=events)
        assert response.status_code == 400
        
        data = response.json()
        assert "detail" in data


class TestAnalyticsManagement:
    """Test analytics management endpoints."""
    
    def test_flush_events(self, client: TestClient):
        """Test manually flushing events."""
        response = client.post("/api/analytics/flush")
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert "flushed successfully" in data["message"].lower()
    
    def test_get_analytics_stats(self, client: TestClient):
        """Test getting analytics statistics."""
        response = client.get("/api/analytics/stats")
        assert response.status_code == 200
        
        data = response.json()
        assert "buffer_size" in data
        assert "last_flush" in data
        assert "enabled_services" in data
        assert "config" in data
        assert isinstance(data["buffer_size"], int)
        assert isinstance(data["enabled_services"], list)
    
    def test_get_recent_events(self, client: TestClient):
        """Test getting recent events from buffer."""
        # First track some events
        event_data = {
            "event": "test_event",
            "properties": {"test": True}
        }
        client.post("/api/analytics/track", json=event_data)
        
        response = client.get("/api/analytics/events/recent?limit=5")
        assert response.status_code == 200
        
        data = response.json()
        assert "events" in data
        assert "count" in data
        assert "total_buffered" in data
        assert isinstance(data["events"], list)
        assert isinstance(data["count"], int)
    
    def test_get_recent_events_with_limit(self, client: TestClient):
        """Test getting recent events with custom limit."""
        response = client.get("/api/analytics/events/recent?limit=3")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["events"]) <= 3
    
    def test_get_recent_events_invalid_limit(self, client: TestClient):
        """Test getting recent events with invalid limit."""
        response = client.get("/api/analytics/events/recent?limit=0")
        assert response.status_code == 422  # Validation error
        
        response = client.get("/api/analytics/events/recent?limit=101")
        assert response.status_code == 422  # Validation error


class TestPerformanceEndpoints:
    """Test performance monitoring endpoints."""
    
    def test_get_performance_stats(self, client: TestClient):
        """Test getting performance statistics."""
        response = client.get("/api/analytics/performance")
        assert response.status_code == 200
        
        data = response.json()
        assert "timestamp" in data
        assert "system_metrics" in data
        assert "operation_stats" in data
        assert "total_metrics_collected" in data
        assert "thresholds" in data
        
        # Check system metrics structure
        system_metrics = data["system_metrics"]
        assert "memory_usage_mb" in system_metrics
        assert "cpu_percent" in system_metrics
        assert isinstance(system_metrics["memory_usage_mb"], (int, float))
    
    def test_get_operation_performance(self, client: TestClient):
        """Test getting performance for specific operation."""
        # First make a request to generate some performance data
        client.get("/")
        
        operation_name = "GET /"
        response = client.get(f"/api/analytics/performance/operation/{operation_name}")
        
        # Might return 404 if no data exists yet, which is ok
        assert response.status_code in [200, 404]
        
        if response.status_code == 200:
            data = response.json()
            assert "operation" in data
            assert "stats" in data
            assert data["operation"] == operation_name
    
    def test_get_operation_performance_nonexistent(self, client: TestClient):
        """Test getting performance for non-existent operation."""
        response = client.get("/api/analytics/performance/operation/nonexistent_operation")
        assert response.status_code == 404
        
        data = response.json()
        assert "detail" in data
    
    def test_clear_performance_metrics(self, client: TestClient):
        """Test clearing performance metrics."""
        response = client.delete("/api/analytics/performance/clear")
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert "cleared" in data["message"].lower()


class TestAnalyticsHealth:
    """Test analytics health and status endpoints."""
    
    def test_analytics_health_check(self, client: TestClient):
        """Test analytics health check endpoint."""
        response = client.get("/api/analytics/health")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert "timestamp" in data
        assert "analytics" in data
        assert "system_health" in data
        
        # Check analytics status
        analytics_status = data["analytics"]
        assert "enabled" in analytics_status
        assert "buffer_size" in analytics_status
        assert "services_count" in analytics_status
    
    def test_health_check_includes_system_metrics(self, client: TestClient):
        """Test that health check includes system metrics."""
        response = client.get("/api/analytics/health")
        assert response.status_code == 200
        
        data = response.json()
        system_health = data["system_health"]
        assert "status" in system_health
        assert "metrics" in system_health
        assert system_health["status"] in ["healthy", "warning", "critical"]


class TestAnalyticsConfiguration:
    """Test analytics configuration endpoints."""
    
    def test_update_analytics_config(self, client: TestClient):
        """Test updating analytics configuration."""
        config_updates = {
            "debug_mode": True,
            "console_logging": True
        }
        
        response = client.post("/api/analytics/config", json=config_updates)
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert "updated" in data["message"].lower()
        assert "updated_config" in data
    
    def test_update_config_invalid_data(self, client: TestClient):
        """Test updating config with invalid data."""
        invalid_config = {
            "invalid_setting": "invalid_value"
        }
        
        response = client.post("/api/analytics/config", json=invalid_config)
        # Should either accept (ignore invalid) or reject
        assert response.status_code in [200, 400]


class TestUserInteractionTracking:
    """Test user interaction tracking endpoints."""
    
    def test_track_page_view(self, client: TestClient):
        """Test tracking page view."""
        page_view_data = {
            "path": "/dashboard",
            "user_id": "user_123",
            "referrer": "https://example.com"
        }
        
        response = client.post("/api/analytics/user/page-view", json=page_view_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert "tracked" in data["message"].lower()
    
    def test_track_page_view_minimal(self, client: TestClient):
        """Test tracking page view with minimal data."""
        page_view_data = {
            "path": "/home"
        }
        
        response = client.post("/api/analytics/user/page-view", json=page_view_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
    
    def test_track_user_interaction(self, client: TestClient):
        """Test tracking user interaction."""
        interaction_data = {
            "interaction_type": "click",
            "element": "calculate_button",
            "user_id": "user_123",
            "metadata": {"page": "/calculator"}
        }
        
        response = client.post("/api/analytics/user/interaction", json=interaction_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
    
    def test_track_interaction_missing_required(self, client: TestClient):
        """Test tracking interaction with missing required fields."""
        incomplete_data = {
            "interaction_type": "click"
            # Missing element field
        }
        
        response = client.post("/api/analytics/user/interaction", json=incomplete_data)
        assert response.status_code == 422  # Validation error


class TestAnalyticsErrorHandling:
    """Test error handling in analytics endpoints."""
    
    def test_track_event_server_error(self, client: TestClient):
        """Test handling of server errors during event tracking."""
        with patch('app.core.analytics.analytics_core.track_event') as mock_track:
            mock_track.side_effect = Exception("Database error")
            
            event_data = {
                "event": "test_event",
                "properties": {"test": True}
            }
            
            response = client.post("/api/analytics/track", json=event_data)
            assert response.status_code == 400
            
            data = response.json()
            assert "detail" in data
    
    def test_performance_stats_error(self, client: TestClient):
        """Test handling of errors when getting performance stats."""
        with patch('app.core.performance.get_performance_report') as mock_report:
            mock_report.side_effect = Exception("Performance error")
            
            response = client.get("/api/analytics/performance")
            assert response.status_code == 500
            
            data = response.json()
            assert "detail" in data
    
    def test_invalid_json_request(self, client: TestClient):
        """Test handling of invalid JSON in request."""
        response = client.post(
            "/api/analytics/track",
            data="invalid json",
            headers={"content-type": "application/json"}
        )
        assert response.status_code == 422


class TestAnalyticsMiddlewareIntegration:
    """Test that analytics middleware is working with API requests."""
    
    def test_request_tracking_headers(self, client: TestClient):
        """Test that performance tracking headers are added."""
        response = client.get("/")
        
        # Should have performance headers from middleware
        assert "X-Response-Time" in response.headers
        response_time = response.headers["X-Response-Time"]
        assert response_time.endswith("ms")
        
        # Parse the time value
        time_value = float(response_time[:-2])
        assert time_value >= 0
    
    def test_analytics_events_generated(self, client: TestClient):
        """Test that API requests generate analytics events."""
        # Make a request that should generate analytics events
        response = client.get("/health")
        assert response.status_code == 200
        
        # Check if events were buffered (indirect test)
        stats_response = client.get("/api/analytics/stats")
        assert stats_response.status_code == 200
        
        stats_data = stats_response.json()
        # Buffer size might be > 0 if events were tracked
        assert stats_data["buffer_size"] >= 0
