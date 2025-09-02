"""Pydantic schemas for API request/response validation."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


# Debt schemas
class DebtCreate(BaseModel):
    """Schema for creating a new debt."""
    name: str = Field(..., min_length=1, max_length=100, description="Name of the debt")
    balance: float = Field(..., ge=0, description="Current balance amount")
    interest_rate: float = Field(..., ge=0, le=100, description="Annual interest rate as percentage")
    minimum_payment: float = Field(..., ge=0, description="Minimum monthly payment required")
    due_date: int = Field(..., ge=1, le=31, description="Day of month payment is due")


class DebtUpdate(BaseModel):
    """Schema for updating an existing debt."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    balance: Optional[float] = Field(None, ge=0)
    interest_rate: Optional[float] = Field(None, ge=0, le=100)
    minimum_payment: Optional[float] = Field(None, ge=0)
    due_date: Optional[int] = Field(None, ge=1, le=31)


class DebtResponse(BaseModel):
    """Schema for debt API responses."""
    id: int
    name: str
    balance: float
    interest_rate: float
    minimum_payment: float
    due_date: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Nudge schemas
class NudgeCreate(BaseModel):
    """Schema for creating a new nudge."""
    debt_id: Optional[int] = Field(None, description="Associated debt ID")
    title: str = Field(..., min_length=1, max_length=200, description="Title of the nudge")
    message: str = Field(..., min_length=1, description="Nudge message content")
    nudge_type: str = Field(..., description="Type of nudge (reminder, motivation, tip)")
    priority: str = Field(default="medium", description="Priority level (low, medium, high)")
    scheduled_for: Optional[datetime] = Field(None, description="When to send the nudge")


class NudgeResponse(BaseModel):
    """Schema for nudge API responses."""
    id: int
    debt_id: Optional[int]
    title: str
    message: str
    nudge_type: str
    priority: str
    is_active: bool
    created_at: datetime
    scheduled_for: Optional[datetime]
    sent_at: Optional[datetime]

    class Config:
        from_attributes = True


# Analytics schemas
class AnalyticsEventCreate(BaseModel):
    """Schema for creating analytics events."""
    debt_id: Optional[int] = Field(None, description="Associated debt ID")
    event_type: str = Field(..., description="Type of event (payment, balance_update, goal_set)")
    event_data: dict = Field(..., description="Event data as dictionary")
    user_agent: Optional[str] = Field(None, description="User agent string")


class AnalyticsEventResponse(BaseModel):
    """Schema for analytics event responses."""
    id: int
    debt_id: Optional[int]
    event_type: str
    event_data: str  # JSON string in database
    user_agent: Optional[str]
    timestamp: datetime

    class Config:
        from_attributes = True


# Progress analytics schemas
class ProgressAnalyticsResponse(BaseModel):
    """Schema for progress analytics responses."""
    total_debt: float
    total_minimum_payments: float
    estimated_payoff_months: Optional[int]
    interest_saved_potential: Optional[float]
    debt_count: int
    last_updated: datetime


# Error schemas
class ErrorResponse(BaseModel):
    """Schema for error responses."""
    detail: str
    error_code: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# Payoff Plan schemas
class PayoffPlanRequest(BaseModel):
    """Schema for payoff plan calculation request."""
    debts: list[DebtCreate] = Field(..., min_items=1, max_items=10, description="List of debts to calculate payoff for")
    strategy: str = Field(..., description="Payoff strategy: 'snowball', 'avalanche', or 'compare'")
    extra_payment: float = Field(default=0.0, ge=0, description="Extra monthly payment amount")


class PayoffPlanResponse(BaseModel):
    """Schema for payoff plan calculation response."""
    strategy: str
    total_months: int
    total_payments: float
    total_interest: float
    payoff_timeline: dict
    monthly_schedule: list
    summary: dict
