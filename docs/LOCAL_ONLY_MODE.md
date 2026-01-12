# Local-Only Mode

This multi-agent system is configured to run **100% locally** using llama.cpp. No cloud APIs are used.

## Why Local-Only?

✅ **Zero Cost** - No API fees  
✅ **Complete Privacy** - Data never leaves your machine  
✅ **No Internet Required** - Works offline  
✅ **Full Control** - Choose any model you want  
✅ **No Rate Limits** - Use as much as you need  

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Multi-Agent System                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │ Business │  │Developer │  │    QA    │  ...        │
│  │ Analyst  │  │          │  │ Engineer │             │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘             │
│       │             │              │                    │
│       └─────────────┴──────────────┘                    │
│                     │                                   │
│              ┌──────▼──────┐                           │
│              │ base_agent  │                           │
│              │  .py        │                           │
│              └──────┬──────┘                           │
└─────────────────────┼──────────────────────────────────┘
                      │
                      │ OpenAI-compatible API
                      │ (http://127.0.0.1:8080/v1)
                      │
           ┌──────────▼──────────┐
           │   llama-server      │
           │   (llama.cpp)       │
           └──────────┬──────────┘
                      │
           ┌──────────▼──────────┐
           │  Devstral-Small-2   │
           │  24B-Instruct       │
           │  (Local GGUF Model) │
           └─────────────────────┘
```

## How It Works

### 1. Local llama-server

The system uses **llama.cpp's server** which provides an OpenAI-compatible API:

```bash
llama-server \
  -hf unsloth/Devstral-Small-2-24B-Instruct-2512-GGUF:UD-Q4_K_XL \
  -ngl 99 \
  --ctx-size 16384 \
  --host 127.0.0.1 \
  --port 8080
```

This creates a local API endpoint at `http://127.0.0.1:8080/v1`

### 2. Agent Communication

Each agent in `base_agent.py`:

```python
# Check for local server (REQUIRED)
api_base = os.getenv('OPENAI_API_BASE')
if not api_base:
    raise Error("Local llama-server required!")

# Use OpenAI client to talk to local server
client = AsyncOpenAI(
    base_url=api_base,  # http://127.0.0.1:8080/v1
    api_key="not-needed"
)

response = await client.chat.completions.create(
    model="devstral",
    messages=[...]
)
```

### 3. No Cloud Fallback

**Important:** The system has **NO fallback** to cloud APIs. If `OPENAI_API_BASE` is not set, the system will fail with a clear error message telling you to start the local server.

This is intentional to ensure:
- No accidental cloud API usage
- No surprise costs
- Complete data privacy

## Setup

### 1. Install llama.cpp

```bash
# macOS
brew install llama.cpp

# Or from source
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
make
```

### 2. Configure Environment

Your `.env` file must have:

```bash
OPENAI_API_BASE=http://127.0.0.1:8080/v1
OPENAI_API_KEY=not-needed
OPENAI_API_MODEL=devstral
```

### 3. Start llama-server

```bash
./scripts/start_llama_server.sh
```

Wait for "Server started" message.

### 4. Run Agents

```bash
source venv/bin/activate
python simple_test.py
```

## Validation

The system validates local server on every agent task:

```python
if not os.getenv('OPENAI_API_BASE'):
    return {
        "success": False,
        "error": "OPENAI_API_BASE not configured. Local llama-server required."
    }
```

## Error Messages

### "OPENAI_API_BASE not configured"

**Cause:** `.env` file missing or `OPENAI_API_BASE` not set

**Fix:**
```bash
# Add to .env
echo "OPENAI_API_BASE=http://127.0.0.1:8080/v1" >> .env
echo "OPENAI_API_KEY=not-needed" >> .env
echo "OPENAI_API_MODEL=devstral" >> .env
```

### "Connection refused"

**Cause:** llama-server not running

**Fix:**
```bash
./scripts/start_llama_server.sh
```

### "Model not found"

**Cause:** Wrong model name in `OPENAI_API_MODEL`

**Fix:**
```bash
# Check available models
curl http://127.0.0.1:8080/v1/models

# Update .env with correct model name
```

## Dependencies

### Required

- **llama.cpp** - Local LLM server
- **openai** - Python client (used for local API)
- **python-dotenv** - Environment configuration

### NOT Required

- ~~cursor-agent-tools~~ - Removed (was for cloud APIs)
- ~~anthropic~~ - Not used
- ~~ollama~~ - Not used (llama.cpp is used instead)

## Model Selection

You can use any GGUF model with llama-server:

```bash
# Set before starting server
export LLAMA_MODEL="unsloth/Qwen2.5-Coder-32B-Instruct-GGUF"
./scripts/start_llama_server.sh
```

Popular models:
- **Devstral-Small-2-24B** (default) - Fast, good for coding
- **Qwen2.5-Coder-32B** - Excellent code generation
- **DeepSeek-Coder-33B** - Strong coding capabilities
- **CodeLlama-34B** - Meta's code model

## Performance

### Hardware Requirements

**Minimum:**
- 16GB RAM
- 8-core CPU
- 50GB disk space

**Recommended:**
- 32GB+ RAM
- Apple Silicon M1/M2/M3 or NVIDIA GPU
- 100GB+ disk space

### Optimization

**For Apple Silicon:**
```bash
export LLAMA_GPU_LAYERS=99  # Use all GPU
export LLAMA_CTX_SIZE=16384
```

**For CPU-only:**
```bash
export LLAMA_GPU_LAYERS=0
export LLAMA_THREADS=8
export LLAMA_CTX_SIZE=4096  # Smaller context
```

## Security

### Data Privacy

✅ All data stays on your machine  
✅ No external API calls  
✅ No telemetry or tracking  
✅ Complete control over data  

### Network

The llama-server binds to `127.0.0.1` (localhost only):
- Not accessible from network
- Only local processes can connect
- No firewall configuration needed

## Monitoring

### Check Server Status

```bash
./scripts/check_llama_server.sh
```

### View Logs

```bash
# Server logs
tail -f logs/llama-server.log

# Agent logs
tail -f logs/agent_system.log
```

### Resource Usage

```bash
# GPU (Metal)
sudo powermetrics --samplers gpu_power

# CPU/Memory
htop
```

## Troubleshooting

### Slow Performance

1. **Increase GPU layers:**
   ```bash
   export LLAMA_GPU_LAYERS=99
   ```

2. **Use smaller model:**
   ```bash
   export LLAMA_MODEL="unsloth/Llama-3.2-3B-Instruct-GGUF"
   ```

3. **Reduce context:**
   ```bash
   export LLAMA_CTX_SIZE=4096
   ```

### Out of Memory

1. **Use smaller quantization:**
   ```bash
   export LLAMA_MODEL="model-name:Q4_K_M"  # Instead of Q8
   ```

2. **Reduce context:**
   ```bash
   export LLAMA_CTX_SIZE=4096
   ```

3. **Offload fewer layers:**
   ```bash
   export LLAMA_GPU_LAYERS=32
   ```

## Comparison: Local vs Cloud

| Feature | Local (llama.cpp) | Cloud (OpenAI/Anthropic) |
|---------|-------------------|--------------------------|
| **Cost** | Free | $0.002-0.06 per task |
| **Privacy** | 100% private | Data sent to third party |
| **Speed** | Fast (with GPU) | Fast (network dependent) |
| **Internet** | Not required | Required |
| **Setup** | Initial setup needed | Instant |
| **Models** | Any GGUF model | Provider's models only |
| **Control** | Full control | Limited control |
| **Limits** | Hardware only | Rate limits apply |

## Best Practices

1. **Always start server first**
   ```bash
   ./scripts/start_llama_server.sh
   # Wait for "Server started"
   python simple_test.py
   ```

2. **Monitor resources**
   - Watch GPU/CPU usage
   - Check memory consumption
   - Monitor disk space

3. **Choose appropriate model**
   - Development: 3B-7B (fast)
   - Production: 13B-34B (quality)
   - Specific tasks: Fine-tuned models

4. **Keep llama.cpp updated**
   ```bash
   brew upgrade llama.cpp
   ```

5. **Regular backups**
   - Backup your models
   - Save configuration
   - Keep logs for debugging

## Summary

Your multi-agent system is **100% local**:

✅ No cloud API dependencies  
✅ No API keys needed (except dummy "not-needed")  
✅ No external network calls  
✅ Complete data privacy  
✅ Zero ongoing costs  

The system will **refuse to run** without a local llama-server, ensuring you never accidentally use cloud APIs.

## Resources

- [llama.cpp GitHub](https://github.com/ggerganov/llama.cpp)
- [GGUF Models Hub](https://huggingface.co/models?library=gguf)
- [llama.cpp Server Docs](https://github.com/ggerganov/llama.cpp/blob/master/examples/server/README.md)
- [Project Setup Guide](./LLAMA_CPP_SETUP.md)
