# LLM Scripts Quick Reference

## 🚀 Essential Commands

```bash
# Start server
./scripts/start_llama_server.sh

# Check health
./scripts/check_llama_server.sh

# Stop server
./scripts/stop_llama_server.sh

# Restart server
./scripts/restart_llama_server.sh
```

## 📊 Monitoring

```bash
# Continuous monitoring
./scripts/monitor_llama_server.sh

# With auto-restart
./scripts/monitor_llama_server.sh --auto-restart

# Quick status (for scripts)
./scripts/check_server_status.sh
```

## ⚙️ Configuration

```bash
# Interactive wizard
./scripts/configure_llama_server.sh

# Show current config
./scripts/configure_llama_server.sh --show

# Export config
./scripts/configure_llama_server.sh --export
```

## 🎯 Performance Testing

```bash
# Full benchmark suite
./scripts/benchmark_llama_server.sh

# Specific tests
./scripts/benchmark_llama_server.sh --latency
./scripts/benchmark_llama_server.sh --throughput
./scripts/benchmark_llama_server.sh --concurrent
./scripts/benchmark_llama_server.sh --stress
```

## 🔧 Environment Variables

```bash
# Model & Network
export LLAMA_MODEL="unsloth/Devstral-Small-2-24B-Instruct-2512-GGUF:UD-Q4_K_XL"
export LLAMA_HOST="127.0.0.1"
export LLAMA_PORT="8080"

# Performance
export LLAMA_CTX_SIZE="16384"      # Context window
export LLAMA_GPU_LAYERS="99"       # GPU layers
export LLAMA_THREADS="-1"          # CPU threads
export LLAMA_BATCH_SIZE="512"      # Batch size
export LLAMA_PARALLEL="4"          # Concurrent requests

# Logging
export LLAMA_LOG_LEVEL="info"      # debug|info|warning|error
```

## 📋 Common Workflows

### Start & Verify
```bash
./scripts/start_llama_server.sh && ./scripts/check_llama_server.sh
```

### Restart & Monitor
```bash
./scripts/restart_llama_server.sh && ./scripts/monitor_llama_server.sh
```

### Configure & Start
```bash
./scripts/configure_llama_server.sh
./scripts/start_llama_server.sh
```

### Test Performance
```bash
./scripts/start_llama_server.sh
./scripts/benchmark_llama_server.sh
```

## 🆘 Troubleshooting

```bash
# View logs
tail -f logs/llama-server.log

# Detailed diagnostics
./scripts/check_llama_server.sh --verbose

# Force stop if stuck
pkill -9 llama-server

# Check what's using the port
lsof -i :8080

# View server resource usage
ps aux | grep llama-server
```

## 🎚️ Configuration Presets

| Preset | Model | RAM | Use Case |
|--------|-------|-----|----------|
| Dev | Llama-3.2-3B | 6GB | Fast development |
| Balanced | Devstral-24B | 18GB | Recommended default |
| Production | Qwen2.5-32B | 24GB | High quality |
| Max Performance | Qwen2.5-32B-Q8 | 40GB | Best quality |
| CPU Only | Llama-3.2-3B | 6GB | No GPU needed |

## 📈 Monitoring Modes

```bash
# Basic (30s checks)
./scripts/monitor_llama_server.sh

# Fast checks (10s)
./scripts/monitor_llama_server.sh --interval 10

# Production (auto-restart enabled)
./scripts/monitor_llama_server.sh --auto-restart --interval 60
```

## 🔒 Exit Codes

### check_server_status.sh
- `0` - Server healthy
- `1` - Server not running
- `2` - Server running but unhealthy

### Other scripts
- `0` - Success
- `1` - Error

## 📦 Log Files

```bash
logs/
├── llama-server.log       # Server output
├── llama-server.pid       # Process ID
├── monitor.log            # Monitor activity
└── benchmark/             # Benchmark results
```

## 🔗 Quick Links

- [Full Documentation](README.md)
- [Main Project README](../README.md)
- [llama.cpp Setup Guide](../docs/LLAMA_CPP_SETUP.md)
- [Troubleshooting Guide](../docs/TROUBLESHOOTING.md)

## 💡 Tips

1. **Always check health** before running agents:
   ```bash
   ./scripts/check_server_status.sh && python main.py
   ```

2. **Use monitoring in production**:
   ```bash
   nohup ./scripts/monitor_llama_server.sh --auto-restart &
   ```

3. **Benchmark after config changes**:
   ```bash
   ./scripts/benchmark_llama_server.sh --latency
   ```

4. **Save your configuration**:
   ```bash
   ./scripts/configure_llama_server.sh
   source .llama/server.conf
   ```

5. **Check logs on errors**:
   ```bash
   tail -100 logs/llama-server.log
   ```

---

**Need Help?** Run any script with `--help`:
```bash
./scripts/check_llama_server.sh --help
```
