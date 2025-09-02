"""Analytics event tracking system with console logging for development."""

import json
import time
from datetime import datetime
from typing import Dict, Any, Optional
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class EventType(str, Enum):
    """Predefined analytics event types."""
    ADD_DEBT = "add_debt"
    VIEW_PLAN = "view_plan"
    NUDGE_GENERATED = "nudge_generated"
    NUDGE_VALIDATED = "nudge_validated"
    NUDGE_REJECTED = "nudge_rejected"
    NUDGE_SENT = "nudge_sent"
    SLIP_ALERT_FIRED = "slip_alert_fired"
    SLIP_ACTION_CONFIRMED = "slip_action_confirmed"
    API_REQUEST = "api_request"
    ERROR_OCCURRED = "error_occurred"


def analytics_event(name: str, props: Optional[Dict[str, Any]] = None) -> None:
    """
    Track analytics event with console logging for development.
    
    Args:
        name: Event name (use EventType enum values)
        props: Optional event properties dictionary
    """
    if props is None:
        props = {}
    
    # Add standard metadata
    event_data = {
        "event": name,
        "timestamp": datetime.utcnow().isoformat(),
        "properties": props,
        "session_id": _get_session_id(),
        "environment": "development"
    }
    
    # Console logging for development
    logger.info(f"📊 Analytics Event: {json.dumps(event_data, indent=2)}")
    
    # TODO: Add integration hooks for production analytics services
    # This is where external services like Mixpanel, Amplitude, etc. would be called
    
    # Store in database if analytics service is available
    try:
        from backend.app.services.analytics_service import AnalyticsService
        from backend.app.schemas.analytics import AnalyticsEventCreate, EventType as DBEventType, EventCategory
        
        # Map to database event
        db_event = AnalyticsEventCreate(
            user_id=props.get("user_id", "anonymous"),
            event_type=DBEventType.USER_ACTION,
            event_name=name,
            category=EventCategory.ENGAGEMENT,
            properties=props,
            session_id=_get_session_id(),
            source="api"
        )
        
        analytics_service = AnalyticsService()
        analytics_service.track_event(db_event)
        
    except ImportError:
        # Analytics service not available yet
        logger.debug("Analytics service not available, using console logging only")


def track_performance(operation: str, duration_ms: float, metadata: Optional[Dict[str, Any]] = None) -> None:
    """
    Track performance metrics for API operations.
    
    Args:
        operation: Name of the operation being tracked
        duration_ms: Duration in milliseconds
        metadata: Optional additional metadata
    """
    if metadata is None:
        metadata = {}
    
    perf_data = {
        "operation": operation,
        "duration_ms": duration_ms,
        "timestamp": datetime.utcnow().isoformat(),
        "metadata": metadata
    }
    
    # Log performance data
    logger.info(f"⚡ Performance: {operation} took {duration_ms:.2f}ms")
    
    # Track as analytics event
    analytics_event("performance_metric", {
        "operation": operation,
        "duration_ms": duration_ms,
        **metadata
    })


def track_api_request(method: str, path: str, status_code: int, duration_ms: float, user_id: Optional[str] = None) -> None:
    """
    Track API request metrics.
    
    Args:
        method: HTTP method
        path: Request path
        status_code: HTTP status code
        duration_ms: Request duration in milliseconds
        user_id: Optional user identifier
    """
    analytics_event(EventType.API_REQUEST, {
        "method": method,
        "path": path,
        "status_code": status_code,
        "duration_ms": duration_ms,
        "user_id": user_id,
        "success": 200 <= status_code < 300
    })


def track_error(error_type: str, error_message: str, context: Optional[Dict[str, Any]] = None) -> None:
    """
    Track error events for monitoring and debugging.
    
    Args:
        error_type: Type/category of error
        error_message: Error message or description
        context: Optional context information
    """
    if context is None:
        context = {}
    
    analytics_event(EventType.ERROR_OCCURRED, {
        "error_type": error_type,
        "error_message": error_message,
        "context": context
    })


def _get_session_id() -> str:
    """Generate or retrieve session ID for tracking."""
    # Simple session ID generation for development
    # In production, this would integrate with proper session management
    return f"dev_session_{int(time.time())}"


# Integration hooks for external analytics services
class AnalyticsIntegration:
    """Base class for external analytics service integrations."""
    
    def track_event(self, event_name: str, properties: Dict[str, Any]) -> None:
        """Override this method to integrate with external services."""
        raise NotImplementedError
    
    def identify_user(self, user_id: str, traits: Dict[str, Any]) -> None:
        """Override this method to identify users in external services."""
        raise NotImplementedError


# Registry for analytics integrations
_integrations: list[AnalyticsIntegration] = []


def register_integration(integration: AnalyticsIntegration) -> None:
    """Register an external analytics integration."""
    _integrations.append(integration)
    logger.info(f"Registered analytics integration: {integration.__class__.__name__}")


def _notify_integrations(event_name: str, properties: Dict[str, Any]) -> None:
    """Notify all registered integrations of an event."""
    for integration in _integrations:
        try:
            integration.track_event(event_name, properties)
        except Exception as e:
            logger.error(f"Analytics integration error: {e}")


# Example integration for future use
class MixpanelIntegration(AnalyticsIntegration):
    """Example Mixpanel integration (placeholder)."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def track_event(self, event_name: str, properties: Dict[str, Any]) -> None:
        # TODO: Implement actual Mixpanel API calls
        logger.debug(f"Mixpanel: {event_name} - {properties}")
    
    def identify_user(self, user_id: str, traits: Dict[str, Any]) -> None:
        # TODO: Implement user identification
        logger.debug(f"Mixpanel identify: {user_id} - {traits}")
