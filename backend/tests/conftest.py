"""Test configuration and shared fixtures for the debt payoff backend."""

import pytest
from typing import Dict, Any
from datetime import datetime


@pytest.fixture
def sample_debts():
    """Sample debt data for testing."""
    return [
        {
            "id": 1,
            "name": "Credit Card",
            "balance": 2500.0,
            "interest_rate": 18.5,
            "minimum_payment": 75.0
        },
        {
            "id": 2,
            "name": "Student Loan", 
            "balance": 15000.0,
            "interest_rate": 6.8,
            "minimum_payment": 200.0
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
