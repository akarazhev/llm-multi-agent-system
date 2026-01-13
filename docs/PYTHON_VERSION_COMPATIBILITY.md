# Python Version Requirement

## ⚠️ Python 3.12 Required

**This project requires Python 3.12.x**

No other Python version is supported or tested.

---

## 🎯 Why Python 3.12?

### The Issue with Other Versions

| Python Version | Status | Reason |
|----------------|--------|--------|
| **3.12.x** | ✅ **Required** | Fully compatible, tested, stable |
| 3.11.x | ⚠️ Not supported | Not tested with this project |
| 3.13.x | ❌ Incompatible | Potential compatibility issues |
| 3.14.x | ❌ Broken | Pydantic v1 incompatible, LangChain breaks |

###  Why Not Python 3.14?

Python 3.14 introduces breaking changes that affect:
- **Pydantic v1** - Used internally by LangChain
- **LangGraph** - Import paths and checkpointing
- **LangChain Core** - Multiple compatibility issues

Error you'd see with Python 3.14:
```
UserWarning: Core Pydantic V1 functionality isn't compatible with Python 3.14
ModuleNotFoundError: No module named 'langgraph.checkpoint.aiosqlite'
```

---

## 🚀 Installing Python 3.12

### macOS (Homebrew)

```bash
# Install Python 3.12
brew install python@3.12

# Verify
python3.12 --version
# Output: Python 3.12.x

# Find installation path
which python3.12
# Output: /opt/homebrew/bin/python3.12
```

### Ubuntu/Debian

```bash
# Add deadsnakes PPA
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update

# Install Python 3.12
sudo apt install python3.12 python3.12-venv python3.12-dev

# Verify
python3.12 --version
```

### Windows

1. Download Python 3.12.x from [python.org](https://www.python.org/downloads/)
2. Run installer
3. ✅ Check "Add Python 3.12 to PATH"
4. Complete installation
5. Verify in CMD: `py -3.12 --version`

### Using pyenv (Cross-platform)

```bash
# Install pyenv
curl https://pyenv.run | bash

# Install Python 3.12
pyenv install 3.12.7

# Set as local version for this project
cd /Users/andrey.karazhev/Developer/spg/llm-multi-agent-system
pyenv local 3.12.7

# Verify
python --version  # Shows 3.12.7
```

---

## 🔧 Setting Up the Project

### Complete Setup

```bash
# 1. Verify Python 3.12 is installed
python3.12 --version

# 2. Navigate to project
cd /Users/andrey.karazhev/Developer/spg/llm-multi-agent-system

# 3. Create virtual environment with Python 3.12
python3.12 -m venv venv

# 4. Activate virtual environment
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# 5. Verify Python version inside venv
python --version
# Should show: Python 3.12.x

# 6. Install dependencies
pip install -r requirements.txt

# 7. Test installation
python -c "import langgraph; print('✓ Success')"
```

---

## 🐛 Troubleshooting

### Issue: "python3.12: command not found"

**You don't have Python 3.12 installed.**

**Solution:**
```bash
# macOS
brew install python@3.12

# Ubuntu/Debian
sudo apt install python3.12

# Then verify
python3.12 --version
```

### Issue: "Pydantic v1 not compatible" warning

**You're using Python 3.14 or newer.**

**Solution:**
```bash
# Check Python version
python --version

# If 3.14+, remove venv and recreate with 3.12
deactivate
rm -rf venv
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: Wrong Python inside venv

**Venv was created with wrong Python version.**

**Solution:**
```bash
# Check version inside venv
source venv/bin/activate
python --version

# If not 3.12.x, recreate venv
deactivate
rm -rf venv
python3.12 -m venv venv
source venv/bin/activate
python --version  # Verify shows 3.12.x
pip install -r requirements.txt
```

### Issue: "ModuleNotFoundError: No module named 'langgraph'"

**Dependencies not installed or wrong venv.**

**Solution:**
```bash
# Make sure venv is activated
source venv/bin/activate

# Verify Python version
python --version  # Must be 3.12.x

# Reinstall dependencies
pip install -r requirements.txt

# Test
python -c "import langgraph"
```

---

## 🔄 Migrating from Wrong Python Version

### If you currently have Python 3.14:

```bash
# 1. Check current version
python --version

# 2. Install Python 3.12
brew install python@3.12  # macOS

# 3. Remove old venv
deactivate  # if active
rm -rf venv

# 4. Create new venv with Python 3.12
python3.12 -m venv venv

# 5. Activate
source venv/bin/activate

# 6. Verify
python --version  # Should show 3.12.x

# 7. Install dependencies
pip install -r requirements.txt

# 8. Test
python examples/langgraph_feature_development.py
```

---

## 🎯 Automated Fix Script

We provide a script that automatically fixes Python version issues:

```bash
# Run the fix script
./scripts/fix_python_version.sh

# This will:
# 1. Find Python 3.12 on your system
# 2. Backup your current venv
# 3. Create new venv with Python 3.12
# 4. Install all dependencies
# 5. Verify everything works
```

---

## ✅ Verification

After setup, verify everything is correct:

```bash
# 1. Activate venv
source venv/bin/activate

# 2. Check Python version
python --version
# Should output: Python 3.12.x

# 3. Check pip version
pip --version
# Should reference Python 3.12

# 4. Test imports
python -c "import langgraph; print('✓ LangGraph')"
python -c "import langchain_core; print('✓ LangChain')"
python -c "from src.orchestrator.langgraph_orchestrator import LangGraphOrchestrator; print('✓ Project')"

# 5. Run example
python examples/langgraph_feature_development.py
```

---

## 📊 Dependency Compatibility

| Package | Python 3.12 | Notes |
|---------|-------------|-------|
| pydantic v1 | ✅ | Fully compatible |
| langchain-core | ✅ | Fully compatible |
| langgraph | ✅ | Fully compatible |
| openai | ✅ | Fully compatible |
| aiosqlite | ✅ | Fully compatible |
| All project deps | ✅ | Tested and working |

---

## 🎓 Best Practices

### 1. Always Use Python 3.12

```bash
# ✅ CORRECT
python3.12 -m venv venv

# ❌ WRONG - Don't use these
python3 -m venv venv      # Unknown version!
python -m venv venv       # Unknown version!
python3.14 -m venv venv   # Too new, will break!
```

### 2. Verify Before Working

```bash
# Before starting work, always verify
source venv/bin/activate
python --version  # Must show 3.12.x
```

### 3. Document in Your Team

Make sure everyone on your team uses Python 3.12:
```bash
# Add to your team documentation
echo "Python 3.12 required" >> SETUP_NOTES.md
```

---

## 📚 Additional Resources

- **Python 3.12 Download**: https://www.python.org/downloads/release/python-3127/
- **pyenv Documentation**: https://github.com/pyenv/pyenv
- **Homebrew**: https://brew.sh/

---

## 🎯 Summary

**Requirement:** Python 3.12.x only

**Installation:**
```bash
brew install python@3.12  # macOS
```

**Setup:**
```bash
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Verification:**
```bash
python --version  # Must show 3.12.x
```

---

**Status:** ✅ Updated for Python 3.12 requirement  
**Date:** January 13, 2026  
**Version:** 1.0.0
