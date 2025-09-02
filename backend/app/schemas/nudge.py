"""Nudge data models and schemas."""

from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum
from sqlmodel import SQLModel, Field, Column, JSON
from pydantic import validator


class NudgeType(str, Enum):
    """Types of nudges that can be sent to users."""
    PAYMENT_REMINDER = "payment_reminder"
    PROGRESS_UPDATE = "progress_update"
    MILESTONE_CELEBRATION = "milestone_celebration"
    STRATEGY_SUGGESTION = "strategy_suggestion"
    MOTIVATION = "motivation"
    WARNING = "warning"


class NudgeStatus(str, Enum):
    """Status of nudge validation and delivery."""
    PENDING = "pending"
    VALIDATED = "validated"
    SENT = "sent"
    FAILED = "failed"
    DISMISSED = "dismissed"


class NudgeBase(SQLModel):
    """Base nudge model with common fields."""
    user_id: str = Field(index=True, description="User identifier")
    nudge_type: NudgeType = Field(description="Type of nudge")
    title: str = Field(max_length=200, description="Nudge title")
    message: str = Field(description="Nudge message content")
    priority: int = Field(default=1, ge=1, le=5, description="Priority level (1-5)")
    metadata: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    scheduled_for: Optional[datetime] = Field(default=None, description="When to send the nudge")
    expires_at: Optional[datetime] = Field(default=None, description="When the nudge expires")


class Nudge(NudgeBase, table=True):
    """Nudge database model."""
    __tablename__ = "nudges"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    status: NudgeStatus = Field(default=NudgeStatus.PENDING, index=True)
    validation_status: Optional[str] = Field(default=None, description="AI validation result")
    validation_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    sent_at: Optional[datetime] = Field(default=None)
    dismissed_at: Optional[datetime] = Field(default=None)
    
    @validator('updated_at', pre=True, always=True)
    def set_updated_at(cls, v):
        return datetime.utcnow()


class NudgeCreate(NudgeBase):
    """Schema for creating a new nudge."""
    pass


class NudgeUpdate(SQLModel):
    """Schema for updating a nudge."""
    title: Optional[str] = Field(default=None, max_length=200)
    message: Optional[str] = Field(default=None)
    priority: Optional[int] = Field(default=None, ge=1, le=5)
    status: Optional[NudgeStatus] = Field(default=None)
    metadata: Optional[Dict[str, Any]] = Field(default=None)
    scheduled_for: Optional[datetime] = Field(default=None)
    expires_at: Optional[datetime] = Field(default=None)


class NudgeResponse(NudgeBase):
    """Schema for nudge API responses."""
    id: int
    status: NudgeStatus
    validation_status: Optional[str]
    validation_score: Optional[float]
    created_at: datetime
    updated_at: datetime
    sent_at: Optional[datetime]
    dismissed_at: Optional[datetime]
