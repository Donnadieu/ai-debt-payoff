"""Analytics event data models and schemas."""

from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum
from sqlmodel import SQLModel, Field, Column, JSON
from pydantic import validator


class EventType(str, Enum):
    """Types of analytics events."""
    USER_ACTION = "user_action"
    SYSTEM_EVENT = "system_event"
    NUDGE_INTERACTION = "nudge_interaction"
    PAYMENT_EVENT = "payment_event"
    GOAL_EVENT = "goal_event"
    ERROR_EVENT = "error_event"


class EventCategory(str, Enum):
    """Categories for analytics events."""
    ENGAGEMENT = "engagement"
    PERFORMANCE = "performance"
    BEHAVIOR = "behavior"
    SYSTEM = "system"
    ERROR = "error"


class AnalyticsEventBase(SQLModel):
    """Base analytics event model."""
    user_id: str = Field(index=True, description="User identifier")
    event_type: EventType = Field(description="Type of event")
    event_name: str = Field(max_length=100, description="Specific event name")
    category: EventCategory = Field(description="Event category")
    properties: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    session_id: Optional[str] = Field(default=None, index=True, description="User session ID")
    source: Optional[str] = Field(default=None, description="Event source (web, mobile, api)")


class AnalyticsEvent(AnalyticsEventBase, table=True):
    """Analytics event database model."""
    __tablename__ = "analytics_events"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow, index=True)
    processed: bool = Field(default=False, index=True)
    processed_at: Optional[datetime] = Field(default=None)


class AnalyticsEventCreate(AnalyticsEventBase):
    """Schema for creating analytics events."""
    pass


class AnalyticsEventResponse(AnalyticsEventBase):
    """Schema for analytics event API responses."""
    id: int
    timestamp: datetime
    processed: bool
    processed_at: Optional[datetime]


class UserSessionBase(SQLModel):
    """Base user session model."""
    user_id: str = Field(index=True, description="User identifier")
    session_id: str = Field(unique=True, index=True, description="Unique session identifier")
    source: Optional[str] = Field(default=None, description="Session source")
    user_agent: Optional[str] = Field(default=None, description="User agent string")
    ip_address: Optional[str] = Field(default=None, description="User IP address")


class UserSession(UserSessionBase, table=True):
    """User session database model."""
    __tablename__ = "user_sessions"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    started_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    last_activity: datetime = Field(default_factory=datetime.utcnow, index=True)
    ended_at: Optional[datetime] = Field(default=None)
    is_active: bool = Field(default=True, index=True)
    
    @validator('last_activity', pre=True, always=True)
    def update_last_activity(cls, v):
        return datetime.utcnow()


class UserSessionCreate(UserSessionBase):
    """Schema for creating user sessions."""
    pass


class UserSessionResponse(UserSessionBase):
    """Schema for user session API responses."""
    id: int
    started_at: datetime
    last_activity: datetime
    ended_at: Optional[datetime]
    is_active: bool
