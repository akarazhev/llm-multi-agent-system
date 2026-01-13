# LLM Management Scripts

Comprehensive management toolkit for llama.cpp server operations.

## Overview

This directory contains professional-grade scripts for managing the llama.cpp local LLM server used by the multi-agent system. All scripts feature enhanced error handling, verbose logging, and production-ready reliability.

## Quick Start

```bash
# 1. Configure the server (interactive wizard)
./scripts/configure_llama_server.sh

# 2. Start the server
./scripts/start_llama_server.sh

# 3. Check server health
./scripts/check_llama_server.sh

# 4. Monitor continuously
./scripts/monitor_llama_server.sh --auto-restart
```

## Scripts Reference

### 🚀 Start Server

**`start_llama_server.sh`**

Starts the llama-server with comprehensive validation and monitoring.

**Features:**
- Automatic port conflict detection and resolution
- System resource checking (CPU, memory, disk)
- Configuration validation
- Model auto-download from HuggingFace
- Graceful handling of existing processes
- Real-time startup monitoring
- Health check verification

**Usage:**
```bash
# Default (Q8_0 quantization - higher quality)
./scripts/start_llama_server.sh

# Use smaller/faster model (UD-Q4_K_XL)
MODEL_QUANTIZATION=UD-Q4_K_XL ./scripts/start_llama_server.sh

# With custom configuration
LLAMA_PORT=8081 LLAMA_CTX_SIZE=8192 ./scripts/start_llama_server.sh

# Use full model path directly
LLAMA_MODEL="unsloth/Devstral-Small-2-24B-Instruct-2512-GGUF:Q8_0" ./scripts/start_llama_server.sh
```

**Configuration:**
```bash
# Model selection - choose quantization level
# Option 1: Use MODEL_QUANTIZATION (recommended)
export MODEL_QUANTIZATION="Q8_0"        # Higher quality, ~24GB (default)
# or
export MODEL_QUANTIZATION="UD-Q4_K_XL"  # Smaller, faster, ~12GB

# Option 2: Set full model path directly
export LLAMA_MODEL="unsloth/Devstral-Small-2-24B-Instruct-2512-GGUF:Q8_0"
# or
export LLAMA_MODEL="unsloth/Devstral-Small-2-24B-Instruct-2512-GGUF:UD-Q4_K_XL"

# Other configuration options
export LLAMA_HOST="127.0.0.1"
export LLAMA_PORT="8080"
export LLAMA_CTX_SIZE="16384"
export LLAMA_GPU_LAYERS="99"
export LLAMA_THREADS="-1"
export LLAMA_BATCH_SIZE="512"
export LLAMA_PARALLEL="4"
export LLAMA_LOG_LEVEL="info"
```

**Model Quantization Options:**
- **Q8_0** (default): Higher quality, larger size (~24GB), better accuracy. Recommended for production use.
- **UD-Q4_K_XL**: Smaller size (~12GB), faster inference, slightly lower quality. Good for development or systems with limited memory.

**Output:**
- Real-time progress indicators
- Configuration summary
- Health check results
- Connection details
- Log file location

---

### ✋ Stop Server

**`stop_llama_server.sh`**

Gracefully stops the llama-server with proper cleanup.

**Features:**
- Graceful shutdown with SIGTERM
- Force kill option if graceful fails
- Port cleanup verification
- Process status display
- PID file management
- Zombie process detection

**Usage:**
```bash
./scripts/stop_llama_server.sh
```

**Exit Codes:**
- 0: Successfully stopped
- 1: Error during stop

---

### 🔄 Restart Server

**`restart_llama_server.sh`**

Safely restarts the server with health verification.

**Features:**
- Safe stop-then-start sequence
- Health check waiting
- Automatic verification
- Error recovery

**Usage:**
```bash
./scripts/restart_llama_server.sh
```

---

### 🏥 Health Check

**`check_llama_server.sh`**

Comprehensive health monitoring and diagnostics.

**Features:**
- Process status verification
- Network port checking
- HTTP connectivity testing
- API health endpoint validation
- Model availability checking
- Inference endpoint testing
- System resource reporting
- Log file analysis

**Usage:**
```bash
# Standard check
./scripts/check_llama_server.sh

# Verbose output with detailed diagnostics
./scripts/check_llama_server.sh --verbose

# Show help
./scripts/check_llama_server.sh --help
```

**Output:**
```
[1/6] Checking server process...
  ✓ Server process is running
    PID: 12345
    Runtime: 02:15:30
    Memory: 14256MB
    CPU: 45.2%

[2/6] Checking network port...
  ✓ Port 8080 is listening

[3/6] Checking HTTP connectivity...
  ✓ HTTP connection successful
    Response time: 0.025s

[4/6] Checking API health...
  ✓ Health endpoint responding

[5/6] Checking available models...
  ✓ Models endpoint responding
    Available models: 1

[6/6] Testing inference endpoint...
  ✓ Inference endpoint working
    Response time: 2s

✓ Server Status: HEALTHY 🟢
```

---

### 📊 Simple Status Check

**`check_server_status.sh`**

Fast, scriptable status check for automation and CI/CD.

**Features:**
- Quick process check
- Port verification
- Health endpoint validation
- Silent mode for scripting
- Clear exit codes

**Usage:**
```bash
# Normal mode
./scripts/check_server_status.sh

# Quiet mode (for scripts)
QUIET=true ./scripts/check_server_status.sh
if [ $? -eq 0 ]; then
    echo "Server is healthy"
fi
```

**Exit Codes:**
- 0: Server is healthy
- 1: Server is not running
- 2: Server running but not healthy

---

### 📈 Monitor Server

**`monitor_llama_server.sh`**

Continuous monitoring with auto-restart capabilities.

**Features:**
- Real-time status updates
- Automatic health checks
- Performance metrics
- Auto-restart on failure
- Consecutive failure tracking
- Restart cooldown management
- Configurable check intervals
- Resource usage monitoring

**Usage:**
```bash
# Basic monitoring (30s interval)
./scripts/monitor_llama_server.sh

# With auto-restart enabled
./scripts/monitor_llama_server.sh --auto-restart

# Custom check interval (10 seconds)
./scripts/monitor_llama_server.sh --interval 10

# Combined options
./scripts/monitor_llama_server.sh --auto-restart --interval 15
```

**Environment Variables:**
```bash
export MONITOR_INTERVAL=30              # Check interval in seconds
export MONITOR_AUTO_RESTART=true        # Enable auto-restart
export MONITOR_MAX_RESTARTS=3           # Max restart attempts
export MONITOR_RESTART_COOLDOWN=60      # Seconds between restarts
```

**Output:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Status Check at 2026-01-13 14:30:00
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ Server Status: HEALTHY

Server Metrics:
  PID:     12345
  Runtime: 02:15:30
  Memory:  14256MB
  CPU:     45.2%

Performance:
  Latency: 234ms

Monitor Statistics:
  Uptime:       00:45:12
  Restarts:     0/3
  Failures:     0/3

Next check in 30s...
```

---

### ⚙️ Configure Server

**`configure_llama_server.sh`**

Interactive configuration wizard with presets.

**Features:**
- Interactive configuration wizard
- Pre-configured optimization presets
- .env file management
- Configuration validation
- Export to shell scripts
- Hardware recommendations

**Usage:**
```bash
# Interactive wizard
./scripts/configure_llama_server.sh

# Show current configuration
./scripts/configure_llama_server.sh --show

# Export as environment variables
./scripts/configure_llama_server.sh --export
```

**Presets:**

1. **Development** - Fast, low memory
   - Model: Llama-3.2-3B
   - Context: 4096
   - Memory: ~6GB

2. **Balanced** - Default, recommended
   - Model: Devstral-Small-2-24B
   - Context: 16384
   - Memory: ~18GB

3. **Production** - High quality
   - Model: Qwen2.5-Coder-32B
   - Context: 16384
   - Memory: ~24GB

4. **Maximum Performance** - Best quality
   - Model: Qwen2.5-Coder-32B (Q8)
   - Context: 32768
   - Memory: ~40GB

5. **CPU Only** - No GPU required
   - Model: Llama-3.2-3B
   - Context: 4096
   - GPU Layers: 0

**Output Files:**
- `.llama/server.conf` - Shell configuration
- `.env` - Environment configuration

---

### 🎯 Benchmark Server

**`benchmark_llama_server.sh`**

Comprehensive performance testing suite.

**Features:**
- Latency testing with various prompts
- Throughput measurement (tokens/sec)
- Concurrent request handling
- Stress testing under load
- Performance metrics collection
- JSON results export

**Usage:**
```bash
# Run all tests
./scripts/benchmark_llama_server.sh

# Run specific tests
./scripts/benchmark_llama_server.sh --latency
./scripts/benchmark_llama_server.sh --throughput
./scripts/benchmark_llama_server.sh --concurrent
./scripts/benchmark_llama_server.sh --stress
```

**Test Types:**

1. **Latency Test**
   - Measures response time
   - Tests different prompt sizes
   - Min/avg/max calculations
   - Multiple iterations for accuracy

2. **Throughput Test**
   - Tokens per second
   - Different response lengths
   - Time per token
   - Efficiency metrics

3. **Concurrent Test**
   - Multiple simultaneous requests
   - 1, 2, 4, 8 concurrent clients
   - Total time and per-request average
   - Requests per second

4. **Stress Test**
   - 30-second continuous load
   - Success/error tracking
   - Average latency under load
   - Failure rate analysis

**Output:**
```
=== Latency Test ===
Prompt                                             Min (ms)        Avg (ms)        Max (ms)
────────────────────────────────────────────────────────────────────────────────
Hello                                              150             175             220
Write a Python function...                        280             310             350

=== Throughput Test ===
Max Tokens      Avg Latency     Tokens/sec      Time/Token
────────────────────────────────────────────────────────────────────────────────
10              200ms           50.00           20ms
50              850ms           58.82           17ms

=== Concurrent Requests Test ===
Concurrent      Total Time      Avg/Request     Requests/sec
────────────────────────────────────────────────────────────────────────────────
1               300ms           300ms           3.33
4               450ms           112ms           8.89
```

**Results:**
- Saved to `logs/benchmark/results_TIMESTAMP.json`
- Contains detailed metrics
- Can be used for comparison

---

## Environment Setup Scripts

### `setup_env.sh` (Unix/Linux/macOS)

Sets up Python environment with dependencies.

```bash
./scripts/setup_env.sh
```

### `setup_env.bat` (Windows)

Sets up Python environment on Windows.

```bash
setup_env.bat
```

---

## Configuration Files

### Generated Configurations

Scripts create and maintain:

- `logs/llama-server.log` - Server output log
- `logs/llama-server.pid` - Process ID file
- `logs/monitor.log` - Monitor activity log
- `logs/benchmark/` - Benchmark results
- `.llama/server.conf` - Server configuration
- `.env` - Environment variables

### Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `LLAMA_MODEL` | `unsloth/Devstral-Small-2-24B...` | HuggingFace model or local path |
| `LLAMA_HOST` | `127.0.0.1` | Server bind address |
| `LLAMA_PORT` | `8080` | Server port |
| `LLAMA_CTX_SIZE` | `16384` | Context window size (tokens) |
| `LLAMA_GPU_LAYERS` | `99` | GPU layers (-1 or 99 = all) |
| `LLAMA_THREADS` | `-1` | CPU threads (-1 = auto) |
| `LLAMA_BATCH_SIZE` | `512` | Batch processing size |
| `LLAMA_PARALLEL` | `4` | Parallel request slots |
| `LLAMA_LOG_LEVEL` | `info` | Logging level |

---

## Usage Examples

### Basic Workflow

```bash
# 1. Start server
./scripts/start_llama_server.sh

# 2. Verify health
./scripts/check_llama_server.sh

# 3. Run your agents
python main.py

# 4. Stop server when done
./scripts/stop_llama_server.sh
```

### Development Workflow

```bash
# Start with monitoring
./scripts/start_llama_server.sh
./scripts/monitor_llama_server.sh &

# Make changes, restart as needed
./scripts/restart_llama_server.sh

# Check performance
./scripts/benchmark_llama_server.sh
```

### Production Deployment

```bash
# Configure for production
./scripts/configure_llama_server.sh
# Select preset 3 (Production)

# Start with monitoring and auto-restart
./scripts/start_llama_server.sh
./scripts/monitor_llama_server.sh --auto-restart --interval 60 &

# Log monitoring to file
nohup ./scripts/monitor_llama_server.sh --auto-restart > monitor.out 2>&1 &
```

### CI/CD Integration

```bash
# In your CI/CD pipeline
./scripts/start_llama_server.sh

# Wait for healthy status
until QUIET=true ./scripts/check_server_status.sh; do
    echo "Waiting for server..."
    sleep 5
done

# Run tests
pytest tests/

# Cleanup
./scripts/stop_llama_server.sh
```

### Automated Health Checks

```bash
# Cron job for health monitoring (every 5 minutes)
*/5 * * * * cd /path/to/project && QUIET=true ./scripts/check_server_status.sh || ./scripts/restart_llama_server.sh

# Systemd service monitoring
[Unit]
Description=llama-server Monitor
After=network.target

[Service]
Type=simple
ExecStart=/path/to/scripts/monitor_llama_server.sh --auto-restart
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## Troubleshooting

### Server Won't Start

```bash
# Check if port is in use
lsof -i :8080

# Check system resources
./scripts/configure_llama_server.sh --show

# View detailed logs
tail -f logs/llama-server.log

# Try with verbose checking
./scripts/check_llama_server.sh --verbose
```

### Performance Issues

```bash
# Run benchmark to identify bottlenecks
./scripts/benchmark_llama_server.sh

# Check resource usage
./scripts/monitor_llama_server.sh

# Try different configuration
./scripts/configure_llama_server.sh
# Select a lighter preset
```

### Connection Errors

```bash
# Verify server is running
./scripts/check_server_status.sh

# Check firewall rules
sudo iptables -L | grep 8080  # Linux
sudo pfctl -s rules | grep 8080  # macOS

# Test direct connection
curl http://127.0.0.1:8080/health
```

---

## Best Practices

1. **Always use health checks** before running agents
   ```bash
   ./scripts/check_server_status.sh && python main.py
   ```

2. **Monitor resource usage** during development
   ```bash
   ./scripts/monitor_llama_server.sh --interval 15
   ```

3. **Benchmark after configuration changes**
   ```bash
   ./scripts/benchmark_llama_server.sh --throughput
   ```

4. **Use appropriate preset** for your hardware
   - 8-16GB RAM: Development preset
   - 16-32GB RAM: Balanced preset
   - 32GB+ RAM: Production preset

5. **Enable auto-restart** for production
   ```bash
   ./scripts/monitor_llama_server.sh --auto-restart
   ```

6. **Regular log rotation**
   ```bash
   # Logs automatically rotate at 100MB
   # Or manually:
   mv logs/llama-server.log logs/llama-server.log.old
   ```

---

## Architecture

### Script Dependencies

```
configure_llama_server.sh
    ↓
start_llama_server.sh
    ↓
check_llama_server.sh ←→ monitor_llama_server.sh
    ↓                           ↓
check_server_status.sh    restart_llama_server.sh
    ↓
stop_llama_server.sh
    ↓
benchmark_llama_server.sh
```

### File Structure

```
scripts/
├── README.md                      # This file
├── start_llama_server.sh          # Start server
├── stop_llama_server.sh           # Stop server
├── restart_llama_server.sh        # Restart server
├── check_llama_server.sh          # Comprehensive health check
├── check_server_status.sh         # Quick status check
├── monitor_llama_server.sh        # Continuous monitoring
├── configure_llama_server.sh      # Configuration wizard
├── benchmark_llama_server.sh      # Performance testing
├── setup_env.sh                   # Environment setup (Unix)
└── setup_env.bat                  # Environment setup (Windows)

logs/
├── llama-server.log              # Server output
├── llama-server.pid              # Process ID
├── monitor.log                   # Monitor activity
└── benchmark/                    # Benchmark results
    └── results_TIMESTAMP.json

.llama/
└── server.conf                   # Server configuration
```

---

## Advanced Features

### Custom Health Checks

Create custom health check scripts:

```bash
#!/bin/bash
source scripts/check_server_status.sh

# Add custom checks
if [ -f "my_custom_check.sh" ]; then
    ./my_custom_check.sh
fi
```

### Multi-Instance Management

Run multiple servers on different ports:

```bash
# Terminal 1 - Coding model
LLAMA_PORT=8080 LLAMA_MODEL="Qwen2.5-Coder-32B" ./scripts/start_llama_server.sh

# Terminal 2 - General model  
LLAMA_PORT=8081 LLAMA_MODEL="Llama-3.2-70B" ./scripts/start_llama_server.sh

# Monitor both
LLAMA_PORT=8080 ./scripts/monitor_llama_server.sh &
LLAMA_PORT=8081 ./scripts/monitor_llama_server.sh &
```

### Integration with Systemd

Create a systemd service:

```ini
# /etc/systemd/system/llama-server.service
[Unit]
Description=llama.cpp LLM Server
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/project
# Option 1: Use MODEL_QUANTIZATION (recommended)
Environment="MODEL_QUANTIZATION=Q8_0"
# Option 2: Or set full model path directly
# Environment="LLAMA_MODEL=unsloth/Devstral-Small-2-24B-Instruct-2512-GGUF:Q8_0"
# For smaller/faster model, use: Environment="MODEL_QUANTIZATION=UD-Q4_K_XL"
Environment="LLAMA_PORT=8080"
ExecStart=/path/to/scripts/start_llama_server.sh
ExecStop=/path/to/scripts/stop_llama_server.sh
Restart=on-failure
RestartSec=30

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable llama-server
sudo systemctl start llama-server
sudo systemctl status llama-server
```

---

## Performance Tips

1. **GPU Acceleration**
   - macOS: Automatically uses Metal
   - Linux/NVIDIA: Use CUDA-enabled build
   - Set `LLAMA_GPU_LAYERS=99` for maximum GPU usage

2. **Memory Optimization**
   - Reduce `LLAMA_CTX_SIZE` if running out of memory
   - Use smaller quantizations (Q4_K_M instead of Q8_0)
   - Close other memory-intensive applications

3. **CPU Performance**
   - Set `LLAMA_THREADS` to physical core count (not including hyperthreading)
   - Use `LLAMA_THREADS=-1` for auto-detection

4. **Concurrency**
   - Increase `LLAMA_PARALLEL` for handling multiple requests
   - Default `4` is good for most use cases
   - Increase to `8` or more for high-traffic scenarios

5. **Batch Processing**
   - Larger `LLAMA_BATCH_SIZE` = faster but more memory
   - Default `512` balances speed and memory
   - Reduce to `256` on low-memory systems

---

## License

These scripts are part of the LLM Multi-Agent System project.

---

## Support

For issues or questions:

1. Check the logs: `tail -f logs/llama-server.log`
2. Run diagnostics: `./scripts/check_llama_server.sh --verbose`
3. Consult the main project documentation: `../docs/`
4. Open an issue on the project repository

---

**Last Updated:** January 2026
**Script Version:** 2.0
**Compatible with:** llama.cpp latest, macOS, Linux, Windows (WSL)
