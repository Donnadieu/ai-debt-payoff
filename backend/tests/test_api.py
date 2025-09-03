"""Tests for API endpoints and request/response handling."""

import pytest
import json
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock

from main import app
from schemas import PayoffPlanRequest
from models import Debt


class TestRootEndpoints:
    """Test root and health endpoints."""
    
    def test_root_endpoint(self, client: TestClient):
        """Test root endpoint returns basic info."""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "docs" in data
        assert data["docs"] == "/docs"
    
    def test_health_endpoint(self, client: TestClient):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
        assert "environment" in data


class TestDebtEndpoints:
    """Test debt management API endpoints."""
    
    def test_get_debts_empty(self, client: TestClient):
        """Test getting debts when none exist."""
        response = client.get("/api/v1/debts")
        assert response.status_code == 200
        
        data = response.json()
        assert "debts" in data
        assert data["debts"] == []
    
    def test_create_debt_placeholder(self, client: TestClient):
        """Test debt creation placeholder endpoint."""
        response = client.post("/api/v1/debts")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "to be implemented" in data["message"].lower()
    
    def test_get_debt_by_id(self, client: TestClient):
        """Test getting specific debt by ID."""
        debt_id = 123
        response = client.get(f"/api/v1/debts/{debt_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert "debt_id" in data
        assert data["debt_id"] == debt_id
    
    def test_update_debt(self, client: TestClient):
        """Test updating specific debt."""
        debt_id = 123
        response = client.put(f"/api/v1/debts/{debt_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert "debt_id" in data
        assert data["debt_id"] == debt_id
    
    def test_delete_debt(self, client: TestClient):
        """Test deleting specific debt."""
        debt_id = 123
        response = client.delete(f"/api/v1/debts/{debt_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert "debt_id" in data
        assert data["debt_id"] == debt_id


class TestPayoffPlanEndpoint:
    """Test debt payoff plan calculation endpoint."""
    
    def test_calculate_snowball_plan(self, client: TestClient, sample_debt_portfolio):
        """Test snowball strategy calculation."""
        request_data = {
            "debts": sample_debt_portfolio,
            "strategy": "snowball",
            "extra_payment": 100.0
        }
        
        response = client.post("/plan", json=request_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "strategy" in data
        assert data["strategy"] == "snowball"
        assert "total_interest" in data
        assert "payoff_months" in data
        assert "monthly_schedule" in data
        assert isinstance(data["total_interest"], (int, float))
        assert data["payoff_months"] > 0
    
    def test_calculate_avalanche_plan(self, client: TestClient, sample_debt_portfolio):
        """Test avalanche strategy calculation."""
        request_data = {
            "debts": sample_debt_portfolio,
            "strategy": "avalanche",
            "extra_payment": 150.0
        }
        
        response = client.post("/plan", json=request_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "strategy" in data
        assert data["strategy"] == "avalanche"
        assert "total_interest" in data
        assert "payoff_months" in data
        assert "monthly_schedule" in data
    
    def test_compare_strategies(self, client: TestClient, sample_debt_portfolio):
        """Test strategy comparison."""
        request_data = {
            "debts": sample_debt_portfolio,
            "strategy": "compare",
            "extra_payment": 200.0
        }
        
        response = client.post("/plan", json=request_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "snowball" in data
        assert "avalanche" in data
        assert "recommendation" in data
        
        # Check both strategies have required fields
        for strategy in ["snowball", "avalanche"]:
            assert "total_interest" in data[strategy]
            assert "payoff_months" in data[strategy]
    
    def test_invalid_strategy(self, client: TestClient, sample_debt_portfolio):
        """Test invalid strategy returns error."""
        request_data = {
            "debts": sample_debt_portfolio,
            "strategy": "invalid_strategy",
            "extra_payment": 100.0
        }
        
        response = client.post("/plan", json=request_data)
        assert response.status_code == 400
        
        data = response.json()
        assert "detail" in data
        assert "invalid strategy" in data["detail"].lower()
    
    def test_empty_debt_portfolio(self, client: TestClient):
        """Test empty debt portfolio returns validation error."""
        request_data = {
            "debts": [],
            "strategy": "snowball",
            "extra_payment": 100.0
        }
        
        response = client.post("/plan", json=request_data)
        assert response.status_code == 400
        
        data = response.json()
        assert "detail" in data
        assert "errors" in data["detail"]
    
    def test_invalid_debt_data(self, client: TestClient):
        """Test invalid debt data returns validation error."""
        invalid_debt = {
            "name": "Invalid Debt",
            "balance": -1000.0,  # Negative balance
            "apr": 15.0,
            "min_payment": 50.0
        }
        
        request_data = {
            "debts": [invalid_debt],
            "strategy": "snowball",
            "extra_payment": 100.0
        }
        
        response = client.post("/plan", json=request_data)
        assert response.status_code == 400
        
        data = response.json()
        assert "detail" in data
        assert "errors" in data["detail"]
    
    def test_missing_required_fields(self, client: TestClient):
        """Test missing required fields returns validation error."""
        incomplete_debt = {
            "name": "Incomplete Debt",
            "balance": 1000.0
            # Missing apr and min_payment
        }
        
        request_data = {
            "debts": [incomplete_debt],
            "strategy": "snowball",
            "extra_payment": 100.0
        }
        
        response = client.post("/plan", json=request_data)
        assert response.status_code == 422  # Pydantic validation error
    
    def test_zero_extra_payment(self, client: TestClient, sample_debt_portfolio):
        """Test calculation with zero extra payment."""
        request_data = {
            "debts": sample_debt_portfolio,
            "strategy": "snowball",
            "extra_payment": 0.0
        }
        
        response = client.post("/plan", json=request_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["payoff_months"] > 0
        assert data["total_interest"] > 0


class TestNudgeEndpoints:
    """Test nudge/coaching API endpoints."""
    
    def test_get_nudges_empty(self, client: TestClient):
        """Test getting nudges when none exist."""
        response = client.get("/api/v1/nudges")
        assert response.status_code == 200
        
        data = response.json()
        assert "nudges" in data
        assert data["nudges"] == []
    
    def test_create_nudge_placeholder(self, client: TestClient):
        """Test nudge creation placeholder endpoint."""
        response = client.post("/api/v1/nudges")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "to be implemented" in data["message"].lower()


class TestSlipDetectionEndpoints:
    """Test slip detection API endpoints."""
    
    def test_slip_detection_endpoints_exist(self, client: TestClient):
        """Test that slip detection endpoints are accessible."""
        # Test the slip detection router is included
        response = client.get("/api/v1/slip/health")
        # Should return 200 or 404, but not 500 (router not included)
        assert response.status_code in [200, 404, 405]


class TestErrorHandling:
    """Test API error handling and HTTP status codes."""
    
    def test_404_for_nonexistent_endpoint(self, client: TestClient):
        """Test 404 for non-existent endpoints."""
        response = client.get("/nonexistent/endpoint")
        assert response.status_code == 404
    
    def test_405_for_wrong_method(self, client: TestClient):
        """Test 405 for wrong HTTP method."""
        response = client.delete("/")  # Root only supports GET
        assert response.status_code == 405
    
    def test_422_for_invalid_json(self, client: TestClient):
        """Test 422 for invalid JSON in request body."""
        response = client.post(
            "/plan",
            data="invalid json",
            headers={"content-type": "application/json"}
        )
        assert response.status_code == 422
    
    def test_internal_server_error_handling(self, client: TestClient):
        """Test that internal server errors are handled gracefully."""
        # This would require mocking an internal error
        # For now, just ensure the endpoint exists and doesn't crash
        response = client.post("/plan", json={})
        # Should return 422 (validation error) not 500 (server error)
        assert response.status_code == 422


class TestRequestValidation:
    """Test request validation and data sanitization."""
    
    def test_request_size_limits(self, client: TestClient):
        """Test request size limits."""
        # Create a very large debt portfolio
        large_portfolio = []
        for i in range(1000):  # Very large portfolio
            large_portfolio.append({
                "name": f"Debt {i}",
                "balance": 1000.0,
                "apr": 15.0,
                "min_payment": 50.0
            })
        
        request_data = {
            "debts": large_portfolio,
            "strategy": "snowball",
            "extra_payment": 100.0
        }
        
        response = client.post("/plan", json=request_data)
        # Should either process or return appropriate error
        assert response.status_code in [200, 400, 413, 422]
    
    def test_string_sanitization(self, client: TestClient):
        """Test that string inputs are properly sanitized."""
        debt_with_special_chars = {
            "name": "<script>alert('xss')</script>",
            "balance": 1000.0,
            "apr": 15.0,
            "min_payment": 50.0
        }
        
        request_data = {
            "debts": [debt_with_special_chars],
            "strategy": "snowball",
            "extra_payment": 100.0
        }
        
        response = client.post("/plan", json=request_data)
        # Should process without executing script
        assert response.status_code in [200, 400]
        
        if response.status_code == 200:
            # Ensure script tags are not in response
            response_text = response.text
            assert "<script>" not in response_text
    
    def test_numeric_validation(self, client: TestClient):
        """Test numeric field validation."""
        debt_with_string_numbers = {
            "name": "Test Debt",
            "balance": "not_a_number",
            "apr": 15.0,
            "min_payment": 50.0
        }
        
        request_data = {
            "debts": [debt_with_string_numbers],
            "strategy": "snowball",
            "extra_payment": 100.0
        }
        
        response = client.post("/plan", json=request_data)
        assert response.status_code == 422  # Validation error


class TestResponseFormat:
    """Test API response format and structure."""
    
    def test_response_headers(self, client: TestClient):
        """Test that responses have appropriate headers."""
        response = client.get("/")
        
        # Should have content-type header
        assert "content-type" in response.headers
        assert "application/json" in response.headers["content-type"]
    
    def test_error_response_format(self, client: TestClient):
        """Test that error responses have consistent format."""
        response = client.post("/plan", json={})
        assert response.status_code == 422
        
        data = response.json()
        assert "detail" in data
        # Pydantic validation errors have specific format
        assert isinstance(data["detail"], (list, str, dict))
    
    def test_success_response_format(self, client: TestClient, sample_debt_data):
        """Test that success responses have consistent format."""
        request_data = {
            "debts": [sample_debt_data],
            "strategy": "snowball",
            "extra_payment": 100.0
        }
        
        response = client.post("/plan", json=request_data)
        assert response.status_code == 200
        
        data = response.json()
        # Should be valid JSON with expected structure
        assert isinstance(data, dict)
        assert "strategy" in data
        assert "total_interest" in data
        assert "payoff_months" in data


class TestCORSHeaders:
    """Test CORS headers for frontend integration."""
    
    def test_cors_headers_present(self, client: TestClient):
        """Test that CORS headers are present in responses."""
        response = client.get("/")
        
        # CORS headers should be present
        cors_headers = [
            "access-control-allow-origin",
            "access-control-allow-methods",
            "access-control-allow-headers"
        ]
        
        # At least some CORS headers should be present
        present_headers = [h for h in cors_headers if h in response.headers]
        assert len(present_headers) > 0
    
    def test_options_request(self, client: TestClient):
        """Test OPTIONS request for CORS preflight."""
        response = client.options("/")
        # Should not return 405 (method not allowed)
        assert response.status_code in [200, 204]
