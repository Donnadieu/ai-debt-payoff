"""Analytics API endpoints for event tracking and performance monitoring."""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel, Field
from datetime import datetime

from ..core.analytics import analytics_core, analytics_config, get_analytics_stats
from ..core.performance import performance_monitor, get_performance_report, health_check

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


class EventRequest(BaseModel):
    """Request model for tracking events."""
    event: str = Field(..., description="Event name")
    properties: Dict[str, Any] = Field(default_factory=dict, description="Event properties")
    user_id: Optional[str] = Field(None, description="User ID")


class EventResponse(BaseModel):
    """Response model for event tracking."""
    success: bool
    message: str
    event_id: Optional[str] = None


class AnalyticsStatsResponse(BaseModel):
    """Response model for analytics statistics."""
    buffer_size: int
    last_flush: float
    enabled_services: List[str]
    config: Dict[str, Any]


class PerformanceStatsResponse(BaseModel):
    """Response model for performance statistics."""
    timestamp: str
    system_metrics: Dict[str, float]
    operation_stats: Dict[str, Dict[str, float]]
    total_metrics_collected: int
    thresholds: Dict[str, float]


@router.post("/track", response_model=EventResponse)
async def track_event(event_request: EventRequest):
    """Track an analytics event."""
    try:
        analytics_core.track_event(
            event_name=event_request.event,
            properties=event_request.properties,
            user_id=event_request.user_id
        )
        
        return EventResponse(
            success=True,
            message="Event tracked successfully"
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to track event: {str(e)}")


@router.post("/batch-track")
async def batch_track_events(events: List[EventRequest]):
    """Track multiple analytics events in batch."""
    try:
        tracked_count = 0
        
        for event_request in events:
            analytics_core.track_event(
                event_name=event_request.event,
                properties=event_request.properties,
                user_id=event_request.user_id
            )
            tracked_count += 1
        
        return {
            "success": True,
            "message": f"Successfully tracked {tracked_count} events",
            "tracked_count": tracked_count
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to track batch events: {str(e)}")


@router.post("/flush")
async def flush_events():
    """Manually flush buffered events."""
    try:
        analytics_core.flush_events()
        return {"success": True, "message": "Events flushed successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to flush events: {str(e)}")


@router.get("/stats", response_model=AnalyticsStatsResponse)
async def get_stats():
    """Get analytics system statistics."""
    try:
        stats = get_analytics_stats()
        return AnalyticsStatsResponse(**stats)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get analytics stats: {str(e)}")


@router.get("/performance", response_model=PerformanceStatsResponse)
async def get_performance_stats():
    """Get performance monitoring statistics."""
    try:
        report = get_performance_report()
        return PerformanceStatsResponse(**report)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get performance stats: {str(e)}")


@router.get("/performance/operation/{operation_name}")
async def get_operation_performance(operation_name: str):
    """Get performance statistics for a specific operation."""
    try:
        stats = performance_monitor.get_operation_stats(operation_name)
        
        if not stats:
            raise HTTPException(status_code=404, detail=f"No performance data found for operation: {operation_name}")
        
        return {
            "operation": operation_name,
            "stats": stats
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get operation performance: {str(e)}")


@router.get("/health")
async def analytics_health():
    """Health check endpoint for analytics system."""
    try:
        system_health = health_check()
        analytics_stats = get_analytics_stats()
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "analytics": {
                "enabled": analytics_config.enabled,
                "buffer_size": analytics_stats["buffer_size"],
                "services_count": len(analytics_stats["enabled_services"])
            },
            "system_health": system_health
        }
    
    except Exception as e:
        return {
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e)
        }


@router.post("/config")
async def update_analytics_config(config_updates: Dict[str, Any]):
    """Update analytics configuration."""
    try:
        from ..core.analytics import configure_analytics
        
        configure_analytics(**config_updates)
        
        return {
            "success": True,
            "message": "Analytics configuration updated",
            "updated_config": config_updates
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to update config: {str(e)}")


@router.get("/events/recent")
async def get_recent_events(limit: int = Query(10, ge=1, le=100)):
    """Get recent analytics events from buffer."""
    try:
        # Get recent events from buffer (limited implementation)
        recent_events = list(analytics_core.event_buffer)[-limit:]
        
        return {
            "events": recent_events,
            "count": len(recent_events),
            "total_buffered": len(analytics_core.event_buffer)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get recent events: {str(e)}")


@router.delete("/performance/clear")
async def clear_performance_metrics():
    """Clear all performance metrics."""
    try:
        performance_monitor.clear_metrics()
        
        return {
            "success": True,
            "message": "Performance metrics cleared"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear metrics: {str(e)}")


# User interaction tracking endpoints
@router.post("/user/page-view")
async def track_page_view(
    path: str,
    user_id: Optional[str] = None,
    referrer: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
):
    """Track page view event."""
    try:
        properties = {
            "path": path,
            "referrer": referrer,
            **(metadata or {})
        }
        
        analytics_core.track_event("page_view", properties, user_id)
        
        return {"success": True, "message": "Page view tracked"}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to track page view: {str(e)}")


@router.post("/user/interaction")
async def track_user_interaction(
    interaction_type: str,
    element: str,
    user_id: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
):
    """Track user interaction event."""
    try:
        properties = {
            "interaction_type": interaction_type,
            "element": element,
            **(metadata or {})
        }
        
        analytics_core.track_event("user_interaction", properties, user_id)
        
        return {"success": True, "message": "User interaction tracked"}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to track interaction: {str(e)}")
