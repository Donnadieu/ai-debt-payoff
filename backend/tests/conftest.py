"""Test configuration and shared fixtures for the debt payoff backend."""

import pytest
from typing import Dict, Any
from datetime import datetime
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    """FastAPI test client fixture."""
    return TestClient(app)


@pytest.fixture
def sample_debt():
    """Sample debt data for testing."""
    return {
        "name": "Credit Card",
        "balance": 5000.0,
        "interest_rate": 18.5,
        "minimum_payment": 150.0,
        "due_date": 15
    }


@pytest.fixture
def sample_debts():
    """Multiple sample debts for testing."""
    return [
        {
            "name": "Credit Card A",
            "balance": 3000.0,
            "interest_rate": 22.0,
            "minimum_payment": 100.0,
            "due_date": 5
        },
        {
            "name": "Credit Card B",
            "balance": 1500.0,
            "interest_rate": 15.5,
            "minimum_payment": 50.0,
            "due_date": 20
        },
        {
            "name": "Personal Loan",
            "balance": 8000.0,
            "interest_rate": 12.0,
            "minimum_payment": 200.0,
            "due_date": 10
        }
    ]


@pytest.fixture
def sample_analytics_event():
    """Sample analytics event for testing."""
    return {
        "event": "debt_added",
        "properties": {
            "debt_name": "Credit Card",
            "balance": 2500.0,
            "interest_rate": 18.5
        },
        "user_id": "user_123"
    }
