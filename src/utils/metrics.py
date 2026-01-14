"""
Metrics collection and monitoring for production observability.
"""
import time
import logging
from typing import Dict, Any, Optional
from collections import defaultdict
from datetime import datetime
from dataclasses import dataclass, field
import asyncio

logger = logging.getLogger(__name__)


@dataclass
class Metric:
    """Represents a single metric data point"""
    name: str
    value: float
    timestamp: datetime
    tags: Dict[str, str] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'value': self.value,
            'timestamp': self.timestamp.isoformat(),
            'tags': self.tags
        }


class MetricsCollector:
    """
    Lightweight metrics collector for monitoring system performance.
    
    Collects:
    - Request counts and rates
    - Response times (latency)
    - Error rates
    - Success rates
    - Resource usage
    """
    
    _instance: Optional['MetricsCollector'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self.counters: Dict[str, int] = defaultdict(int)
        self.gauges: Dict[str, float] = defaultdict(float)
        self.histograms: Dict[str, list] = defaultdict(list)
        self.timers: Dict[str, float] = {}
        self._initialized = True
        
        logger.info("Metrics collector initialized")
    
    def increment(self, metric_name: str, value: int = 1, tags: Optional[Dict[str, str]] = None):
        """Increment a counter metric"""
        key = self._make_key(metric_name, tags)
        self.counters[key] += value
    
    def gauge(self, metric_name: str, value: float, tags: Optional[Dict[str, str]] = None):
        """Set a gauge metric (current value)"""
        key = self._make_key(metric_name, tags)
        self.gauges[key] = value
    
    def histogram(self, metric_name: str, value: float, tags: Optional[Dict[str, str]] = None):
        """Add a value to a histogram (for percentile calculations)"""
        key = self._make_key(metric_name, tags)
        self.histograms[key].append(value)
        
        # Keep only last 1000 values to prevent memory issues
        if len(self.histograms[key]) > 1000:
            self.histograms[key] = self.histograms[key][-1000:]
    
    def timing(self, metric_name: str, duration_ms: float, tags: Optional[Dict[str, str]] = None):
        """Record a timing/duration metric"""
        self.histogram(f"{metric_name}.duration_ms", duration_ms, tags)
        self.increment(f"{metric_name}.count", 1, tags)
    
    def start_timer(self, timer_id: str):
        """Start a timer"""
        self.timers[timer_id] = time.time()
    
    def stop_timer(self, timer_id: str, metric_name: str, tags: Optional[Dict[str, str]] = None) -> float:
        """Stop a timer and record the duration"""
        if timer_id not in self.timers:
            logger.warning(f"Timer {timer_id} was not started")
            return 0.0
        
        start_time = self.timers.pop(timer_id)
        duration_ms = (time.time() - start_time) * 1000
        self.timing(metric_name, duration_ms, tags)
        return duration_ms
    
    def _make_key(self, metric_name: str, tags: Optional[Dict[str, str]]) -> str:
        """Create a unique key for a metric with tags"""
        if not tags:
            return metric_name
        
        tag_str = ','.join(f"{k}={v}" for k, v in sorted(tags.items()))
        return f"{metric_name}[{tag_str}]"
    
    def get_stats(self) -> Dict[str, Any]:
        """Get all collected metrics"""
        stats = {
            'counters': dict(self.counters),
            'gauges': dict(self.gauges),
            'histograms': {}
        }
        
        # Calculate histogram statistics
        for key, values in self.histograms.items():
            if values:
                sorted_values = sorted(values)
                stats['histograms'][key] = {
                    'count': len(values),
                    'min': min(values),
                    'max': max(values),
                    'avg': sum(values) / len(values),
                    'p50': sorted_values[int(len(values) * 0.5)],
                    'p95': sorted_values[int(len(values) * 0.95)],
                    'p99': sorted_values[int(len(values) * 0.99)]
                }
        
        return stats
    
    def reset(self):
        """Reset all metrics"""
        self.counters.clear()
        self.gauges.clear()
        self.histograms.clear()
        self.timers.clear()
        logger.info("Metrics reset")


# Global instance
_metrics = MetricsCollector()


def increment(metric_name: str, value: int = 1, tags: Optional[Dict[str, str]] = None):
    """Increment a counter metric"""
    _metrics.increment(metric_name, value, tags)


def gauge(metric_name: str, value: float, tags: Optional[Dict[str, str]] = None):
    """Set a gauge metric"""
    _metrics.gauge(metric_name, value, tags)


def histogram(metric_name: str, value: float, tags: Optional[Dict[str, str]] = None):
    """Add a value to a histogram"""
    _metrics.histogram(metric_name, value, tags)


def timing(metric_name: str, duration_ms: float, tags: Optional[Dict[str, str]] = None):
    """Record a timing metric"""
    _metrics.timing(metric_name, duration_ms, tags)


def start_timer(timer_id: str):
    """Start a timer"""
    _metrics.start_timer(timer_id)


def stop_timer(timer_id: str, metric_name: str, tags: Optional[Dict[str, str]] = None) -> float:
    """Stop a timer and record the duration"""
    return _metrics.stop_timer(timer_id, metric_name, tags)


def get_metrics() -> Dict[str, Any]:
    """Get all collected metrics"""
    return _metrics.get_stats()


def reset_metrics():
    """Reset all metrics"""
    _metrics.reset()


class timer_context:
    """Context manager for timing code blocks"""
    
    def __init__(self, metric_name: str, tags: Optional[Dict[str, str]] = None):
        self.metric_name = metric_name
        self.tags = tags
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time:
            duration_ms = (time.time() - self.start_time) * 1000
            timing(self.metric_name, duration_ms, self.tags)


async def metrics_reporter(interval: int = 60):
    """
    Background task to periodically report metrics.
    
    Args:
        interval: Reporting interval in seconds
    """
    while True:
        try:
            await asyncio.sleep(interval)
            
            stats = get_metrics()
            logger.info(f"Metrics Report: {stats}")
            
            # Here you could send metrics to external monitoring systems:
            # - Prometheus push gateway
            # - StatsD/Datadog
            # - CloudWatch
            # - Custom monitoring endpoint
            
        except Exception as e:
            logger.error(f"Error in metrics reporter: {e}")


# Predefined metric names for consistency
class MetricNames:
    """Standard metric names used across the system"""
    
    # LLM API metrics
    LLM_REQUEST = "llm.request"
    LLM_SUCCESS = "llm.success"
    LLM_ERROR = "llm.error"
    LLM_TIMEOUT = "llm.timeout"
    LLM_RETRY = "llm.retry"
    LLM_CIRCUIT_BREAKER_OPEN = "llm.circuit_breaker.open"
    LLM_CIRCUIT_BREAKER_HALF_OPEN = "llm.circuit_breaker.half_open"
    LLM_CONTEXT_TRUNCATION = "llm.context.truncation"
    LLM_STREAMING = "llm.streaming"
    
    # Agent metrics
    AGENT_TASK_START = "agent.task.start"
    AGENT_TASK_COMPLETE = "agent.task.complete"
    AGENT_TASK_ERROR = "agent.task.error"
    AGENT_TASK_DURATION = "agent.task.duration"
    
    # Workflow metrics
    WORKFLOW_START = "workflow.start"
    WORKFLOW_COMPLETE = "workflow.complete"
    WORKFLOW_ERROR = "workflow.error"
    WORKFLOW_DURATION = "workflow.duration"
    
    # Resource metrics
    ACTIVE_AGENTS = "resource.active_agents"
    ACTIVE_TASKS = "resource.active_tasks"
    QUEUE_SIZE = "resource.queue_size"
    
    # File operations
    FILE_CREATED = "file.created"
    FILE_WRITE_ERROR = "file.write_error"
