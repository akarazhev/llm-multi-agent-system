# Virtual Environment Setup Guide - Python 3.12

## 📋 Base Requirement

**This project requires Python 3.12**

No other Python version is supported. Python 3.12 must be used to create the virtual environment.

---

## 🚀 Quick Setup (60 seconds)

```bash
# 1. Install Python 3.12 (if not already installed)
brew install python@3.12  # macOS

# 2. Create virtual environment with Python 3.12
python3.12 -m venv venv

# 3. Activate virtual environment
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# 4. Install dependencies (inside venv, use pip)
pip install -r requirements.txt

# 5. Verify
python --version  # Should show Python 3.12.x
```

---

## 📖 The Workflow

### Step 1: Install Python 3.12

#### macOS (Homebrew)
```bash
brew install python@3.12

# Verify installation
python3.12 --version
# Output: Python 3.12.x
```

#### Ubuntu/Debian
```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.12 python3.12-venv

# Verify
python3.12 --version
```

#### Windows
1. Download Python 3.12 from [python.org](https://www.python.org/downloads/)
2. Run installer, check "Add Python to PATH"
3. Verify: `py -3.12 --version`

---

### Step 2: Create Virtual Environment

```bash
# Navigate to project
cd /Users/andrey.karazhev/Developer/spg/llm-multi-agent-system

# Create venv with Python 3.12 (MUST use python3.12)
python3.12 -m venv venv
```

**Why `python3.12`?**
- Ensures exactly Python 3.12 is used
- Avoids version conflicts
- Required for LangChain/LangGraph compatibility

---

### Step 3: Activate Virtual Environment

```bash
# Linux/macOS
source venv/bin/activate

# Windows CMD
venv\Scripts\activate

# Windows PowerShell
venv\Scripts\Activate.ps1

# You'll see (venv) in your prompt:
(venv) user@host:~/project$
```

---

### Step 4: Install Dependencies

```bash
# Inside venv, use python and pip (NOT python3.12/pip3.12)
pip install -r requirements.txt

# Why just 'pip' and not 'pip3.12'?
# Inside venv, 'pip' already points to Python 3.12's pip
```

---

### Step 5: Verify Installation

```bash
# Check Python version (should be 3.12.x)
python --version

# Check pip version
pip --version

# Test imports
python -c "import langgraph; print('✓ LangGraph works')"
python -c "from src.orchestrator.langgraph_orchestrator import LangGraphOrchestrator; print('✓ Project imports work')"
```

---

## 📊 Command Reference

### Creating & Managing Virtual Environment

| Action | Command |
|--------|---------|
| **Create venv** | `python3.12 -m venv venv` |
| **Activate (Linux/macOS)** | `source venv/bin/activate` |
| **Activate (Windows)** | `venv\Scripts\activate` |
| **Check if active** | `echo $VIRTUAL_ENV` (shows path if active) |
| **Deactivate** | `deactivate` |
| **Delete venv** | `rm -rf venv` |

### Inside Virtual Environment

| Action | Command |
|--------|---------|
| **Check Python** | `python --version` |
| **Install package** | `pip install package` |
| **Install all deps** | `pip install -r requirements.txt` |
| **List packages** | `pip list` |
| **Run script** | `python script.py` |

---

## ✅ Daily Workflow

```bash
# Morning: Start work
cd /Users/andrey.karazhev/Developer/spg/llm-multi-agent-system
source venv/bin/activate

# Work on your code (use python, not python3.12)
python examples/langgraph_feature_development.py
python main.py
pip install new-package

# Evening: Done for the day (optional)
deactivate
```

---

## 🔧 Troubleshooting

### "python3.12: command not found"

**Solution:**
```bash
# Install Python 3.12
brew install python@3.12  # macOS
sudo apt install python3.12  # Ubuntu

# Verify
which python3.12
python3.12 --version
```

### "Wrong Python version inside venv"

**Solution:**
```bash
# Check version
source venv/bin/activate
python --version

# If not 3.12.x, recreate venv
deactivate
rm -rf venv
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### "Module not found" errors

**Solution:**
```bash
# Make sure venv is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Verify
python -c "import langgraph"
```

### Venv won't activate

**Solution:**
```bash
# Check if venv exists
ls venv/bin/activate

# If not, create it
python3.12 -m venv venv

# Then activate
source venv/bin/activate
```

---

## 🎯 Best Practices

### 1. Always Use Python 3.12

```bash
# ✅ CORRECT: Use python3.12 to create venv
python3.12 -m venv venv

# ❌ WRONG: Don't use other versions
python3 -m venv venv      # Could be 3.14 or any version!
python -m venv venv       # Unknown version!
```

### 2. Activate Before Working

```bash
# ✅ CORRECT: Activate first
source venv/bin/activate
python script.py

# ❌ WRONG: Running without activation
python3.12 script.py  # Uses system Python, not venv!
```

### 3. Use Simple Commands Inside Venv

```bash
# ✅ CORRECT: Inside venv
source venv/bin/activate
python script.py    # Simple!
pip install package # Simple!

# ❌ WRONG: Unnecessary complexity
source venv/bin/activate
python3.12 script.py  # Why? Just use python!
pip3.12 install package  # Why? Just use pip!
```

---

## 📚 Why Python 3.12?

### Compatibility Matrix

| Component | Python 3.12 | Python 3.11 | Python 3.14 |
|-----------|-------------|-------------|-------------|
| Pydantic v1 | ✅ | ✅ | ❌ |
| LangChain | ✅ | ✅ | ❌ |
| LangGraph | ✅ | ✅ | ❌ |
| OpenAI SDK | ✅ | ✅ | ✅ |
| **This Project** | ✅ **Required** | ⚠️ Not tested | ❌ Broken |

**We chose Python 3.12 as the standard** because:
- ✅ Fully compatible with all dependencies
- ✅ Stable and well-tested
- ✅ Latest version that works with LangChain/LangGraph
- ✅ Avoids Python 3.14 compatibility issues

---

## 🎓 Complete Example

```bash
# Full setup from scratch

# 1. Check if Python 3.12 is installed
python3.12 --version
# If not found, install it:
brew install python@3.12

# 2. Navigate to project
cd /Users/andrey.karazhev/Developer/spg/llm-multi-agent-system

# 3. Create venv
python3.12 -m venv venv

# 4. Activate
source venv/bin/activate

# 5. Verify Python version
python --version
# Should output: Python 3.12.x

# 6. Upgrade pip
pip install --upgrade pip

# 7. Install dependencies
pip install -r requirements.txt

# 8. Test installation
python -c "import langgraph; print('✓ Success')"

# 9. Run example
python examples/langgraph_feature_development.py

# 10. Done! Deactivate when finished
deactivate
```

---

## 🔄 Updating Dependencies

```bash
# Activate venv
source venv/bin/activate

# Update specific package
pip install --upgrade langgraph

# Update all packages
pip install --upgrade -r requirements.txt

# Freeze current versions
pip freeze > requirements-lock.txt
```

---

## 🗑️ Cleaning Up

```bash
# Remove virtual environment
rm -rf venv

# Remove Python cache files
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Recreate clean venv
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## ✅ Verification Checklist

Before running the project:

- [ ] Python 3.12 installed (`python3.12 --version`)
- [ ] Virtual environment created (`python3.12 -m venv venv`)
- [ ] Virtual environment activated (`source venv/bin/activate`)
- [ ] Python version correct inside venv (`python --version` shows 3.12.x)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] LangGraph imports work (`python -c "import langgraph"`)
- [ ] Project imports work (`python -c "from src.orchestrator import LangGraphOrchestrator"`)

---

## 🎯 Summary

| Step | Command |
|------|---------|
| **1. Install Python 3.12** | `brew install python@3.12` |
| **2. Create venv** | `python3.12 -m venv venv` |
| **3. Activate venv** | `source venv/bin/activate` |
| **4. Install deps** | `pip install -r requirements.txt` |
| **5. Run project** | `python script.py` |

**Remember:**
- Use `python3.12` ONLY to create the venv
- Inside venv, use `python` and `pip` (not `python3.12`/`pip3.12`)
- Python 3.12 is required - no other version is supported

---

**Status:** ✅ Updated for Python 3.12 only  
**Date:** January 13, 2026
