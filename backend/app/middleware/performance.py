"""FastAPI middleware for performance monitoring and analytics integration."""

import time
from typing import Callable
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import logging

from ..core.analytics import analytics_core
from ..core.performance import performance_monitor, PerformanceTimer

logger = logging.getLogger(__name__)


class PerformanceMiddleware(BaseHTTPMiddleware):
    """Middleware to track API performance and analytics events."""
    
    def __init__(self, app: FastAPI, track_analytics: bool = True):
        super().__init__(app)
        self.track_analytics = track_analytics
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request with performance tracking."""
        start_time = time.time()
        
        # Extract request metadata
        method = request.method
        path = request.url.path
        user_agent = request.headers.get("user-agent", "unknown")
        client_ip = request.client.host if request.client else "unknown"
        
        # Generate operation name for tracking
        operation_name = f"{method} {path}"
        
        # Track request start
        request_metadata = {
            "method": method,
            "path": path,
            "user_agent": user_agent,
            "client_ip": client_ip,
            "query_params": dict(request.query_params)
        }
        
        response = None
        error_occurred = False
        
        try:
            # Process request with performance timing
            with PerformanceTimer(operation_name, request_metadata):
                response = await call_next(request)
            
        except Exception as e:
            error_occurred = True
            logger.error(f"Request failed: {operation_name} - {str(e)}")
            
            # Track error event
            if self.track_analytics:
                analytics_core.track_event("api_error", {
                    "operation": operation_name,
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                    **request_metadata
                })
            
            raise
        
        finally:
            # Calculate total request time
            duration_ms = (time.time() - start_time) * 1000
            
            # Track analytics event for successful requests
            if not error_occurred and response and self.track_analytics:
                try:
                    analytics_core.track_event("api_request", {
                        "operation": operation_name,
                        "status_code": response.status_code,
                        "duration_ms": duration_ms,
                        "success": 200 <= response.status_code < 400,
                        **request_metadata
                    })
                except Exception as e:
                    # Log analytics error but don't fail the request
                    logger.warning(f"Analytics tracking failed: {e}")
            
            # Add performance headers to response
            if response:
                response.headers["X-Response-Time"] = f"{duration_ms:.2f}ms"
                response.headers["X-Request-ID"] = request.headers.get("X-Request-ID", "unknown")
        
        return response


class AnalyticsMiddleware(BaseHTTPMiddleware):
    """Middleware specifically for analytics event tracking."""
    
    def __init__(self, app: FastAPI, sample_rate: float = 1.0):
        super().__init__(app)
        self.sample_rate = sample_rate  # 0.0 to 1.0 for sampling
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Track user interactions and page views."""
        import random
        
        # Sample requests based on sample_rate
        if random.random() > self.sample_rate:
            return await call_next(request)
        
        # Extract user context
        user_id = request.headers.get("X-User-ID")
        session_id = request.headers.get("X-Session-ID")
        
        # Track page view for GET requests
        if request.method == "GET" and not request.url.path.startswith("/api/"):
            analytics_core.track_event("page_view", {
                "path": request.url.path,
                "referrer": request.headers.get("referer"),
                "user_agent": request.headers.get("user-agent")
            }, user_id=user_id)
        
        # Process request
        response = await call_next(request)
        
        # Track API usage
        if request.url.path.startswith("/api/"):
            analytics_core.track_event("api_usage", {
                "endpoint": request.url.path,
                "method": request.method,
                "status_code": response.status_code,
                "user_id": user_id,
                "session_id": session_id
            })
        
        return response


def setup_middleware(app: FastAPI, enable_performance: bool = True, enable_analytics: bool = True) -> None:
    """Setup all monitoring middleware for the FastAPI app."""
    
    if enable_performance:
        app.add_middleware(PerformanceMiddleware, track_analytics=enable_analytics)
        logger.info("Performance middleware enabled")
    
    if enable_analytics and not enable_performance:
        # Only add analytics middleware if performance middleware isn't already tracking
        app.add_middleware(AnalyticsMiddleware)
        logger.info("Analytics middleware enabled")
    
    logger.info("Monitoring middleware setup complete")


# Health check endpoint helper
async def performance_health_check() -> dict:
    """Generate performance health check data."""
    from ..core.performance import get_performance_report, health_check
    
    return {
        "performance_report": get_performance_report(),
        "health_status": health_check()
    }


# Middleware configuration
class MiddlewareConfig:
    """Configuration for monitoring middleware."""
    
    def __init__(self):
        self.performance_enabled = True
        self.analytics_enabled = True
        self.analytics_sample_rate = 1.0
        self.track_query_params = True
        self.track_headers = False
        self.excluded_paths = ["/health", "/metrics", "/favicon.ico"]
    
    def should_track_path(self, path: str) -> bool:
        """Check if path should be tracked."""
        return path not in self.excluded_paths


# Global middleware configuration
middleware_config = MiddlewareConfig()
