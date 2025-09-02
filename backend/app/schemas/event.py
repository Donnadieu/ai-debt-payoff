"""Event schema models for analytics validation and persistence."""

from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum
from sqlmodel import SQLModel, Field, Column, JSON
from pydantic import BaseModel, validator


class EventType(str, Enum):
    """Enumeration of supported event types."""
    PAGE_VIEW = "page_view"
    USER_INTERACTION = "user_interaction"
    API_REQUEST = "api_request"
    API_ERROR = "api_error"
    OPERATION_TIMING = "operation_timing"
    SYSTEM_METRIC = "system_metric"
    CUSTOM = "custom"


class EventSeverity(str, Enum):
    """Event severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AnalyticsEvent(SQLModel, table=True):
    """Database model for analytics events."""
    __tablename__ = "analytics_events"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    event_id: str = Field(index=True, description="Unique event identifier")
    event_type: EventType = Field(index=True, description="Type of event")
    event_name: str = Field(index=True, description="Event name")
    
    # Event data
    properties: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    metadata: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    
    # User context
    user_id: Optional[str] = Field(default=None, index=True)
    session_id: Optional[str] = Field(default=None, index=True)
    
    # Timing and location
    timestamp: datetime = Field(default_factory=datetime.utcnow, index=True)
    timezone: Optional[str] = Field(default=None)
    
    # Technical context
    user_agent: Optional[str] = Field(default=None)
    ip_address: Optional[str] = Field(default=None)
    referrer: Optional[str] = Field(default=None)
    
    # Event classification
    severity: EventSeverity = Field(default=EventSeverity.LOW)
    tags: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    
    # Processing status
    processed: bool = Field(default=False, index=True)
    processed_at: Optional[datetime] = Field(default=None)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class EventCreate(BaseModel):
    """Schema for creating new events."""
    event_name: str = Field(..., min_length=1, max_length=100)
    event_type: EventType = Field(default=EventType.CUSTOM)
    properties: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    user_id: Optional[str] = Field(None, max_length=100)
    session_id: Optional[str] = Field(None, max_length=100)
    severity: EventSeverity = Field(default=EventSeverity.LOW)
    tags: List[str] = Field(default_factory=list)
    
    @validator('properties')
    def validate_properties(cls, v):
        """Validate event properties."""
        if len(v) > 50:
            raise ValueError("Too many properties (max 50)")
        
        for key, value in v.items():
            if len(str(key)) > 100:
                raise ValueError(f"Property key too long: {key}")
            if isinstance(value, str) and len(value) > 1000:
                raise ValueError(f"Property value too long for key: {key}")
        
        return v
    
    @validator('tags')
    def validate_tags(cls, v):
        """Validate event tags."""
        if len(v) > 20:
            raise ValueError("Too many tags (max 20)")
        
        for tag in v:
            if len(tag) > 50:
                raise ValueError(f"Tag too long: {tag}")
        
        return v


class EventUpdate(BaseModel):
    """Schema for updating events."""
    processed: Optional[bool] = None
    severity: Optional[EventSeverity] = None
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class EventResponse(BaseModel):
    """Response schema for event operations."""
    id: int
    event_id: str
    event_name: str
    event_type: EventType
    timestamp: datetime
    user_id: Optional[str]
    session_id: Optional[str]
    severity: EventSeverity
    processed: bool
    
    class Config:
        from_attributes = True


class EventBatch(BaseModel):
    """Schema for batch event operations."""
    events: List[EventCreate] = Field(..., min_items=1, max_items=100)
    
    @validator('events')
    def validate_batch_size(cls, v):
        """Validate batch size."""
        if len(v) > 100:
            raise ValueError("Batch size too large (max 100 events)")
        return v


class EventQuery(BaseModel):
    """Schema for querying events."""
    event_type: Optional[EventType] = None
    event_name: Optional[str] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    severity: Optional[EventSeverity] = None
    processed: Optional[bool] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    tags: Optional[List[str]] = None
    limit: int = Field(default=100, ge=1, le=1000)
    offset: int = Field(default=0, ge=0)
    
    @validator('end_date')
    def validate_date_range(cls, v, values):
        """Validate date range."""
        if v and 'start_date' in values and values['start_date']:
            if v <= values['start_date']:
                raise ValueError("end_date must be after start_date")
        return v


class EventStats(BaseModel):
    """Schema for event statistics."""
    total_events: int
    events_by_type: Dict[str, int]
    events_by_severity: Dict[str, int]
    processed_events: int
    unprocessed_events: int
    date_range: Dict[str, Optional[datetime]]
    top_users: List[Dict[str, Any]]
    top_events: List[Dict[str, Any]]


class EventValidationError(BaseModel):
    """Schema for event validation errors."""
    field: str
    message: str
    value: Any


class EventValidationResult(BaseModel):
    """Schema for event validation results."""
    valid: bool
    errors: List[EventValidationError] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)


# Performance event specific schemas
class PerformanceEvent(BaseModel):
    """Schema for performance-related events."""
    operation: str
    duration_ms: float
    memory_usage_mb: Optional[float] = None
    cpu_percent: Optional[float] = None
    success: bool = True
    error_message: Optional[str] = None
    
    def to_analytics_event(self, user_id: Optional[str] = None) -> EventCreate:
        """Convert to analytics event."""
        return EventCreate(
            event_name="performance_metric",
            event_type=EventType.OPERATION_TIMING,
            properties={
                "operation": self.operation,
                "duration_ms": self.duration_ms,
                "memory_usage_mb": self.memory_usage_mb,
                "cpu_percent": self.cpu_percent,
                "success": self.success,
                "error_message": self.error_message
            },
            user_id=user_id,
            severity=EventSeverity.HIGH if self.duration_ms > 2000 else EventSeverity.LOW
        )


class UserInteractionEvent(BaseModel):
    """Schema for user interaction events."""
    interaction_type: str  # click, scroll, form_submit, etc.
    element: str
    page_path: str
    coordinates: Optional[Dict[str, float]] = None
    
    def to_analytics_event(self, user_id: Optional[str] = None) -> EventCreate:
        """Convert to analytics event."""
        return EventCreate(
            event_name="user_interaction",
            event_type=EventType.USER_INTERACTION,
            properties={
                "interaction_type": self.interaction_type,
                "element": self.element,
                "page_path": self.page_path,
                "coordinates": self.coordinates
            },
            user_id=user_id,
            severity=EventSeverity.LOW
        )


class APIRequestEvent(BaseModel):
    """Schema for API request events."""
    method: str
    path: str
    status_code: int
    duration_ms: float
    user_agent: Optional[str] = None
    
    def to_analytics_event(self, user_id: Optional[str] = None) -> EventCreate:
        """Convert to analytics event."""
        severity = EventSeverity.HIGH if status_code >= 500 else EventSeverity.LOW
        
        return EventCreate(
            event_name="api_request",
            event_type=EventType.API_REQUEST,
            properties={
                "method": self.method,
                "path": self.path,
                "status_code": self.status_code,
                "duration_ms": self.duration_ms,
                "user_agent": self.user_agent
            },
            user_id=user_id,
            severity=severity
        )
