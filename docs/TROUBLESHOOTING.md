# Troubleshooting Guide

Common issues and solutions for the LLM Multi-Agent System.

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [Configuration Issues](#configuration-issues)
3. [llama-server Issues](#llama-server-issues)
4. [Agent Execution Issues](#agent-execution-issues)
5. [Performance Issues](#performance-issues)
6. [File Operation Issues](#file-operation-issues)
7. [Network & Connection Issues](#network--connection-issues)
8. [Memory & Resource Issues](#memory--resource-issues)
9. [Platform-Specific Issues](#platform-specific-issues)
10. [Getting Help](#getting-help)

## Installation Issues

### Issue: Python Version Too Old

**Error:**
```
RuntimeError: Python 3.12 required. Current version: x.x.x
```

**Solution:**
```bash
# macOS with Homebrew
brew install python@3.12

# Ubuntu/Debian
sudo apt install python3.12 python3.12-venv

# Windows - Download Python 3.12 from python.org
# https://www.python.org/downloads/

# Verify installation
python3.12 --version

# Recreate virtual environment
rm -rf venv
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: pip install Fails

**Error:**
```
ERROR: Could not install packages due to an EnvironmentError
```

**Solution:**
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Use --user flag if permission denied
pip install --user -r requirements.txt

# Or use virtual environment (recommended)
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: llama.cpp Not Found

**Error:**
```
bash: llama-server: command not found
```

**Solution:**
```bash
# macOS
brew install llama.cpp

# Verify installation
which llama-server
llama-server --version

# If not in PATH, use full path
/opt/homebrew/bin/llama-server

# Or add to PATH
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Issue: Module Not Found

**Error:**
```
ModuleNotFoundError: No module named 'src'
```

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt

# Verify installation
python -c "from src.orchestrator import AgentOrchestrator; print('OK')"
```

## Configuration Issues

### Issue: "OPENAI_API_BASE not configured"

**Error:**
```
ERROR: OPENAI_API_BASE not configured. Local llama-server required.
```

**Solution:**
```bash
# Create .env file
cp .env.example .env

# Add required configuration
cat >> .env << EOF
OPENAI_API_BASE=http://127.0.0.1:8080/v1
OPENAI_API_KEY=not-needed
OPENAI_API_MODEL=devstral
EOF

# Verify
source venv/bin/activate
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('OPENAI_API_BASE'))"
```

### Issue: Configuration File Not Found

**Error:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'config.yaml'
```

**Solution:**
```bash
# Check if config.yaml exists
ls -l config.yaml

# If missing, create from example or default
cat > config.yaml << EOF
workspace: "."
log_level: "INFO"
llm_timeout: 300
max_concurrent_agents: 5

agents:
  business_analyst:
    enabled: true
  developer:
    enabled: true
  qa_engineer:
    enabled: true
  devops_engineer:
    enabled: true
  technical_writer:
    enabled: true
EOF
```

### Issue: Invalid YAML Syntax

**Error:**
```
yaml.scanner.ScannerError: while scanning for the next token
```

**Solution:**
```bash
# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('config.yaml'))"

# Common issues:
# 1. Incorrect indentation (use spaces, not tabs)
# 2. Missing colons
# 3. Unquoted special characters

# Use a YAML validator
# https://www.yamllint.com/
```

## llama-server Issues

### Issue: Connection Refused

**Error:**
```
requests.exceptions.ConnectionError: Connection refused
```

**Solution:**
```bash
# 1. Check if llama-server is running
curl http://127.0.0.1:8080/health

# 2. If not running, start it
# Ensure your local LLM server is running on port 8080

# 3. Check the logs
tail -f logs/llama-server.log

# 4. Verify port is correct
lsof -i :8080  # macOS/Linux
netstat -ano | findstr :8080  # Windows

# 5. If port is in use, change it
export LLAMA_PORT=8081
# Ensure your local LLM server is running on port 8080

# Update .env
OPENAI_API_BASE=http://127.0.0.1:8081/v1
```

### Issue: Model Not Found

**Error:**
```
Error: Model file not found
```

**Solution:**
```bash
# 1. Check model file exists
ls -lh models/*.gguf

# 2. Download model if missing
mkdir -p models
cd models

# Download Devstral (default)
wget https://huggingface.co/unsloth/Devstral-Small-2-24B-Instruct-2512-GGUF/resolve/main/Devstral-Small-2-24B-Instruct-2512.Q4_K_M.gguf

# Or use llama-cli to download from HuggingFace
llama-cli -hf unsloth/Devstral-Small-2-24B-Instruct-2512-GGUF:UD-Q4_K_XL

# 3. Update start script with correct model path
export LLAMA_MODEL_PATH="$(pwd)/models/your-model.gguf"
# Ensure your local LLM server is running on port 8080
```

### Issue: llama-server Crashes

**Error:**
```
llama-server: Segmentation fault
```

**Solution:**
```bash
# 1. Check system resources
free -h  # Linux
vm_stat  # macOS

# 2. Reduce memory usage
export LLAMA_CTX_SIZE=4096  # Smaller context
export LLAMA_GPU_LAYERS=0   # CPU only
# Ensure your local LLM server is running on port 8080

# 3. Use smaller model
export LLAMA_MODEL="unsloth/Llama-3.2-3B-Instruct-GGUF:Q4_K_M"

# 4. Update llama.cpp
brew upgrade llama.cpp  # macOS
# Or rebuild from source
cd llama.cpp && git pull && make clean && make

# 5. Check logs for specific error
tail -100 logs/llama-server-error.log
```

### Issue: Wrong Model Loaded

**Error:**
```
Error: Model mismatch - expected 'devstral', got 'qwen2.5-coder'
```

**Solution:**
```bash
# 1. Check model name in llama-server output
curl http://127.0.0.1:8080/v1/models

# 2. Update .env to match
# Change OPENAI_API_MODEL to match the actual model name

# 3. Or restart your local LLM server with correct model
# Stop your local LLM server
export LLAMA_MODEL="unsloth/Devstral-Small-2-24B-Instruct-2512-GGUF:UD-Q4_K_XL"
# Ensure your local LLM server is running on port 8080
```

## Agent Execution Issues

### Issue: Task Timeout

**Error:**
```
ERROR: Task timed out after 300 seconds
```

**Solution:**
```yaml
# Increase timeout in config.yaml
llm_timeout: 600  # 10 minutes
task_timeout: 900    # 15 minutes

# Or set environment variable
export LLM_TIMEOUT=600
```

### Issue: Agent Task Fails

**Error:**
```
ERROR: Agent failed to complete task: [error details]
```

**Solution:**
```bash
# 1. Check logs for specific error
tail -100 logs/agent_system.log | grep ERROR

# 2. Verify LLM server is responding
curl http://127.0.0.1:8080/v1/models

# 3. Test simple task
python tests/simple_test.py

# 4. Check agent-specific configuration
# Verify languages, frameworks, etc. in config.yaml

# 5. Increase log level for debugging
# In config.yaml:
log_level: "DEBUG"
```

### Issue: No Files Generated

**Error:**
```
WARNING: No code blocks found in response
```

**Solution:**
```bash
# 1. Check if LLM is returning properly formatted code
# Look in logs for the actual LLM response

# 2. Verify prompt includes format instructions
# Should mention code blocks with filenames

# 3. Try different prompt approach
# Some models need explicit formatting instructions

# 4. Check FileWriter is working
python tests/test_file_writer.py

# 5. Try simpler requirement
# Start with basic "Create a hello world Python script"
```

### Issue: Duplicate Files Created

**Error:**
```
Multiple files with same name created
```

**Solution:**
This is a known issue with some LLM responses. The FileWriter has logic to handle this:

```python
# The system should avoid duplicates, but if it happens:
# 1. Check output directory for duplicates
ls -la output/generated/

# 2. Clean up duplicates manually
rm output/generated/duplicate_file.py

# 3. Verify FileWriter logic
python tests/test_no_duplicates.py
```

## Performance Issues

### Issue: Slow Inference

**Symptoms:**
- Tasks taking > 2 minutes
- High CPU usage
- System becomes unresponsive

**Solution:**
```bash
# 1. Enable GPU acceleration
export LLAMA_GPU_LAYERS=99
# Ensure your local LLM server is running on port 8080

# 2. Verify GPU is being used
# macOS
sudo powermetrics --samplers gpu_power

# NVIDIA
nvidia-smi

# 3. Use faster model
export LLAMA_MODEL="unsloth/Llama-3.2-3B-Instruct-GGUF:Q4_K_M"

# 4. Reduce context size
export LLAMA_CTX_SIZE=4096

# 5. Increase CPU threads (if CPU-only)
export LLAMA_THREADS=16
```

### Issue: High Memory Usage

**Symptoms:**
- System using > 90% RAM
- Swap space heavily used
- System slowing down

**Solution:**
```bash
# 1. Check memory usage
free -h  # Linux
vm_stat  # macOS

# 2. Reduce context size
export LLAMA_CTX_SIZE=4096

# 3. Use smaller model
export LLAMA_MODEL="unsloth/Llama-3.2-3B-Instruct-GGUF:Q4_K_M"

# 4. Reduce concurrent agents
# In config.yaml:
max_concurrent_agents: 3  # Instead of 5

# 5. Offload fewer layers to GPU
export LLAMA_GPU_LAYERS=32  # Instead of 99
```

### Issue: Disk Space Full

**Error:**
```
OSError: [Errno 28] No space left on device
```

**Solution:**
```bash
# 1. Check disk space
df -h

# 2. Clean old outputs
rm -rf output/workflow_*_2024-01-*.json

# 3. Clean logs
rm logs/*.log.gz
truncate -s 0 logs/agent_system.log

# 4. Remove unused models
rm models/*Q8*.gguf  # Keep only Q4 models

# 5. Configure log rotation
# See DEPLOYMENT.md for logrotate configuration
```

## File Operation Issues

### Issue: Permission Denied

**Error:**
```
PermissionError: [Errno 13] Permission denied: 'output/file.py'
```

**Solution:**
```bash
# 1. Check file permissions
ls -la output/

# 2. Fix permissions
chmod -R u+rw output/
chmod -R u+rw logs/

# 3. Check workspace ownership
# Ensure workspace is owned by your user
sudo chown -R $USER:$USER /path/to/workspace

# 4. Run with proper user (not root)
# Don't use sudo unless necessary
```

### Issue: File Already Exists

**Error:**
```
FileExistsError: [Errno 17] File exists: 'output/file.py'
```

**Solution:**
```python
# This is usually handled automatically, but if it persists:

# 1. Check FileWriter configuration
# Should handle overwrites

# 2. Manually clean output directory
rm -rf output/generated/*

# 3. Or move to backup
mv output/generated output/generated.backup

# 4. Create fresh output directory
mkdir -p output/generated
```

### Issue: Invalid File Path

**Error:**
```
ValueError: Invalid file path contains '..'
```

**Solution:**
```bash
# This is a security feature to prevent directory traversal

# 1. Check the LLM response
# File paths should be relative, not absolute

# 2. Verify workspace configuration
# Should be set to a valid directory

# 3. Adjust path validation if needed (advanced)
# Only do this if you understand the security implications
```

## Network & Connection Issues

### Issue: DNS Resolution Fails (During Model Download)

**Error:**
```
requests.exceptions.ConnectionError: Failed to resolve 'huggingface.co'
```

**Solution:**
```bash
# 1. Check internet connectivity
ping -c 3 google.com

# 2. Check DNS
nslookup huggingface.co

# 3. Try different DNS
# Add to /etc/resolv.conf:
nameserver 8.8.8.8
nameserver 8.8.4.4

# 4. Download model manually
wget https://huggingface.co/...model.gguf

# 5. Use mirror or alternative source
```

### Issue: Firewall Blocking

**Error:**
```
Connection timeout
```

**Solution:**
```bash
# 1. Check if firewall is blocking
sudo ufw status  # Linux
pfctl -s rules   # macOS

# 2. Allow localhost connections (should be default)
sudo ufw allow from 127.0.0.1

# 3. Verify llama-server binds to localhost
# Should use --host 127.0.0.1, not 0.0.0.0
```

## Memory & Resource Issues

### Issue: Out of Memory (OOM)

**Error:**
```
RuntimeError: CUDA out of memory
# or
Killed (Linux)
```

**Solution:**
```bash
# 1. Use smaller quantization
export LLAMA_MODEL="model:Q4_K_M"  # Instead of Q8_0

# 2. Reduce context size
export LLAMA_CTX_SIZE=4096  # Instead of 16384

# 3. Reduce GPU layers
export LLAMA_GPU_LAYERS=32  # Instead of 99

# 4. Use CPU inference
export LLAMA_GPU_LAYERS=0

# 5. Close other applications
# Free up RAM before running

# 6. Add swap space (Linux)
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### Issue: CPU Overload

**Symptoms:**
- CPU at 100%
- System very slow
- Fans at maximum

**Solution:**
```bash
# 1. Reduce thread count
export LLAMA_THREADS=4  # Instead of auto-detect

# 2. Lower process priority
nice -n 19 # Ensure your local LLM server is running on port 8080

# 3. Limit CPU usage (Linux)
cpulimit -l 50 -p $(pgrep llama-server)

# 4. Use GPU instead
export LLAMA_GPU_LAYERS=99
```

## Platform-Specific Issues

### macOS Issues

#### Issue: "llama-server" cannot be opened

**Error:**
```
"llama-server" can't be opened because Apple cannot check it for malicious software
```

**Solution:**
```bash
# Remove quarantine attribute
xattr -d com.apple.quarantine $(which llama-server)

# Or allow in System Preferences
# System Preferences > Security & Privacy > Allow anyway
```

#### Issue: Metal Performance Issues

**Solution:**
```bash
# Verify Metal is enabled
system_profiler SPDisplaysDataType | grep Metal

# Force Metal usage
export LLAMA_METAL=1
export LLAMA_GPU_LAYERS=99

# Update llama.cpp for latest Metal optimizations
brew upgrade llama.cpp
```

### Linux Issues

#### Issue: CUDA Not Found

**Error:**
```
Could not load CUDA library
```

**Solution:**
```bash
# 1. Verify NVIDIA driver
nvidia-smi

# 2. Install CUDA toolkit
# Ubuntu
sudo apt install nvidia-cuda-toolkit

# 3. Rebuild llama.cpp with CUDA
cd llama.cpp
make clean
make LLAMA_CUDA=1

# 4. Set environment variables
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
```

### Windows Issues

#### Issue: PowerShell Execution Policy

**Error:**
```
cannot be loaded because running scripts is disabled
```

**Solution:**
```powershell
# Run as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or bypass for single script
powershell -ExecutionPolicy Bypass -File script.ps1
```

#### Issue: Long Path Support

**Error:**
```
OSError: [WinError 206] The filename or extension is too long
```

**Solution:**
```powershell
# Enable long path support (Windows 10+)
# Run as Administrator
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" `
    -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force

# Restart required
```

## Getting Help

### Before Asking for Help

1. **Check logs:**
   ```bash
   tail -100 logs/agent_system.log
   tail -100 logs/llama-server.log
   ```

2. **Verify configuration:**
   ```bash
   cat .env
   cat config.yaml
   ```

3. **Test components:**
   ```bash
   # Test LLM server
   curl http://127.0.0.1:8080/v1/models
   
   # Test agent system
   python tests/simple_test.py
   
   # Test file writer
   python tests/test_file_writer.py
   ```

4. **Gather system information:**
   ```bash
   # Python version
   python --version
   
   # Operating system
   uname -a  # macOS/Linux
   systeminfo  # Windows
   
   # Memory
   free -h  # Linux
   vm_stat  # macOS
   
   # Disk space
   df -h
   ```

### Where to Get Help

1. **Documentation:**
   - [Quick Start](QUICK_START.md)
   - [Architecture](ARCHITECTURE.md)
   - [API Reference](API_REFERENCE.md)
   - [Deployment](DEPLOYMENT.md)

2. **Examples:**
   - Check `examples/` directory
   - Run example scripts

3. **GitHub Issues:**
   - Search existing issues
   - Create new issue with:
     - Error message
     - Steps to reproduce
     - System information
     - Configuration (sanitized)
     - Logs (relevant portions)

4. **Community:**
   - Project discussions
   - Stack Overflow (tag: llm-multi-agent)

### Creating a Good Bug Report

Include:

1. **Environment:**
   ```
   OS: macOS 14.0
   Python: 3.11.5
   llama.cpp: 1.2.3
   Model: Devstral-Small-2-24B Q4_K_M
   ```

2. **Configuration:**
   ```yaml
   # Sanitized config.yaml and .env
   # Remove any sensitive information
   ```

3. **Steps to Reproduce:**
   ```
   1. Start llama-server
   2. Run python main.py
   3. Enter requirement: "..."
   4. Select workflow: 1
   5. Error occurs at step X
   ```

4. **Expected vs Actual:**
   ```
   Expected: Task completes successfully
   Actual: Task times out after 300 seconds
   ```

5. **Logs:**
   ```
   # Last 50 lines of relevant log
   # Include full error traceback
   ```

6. **What You've Tried:**
   ```
   - Increased timeout to 600s
   - Restarted llama-server
   - Tried simpler requirement
   ```

## Quick Reference

### Health Check Commands

```bash
# Check all components
./scripts/check_system_health.sh

# Check llama-server
curl http://127.0.0.1:8080/health

# Check agent system
python -c "from src.orchestrator import AgentOrchestrator; print('OK')"

# Check configuration
python -c "from src.config import load_config; c=load_config(); print(c.workspace)"

# Check disk space
df -h

# Check memory
free -h  # Linux
vm_stat  # macOS

# Check processes
ps aux | grep llama-server
ps aux | grep python
```

### Log Locations

```bash
# Agent system logs
tail -f logs/agent_system.log

# llama-server logs
tail -f logs/llama-server.log

# System journal (Linux)
sudo journalctl -u llama-server.service -f
sudo journalctl -u agent-system.service -f
```

### Common Fixes

```bash
# Restart everything
# Stop your local LLM server
# Ensure your local LLM server is running on port 8080
python main.py

# Clean and restart
rm -rf output/generated/*
rm logs/*.log
# Ensure your local LLM server is running on port 8080
python main.py

# Reset configuration
cp .env.example .env
# Edit .env with your settings
cp config.yaml.example config.yaml
# Edit config.yaml
```

---

If you've tried everything here and still have issues, please create a GitHub issue with detailed information.
