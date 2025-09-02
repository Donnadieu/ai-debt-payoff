"""Performance monitoring utilities for API operations."""

import time
import psutil
import threading
from datetime import datetime
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from collections import defaultdict, deque
import logging

logger = logging.getLogger(__name__)


@dataclass
class PerformanceMetric:
    """Performance metric data structure."""
    operation: str
    duration_ms: float
    timestamp: datetime
    memory_usage_mb: float
    cpu_percent: float
    metadata: Dict[str, Any]


class PerformanceMonitor:
    """Performance monitoring system with metrics collection."""
    
    def __init__(self, max_metrics: int = 1000):
        self.metrics: deque[PerformanceMetric] = deque(maxlen=max_metrics)
        self.operation_stats: Dict[str, List[float]] = defaultdict(list)
        self.lock = threading.Lock()
    
    def record_metric(self, operation: str, duration_ms: float, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Record a performance metric."""
        if metadata is None:
            metadata = {}
        
        # Get system metrics
        memory_usage = psutil.virtual_memory().used / 1024 / 1024  # MB
        cpu_percent = psutil.cpu_percent()
        
        metric = PerformanceMetric(
            operation=operation,
            duration_ms=duration_ms,
            timestamp=datetime.utcnow(),
            memory_usage_mb=memory_usage,
            cpu_percent=cpu_percent,
            metadata=metadata
        )
        
        with self.lock:
            self.metrics.append(metric)
            self.operation_stats[operation].append(duration_ms)
            
            # Keep only last 100 measurements per operation
            if len(self.operation_stats[operation]) > 100:
                self.operation_stats[operation] = self.operation_stats[operation][-100:]
        
        # Log slow operations
        if duration_ms > 1000:  # > 1 second
            logger.warning(f"Slow operation detected: {operation} took {duration_ms:.2f}ms")
    
    def get_operation_stats(self, operation: str) -> Dict[str, float]:
        """Get statistics for a specific operation."""
        with self.lock:
            durations = self.operation_stats.get(operation, [])
        
        if not durations:
            return {}
        
        return {
            "count": len(durations),
            "avg_ms": sum(durations) / len(durations),
            "min_ms": min(durations),
            "max_ms": max(durations),
            "p95_ms": self._percentile(durations, 95),
            "p99_ms": self._percentile(durations, 99)
        }
    
    def get_all_stats(self) -> Dict[str, Dict[str, float]]:
        """Get statistics for all operations."""
        with self.lock:
            operations = list(self.operation_stats.keys())
        
        return {op: self.get_operation_stats(op) for op in operations}
    
    def get_system_metrics(self) -> Dict[str, float]:
        """Get current system performance metrics."""
        return {
            "memory_usage_mb": psutil.virtual_memory().used / 1024 / 1024,
            "memory_percent": psutil.virtual_memory().percent,
            "cpu_percent": psutil.cpu_percent(),
            "disk_usage_percent": psutil.disk_usage('/').percent
        }
    
    def _percentile(self, data: List[float], percentile: int) -> float:
        """Calculate percentile of data."""
        if not data:
            return 0.0
        
        sorted_data = sorted(data)
        index = int((percentile / 100) * len(sorted_data))
        return sorted_data[min(index, len(sorted_data) - 1)]
    
    def clear_metrics(self) -> None:
        """Clear all stored metrics."""
        with self.lock:
            self.metrics.clear()
            self.operation_stats.clear()


# Global performance monitor
performance_monitor = PerformanceMonitor()


class PerformanceTimer:
    """Context manager for timing operations."""
    
    def __init__(self, operation: str, metadata: Optional[Dict[str, Any]] = None):
        self.operation = operation
        self.metadata = metadata or {}
        self.start_time = 0.0
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration_ms = (time.time() - self.start_time) * 1000
        
        # Add exception info to metadata if an error occurred
        if exc_type:
            self.metadata.update({
                "error": True,
                "exception_type": exc_type.__name__,
                "exception_message": str(exc_val)
            })
        
        performance_monitor.record_metric(self.operation, duration_ms, self.metadata)


def time_operation(operation: str, metadata: Optional[Dict[str, Any]] = None):
    """Decorator to time function execution."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            with PerformanceTimer(operation, metadata):
                return func(*args, **kwargs)
        return wrapper
    return decorator


class PerformanceAlert:
    """Performance alerting system."""
    
    def __init__(self):
        self.thresholds = {
            "slow_request_ms": 2000,
            "high_memory_percent": 85,
            "high_cpu_percent": 90,
            "high_disk_percent": 90
        }
        self.alert_callbacks = []
    
    def add_alert_callback(self, callback):
        """Add callback function for performance alerts."""
        self.alert_callbacks.append(callback)
    
    def check_thresholds(self, metric: PerformanceMetric) -> None:
        """Check if metric exceeds thresholds and trigger alerts."""
        alerts = []
        
        if metric.duration_ms > self.thresholds["slow_request_ms"]:
            alerts.append(f"Slow operation: {metric.operation} took {metric.duration_ms:.2f}ms")
        
        if metric.memory_usage_mb > 0:  # Only check if we have memory data
            memory_percent = psutil.virtual_memory().percent
            if memory_percent > self.thresholds["high_memory_percent"]:
                alerts.append(f"High memory usage: {memory_percent:.1f}%")
        
        if metric.cpu_percent > self.thresholds["high_cpu_percent"]:
            alerts.append(f"High CPU usage: {metric.cpu_percent:.1f}%")
        
        # Trigger alerts
        for alert in alerts:
            logger.warning(f"Performance Alert: {alert}")
            for callback in self.alert_callbacks:
                try:
                    callback(alert, metric)
                except Exception as e:
                    logger.error(f"Alert callback error: {e}")


# Global performance alerting
performance_alert = PerformanceAlert()


def get_performance_report() -> Dict[str, Any]:
    """Generate comprehensive performance report."""
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "system_metrics": performance_monitor.get_system_metrics(),
        "operation_stats": performance_monitor.get_all_stats(),
        "total_metrics_collected": len(performance_monitor.metrics),
        "thresholds": performance_alert.thresholds
    }


def configure_performance_monitoring(**kwargs) -> None:
    """Configure performance monitoring settings."""
    if "thresholds" in kwargs:
        performance_alert.thresholds.update(kwargs["thresholds"])
        logger.info(f"Updated performance thresholds: {kwargs['thresholds']}")
    
    if "max_metrics" in kwargs:
        # Would need to recreate monitor with new size
        logger.info(f"Max metrics setting: {kwargs['max_metrics']}")


# Health check function
def health_check() -> Dict[str, Any]:
    """Perform system health check."""
    system_metrics = performance_monitor.get_system_metrics()
    
    health_status = "healthy"
    issues = []
    
    if system_metrics["memory_percent"] > 90:
        health_status = "warning"
        issues.append("High memory usage")
    
    if system_metrics["cpu_percent"] > 95:
        health_status = "critical"
        issues.append("Critical CPU usage")
    
    if system_metrics["disk_usage_percent"] > 95:
        health_status = "critical"
        issues.append("Critical disk usage")
    
    return {
        "status": health_status,
        "issues": issues,
        "metrics": system_metrics,
        "timestamp": datetime.utcnow().isoformat()
    }
