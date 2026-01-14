# LLM Server Configuration Analysis

## Your Current Configuration

```bash
llama-server \
  -hf unsloth/Devstral-Small-2-24B-Instruct-2512-GGUF:UD-Q4_K_XL \
  -ngl 99 \
  --threads -1 \
  --ctx-size 16384 \
  --batch-size 512 \
  --parallel 4 \
  --host 127.0.0.1 \
  --port 8080 \
  --jinja \
  --temp 0.15 \
  --min-p 0.01 \
  --prio 3 \
  --alias unsloth/Devstral-Small-2-24B-Instruct-2512
```

---

## Configuration Analysis

### ✅ **EXCELLENT Settings**

| Parameter | Value | Assessment | Notes |
|-----------|-------|------------|-------|
| `--ctx-size` | **16384** | ✅ **GOOD** | Perfect for documentation tasks |
| `--batch-size` | **512** | ✅ **OPTIMAL** | Good balance for throughput |
| `--parallel` | **4** | ✅ **GOOD** | Allows concurrent requests |
| `--temp` | **0.15** | ✅ **EXCELLENT** | Low temperature = consistent, focused output |
| `--min-p` | **0.01** | ✅ **GOOD** | Reduces randomness |
| `--jinja` | **enabled** | ✅ **REQUIRED** | Enables proper prompt templating |
| `-ngl` | **99** | ✅ **OPTIMAL** | GPU offloading (all layers) |
| `--threads` | **-1** | ✅ **AUTO** | Uses all available CPU cores |

### 📊 **Context Window Analysis**

Your `--ctx-size 16384` means:
- **Total tokens available**: 16,384 tokens (~12,000 words)
- **Input + Output must fit**: `prompt_tokens + max_tokens ≤ 16384`

**Current Problem**:
- Your `.env` has `OPENAI_MAX_TOKENS=2048` ❌ **TOO LOW**
- For comprehensive docs: Should be `8192` ✅

**Token Distribution**:
```
Total Context: 16384 tokens
├─ Input Prompt: ~8192 tokens (50%)
└─ Output Generation: ~8192 tokens (50%)
```

---

## ⚠️ **ISSUE IDENTIFIED**

### The Mismatch

| Setting | Current | Should Be | Impact |
|---------|---------|-----------|--------|
| llama-server `--ctx-size` | 16384 | ✅ Good | Supports large responses |
| `.env` `OPENAI_MAX_TOKENS` | **2048** | ❌ **Too Low** | **Truncates responses!** |

### Why This Causes Truncation

1. **llama-server** can handle up to 16,384 tokens
2. But your **application** limits output to only 2,048 tokens
3. When Business Analyst needs 5,000+ tokens for comprehensive docs:
   - LLM generates content
   - Hits 2,048 token limit
   - **Stops mid-sentence** ❌
   - File is incomplete

---

## ✅ **RECOMMENDED CONFIGURATION**

### Option 1: Conservative (Recommended)

**For your `--ctx-size 16384` setup**:

```bash
# .env file
OPENAI_MAX_TOKENS=8192
```

**Why 8192?**
- Leaves 8K tokens for input prompt (system + user prompt)
- Allows 8K tokens for output (plenty for documentation)
- 50/50 split is safe and balanced

**Token Budget**:
```
Input:  8,192 tokens (system prompt + user prompt)
Output: 8,192 tokens (LLM response)
Total:  16,384 tokens ✅ Fits perfectly
```

### Option 2: Aggressive (For Very Large Documents)

```bash
# .env file
OPENAI_MAX_TOKENS=12288
```

**Why 12288?**
- Leaves 4K tokens for input
- Allows 12K tokens for output
- Good for very comprehensive documentation
- **Risk**: May fail if prompts are too long

**Token Budget**:
```
Input:  4,096 tokens (system prompt + user prompt)
Output: 12,288 tokens (LLM response)
Total:  16,384 tokens ✅ Fits perfectly
```

### Option 3: Maximum (Not Recommended)

```bash
# .env file
OPENAI_MAX_TOKENS=14336
```

**Why NOT recommended?**
- Only 2K tokens left for prompt
- System prompts are ~500-1000 tokens
- User prompts can be 1000-3000 tokens
- **High risk** of exceeding context window

---

## 🎯 **RECOMMENDED ACTION**

### 1. Update Your `.env` File

```bash
# Replace this line in your .env:
OPENAI_MAX_TOKENS=2048  # ❌ TOO LOW

# With this:
OPENAI_MAX_TOKENS=8192  # ✅ OPTIMAL
```

### 2. Per-Agent Token Limits (Optional - Advanced)

For even better control, set different limits per agent:

```bash
# .env file

# Default for all agents
OPENAI_MAX_TOKENS=8192

# Business Analyst - needs high tokens for detailed analysis
BUSINESSANALYST_MAX_TOKENS=10240

# Technical Writer - needs highest for comprehensive docs
TECHNICALWRITER_MAX_TOKENS=12288

# Developer - moderate for code generation
DEVELOPER_MAX_TOKENS=6144

# QA Engineer - moderate for test cases
QAENGINEER_MAX_TOKENS=6144

# DevOps Engineer - moderate for configs
DEVOPSENGINEER_MAX_TOKENS=6144
```

**Note**: This requires a code change in `base_agent.py` to read per-agent env vars.

---

## 📈 **CONTEXT WINDOW UPGRADE OPTIONS**

If you need even more capacity:

### Option A: Double Context Window

```bash
llama-server --ctx-size 32768 ...
```

Then in `.env`:
```bash
OPENAI_MAX_TOKENS=16384  # Double capacity
```

### Option B: Quadruple Context Window

```bash
llama-server --ctx-size 65536 ...
```

Then in `.env`:
```bash
OPENAI_MAX_TOKENS=32768  # Massive capacity
```

**Considerations**:
- ⚠️ **Memory**: Larger context = more VRAM/RAM needed
- ⚠️ **Speed**: Larger context = slower processing
- ⚠️ **GPU**: Check your GPU VRAM capacity
- ✅ **Best for**: Very complex, multi-file documentation

---

## 🔍 **VERIFICATION**

### After Updating `OPENAI_MAX_TOKENS=8192`

1. **Test with Business Analyst**:
   ```bash
   cd /Users/andrey.karazhev/Developer/spg/llm-multi-agent-system
   source venv/bin/activate
   python examples/simple_workflow.py
   ```

2. **Check Generated Files**:
   ```bash
   # Files should be complete, not truncated
   ls -lh output/*/business_analyst/*.md
   ```

3. **Monitor Logs** for token usage:
   ```bash
   tail -f logs/agent_system.log | grep -i "tokens\|truncat"
   ```

4. **Look for Warnings**:
   ```
   WARNING: Response may be truncated - used 8000/8192 tokens
   ```

---

## 🎯 **YOUR SPECIFIC CASE**

### Current Setup
- ✅ llama-server: `--ctx-size 16384` (GOOD)
- ❌ Application: `OPENAI_MAX_TOKENS=2048` (TOO LOW)

### What's Happening
1. Business Analyst generates comprehensive documentation
2. Needs ~5,000-8,000 tokens for complete response
3. Application limits output to 2,048 tokens
4. **Response is truncated** mid-sentence
5. File parser receives incomplete content
6. Result: `jira_structure.md` is cut off

### Solution
```bash
# Update .env:
OPENAI_MAX_TOKENS=8192
```

### Expected Result
✅ Full responses up to 8,192 tokens  
✅ Complete documentation files  
✅ No truncation  
✅ All sections present  

---

## 📊 **TOKEN USAGE BY AGENT**

Based on typical tasks:

| Agent | Typical Output | Recommended `max_tokens` |
|-------|----------------|-------------------------|
| Business Analyst | 4,000-8,000 tokens | **8192-10240** |
| Technical Writer | 5,000-12,000 tokens | **10240-12288** |
| Developer | 2,000-6,000 tokens | **6144-8192** |
| QA Engineer | 2,000-5,000 tokens | **6144** |
| DevOps Engineer | 1,500-4,000 tokens | **4096-6144** |

---

## ✅ **SUMMARY**

### Your llama-server Configuration: ✅ **EXCELLENT**
- Context window of 16,384 is perfect
- Temperature of 0.15 is ideal for code/docs
- Parallel requests (4) good for multi-agent system
- All settings are production-ready

### Your Application Configuration: ❌ **NEEDS FIX**
- `OPENAI_MAX_TOKENS=2048` is too low
- Should be **8192** minimum
- This is causing all your truncation issues

### **IMMEDIATE ACTION REQUIRED**:

```bash
# In your .env file:
OPENAI_MAX_TOKENS=8192
```

This single change will fix all truncation issues! 🎉

---

## 📚 **Related Documentation**

- `docs/LLM_TOKEN_LIMITS.md` - Detailed token configuration guide
- `docs/PARSER_VERIFICATION_FINAL.md` - Parser verification report
- `.env.example` - Updated with 8192 default
- `PRODUCTION_READY_CHECKLIST.md` - Production deployment guide

---

**Configuration Status**: ⚠️ **Needs Minor Adjustment**  
**Fix Required**: Update `OPENAI_MAX_TOKENS` from 2048 → 8192  
**Impact**: 🔴 **High** - Fixes all truncation issues  
**Effort**: 🟢 **Low** - Single line change in `.env`  
**Risk**: 🟢 **None** - Purely a configuration improvement
