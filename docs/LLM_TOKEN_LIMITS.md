# LLM Token Limits Configuration

## Problem

The default `max_tokens=2048` configuration is too low for comprehensive documentation and analysis tasks. This causes LLM responses to be truncated mid-generation, resulting in incomplete files.

## Symptoms

- Documentation files cut off mid-sentence
- JSON blocks incomplete
- Markdown files missing sections
- Agent responses show "Task Completed: True" but files are truncated

## Root Cause

The `OPENAI_MAX_TOKENS` environment variable limits the maximum number of tokens the LLM can generate in a single response. For complex documentation tasks (Business Analyst, Technical Writer), 2048 tokens (~1500 words) is insufficient.

## Solution

### 1. Increase Global Max Tokens

Edit your `.env` file:

```bash
# For comprehensive documentation (recommended)
OPENAI_MAX_TOKENS=8192

# For very large documents
OPENAI_MAX_TOKENS=16384
```

### 2. Per-Agent Token Limits (Recommended)

Different agents have different needs:

```bash
# Business Analyst - needs high token count for detailed analysis
BA_MAX_TOKENS=8192

# Developer - moderate token count for code generation
DEV_MAX_TOKENS=4096

# QA Engineer - moderate for test cases
QA_MAX_TOKENS=4096

# DevOps Engineer - moderate for configs
DEVOPS_MAX_TOKENS=4096

# Technical Writer - highest for comprehensive docs
TW_MAX_TOKENS=16384
```

### 3. Context Window Considerations

Your llama-server is configured with:
- `--ctx-size 16384` (context window)
- This includes BOTH input prompt AND output tokens

**Formula**: `max_tokens + prompt_tokens ≤ ctx_size`

**Recommendations**:
- For `ctx_size=16384`: Use `max_tokens=8192` (leaves 8K for prompt)
- For `ctx_size=32768`: Use `max_tokens=16384` (leaves 16K for prompt)
- For `ctx_size=65536`: Use `max_tokens=32768` (leaves 32K for prompt)

## Implementation

### Option A: Quick Fix (Global)

```bash
# In your .env file
OPENAI_MAX_TOKENS=8192
```

### Option B: Per-Agent Configuration (Better)

Modify `src/agents/base_agent.py` to support per-agent token limits:

```python
# In _call_local_llama_server method
agent_type = self.__class__.__name__.lower()
max_tokens_key = f"{agent_type.upper()}_MAX_TOKENS"
max_tokens = int(os.getenv(max_tokens_key, os.getenv('OPENAI_MAX_TOKENS', '8192')))
```

Then in `.env`:

```bash
# Default for all agents
OPENAI_MAX_TOKENS=4096

# Override for specific agents
BUSINESSANALYST_MAX_TOKENS=8192
TECHNICALWRITER_MAX_TOKENS=16384
```

## Verification

After increasing `max_tokens`, test with a complex task:

```python
from src.agents.business_analyst import BusinessAnalyst

agent = BusinessAnalyst("test_ba")
result = await agent.process_task(
    "Create comprehensive API documentation with multiple sections",
    task_id="test_001"
)

# Check that all sections are complete
assert "## Conclusion" in result['result']  # Last section should be present
```

## Monitoring

Add logging to track token usage:

```python
logger.info(f"Generated {response.usage.completion_tokens} tokens (max: {max_tokens})")

if response.usage.completion_tokens >= max_tokens * 0.95:
    logger.warning(f"Response may be truncated - used {response.usage.completion_tokens}/{max_tokens} tokens")
```

## Best Practices

1. **Set appropriate limits per agent type**:
   - Code generation: 4096-8192 tokens
   - Documentation: 8192-16384 tokens
   - Simple responses: 2048-4096 tokens

2. **Monitor token usage** in logs to identify truncation

3. **Increase context window** if you need larger outputs:
   ```bash
   llama-server --ctx-size 32768 ...
   ```

4. **Use streaming** to detect truncation early

5. **Implement chunking** for very large documents (split into multiple files)

## Current Configuration

Your llama-server:
```bash
--ctx-size 16384
--batch-size 512
```

**Recommended `.env` settings**:
```bash
OPENAI_MAX_TOKENS=8192  # Leaves 8K for prompt
OPENAI_TEMPERATURE=0.15  # Your current setting
```

## Related Files

- `.env.example` - Environment variable template
- `src/agents/base_agent.py` - LLM call implementation (line 252)
- `config.yaml` - Global configuration
- `docs/PRODUCTION_READY_GUIDE.md` - Production configuration guide
