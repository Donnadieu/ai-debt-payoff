"""Event service for analytics event validation, formatting, and persistence."""

import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from sqlmodel import Session, select, func, and_, or_

from ..core.database import get_session
from ..core.transaction import transactional
from ..schemas.event import (
    AnalyticsEvent, EventCreate, EventUpdate, EventQuery, 
    EventStats, EventValidationResult, EventValidationError,
    PerformanceEvent, UserInteractionEvent, APIRequestEvent
)
from ..core.repository import BaseRepository


class EventRepository(BaseRepository[AnalyticsEvent, EventCreate, EventUpdate]):
    """Repository for analytics events."""
    
    def __init__(self, session: Session):
        super().__init__(AnalyticsEvent, session)
    
    def find_by_user_id(self, user_id: str, limit: int = 100) -> List[AnalyticsEvent]:
        """Find events by user ID."""
        statement = select(AnalyticsEvent).where(
            AnalyticsEvent.user_id == user_id
        ).order_by(AnalyticsEvent.timestamp.desc()).limit(limit)
        
        return self.session.exec(statement).all()
    
    def find_by_session_id(self, session_id: str) -> List[AnalyticsEvent]:
        """Find events by session ID."""
        statement = select(AnalyticsEvent).where(
            AnalyticsEvent.session_id == session_id
        ).order_by(AnalyticsEvent.timestamp.asc())
        
        return self.session.exec(statement).all()
    
    def find_by_date_range(self, start_date: datetime, end_date: datetime) -> List[AnalyticsEvent]:
        """Find events within date range."""
        statement = select(AnalyticsEvent).where(
            and_(
                AnalyticsEvent.timestamp >= start_date,
                AnalyticsEvent.timestamp <= end_date
            )
        ).order_by(AnalyticsEvent.timestamp.desc())
        
        return self.session.exec(statement).all()
    
    def count_by_type(self) -> Dict[str, int]:
        """Count events by type."""
        statement = select(
            AnalyticsEvent.event_type,
            func.count(AnalyticsEvent.id).label('count')
        ).group_by(AnalyticsEvent.event_type)
        
        results = self.session.exec(statement).all()
        return {event_type: count for event_type, count in results}
    
    def get_unprocessed_events(self, limit: int = 1000) -> List[AnalyticsEvent]:
        """Get unprocessed events."""
        statement = select(AnalyticsEvent).where(
            AnalyticsEvent.processed == False
        ).order_by(AnalyticsEvent.timestamp.asc()).limit(limit)
        
        return self.session.exec(statement).all()


class EventValidator:
    """Validates analytics events before persistence."""
    
    MAX_PROPERTIES = 50
    MAX_PROPERTY_KEY_LENGTH = 100
    MAX_PROPERTY_VALUE_LENGTH = 1000
    MAX_TAGS = 20
    MAX_TAG_LENGTH = 50
    MAX_EVENT_NAME_LENGTH = 100
    
    @classmethod
    def validate_event(cls, event: EventCreate) -> EventValidationResult:
        """Validate event data."""
        errors = []
        warnings = []
        
        # Validate event name
        if len(event.event_name) > cls.MAX_EVENT_NAME_LENGTH:
            errors.append(EventValidationError(
                field="event_name",
                message=f"Event name too long (max {cls.MAX_EVENT_NAME_LENGTH})",
                value=event.event_name
            ))
        
        # Validate properties
        if len(event.properties) > cls.MAX_PROPERTIES:
            errors.append(EventValidationError(
                field="properties",
                message=f"Too many properties (max {cls.MAX_PROPERTIES})",
                value=len(event.properties)
            ))
        
        for key, value in event.properties.items():
            if len(str(key)) > cls.MAX_PROPERTY_KEY_LENGTH:
                errors.append(EventValidationError(
                    field=f"properties.{key}",
                    message=f"Property key too long (max {cls.MAX_PROPERTY_KEY_LENGTH})",
                    value=key
                ))
            
            if isinstance(value, str) and len(value) > cls.MAX_PROPERTY_VALUE_LENGTH:
                errors.append(EventValidationError(
                    field=f"properties.{key}",
                    message=f"Property value too long (max {cls.MAX_PROPERTY_VALUE_LENGTH})",
                    value=len(value)
                ))
        
        # Validate tags
        if len(event.tags) > cls.MAX_TAGS:
            errors.append(EventValidationError(
                field="tags",
                message=f"Too many tags (max {cls.MAX_TAGS})",
                value=len(event.tags)
            ))
        
        for tag in event.tags:
            if len(tag) > cls.MAX_TAG_LENGTH:
                errors.append(EventValidationError(
                    field="tags",
                    message=f"Tag too long (max {cls.MAX_TAG_LENGTH})",
                    value=tag
                ))
        
        # Warnings for best practices
        if not event.properties:
            warnings.append("Event has no properties - consider adding context")
        
        if event.event_type.value == "custom" and not event.tags:
            warnings.append("Custom events should have tags for better categorization")
        
        return EventValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )


class EventFormatter:
    """Formats and enriches events before persistence."""
    
    @staticmethod
    def format_event(event_data: EventCreate, context: Optional[Dict[str, Any]] = None) -> AnalyticsEvent:
        """Format event data into database model."""
        if context is None:
            context = {}
        
        # Generate unique event ID
        event_id = str(uuid.uuid4())
        
        # Enrich with context
        enriched_metadata = {
            **event_data.metadata,
            "created_at": datetime.utcnow().isoformat(),
            "source": context.get("source", "api"),
            "version": context.get("version", "1.0")
        }
        
        return AnalyticsEvent(
            event_id=event_id,
            event_name=event_data.event_name,
            event_type=event_data.event_type,
            properties=event_data.properties,
            metadata=enriched_metadata,
            user_id=event_data.user_id,
            session_id=event_data.session_id,
            severity=event_data.severity,
            tags=event_data.tags,
            user_agent=context.get("user_agent"),
            ip_address=context.get("ip_address"),
            referrer=context.get("referrer"),
            timezone=context.get("timezone")
        )


class EventService:
    """Service for managing analytics events."""
    
    def __init__(self, session: Session):
        self.repository = EventRepository(session)
        self.validator = EventValidator()
        self.formatter = EventFormatter()
    
    @transactional
    def create_event(self, event_data: EventCreate, context: Optional[Dict[str, Any]] = None) -> AnalyticsEvent:
        """Create and persist an analytics event."""
        # Validate event
        validation_result = self.validator.validate_event(event_data)
        if not validation_result.valid:
            raise ValueError(f"Event validation failed: {validation_result.errors}")
        
        # Format and create event
        event = self.formatter.format_event(event_data, context)
        return self.repository.create(event)
    
    @transactional
    def create_events_batch(self, events_data: List[EventCreate], context: Optional[Dict[str, Any]] = None) -> List[AnalyticsEvent]:
        """Create multiple events in batch."""
        created_events = []
        
        for event_data in events_data:
            try:
                event = self.create_event(event_data, context)
                created_events.append(event)
            except ValueError as e:
                # Log validation error but continue with other events
                print(f"Skipping invalid event: {e}")
        
        return created_events
    
    def get_event(self, event_id: int) -> Optional[AnalyticsEvent]:
        """Get event by ID."""
        return self.repository.get(event_id)
    
    def get_events_by_query(self, query: EventQuery) -> List[AnalyticsEvent]:
        """Get events based on query parameters."""
        statement = select(AnalyticsEvent)
        conditions = []
        
        if query.event_type:
            conditions.append(AnalyticsEvent.event_type == query.event_type)
        
        if query.event_name:
            conditions.append(AnalyticsEvent.event_name == query.event_name)
        
        if query.user_id:
            conditions.append(AnalyticsEvent.user_id == query.user_id)
        
        if query.session_id:
            conditions.append(AnalyticsEvent.session_id == query.session_id)
        
        if query.severity:
            conditions.append(AnalyticsEvent.severity == query.severity)
        
        if query.processed is not None:
            conditions.append(AnalyticsEvent.processed == query.processed)
        
        if query.start_date:
            conditions.append(AnalyticsEvent.timestamp >= query.start_date)
        
        if query.end_date:
            conditions.append(AnalyticsEvent.timestamp <= query.end_date)
        
        if conditions:
            statement = statement.where(and_(*conditions))
        
        statement = statement.order_by(AnalyticsEvent.timestamp.desc())
        statement = statement.offset(query.offset).limit(query.limit)
        
        return self.repository.session.exec(statement).all()
    
    @transactional
    def update_event(self, event_id: int, update_data: EventUpdate) -> Optional[AnalyticsEvent]:
        """Update an event."""
        event = self.repository.get(event_id)
        if not event:
            return None
        
        update_dict = update_data.dict(exclude_unset=True)
        
        # Mark as processed if updating processed status
        if update_data.processed is True:
            update_dict["processed_at"] = datetime.utcnow()
        
        return self.repository.update(event_id, update_dict)
    
    @transactional
    def mark_events_processed(self, event_ids: List[int]) -> int:
        """Mark multiple events as processed."""
        processed_count = 0
        
        for event_id in event_ids:
            event = self.update_event(event_id, EventUpdate(processed=True))
            if event:
                processed_count += 1
        
        return processed_count
    
    def get_event_stats(self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> EventStats:
        """Get comprehensive event statistics."""
        # Default to last 30 days if no dates provided
        if not end_date:
            end_date = datetime.utcnow()
        if not start_date:
            start_date = end_date - timedelta(days=30)
        
        # Base query for date range
        base_query = select(AnalyticsEvent).where(
            and_(
                AnalyticsEvent.timestamp >= start_date,
                AnalyticsEvent.timestamp <= end_date
            )
        )
        
        # Total events
        total_events = len(self.repository.session.exec(base_query).all())
        
        # Events by type
        events_by_type = self.repository.count_by_type()
        
        # Events by severity
        severity_query = select(
            AnalyticsEvent.severity,
            func.count(AnalyticsEvent.id).label('count')
        ).where(
            and_(
                AnalyticsEvent.timestamp >= start_date,
                AnalyticsEvent.timestamp <= end_date
            )
        ).group_by(AnalyticsEvent.severity)
        
        severity_results = self.repository.session.exec(severity_query).all()
        events_by_severity = {severity: count for severity, count in severity_results}
        
        # Processed vs unprocessed
        processed_query = select(func.count(AnalyticsEvent.id)).where(
            and_(
                AnalyticsEvent.timestamp >= start_date,
                AnalyticsEvent.timestamp <= end_date,
                AnalyticsEvent.processed == True
            )
        )
        processed_events = self.repository.session.exec(processed_query).first() or 0
        unprocessed_events = total_events - processed_events
        
        # Top users (by event count)
        top_users_query = select(
            AnalyticsEvent.user_id,
            func.count(AnalyticsEvent.id).label('count')
        ).where(
            and_(
                AnalyticsEvent.timestamp >= start_date,
                AnalyticsEvent.timestamp <= end_date,
                AnalyticsEvent.user_id.isnot(None)
            )
        ).group_by(AnalyticsEvent.user_id).order_by(func.count(AnalyticsEvent.id).desc()).limit(10)
        
        top_users_results = self.repository.session.exec(top_users_query).all()
        top_users = [{"user_id": user_id, "event_count": count} for user_id, count in top_users_results]
        
        # Top events (by frequency)
        top_events_query = select(
            AnalyticsEvent.event_name,
            func.count(AnalyticsEvent.id).label('count')
        ).where(
            and_(
                AnalyticsEvent.timestamp >= start_date,
                AnalyticsEvent.timestamp <= end_date
            )
        ).group_by(AnalyticsEvent.event_name).order_by(func.count(AnalyticsEvent.id).desc()).limit(10)
        
        top_events_results = self.repository.session.exec(top_events_query).all()
        top_events = [{"event_name": event_name, "count": count} for event_name, count in top_events_results]
        
        return EventStats(
            total_events=total_events,
            events_by_type=events_by_type,
            events_by_severity=events_by_severity,
            processed_events=processed_events,
            unprocessed_events=unprocessed_events,
            date_range={"start_date": start_date, "end_date": end_date},
            top_users=top_users,
            top_events=top_events
        )
    
    def create_performance_event(self, perf_event: PerformanceEvent, user_id: Optional[str] = None) -> AnalyticsEvent:
        """Create event from performance data."""
        event_data = perf_event.to_analytics_event(user_id)
        return self.create_event(event_data)
    
    def create_user_interaction_event(self, interaction: UserInteractionEvent, user_id: Optional[str] = None) -> AnalyticsEvent:
        """Create event from user interaction data."""
        event_data = interaction.to_analytics_event(user_id)
        return self.create_event(event_data)
    
    def create_api_request_event(self, api_event: APIRequestEvent, user_id: Optional[str] = None) -> AnalyticsEvent:
        """Create event from API request data."""
        event_data = api_event.to_analytics_event(user_id)
        return self.create_event(event_data)


# Dependency injection helper
def get_event_service(session: Session = Depends(get_session)) -> EventService:
    """Get event service instance."""
    return EventService(session)
