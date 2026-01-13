# Context Size Error Handling

This document explains how the system handles context size errors when the prompt exceeds the llama-server's configured context window.

## Problem

When sending requests to llama-server, you may encounter errors like:

```
Error code: 400 - {
  'error': {
    'code': 400, 
    'message': 'request (4476 tokens) exceeds the available context size (4096 tokens)',
    'type': 'exceed_context_size_error',
    'n_prompt_tokens': 4476,
    'n_ctx': 4096
  }
}
```

This occurs when:
- The combined system prompt + user prompt + requested completion tokens exceed the server's context window
- The server is configured with a small context size (e.g., `LLAMA_CTX_SIZE=4096`)
- The prompts include large amounts of context (files, requirements, etc.)

## Solution

The system now automatically handles context size errors with **intelligent retry and truncation**:

### 1. **Automatic Detection**

When a context size error occurs, the system:
- Parses the error message to extract the actual context limit
- Identifies this as a recoverable error
- Logs the issue with details about prompt and context sizes

### 2. **Smart Truncation**

The system uses an intelligent truncation strategy:

```python
# Token budget allocation:
available_tokens = server_context_size - completion_tokens (1024)

# Split available tokens:
system_prompt: 30% of available tokens
user_prompt:   70% of available tokens
```

This ensures:
- ✅ System prompts (agent role/instructions) are preserved as much as possible
- ✅ User prompts (task details) get more space since they're more specific
- ✅ Enough tokens reserved for meaningful completions (1024 tokens)

### 3. **Automatic Retry**

After truncation:
1. Prompts are truncated with clear markers: `[System prompt truncated to fit context...]`
2. The request is automatically retried with truncated prompts
3. Detailed logging shows what was truncated and by how much

### 4. **File Content Limits**

File contents included in prompts are now limited more conservatively:
- **Single file**: 1500 characters max
- **Multiple files**: 1000 characters max per file
- Truncation is indicated: `[truncated N chars]`

## Configuration

### Option 1: Increase Server Context Size (Recommended)

Restart llama-server with a larger context window:

```bash
# Stop current server
./scripts/stop_llama_server.sh

# Start with larger context size
export LLAMA_CTX_SIZE=16384  # or 8192, 32768, etc.
./scripts/start_llama_server.sh
```

**Trade-offs:**
- ✅ No truncation needed, full context preserved
- ✅ Better quality responses with more context
- ❌ Higher memory usage
- ❌ Slightly slower inference

### Option 2: Keep Small Context (Works Automatically)

Keep the server at 4096 tokens:
- ✅ Lower memory usage
- ✅ Faster inference
- ✅ Automatic truncation handles errors
- ⚠️ Some context may be lost in truncation

## Usage Examples

### Example 1: Automatic Handling

```python
# This will automatically truncate if needed
result = await agent.execute_llm_task(
    prompt="Very long prompt with lots of context...",
    files=["large_file1.py", "large_file2.py"]
)

if result["success"]:
    # The request succeeded (possibly after truncation)
    output = result["stdout"]
```

**Log output when truncation occurs:**

```
WARNING - User prompt truncated from 15000 to 8400 chars
INFO - Prompt truncation: 20000 -> 12000 chars (est 3000 tokens)
INFO - Retrying with truncated prompts...
INFO - Calling local llama-server with model: devstral (attempt 2)
```

### Example 2: Testing the Fix

Run the included test script:

```bash
python test_context_fix.py
```

This creates an intentionally large prompt to verify:
1. Context error is detected
2. Prompt is truncated
3. Request is retried successfully
4. Response is received

Expected output:

```
Context Size Error Handling Test
================================================================================

API Base: http://127.0.0.1:8080/v1
Prompt size: 18500 characters (~4625 tokens)
Expected behavior: Should trigger context error, then auto-truncate and retry

Calling LLM server...
--------------------------------------------------------------------------------
WARNING - User prompt truncated from 18500 to 8400 chars
INFO - Retrying with truncated prompts...
--------------------------------------------------------------------------------

✅ SUCCESS: Request completed!
Response length: 1234 characters
```

## Technical Details

### Token Estimation

The system uses a rough approximation for token counting:

```python
estimated_tokens = character_count // 4
```

This is approximate but works well for most cases. Actual tokenization may vary by:
- Language (English vs code vs other languages)
- Vocabulary (common words vs technical terms)
- Formatting (spaces, newlines, special characters)

### Truncation Algorithm

```python
def _truncate_prompt_to_fit(system_prompt, user_prompt, max_context_tokens):
    # Reserve tokens for completion
    available_tokens = max_context_tokens - 1024
    available_chars = available_tokens * 4
    
    # Allocate budget
    system_budget = int(available_chars * 0.3)
    user_budget = available_chars - system_budget
    
    # Truncate each if needed
    if len(system_prompt) > system_budget:
        system_prompt = system_prompt[:system_budget] + "\n[truncated...]"
    
    if len(user_prompt) > user_budget:
        user_prompt = user_prompt[:user_budget] + "\n[truncated...]"
    
    return system_prompt, user_prompt
```

### Error Detection

The system detects context errors by:
1. Catching exceptions from the OpenAI client
2. Checking for keywords: `exceed_context_size`, `exceeds the available context size`
3. Parsing error messages to extract: `n_ctx` (context limit), `n_prompt_tokens` (actual size)

### Retry Logic

```python
# First attempt with original prompts
try:
    response = await client.chat.completions.create(...)
except ContextSizeError:
    # Truncate and retry once
    if retry_count == 0:
        truncated_prompts = truncate_prompt_to_fit(...)
        return await call_llm_server(..., retry_count=1)
    else:
        # Don't retry infinitely
        raise
```

## Best Practices

### 1. Right-size Your Context Window

**For most tasks:**
```bash
export LLAMA_CTX_SIZE=8192
```

**For complex tasks with lots of files:**
```bash
export LLAMA_CTX_SIZE=16384
```

**For simple Q&A or small tasks:**
```bash
export LLAMA_CTX_SIZE=4096  # Automatic truncation will handle overflow
```

### 2. Monitor Logs

Watch for truncation warnings:

```bash
tail -f logs/agent_system.log | grep -i truncat
```

If you see frequent truncation, consider increasing context size.

### 3. Limit File Context

When including files in prompts:
- Only include relevant files
- Pre-filter file contents to essential parts
- Use file summaries instead of full contents when possible

### 4. Optimize Prompts

- Keep system prompts concise and focused
- Avoid repeating information in user prompts
- Use structured formats (JSON, YAML) for complex data
- Summarize large contexts before including them

## Troubleshooting

### Still Getting Context Errors After Truncation

If you see:
```
Context size error persisted after truncation
```

This means even after truncation, the prompt is too large. Solutions:
1. Increase `LLAMA_CTX_SIZE` significantly
2. Reduce the complexity of your prompts
3. Split the task into smaller subtasks
4. Remove file contexts from the request

### Truncation Losing Important Context

If truncation removes critical information:
1. Increase `LLAMA_CTX_SIZE` to avoid truncation
2. Restructure prompts to put critical info first
3. Reduce less important context (files, examples, etc.)
4. Break complex tasks into multiple simpler tasks

### Performance Issues

If context handling is slow:
1. The first attempt with full prompt will fail (adds latency)
2. Truncation and retry add overhead
3. **Solution:** Pre-emptively check and truncate before first attempt

## Future Enhancements

Potential improvements:
1. **Pre-emptive truncation**: Check size before first attempt
2. **Smart context selection**: Use embeddings to select most relevant context
3. **Adaptive allocation**: Adjust system/user split based on content
4. **Token counting**: Use actual tokenizer instead of estimation
5. **Context compression**: Summarize large contexts automatically

## Related Documentation

- [Troubleshooting Guide](TROUBLESHOOTING.md) - General error handling
- [Quick Start](QUICK_START.md) - Server configuration
- [Local Only Mode](LOCAL_ONLY_MODE.md) - Understanding the architecture
