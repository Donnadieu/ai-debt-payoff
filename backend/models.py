"""SQLModel database models for the debt payoff application."""

from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class DebtBase(SQLModel):
    """Base debt model with shared fields."""
    name: str = Field(index=True, description="Name of the debt (e.g., 'Credit Card 1')")
    balance: float = Field(ge=0, description="Current balance amount")
    interest_rate: float = Field(ge=0, le=100, description="Annual interest rate as percentage")
    minimum_payment: float = Field(ge=0, description="Minimum monthly payment required")
    due_date: int = Field(ge=1, le=31, description="Day of month payment is due")


class Debt(DebtBase, table=True):
    """Debt database model."""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    nudges: list["Nudge"] = Relationship(back_populates="debt")
    analytics_events: list["AnalyticsEvent"] = Relationship(back_populates="debt")


class NudgeBase(SQLModel):
    """Base nudge model with shared fields."""
    title: str = Field(description="Title of the nudge")
    message: str = Field(description="Nudge message content")
    nudge_type: str = Field(description="Type of nudge (reminder, motivation, tip)")
    priority: str = Field(default="medium", description="Priority level (low, medium, high)")
    is_active: bool = Field(default=True, description="Whether the nudge is active")


class Nudge(NudgeBase, table=True):
    """Nudge database model for AI coaching messages."""
    id: Optional[int] = Field(default=None, primary_key=True)
    debt_id: Optional[int] = Field(default=None, foreign_key="debt.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    scheduled_for: Optional[datetime] = Field(default=None, description="When to send the nudge")
    sent_at: Optional[datetime] = Field(default=None, description="When the nudge was sent")
    
    # Relationships
    debt: Optional[Debt] = Relationship(back_populates="nudges")


class AnalyticsEventBase(SQLModel):
    """Base analytics event model."""
    event_type: str = Field(description="Type of event (payment, balance_update, goal_set)")
    event_data: str = Field(description="JSON string of event data")
    user_agent: Optional[str] = Field(default=None, description="User agent string")


class AnalyticsEvent(AnalyticsEventBase, table=True):
    """Analytics event model for tracking user interactions."""
    id: Optional[int] = Field(default=None, primary_key=True)
    debt_id: Optional[int] = Field(default=None, foreign_key="debt.id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    debt: Optional[Debt] = Relationship(back_populates="analytics_events")
