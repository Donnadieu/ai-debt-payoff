"""
Slip Detection API Schemas - Request/response models for slip detection endpoint.
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from decimal import Decimal


class DebtInput(BaseModel):
    """Individual debt input for slip analysis."""
    id: Optional[str] = Field(None, description="Debt identifier")
    name: str = Field(..., description="Debt name or description")
    minimum_payment: Decimal = Field(..., ge=0, description="Minimum monthly payment required")
    balance: Optional[Decimal] = Field(None, ge=0, description="Current debt balance")


class SlipCheckRequest(BaseModel):
    """Request model for slip detection analysis."""
    monthly_budget: Decimal = Field(..., ge=0, description="Available monthly budget amount")
    debts: List[DebtInput] = Field(..., description="List of debts to analyze")
    
    class Config:
        json_encoders = {
            Decimal: lambda v: float(v)
        }
        schema_extra = {
            "example": {
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
        }


class SlipCheckResponse(BaseModel):
    """Response model for slip detection analysis."""
    is_feasible: bool = Field(..., description="Whether budget covers all minimum payments")
    has_slip: bool = Field(..., description="Whether a budget slip was detected")
    monthly_budget: float = Field(..., description="Input monthly budget amount")
    total_minimum_payments: float = Field(..., description="Sum of all minimum payments")
    surplus: float = Field(..., description="Budget surplus if feasible")
    shortfall: float = Field(..., description="Budget shortfall if not feasible")
    suggestion_amount: float = Field(..., description="Suggested additional budget amount")
    suggestion_text: Optional[str] = Field(None, description="Formatted suggestion text")
    message: str = Field(..., description="Human-readable analysis message")
    
    class Config:
        schema_extra = {
            "example": {
                "is_feasible": False,
                "has_slip": True,
                "monthly_budget": 2500.00,
                "total_minimum_payments": 2650.00,
                "surplus": 0.0,
                "shortfall": 150.00,
                "suggestion_amount": 175.00,
                "suggestion_text": "Apply $175",
                "message": "Budget shortfall of $150.00. Consider applying $175 additional monthly budget."
            }
        }


class SlipAnalyticsEvent(BaseModel):
    """Analytics event model for slip detection tracking."""
    event_type: str = Field(default="slip_detection", description="Event type identifier")
    user_id: Optional[str] = Field(None, description="User identifier")
    session_id: Optional[str] = Field(None, description="Session identifier")
    has_slip: bool = Field(..., description="Whether slip was detected")
    shortfall_amount: float = Field(..., description="Shortfall amount if any")
    suggestion_amount: float = Field(..., description="Suggested remediation amount")
    debt_count: int = Field(..., description="Number of debts analyzed")
    timestamp: Optional[str] = Field(None, description="Event timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "event_type": "slip_detection",
                "user_id": "user_123",
                "session_id": "session_456",
                "has_slip": True,
                "shortfall_amount": 150.00,
                "suggestion_amount": 175.00,
                "debt_count": 2,
                "timestamp": "2025-09-02T05:36:16Z"
            }
        }
