# llama.cpp Integration Guide

This project is fully integrated with **llama.cpp** for running local LLM models. This guide covers everything you need to know.

## Quick Start

### 1. Install llama.cpp

**macOS (Homebrew):**
```bash
brew install llama.cpp
```

**From Source:**
```bash
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
make
# Add to PATH or use full path
```

### 2. Start llama-server

```bash
# From project root
./scripts/start_llama_server.sh
```

This starts the server with your Devstral model on `http://127.0.0.1:8080`

### 3. Run the Multi-Agent System

```bash
source venv/bin/activate
python simple_test.py
```

## Configuration

### Environment Variables

The `.env` file is already configured for llama.cpp:

```bash
# Local llama-server configuration
OPENAI_API_BASE=http://127.0.0.1:8080/v1
OPENAI_API_KEY=not-needed
OPENAI_API_MODEL=devstral
```

### Server Configuration

Customize the llama-server via environment variables:

```bash
# Model selection
export LLAMA_MODEL="unsloth/Devstral-Small-2-24B-Instruct-2512-GGUF:UD-Q4_K_XL"

# Network settings
export LLAMA_HOST="127.0.0.1"
export LLAMA_PORT="8080"

# Performance settings
export LLAMA_CTX_SIZE="16384"      # Context window size
export LLAMA_GPU_LAYERS="99"       # GPU layers (-1 for all)
export LLAMA_THREADS="-1"          # CPU threads (-1 for auto)

# Then start
./scripts/start_llama_server.sh
```

## Available Scripts

### 🚀 Start Server
```bash
./scripts/start_llama_server.sh
```
**Enhanced features:**
- Automatic port conflict detection and resolution
- System resource validation (CPU, memory, disk)
- Configuration verification
- Real-time startup monitoring with health checks
- Graceful handling of existing processes
- Detailed logging and progress indicators

### 🏥 Comprehensive Health Check
```bash
./scripts/check_llama_server.sh

# With verbose diagnostics
./scripts/check_llama_server.sh --verbose
```
**6-stage health verification:**
1. Process status and resource usage
2. Network port availability
3. HTTP connectivity
4. API health endpoint
5. Model availability
6. Inference endpoint testing

### 📊 Continuous Monitoring
```bash
# Basic monitoring
./scripts/monitor_llama_server.sh

# With auto-restart on failure
./scripts/monitor_llama_server.sh --auto-restart

# Custom check interval
./scripts/monitor_llama_server.sh --interval 15
```
**Production-grade monitoring:**
- Real-time performance metrics
- Automatic restart on failure
- Configurable health checks
- Resource usage tracking
- Alert logging

### ⚙️ Configuration Management
```bash
# Interactive configuration wizard
./scripts/configure_llama_server.sh

# View current settings
./scripts/configure_llama_server.sh --show

# Export configuration
./scripts/configure_llama_server.sh --export
```
**Pre-configured presets:**
- Development (fast, 6GB RAM)
- Balanced (default, 18GB RAM)
- Production (high quality, 24GB RAM)
- Maximum Performance (40GB RAM)
- CPU Only (no GPU)

### 🎯 Performance Benchmarking
```bash
# Full benchmark suite
./scripts/benchmark_llama_server.sh

# Specific tests
./scripts/benchmark_llama_server.sh --latency
./scripts/benchmark_llama_server.sh --throughput
./scripts/benchmark_llama_server.sh --concurrent
./scripts/benchmark_llama_server.sh --stress
```
**Comprehensive testing:**
- Latency measurements
- Throughput (tokens/second)
- Concurrent request handling
- Stress testing under load

### 🔄 Restart Server
```bash
./scripts/restart_llama_server.sh
```
Safely restarts with health verification

### ✋ Stop Server
```bash
./scripts/stop_llama_server.sh
```
**Graceful shutdown:**
- SIGTERM before SIGKILL
- Port cleanup verification
- Process status display

### 📋 Quick Status Check
```bash
./scripts/check_server_status.sh
```
Fast check for scripts/automation (exit codes: 0=healthy, 1=down, 2=unhealthy)

### 📖 Documentation
See [`scripts/README.md`](../scripts/README.md) for complete documentation and [`scripts/QUICK_REFERENCE.md`](../scripts/QUICK_REFERENCE.md) for quick command reference.

## Model Selection

### Current Model
**Devstral-Small-2-24B-Instruct** (Q4_K_XL quantization)
- Size: ~14GB
- Context: 16K tokens
- Speed: Fast on Apple Silicon
- Quality: Excellent for coding tasks

### Alternative Models

Change model by setting `LLAMA_MODEL`:

```bash
# Smaller, faster model
export LLAMA_MODEL="unsloth/Llama-3.2-3B-Instruct-GGUF"

# Larger, more capable model
export LLAMA_MODEL="unsloth/Qwen2.5-Coder-32B-Instruct-GGUF"

# Start with new model
./scripts/start_llama_server.sh
```

Popular coding models:
- `Qwen2.5-Coder-*` - Excellent for code generation
- `DeepSeek-Coder-*` - Strong coding capabilities
- `CodeLlama-*` - Meta's code-focused model
- `Llama-3.*` - General purpose, good at code

## Performance Tuning

### GPU Acceleration

**Metal (Apple Silicon):**
```bash
export LLAMA_GPU_LAYERS=99  # Use all GPU layers
```

**CUDA (NVIDIA):**
```bash
export LLAMA_GPU_LAYERS=99
# Ensure CUDA-enabled llama.cpp build
```

**CPU Only:**
```bash
export LLAMA_GPU_LAYERS=0
export LLAMA_THREADS=8  # Adjust based on CPU cores
```

### Context Size

Larger context = more memory but better for complex tasks:

```bash
# Small (fast, less memory)
export LLAMA_CTX_SIZE=4096

# Medium (balanced)
export LLAMA_CTX_SIZE=8192

# Large (slow, more memory)
export LLAMA_CTX_SIZE=32768
```

### Thread Configuration

```bash
# Auto-detect (recommended)
export LLAMA_THREADS=-1

# Manual (use physical cores)
export LLAMA_THREADS=8
```

## Integration with Multi-Agent System

### How It Works

1. **llama-server** runs as OpenAI-compatible API
2. **base_agent.py** detects `OPENAI_API_BASE` environment variable
3. Uses **OpenAI Python client** to communicate with llama-server
4. All agents use the same local model

### Code Flow

```python
# In base_agent.py
api_base = os.getenv('OPENAI_API_BASE')
if api_base:
    # Use local llama-server
    client = AsyncOpenAI(
        base_url=api_base,
        api_key="not-needed"
    )
    response = await client.chat.completions.create(...)
```

### Agent Behavior

Each agent:
- Uses specialized system prompt
- Sends tasks to llama-server
- Receives AI-generated responses
- Processes results asynchronously

## Testing

### Quick Test
```bash
source venv/bin/activate
python simple_test.py
```

### Full Workflow Test
```bash
source venv/bin/activate
python examples/simple_workflow.py
```

### Manual API Test
```bash
curl http://127.0.0.1:8080/v1/models

curl http://127.0.0.1:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "devstral",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

## Troubleshooting

### Server Won't Start

**Issue:** `llama-server: command not found`
```bash
# Install llama.cpp
brew install llama.cpp
```

**Issue:** Port already in use
```bash
# Kill existing process
lsof -ti:8080 | xargs kill -9

# Or use different port
export LLAMA_PORT=8081
./scripts/start_llama_server.sh
```

**Issue:** Model not found
```bash
# llama-server will auto-download from HuggingFace
# Ensure you have internet connection
# Or specify local model path:
export LLAMA_MODEL="/path/to/model.gguf"
```

### Agent Errors

**Issue:** "No API keys configured"
```bash
# Ensure .env has OPENAI_API_BASE
cat .env | grep OPENAI_API_BASE

# Should show:
# OPENAI_API_BASE=http://127.0.0.1:8080/v1
```

**Issue:** Connection refused
```bash
# Check server is running
./scripts/check_llama_server.sh

# Check logs
tail -f logs/llama-server.log
```

**Issue:** Slow responses
```bash
# Increase GPU layers
export LLAMA_GPU_LAYERS=99

# Reduce context size
export LLAMA_CTX_SIZE=8192

# Use smaller model
export LLAMA_MODEL="unsloth/Llama-3.2-3B-Instruct-GGUF"
```

### Memory Issues

**Issue:** Out of memory
```bash
# Use smaller quantization
export LLAMA_MODEL="model-name:Q4_K_M"  # Instead of Q8

# Reduce context
export LLAMA_CTX_SIZE=4096

# Reduce GPU layers
export LLAMA_GPU_LAYERS=32
```

## Advanced Configuration

### Custom Model Path

```bash
# Use local GGUF file
export LLAMA_MODEL="/Users/you/models/custom-model.gguf"
./scripts/start_llama_server.sh
```

### Multiple Instances

Run multiple llama-servers on different ports:

```bash
# Terminal 1 - Coding model
export LLAMA_PORT=8080
export LLAMA_MODEL="Qwen2.5-Coder-32B"
./scripts/start_llama_server.sh

# Terminal 2 - General model
export LLAMA_PORT=8081
export LLAMA_MODEL="Llama-3.2-70B"
./scripts/start_llama_server.sh

# Use in .env
OPENAI_API_BASE=http://127.0.0.1:8080/v1  # Coding tasks
```

### Production Deployment

For production use:

```bash
# Run as background service
nohup ./scripts/start_llama_server.sh > /dev/null 2>&1 &

# Or use systemd/launchd
# Create service file for your OS
```

## Comparison: llama.cpp vs Cloud APIs

### llama.cpp (Local)
✅ **Free** - No API costs  
✅ **Private** - Data stays local  
✅ **Fast** - No network latency (with good hardware)  
✅ **Offline** - Works without internet  
❌ **Hardware** - Requires powerful machine  
❌ **Setup** - Initial configuration needed  

### Cloud APIs (OpenAI/Anthropic)
✅ **Easy** - No setup required  
✅ **Scalable** - Handle any load  
✅ **Latest models** - Access to newest models  
❌ **Cost** - Pay per token  
❌ **Privacy** - Data sent to third party  
❌ **Internet** - Requires connection  

## Best Practices

1. **Start server before running agents**
   ```bash
   ./scripts/start_llama_server.sh
   # Wait for "Server started" message
   python simple_test.py
   ```

2. **Monitor resource usage**
   ```bash
   # Watch GPU usage (Metal)
   sudo powermetrics --samplers gpu_power

   # Watch CPU/Memory
   htop
   ```

3. **Use appropriate model size**
   - Development: 3B-7B models (fast)
   - Production: 13B-34B models (quality)
   - Specific tasks: Fine-tuned models

4. **Optimize for your hardware**
   - Apple Silicon: Use Metal, high GPU layers
   - NVIDIA GPU: Use CUDA build
   - CPU only: Use smaller models, more threads

5. **Keep llama.cpp updated**
   ```bash
   brew upgrade llama.cpp
   ```

## Resources

- [llama.cpp GitHub](https://github.com/ggerganov/llama.cpp)
- [Model Hub](https://huggingface.co/models?library=gguf)
- [Quantization Guide](https://github.com/ggerganov/llama.cpp/blob/master/examples/quantize/README.md)
- [Performance Tips](https://github.com/ggerganov/llama.cpp/discussions)

## Summary

Your multi-agent system is **fully configured** for llama.cpp:

✅ Scripts ready (`start_llama_server.sh`)  
✅ Configuration set (`.env`)  
✅ Integration complete (`base_agent.py`)  
✅ Tests working (`simple_test.py`)  

Just start the server and run your agents! 🚀
