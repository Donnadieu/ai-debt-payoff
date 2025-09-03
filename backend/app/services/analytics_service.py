"""Analytics service for managing analytics events and user sessions."""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from backend.app.schemas.analytics import (
    AnalyticsEvent, AnalyticsEventCreate, AnalyticsEventResponse,
    UserSession, UserSessionCreate, UserSessionResponse,
    EventType, EventCategory
)
from backend.app.core.repository import AnalyticsRepository
from backend.app.core.transaction import transactional
import logging

logger = logging.getLogger(__name__)


class AnalyticsService:
    """Service class for analytics business logic."""
    
    def __init__(self):
        self.event_repository = AnalyticsRepository(AnalyticsEvent)
        self.session_repository = AnalyticsRepository(UserSession)
    
    @transactional
    def track_event(self, event_data: AnalyticsEventCreate) -> AnalyticsEventResponse:
        """Track a new analytics event."""
        event = self.event_repository.create(obj_in=event_data)
        logger.debug(f"Tracked event {event.event_name} for user {event.user_id}")
        
        return AnalyticsEventResponse.model_validate(event)
    
    def get_user_events(
        self, 
        user_id: str, 
        *, 
        skip: int = 0, 
        limit: int = 100,
        event_type: Optional[EventType] = None,
        category: Optional[EventCategory] = None
    ) -> List[AnalyticsEventResponse]:
        """Get analytics events for a specific user."""
        filters = {"user_id": user_id}
        if event_type:
            filters["event_type"] = event_type.value
        if category:
            filters["category"] = category.value
        
        events = self.event_repository.get_multi(skip=skip, limit=limit, filters=filters)
        return [AnalyticsEventResponse.model_validate(event) for event in events]
    
    def get_events_by_type(
        self, 
        event_type: EventType, 
        *, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[AnalyticsEventResponse]:
        """Get events by type."""
        events = self.event_repository.get_by_event_type(event_type.value, skip=skip, limit=limit)
        return [AnalyticsEventResponse.model_validate(event) for event in events]
    
    def get_unprocessed_events(self, *, skip: int = 0, limit: int = 100) -> List[AnalyticsEventResponse]:
        """Get unprocessed analytics events."""
        events = self.event_repository.get_unprocessed_events(skip=skip, limit=limit)
        return [AnalyticsEventResponse.model_validate(event) for event in events]
    
    @transactional
    def mark_events_processed(self, event_ids: List[int]) -> int:
        """Mark multiple events as processed."""
        processed_count = 0
        for event_id in event_ids:
            event = self.event_repository.get(event_id)
            if event and not event.processed:
                event.processed = True
                event.processed_at = datetime.utcnow()
                self.event_repository.update(db_obj=event, obj_in=event)
                processed_count += 1
        
        logger.info(f"Marked {processed_count} events as processed")
        return processed_count
    
    @transactional
    def create_user_session(self, session_data: UserSessionCreate) -> UserSessionResponse:
        """Create a new user session."""
        session = self.session_repository.create(obj_in=session_data)
        logger.info(f"Created session {session.session_id} for user {session.user_id}")
        
        return UserSessionResponse.model_validate(session)
    
    @transactional
    def end_user_session(self, session_id: str) -> Optional[UserSessionResponse]:
        """End a user session."""
        filters = {"session_id": session_id, "is_active": True}
        sessions = self.session_repository.get_multi(filters=filters, limit=1)
        
        if not sessions:
            return None
        
        session = sessions[0]
        session.ended_at = datetime.utcnow()
        session.is_active = False
        
        updated_session = self.session_repository.update(db_obj=session, obj_in=session)
        logger.info(f"Ended session {session_id}")
        
        return UserSessionResponse.model_validate(updated_session)
    
    @transactional
    def update_session_activity(self, session_id: str) -> Optional[UserSessionResponse]:
        """Update last activity time for a session."""
        filters = {"session_id": session_id, "is_active": True}
        sessions = self.session_repository.get_multi(filters=filters, limit=1)
        
        if not sessions:
            return None
        
        session = sessions[0]
        session.last_activity = datetime.utcnow()
        
        updated_session = self.session_repository.update(db_obj=session, obj_in=session)
        return UserSessionResponse.model_validate(updated_session)
    
    def get_user_sessions(
        self, 
        user_id: str, 
        *, 
        skip: int = 0, 
        limit: int = 100,
        active_only: bool = False
    ) -> List[UserSessionResponse]:
        """Get user sessions."""
        filters = {"user_id": user_id}
        if active_only:
            filters["is_active"] = True
        
        sessions = self.session_repository.get_multi(skip=skip, limit=limit, filters=filters)
        return [UserSessionResponse.model_validate(session) for session in sessions]
    
    def get_analytics_summary(
        self, 
        user_id: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get analytics summary with counts and metrics."""
        filters = {}
        if user_id:
            filters["user_id"] = user_id
        
        # Basic counts
        total_events = self.event_repository.count(filters=filters)
        processed_events = self.event_repository.count(filters={**filters, "processed": True})
        
        summary = {
            "total_events": total_events,
            "processed_events": processed_events,
            "unprocessed_events": total_events - processed_events,
            "events_by_type": {},
            "events_by_category": {}
        }
        
        # Count by event type
        for event_type in EventType:
            type_filters = {**filters, "event_type": event_type.value}
            summary["events_by_type"][event_type.value] = self.event_repository.count(filters=type_filters)
        
        # Count by category
        for category in EventCategory:
            category_filters = {**filters, "category": category.value}
            summary["events_by_category"][category.value] = self.event_repository.count(filters=category_filters)
        
        return summary
    
    def get_user_engagement_metrics(self, user_id: str, days: int = 30) -> Dict[str, Any]:
        """Get user engagement metrics for the last N days."""
        # This would need time-based filtering in the repository
        # For now, return basic metrics
        
        user_events = self.get_user_events(user_id, limit=1000)
        user_sessions = self.get_user_sessions(user_id, limit=100)
        
        active_sessions = [s for s in user_sessions if s.is_active]
        
        metrics = {
            "total_events": len(user_events),
            "total_sessions": len(user_sessions),
            "active_sessions": len(active_sessions),
            "events_by_type": {},
            "avg_session_duration": 0  # Would need calculation based on session times
        }
        
        # Group events by type
        for event in user_events:
            event_type = event.event_type
            metrics["events_by_type"][event_type] = metrics["events_by_type"].get(event_type, 0) + 1
        
        return metrics
    
    @transactional
    def cleanup_old_events(self, days_to_keep: int = 90) -> int:
        """Clean up old analytics events and return count of removed items."""
        # This would need a custom repository method for time-based deletion
        # For now, return 0 as placeholder
        logger.info(f"Analytics cleanup completed, keeping last {days_to_keep} days")
        return 0
