"""Core analytics infrastructure for event tracking and performance monitoring."""

import time
import uuid
from datetime import datetime
from typing import Dict, Any, Optional, Callable
from contextlib import contextmanager
from functools import wraps
import logging

logger = logging.getLogger(__name__)


class AnalyticsCore:
    """Core analytics infrastructure with event buffering and batch processing."""
    
    def __init__(self):
        self.event_buffer: list[Dict[str, Any]] = []
        self.buffer_size = 100
        self.flush_interval = 60  # seconds
        self.last_flush = time.time()
    
    def track_event(self, event_name: str, properties: Dict[str, Any], user_id: Optional[str] = None) -> None:
        """Track an event with automatic buffering."""
        event = {
            "id": str(uuid.uuid4()),
            "event": event_name,
            "properties": properties,
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat(),
            "session_id": self._get_session_id()
        }
        
        self.event_buffer.append(event)
        
        # Auto-flush if buffer is full or time interval exceeded
        if len(self.event_buffer) >= self.buffer_size or (time.time() - self.last_flush) > self.flush_interval:
            self.flush_events()
    
    def flush_events(self) -> None:
        """Flush buffered events to storage/external services."""
        if not self.event_buffer:
            return
        
        events_to_flush = self.event_buffer.copy()
        self.event_buffer.clear()
        self.last_flush = time.time()
        
        logger.info(f"📊 Flushing {len(events_to_flush)} analytics events")
        
        # Process events (console logging for development)
        for event in events_to_flush:
            logger.debug(f"Event: {event['event']} - {event['properties']}")
        
        # TODO: Send to external analytics services
        # TODO: Persist to database
    
    def _get_session_id(self) -> str:
        """Get or generate session ID."""
        # Simple session ID for development
        return f"session_{int(time.time() / 3600)}"  # Hourly sessions


# Global analytics instance
analytics_core = AnalyticsCore()


@contextmanager
def track_timing(operation_name: str, metadata: Optional[Dict[str, Any]] = None):
    """Context manager to track operation timing."""
    start_time = time.time()
    if metadata is None:
        metadata = {}
    
    try:
        yield
    finally:
        duration = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        analytics_core.track_event("operation_timing", {
            "operation": operation_name,
            "duration_ms": duration,
            **metadata
        })


def timed_operation(operation_name: str):
    """Decorator to automatically track function execution time."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            with track_timing(operation_name, {"function": func.__name__}):
                return func(*args, **kwargs)
        return wrapper
    return decorator


class EventValidator:
    """Validates analytics events before processing."""
    
    REQUIRED_FIELDS = ["event", "timestamp"]
    MAX_PROPERTY_COUNT = 50
    MAX_PROPERTY_VALUE_LENGTH = 1000
    
    @classmethod
    def validate_event(cls, event: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Validate event structure and content."""
        # Check required fields
        for field in cls.REQUIRED_FIELDS:
            if field not in event:
                return False, f"Missing required field: {field}"
        
        # Validate properties
        properties = event.get("properties", {})
        if not isinstance(properties, dict):
            return False, "Properties must be a dictionary"
        
        if len(properties) > cls.MAX_PROPERTY_COUNT:
            return False, f"Too many properties (max {cls.MAX_PROPERTY_COUNT})"
        
        # Validate property values
        for key, value in properties.items():
            if isinstance(value, str) and len(value) > cls.MAX_PROPERTY_VALUE_LENGTH:
                return False, f"Property '{key}' value too long (max {cls.MAX_PROPERTY_VALUE_LENGTH})"
        
        return True, None


class AnalyticsConfig:
    """Configuration for analytics system."""
    
    def __init__(self):
        self.enabled = True
        self.debug_mode = True
        self.console_logging = True
        self.buffer_size = 100
        self.flush_interval = 60
        self.external_services = {}
    
    def enable_service(self, service_name: str, config: Dict[str, Any]) -> None:
        """Enable an external analytics service."""
        self.external_services[service_name] = config
        logger.info(f"Enabled analytics service: {service_name}")
    
    def disable_service(self, service_name: str) -> None:
        """Disable an external analytics service."""
        if service_name in self.external_services:
            del self.external_services[service_name]
            logger.info(f"Disabled analytics service: {service_name}")


# Global configuration
analytics_config = AnalyticsConfig()


def configure_analytics(**kwargs) -> None:
    """Configure analytics system settings."""
    for key, value in kwargs.items():
        if hasattr(analytics_config, key):
            setattr(analytics_config, key, value)
            logger.info(f"Analytics config updated: {key} = {value}")


def get_analytics_stats() -> Dict[str, Any]:
    """Get analytics system statistics."""
    return {
        "buffer_size": len(analytics_core.event_buffer),
        "last_flush": analytics_core.last_flush,
        "enabled_services": list(analytics_config.external_services.keys()),
        "config": {
            "enabled": analytics_config.enabled,
            "debug_mode": analytics_config.debug_mode,
            "console_logging": analytics_config.console_logging
        }
    }
