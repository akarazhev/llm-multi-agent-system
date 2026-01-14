# Production-Ready Implementation Guide

## Overview

This guide documents the production-ready enhancements implemented in the LLM Multi-Agent System. These improvements ensure reliability, scalability, and observability for production deployments.

## Table of Contents

1. [System Prompts](#system-prompts)
2. [Streaming Responses](#streaming-responses)
3. [Error Handling & Resilience](#error-handling--resilience)
4. [Connection Pooling](#connection-pooling)
5. [Configuration Management](#configuration-management)
6. [Logging & Observability](#logging--observability)
7. [Metrics & Monitoring](#metrics--monitoring)
8. [Deployment Best Practices](#deployment-best-practices)

---

## System Prompts

### Overview

All agents now use professional, production-ready system prompts that follow industry best practices and provide comprehensive guidance to the LLM.

### Key Features

- **Structured Role Definitions**: Clear responsibility breakdown
- **Technical Expertise**: Detailed technology stack and tools
- **Best Practices**: Industry-standard patterns and principles
- **Quality Standards**: Specific requirements for output quality
- **Output Formatting**: Explicit formatting instructions

### Agent System Prompts

#### Business Analyst
- Requirements engineering using SMART and INVEST criteria
- User story creation with Gherkin-style acceptance criteria
- Risk and dependency mapping
- Stakeholder communication frameworks

#### Developer
- SOLID principles and design patterns
- Production-ready code with error handling and logging
- Security considerations (SQL injection, XSS, CSRF)
- Type hints and comprehensive documentation
- Performance and scalability focus

#### QA Engineer
- Comprehensive test coverage strategy (Unit 70-80%, Integration 15-20%, E2E 5-10%)
- AAA (Arrange-Act-Assert) pattern
- Test data management and fixtures
- Security and performance testing
- Quality metrics tracking

#### DevOps Engineer
- Infrastructure as Code (IaC) principles
- Container orchestration best practices
- CI/CD pipeline structure
- Security hardening and compliance
- Observability stack (Metrics, Logging, Tracing)

#### Technical Writer
- Documentation-as-Code approach
- Structured documentation types (Concept, Task, Reference, Troubleshooting)
- API documentation standards (OpenAPI/Swagger)
- Code examples in multiple languages
- Accessibility and inclusivity guidelines

### Usage

System prompts are automatically applied in the `execute_llm_task` method. They are sent as separate system messages to ensure proper context.

```python
# System prompt is retrieved from agent's get_system_prompt() method
system_prompt = self.get_system_prompt()

# Sent as system message
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt}
]
```

---

## Streaming Responses

### Overview

Streaming is now **enabled by default** for all LLM interactions, providing better user experience and responsiveness.

### Features

- **Real-time Feedback**: Tokens appear as they're generated
- **Early Termination**: Can stop generation if needed
- **Better UX**: Users see progress instead of waiting
- **Callback Support**: Custom stream callbacks for UI updates

### Implementation

```python
# Streaming is enabled by default
result = await agent.execute_llm_task(
    prompt="Implement a REST API",
    stream=True,  # Default
    stream_callback=lambda chunk: print(chunk, end='', flush=True)
)
```

### Configuration

```python
# In config.yaml
llm_stream_responses: true  # Enable streaming globally

# Or via environment variable
LLM_STREAM_RESPONSES=true
```

### Custom Stream Callbacks

```python
def my_stream_callback(chunk: str):
    """Process each token as it arrives"""
    # Update UI, log, or process in real-time
    ui.update(chunk)
    logger.debug(f"Received chunk: {chunk}")

result = await agent.execute_llm_task(
    prompt="...",
    stream_callback=my_stream_callback
)
```

---

## Error Handling & Resilience

### Overview

Production-grade error handling with retry logic, exponential backoff, and circuit breaker pattern.

### Features

#### 1. Exponential Backoff Retry

Automatically retries failed requests with increasing delays to handle transient failures.

```python
# Configuration
LLM_MAX_RETRIES=3
LLM_RETRY_INITIAL_DELAY=1.0  # seconds
LLM_RETRY_MAX_DELAY=60.0     # seconds
```

**Behavior**:
- Attempt 1: Immediate
- Attempt 2: Wait 1s (with jitter: 0.5-1.5s)
- Attempt 3: Wait 2s (with jitter: 1-3s)
- Attempt 4: Wait 4s (with jitter: 2-6s)
- Max delay: 60s

#### 2. Circuit Breaker

Prevents cascade failures by failing fast when service is unhealthy.

```python
# Configuration
LLM_CIRCUIT_BREAKER_THRESHOLD=5       # Failures to trigger
LLM_CIRCUIT_BREAKER_TIMEOUT=60.0      # Recovery timeout
LLM_CIRCUIT_BREAKER_HALF_OPEN=3       # Success needed to close
```

**States**:
- **CLOSED**: Normal operation, requests pass through
- **OPEN**: Too many failures, requests fail immediately
- **HALF_OPEN**: Testing recovery, limited requests pass through

#### 3. Context Size Handling

Automatic truncation and retry when context exceeds LLM limits.

```python
# Automatically detects context size errors and retries with truncated content
# - System prompt: 30% of available space
# - User prompt: 70% of available space
```

### Usage Examples

```python
from src.utils import retry, RetryError, CircuitBreakerError

# Manual retry
@retry(max_attempts=3, initial_delay=1.0)
async def my_api_call():
    return await external_api.fetch()

# Handle circuit breaker
try:
    result = await agent.execute_llm_task(prompt)
except CircuitBreakerError:
    # LLM service is temporarily unavailable
    # Fall back to cached response or graceful degradation
    pass
```

---

## Connection Pooling

### Overview

Reusable connection pool for LLM API clients to improve performance and resource efficiency.

### Features

- **Connection Reuse**: Maintains persistent connections
- **Health Monitoring**: Automatic health checks and cleanup
- **Graceful Degradation**: Handles unhealthy clients
- **Statistics Tracking**: Request counts, success rates, latency

### Implementation

The connection pool is automatically used by all agents. No manual configuration required.

```python
# Automatically managed
client = await get_llm_client(
    api_base="http://127.0.0.1:8080/v1",
    timeout=300.0
)

# Get pool statistics
stats = get_pool_stats()
print(f"Active clients: {stats['active_clients']}")
print(f"Success rate: {stats['success_rate']}")
```

### Pool Management

```python
# Manual pool management (if needed)
from src.utils import close_client_pool

# Cleanup on shutdown
await close_client_pool()
```

### Health Monitoring

The pool automatically:
- Tracks request success/failure rates
- Removes clients with > 5 recent failures
- Recreates clients older than 1 hour
- Runs periodic health checks every 5 minutes

---

## Configuration Management

### Overview

Enhanced configuration system with validation, type safety, and environment variable support.

### Configuration Sources (Priority Order)

1. **Environment Variables** (highest priority)
2. **config.yaml** (application configuration)
3. **Default Values** (fallback)

### Configuration Validation

All settings are validated on load:

```python
from src.config import load_config, ConfigValidationError

try:
    settings = load_config()
except ConfigValidationError as e:
    print(f"Configuration error: {e}")
    sys.exit(1)
```

### Available Settings

#### LLM Configuration

```yaml
llm_timeout: 300                      # API timeout (seconds)
llm_max_retries: 3                    # Retry attempts
llm_retry_initial_delay: 1.0          # Initial retry delay
llm_retry_max_delay: 60.0             # Maximum retry delay
llm_circuit_breaker_threshold: 5      # Failures before opening
llm_circuit_breaker_timeout: 60.0     # Recovery timeout
llm_stream_responses: true            # Enable streaming
```

#### Logging Configuration

```yaml
log_level: "INFO"                     # DEBUG, INFO, WARNING, ERROR, CRITICAL
log_file: "logs/agent_system.log"    # Log file path
enable_structured_logging: true       # JSON-formatted logs
```

#### Orchestration Configuration

```yaml
max_concurrent_agents: 5              # Concurrent agent limit
task_retry_attempts: 3                # Task-level retries
task_timeout: 600                     # Task timeout (seconds)
```

### Environment Variables

See `.env.example` for complete list of environment variables.

---

## Logging & Observability

### Overview

Production-ready structured logging with correlation IDs, JSON formatting, and context injection.

### Structured Logging

```python
from src.utils import setup_logging

# Production mode (JSON logs)
setup_logging(
    level="INFO",
    log_file="logs/app.log",
    json_format=True,
    colored_console=False
)

# Development mode (colored console)
setup_logging(
    level="DEBUG",
    json_format=False,
    colored_console=True
)
```

### JSON Log Format

```json
{
  "timestamp": "2026-01-14T10:30:00.123Z",
  "level": "INFO",
  "logger": "src.agents.developer",
  "message": "Task completed successfully",
  "correlation_id": "abc123",
  "agent_id": "dev_001",
  "task_id": "task_456",
  "workflow_id": "wf_789",
  "duration_ms": 1234.56
}
```

### Correlation IDs

Track requests across multiple agents and services:

```python
from src.utils import set_correlation_id, get_correlation_id

# Set correlation ID for current context
correlation_id = set_correlation_id("request-123")

# All logs will include this correlation ID
logger.info("Processing request")  # Includes correlation_id: "request-123"

# Retrieve correlation ID
current_id = get_correlation_id()
```

### Context Logger

Automatically inject context (agent_id, task_id) into logs:

```python
from src.utils import ContextLogger

# Create logger with default context
logger = ContextLogger(__name__, agent_id="dev_001", task_id="task_123")

# All logs include agent_id and task_id
logger.info("Starting task")  # Includes agent_id and task_id
logger.error("Task failed", error_code="E001")  # Additional context
```

### Log Aggregation

JSON logs can be easily ingested by log aggregation systems:
- **ELK Stack** (Elasticsearch, Logstash, Kibana)
- **Loki** (Grafana Loki)
- **CloudWatch Logs**
- **Datadog**
- **Splunk**

---

## Metrics & Monitoring

### Overview

Lightweight metrics collection for monitoring system health and performance.

### Available Metrics

#### LLM API Metrics

```python
from src.utils.metrics import MetricNames, increment, timing

# Count requests
increment(MetricNames.LLM_REQUEST, tags={"agent": "developer"})
increment(MetricNames.LLM_SUCCESS)
increment(MetricNames.LLM_ERROR)

# Record latency
timing(MetricNames.LLM_REQUEST, duration_ms=1234.5)
```

#### Agent Metrics

```python
# Task metrics
increment(MetricNames.AGENT_TASK_START)
increment(MetricNames.AGENT_TASK_COMPLETE)
timing(MetricNames.AGENT_TASK_DURATION, duration_ms=5000)
```

#### Workflow Metrics

```python
# Workflow metrics
increment(MetricNames.WORKFLOW_START)
increment(MetricNames.WORKFLOW_COMPLETE)
timing(MetricNames.WORKFLOW_DURATION, duration_ms=30000)
```

### Timer Context Manager

```python
from src.utils.metrics import timer_context

# Automatically time code blocks
with timer_context("llm.generation", tags={"model": "devstral"}):
    result = await llm_call()
# Duration automatically recorded
```

### Getting Metrics

```python
from src.utils.metrics import get_metrics

stats = get_metrics()
print(f"LLM requests: {stats['counters']['llm.request']}")
print(f"Average latency: {stats['histograms']['llm.request.duration_ms']['avg']}")
print(f"P95 latency: {stats['histograms']['llm.request.duration_ms']['p95']}")
```

### Integration with Monitoring Systems

```python
# Prometheus
from prometheus_client import Counter, Histogram

# Datadog
from datadog import statsd

# Custom metrics reporter
async def report_metrics():
    while True:
        stats = get_metrics()
        # Send to your monitoring system
        await monitoring_service.send(stats)
        await asyncio.sleep(60)
```

---

## Deployment Best Practices

### 1. Environment Configuration

```bash
# Production .env
OPENAI_API_BASE=http://localhost:8080/v1
LOG_LEVEL=INFO
STRUCTURED_LOGGING=true
ENABLE_METRICS=true
LLM_STREAM_RESPONSES=true
LLM_MAX_RETRIES=3
LLM_CIRCUIT_BREAKER_THRESHOLD=5
```

### 2. Resource Limits

```yaml
# config.yaml
max_concurrent_agents: 5     # Adjust based on CPU cores
task_timeout: 600           # Prevent runaway tasks
llm_timeout: 300            # Prevent hanging requests
```

### 3. Monitoring Setup

```bash
# Start with metrics collection enabled
ENABLE_METRICS=true python main.py
```

### 4. Health Checks

```python
# Implement health check endpoint
from src.utils import get_pool_stats, get_metrics

@app.get("/health")
async def health_check():
    pool_stats = get_pool_stats()
    metrics = get_metrics()
    
    return {
        "status": "healthy" if pool_stats['success_rate'] > 0.9 else "degraded",
        "active_clients": pool_stats['active_clients'],
        "success_rate": pool_stats['success_rate'],
        "request_count": metrics['counters'].get('llm.request', 0)
    }
```

### 5. Graceful Shutdown

```python
import signal
import asyncio

async def shutdown():
    logger.info("Shutting down gracefully...")
    
    # Close connection pool
    await close_client_pool()
    
    # Save metrics
    stats = get_metrics()
    with open('metrics_final.json', 'w') as f:
        json.dump(stats, f)
    
    logger.info("Shutdown complete")

# Register signal handlers
signal.signal(signal.SIGTERM, lambda s, f: asyncio.create_task(shutdown()))
signal.signal(signal.SIGINT, lambda s, f: asyncio.create_task(shutdown()))
```

### 6. Error Monitoring

```bash
# Optional: Sentry integration
SENTRY_DSN=https://your-sentry-dsn
```

```python
import sentry_sdk

sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    traces_sample_rate=0.1,
    environment="production"
)
```

### 7. Log Rotation

```yaml
# Use logrotate or similar
/var/log/agent-system/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
}
```

### 8. Performance Tuning

```bash
# Tune based on your LLM server performance
LLM_TIMEOUT=300
LLM_MAX_RETRIES=3
LLM_CIRCUIT_BREAKER_THRESHOLD=5

# Adjust for your workload
MAX_CONCURRENT_AGENTS=5
TASK_TIMEOUT=600
```

---

## Troubleshooting

### Circuit Breaker Frequently Opening

**Symptoms**: `CircuitBreakerError: Circuit breaker is OPEN`

**Solutions**:
1. Check LLM server health and performance
2. Increase `LLM_CIRCUIT_BREAKER_THRESHOLD`
3. Increase `LLM_TIMEOUT` if requests are timing out
4. Monitor metrics to identify root cause

### Context Size Errors

**Symptoms**: Prompts being truncated frequently

**Solutions**:
1. Increase LLM server `--ctx-size` parameter
2. Reduce `per_file_limit` in agent code
3. Be more selective about which files to include in context
4. Use summarization for large files

### High Latency

**Symptoms**: Slow response times

**Solutions**:
1. Enable streaming for better perceived performance
2. Increase LLM server threads: `--threads -1`
3. Use GPU acceleration: `-ngl 99`
4. Optimize batch size: `--batch-size 512`
5. Monitor connection pool health

### Memory Issues

**Symptoms**: High memory usage or OOM errors

**Solutions**:
1. Reduce `max_concurrent_agents`
2. Implement request queuing
3. Monitor histogram sizes in metrics
4. Enable context truncation

---

## Conclusion

This production-ready implementation provides:

✅ **Reliability**: Retry logic, circuit breakers, error handling  
✅ **Performance**: Connection pooling, streaming, resource management  
✅ **Observability**: Structured logging, metrics, correlation IDs  
✅ **Scalability**: Concurrent agents, connection reuse, efficient resource usage  
✅ **Maintainability**: Configuration validation, comprehensive documentation  

The system is now ready for production deployment with enterprise-grade reliability and monitoring capabilities.
