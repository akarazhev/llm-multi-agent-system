# Migration Guide: Production-Ready Enhancements

## Overview

This guide helps you migrate to the production-ready version of the LLM Multi-Agent System. Most changes are backward compatible, but there are new features and configuration options you should be aware of.

## Breaking Changes

### None

All changes are backward compatible. Existing code will continue to work with default values.

## New Features & Enhancements

### 1. Streaming Enabled by Default

**What Changed**: Streaming is now enabled by default for better UX.

**Action Required**: None (automatic)

**If you want to disable streaming**:
```python
# In your code
result = await agent.execute_llm_task(prompt, stream=False)

# Or in config.yaml
llm_stream_responses: false

# Or via environment
LLM_STREAM_RESPONSES=false
```

### 2. Enhanced Configuration

**What Changed**: New configuration options for resilience and monitoring.

**Action Required**: Copy `.env.example` to `.env` and review new settings.

```bash
cp .env.example .env
# Edit .env with your values
```

**New Settings in config.yaml**:
```yaml
# Add these to your config.yaml
llm_max_retries: 3
llm_retry_initial_delay: 1.0
llm_retry_max_delay: 60.0
llm_circuit_breaker_threshold: 5
llm_circuit_breaker_timeout: 60.0
llm_stream_responses: true
enable_structured_logging: true
enable_metrics: true
```

### 3. Improved System Prompts

**What Changed**: All agents have enhanced, production-ready system prompts.

**Action Required**: None (automatic)

**Benefits**:
- More detailed and specific guidance for LLMs
- Better quality outputs
- Consistent formatting
- Industry best practices built-in

### 4. Structured Logging

**What Changed**: JSON-formatted structured logging available.

**Action Required**: Optional - enable if you use log aggregation.

```python
from src.utils import setup_logging

# Production setup (JSON logs)
setup_logging(
    level="INFO",
    log_file="logs/app.log",
    json_format=True,
    colored_console=False
)
```

### 5. Metrics Collection

**What Changed**: Built-in metrics collection for monitoring.

**Action Required**: Optional - metrics are collected automatically if enabled.

```yaml
# In config.yaml
enable_metrics: true
```

**Access metrics**:
```python
from src.utils.metrics import get_metrics

stats = get_metrics()
print(stats)
```

### 6. Connection Pooling

**What Changed**: Automatic connection pool for LLM clients.

**Action Required**: None (automatic)

**Benefits**:
- Better performance through connection reuse
- Automatic health monitoring
- Resource efficiency

### 7. Retry Logic & Circuit Breaker

**What Changed**: Automatic retry with exponential backoff and circuit breaker.

**Action Required**: None (automatic)

**Configure if needed**:
```bash
# In .env
LLM_MAX_RETRIES=3
LLM_CIRCUIT_BREAKER_THRESHOLD=5
LLM_CIRCUIT_BREAKER_TIMEOUT=60.0
```

## Step-by-Step Migration

### Step 1: Update Dependencies

No new dependencies required. All enhancements use existing packages.

```bash
# Verify all dependencies are installed
pip install -r requirements.txt
```

### Step 2: Update Configuration

```bash
# Copy new .env.example
cp .env.example .env

# Edit .env with your settings
nano .env
```

### Step 3: Update config.yaml

Add new settings to your `config.yaml`:

```yaml
# Add these lines
llm_max_retries: 3
llm_retry_initial_delay: 1.0
llm_retry_max_delay: 60.0
llm_circuit_breaker_threshold: 5
llm_circuit_breaker_timeout: 60.0
llm_stream_responses: true
enable_structured_logging: true
enable_metrics: true
```

### Step 4: Test Your Application

```bash
# Run tests to ensure everything works
pytest tests/

# Try a simple workflow
python examples/simple_workflow.py
```

### Step 5: Enable Monitoring (Optional)

```python
# In your application initialization
from src.utils import setup_logging, metrics

# Setup structured logging
setup_logging(
    level="INFO",
    log_file="logs/app.log",
    json_format=True  # For production
)

# Metrics are automatically collected
# Access them with:
stats = metrics.get_metrics()
```

### Step 6: Update Error Handling (Optional)

If you have custom error handling, you can now handle circuit breaker errors:

```python
from src.utils import CircuitBreakerError

try:
    result = await agent.execute_llm_task(prompt)
except CircuitBreakerError:
    # LLM service is temporarily unavailable
    logger.warning("Circuit breaker open, using fallback")
    result = fallback_response()
```

## Verification

### Test Streaming

```python
def stream_callback(chunk):
    print(chunk, end='', flush=True)

result = await agent.execute_llm_task(
    "Write a hello world program",
    stream_callback=stream_callback
)
```

### Test Retry Logic

```python
# Temporarily stop your LLM server to test retries
# You should see automatic retry attempts in logs

# Check metrics
from src.utils.metrics import get_metrics
stats = get_metrics()
print(f"Retries: {stats['counters'].get('llm.retry', 0)}")
```

### Test Circuit Breaker

```python
# After several failures, circuit breaker should open
# You'll see logs about circuit breaker state changes

from src.utils import get_pool_stats
stats = get_pool_stats()
print(f"Success rate: {stats['success_rate']}")
```

### Test Structured Logging

```python
from src.utils import set_correlation_id
import logging

logger = logging.getLogger(__name__)

# Set correlation ID
correlation_id = set_correlation_id("test-123")

# This log will include correlation_id
logger.info("Testing structured logging")
```

## Common Issues

### Issue: Streaming not working

**Solution**: Ensure your LLM server supports streaming:

```bash
# Check your llama-server supports streaming
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "devstral", "messages": [{"role": "user", "content": "test"}], "stream": true}'
```

### Issue: Circuit breaker opening frequently

**Solution**: Adjust thresholds or check LLM server health:

```bash
# In .env
LLM_CIRCUIT_BREAKER_THRESHOLD=10  # Increase threshold
LLM_TIMEOUT=600                    # Increase timeout
```

### Issue: Logs not in JSON format

**Solution**: Enable structured logging:

```python
from src.utils import setup_logging
setup_logging(json_format=True)
```

### Issue: Metrics not being collected

**Solution**: Enable metrics in config:

```yaml
# config.yaml
enable_metrics: true
```

## Rollback Plan

If you need to rollback:

### Option 1: Disable New Features

```yaml
# config.yaml - use old behavior
llm_stream_responses: false
enable_structured_logging: false
enable_metrics: false
llm_max_retries: 0  # Disable retries
```

### Option 2: Git Rollback

```bash
# Find the commit before migration
git log --oneline

# Rollback to previous version
git checkout <previous-commit-hash>
```

## Support

If you encounter issues during migration:

1. Check the [Production-Ready Guide](PRODUCTION_READY_GUIDE.md)
2. Review the [Troubleshooting](TROUBLESHOOTING.md) section
3. Check logs for detailed error messages
4. Open an issue on GitHub with:
   - Configuration files
   - Error messages
   - LLM server setup details

## Next Steps

After successful migration:

1. **Monitor Metrics**: Set up dashboards for key metrics
2. **Tune Configuration**: Adjust retry/timeout values based on your workload
3. **Enable Alerts**: Set up alerts for circuit breaker events
4. **Review Logs**: Use JSON logs with your log aggregation system
5. **Performance Testing**: Load test to verify improvements

## Summary of Benefits

✅ **Better UX**: Streaming responses show progress  
✅ **More Reliable**: Automatic retries and circuit breaker  
✅ **Better Performance**: Connection pooling and reuse  
✅ **Observable**: Structured logs and metrics  
✅ **Production-Ready**: Enterprise-grade error handling  
✅ **Scalable**: Efficient resource management  

Welcome to the production-ready version! 🚀
