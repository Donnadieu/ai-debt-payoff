"""
Integration tests for Slip Detection API endpoint.
"""

import pytest
from fastapi.testclient import TestClient
from decimal import Decimal
import json

# Import the FastAPI app
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app

client = TestClient(app)


class TestSlipAPI:
    """Test suite for slip detection API endpoints."""
    
    def test_slip_check_endpoint_feasible(self):
        """Test /api/v1/slip/check endpoint with feasible budget."""
        request_data = {
            "monthly_budget": 2500.00,
            "debts": [
                {
                    "id": "debt_1",
                    "name": "Credit Card A",
                    "minimum_payment": 150.00,
                    "balance": 5000.00
                },
                {
                    "id": "debt_2",
                    "name": "Student Loan", 
                    "minimum_payment": 300.00,
                    "balance": 25000.00
                }
            ]
        }
        
        response = client.post("/api/v1/slip/check", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["is_feasible"] is True
        assert data["has_slip"] is False
        assert data["monthly_budget"] == 2500.00
        assert data["total_minimum_payments"] == 450.00
        assert data["surplus"] == 2050.00
        assert data["shortfall"] == 0.0
        assert data["suggestion_amount"] == 0.0
        assert data["suggestion_text"] is None
        assert "sufficient" in data["message"].lower()
    
    def test_slip_check_endpoint_with_slip(self):
        """Test /api/v1/slip/check endpoint with budget slip."""
        request_data = {
            "monthly_budget": 400.00,
            "debts": [
                {
                    "id": "debt_1",
                    "name": "Credit Card A",
                    "minimum_payment": 200.00
                },
                {
                    "id": "debt_2", 
                    "name": "Student Loan",
                    "minimum_payment": 350.00
                }
            ]
        }
        
        response = client.post("/api/v1/slip/check", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["is_feasible"] is False
        assert data["has_slip"] is True
        assert data["monthly_budget"] == 400.00
        assert data["total_minimum_payments"] == 550.00
        assert data["surplus"] == 0.0
        assert data["shortfall"] == 150.00
        assert data["suggestion_amount"] == 150.00  # ceil(150/25)*25 = 150
        assert data["suggestion_text"] == "Apply $150"
        assert "shortfall" in data["message"].lower()
    
    def test_slip_check_endpoint_edge_cases(self):
        """Test edge cases for slip check endpoint."""
        # Zero budget
        request_data = {
            "monthly_budget": 0.00,
            "debts": [{"name": "Test Debt", "minimum_payment": 100.00}]
        }
        
        response = client.post("/api/v1/slip/check", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["has_slip"] is True
        assert data["suggestion_amount"] == 25.0
        
        # No debts
        request_data = {
            "monthly_budget": 1000.00,
            "debts": []
        }
        
        response = client.post("/api/v1/slip/check", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["is_feasible"] is True
        assert data["has_slip"] is False
        assert "no debts" in data["message"].lower()
    
    def test_slip_check_validation_errors(self):
        """Test validation errors for invalid requests."""
        # Negative budget
        request_data = {
            "monthly_budget": -100.00,
            "debts": [{"name": "Test", "minimum_payment": 50.00}]
        }
        
        response = client.post("/api/v1/slip/check", json=request_data)
        assert response.status_code == 422  # Validation error
        
        # Missing required fields
        request_data = {
            "monthly_budget": 1000.00
            # Missing debts field
        }
        
        response = client.post("/api/v1/slip/check", json=request_data)
        assert response.status_code == 422
        
        # Invalid debt structure
        request_data = {
            "monthly_budget": 1000.00,
            "debts": [{"name": "Test"}]  # Missing minimum_payment
        }
        
        response = client.post("/api/v1/slip/check", json=request_data)
        assert response.status_code == 422
    
    def test_slip_health_endpoint(self):
        """Test slip service health check endpoint."""
        response = client.get("/api/v1/slip/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "healthy"
        assert data["service"] == "slip_detection"
        assert "timestamp" in data
    
    def test_slip_check_response_schema(self):
        """Test that response matches expected schema."""
        request_data = {
            "monthly_budget": 1000.00,
            "debts": [
                {"name": "Test Debt", "minimum_payment": 200.00}
            ]
        }
        
        response = client.post("/api/v1/slip/check", json=request_data)
        assert response.status_code == 200
        data = response.json()
        
        # Verify all required fields are present
        required_fields = [
            "is_feasible", "has_slip", "monthly_budget", 
            "total_minimum_payments", "surplus", "shortfall",
            "suggestion_amount", "suggestion_text", "message"
        ]
        
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"
        
        # Verify data types
        assert isinstance(data["is_feasible"], bool)
        assert isinstance(data["has_slip"], bool)
        assert isinstance(data["monthly_budget"], (int, float))
        assert isinstance(data["total_minimum_payments"], (int, float))
        assert isinstance(data["surplus"], (int, float))
        assert isinstance(data["shortfall"], (int, float))
        assert isinstance(data["suggestion_amount"], (int, float))
        assert isinstance(data["message"], str)
    
    def test_slip_check_large_request(self):
        """Test slip check with large number of debts."""
        debts = []
        for i in range(50):
            debts.append({
                "id": f"debt_{i}",
                "name": f"Debt {i}",
                "minimum_payment": 50.00,
                "balance": 1000.00
            })
        
        request_data = {
            "monthly_budget": 1000.00,  # Total minimums = 2500, shortfall = 1500
            "debts": debts
        }
        
        response = client.post("/api/v1/slip/check", json=request_data)
        assert response.status_code == 200
        data = response.json()
        
        assert data["total_minimum_payments"] == 2500.00
        assert data["shortfall"] == 1500.00
        assert data["suggestion_amount"] == 1500.00  # ceil(1500/25)*25 = 1500
    
    def test_slip_check_decimal_precision(self):
        """Test handling of decimal precision in calculations."""
        request_data = {
            "monthly_budget": 100.33,
            "debts": [
                {"name": "Debt 1", "minimum_payment": 33.33},
                {"name": "Debt 2", "minimum_payment": 33.34},
                {"name": "Debt 3", "minimum_payment": 33.34}
            ]
        }
        
        response = client.post("/api/v1/slip/check", json=request_data)
        assert response.status_code == 200
        data = response.json()
        
        # Total minimums = 100.01, budget = 100.33, surplus should be 0.32
        assert abs(data["surplus"] - 0.32) < 0.01
        assert data["is_feasible"] is True
    
    def test_api_documentation_accessibility(self):
        """Test that API documentation includes slip endpoints."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        openapi_spec = response.json()
        paths = openapi_spec.get("paths", {})
        
        # Check that slip endpoints are documented
        assert "/api/v1/slip/check" in paths
        assert "/api/v1/slip/health" in paths
        
        # Check that slip check endpoint has proper documentation
        slip_check = paths["/api/v1/slip/check"]
        assert "post" in slip_check
        assert "tags" in slip_check["post"]
        assert "slip-detection" in slip_check["post"]["tags"]
