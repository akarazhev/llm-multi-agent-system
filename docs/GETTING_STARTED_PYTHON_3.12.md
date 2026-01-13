# Getting Started - Python 3.12 Edition

## 🎯 You Need Python 3.12

This project **requires Python 3.12** to work correctly.

---

## ⚡ Complete Setup (3 minutes)

### Step 1: Install Python 3.12

```bash
# macOS
brew install python@3.12

# Ubuntu/Debian
sudo apt install python3.12 python3.12-venv

# Windows
# Download from python.org and install Python 3.12.x
```

### Step 2: Verify Installation

```bash
python3.12 --version
# Should output: Python 3.12.x
```

### Step 3: Setup Project

```bash
# Navigate to project
cd /Users/andrey.karazhev/Developer/spg/llm-multi-agent-system

# Create virtual environment with Python 3.12
python3.12 -m venv venv

# Activate venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Verify Python version inside venv
python --version
# Should output: Python 3.12.x (same as python3.12)

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import langgraph; print('✅ Setup complete!')"
```

### Step 4: Run Example

```bash
# Inside venv (make sure it's activated)
python examples/langgraph_feature_development.py
```

---

## 🎓 Understanding the Commands

### Outside Virtual Environment

| Command | Purpose |
|---------|---------|
| `python3.12 --version` | Check Python 3.12 is installed |
| `python3.12 -m venv venv` | **Create venv** with Python 3.12 |

### Inside Virtual Environment

| Command | Purpose |
|---------|---------|
| `source venv/bin/activate` | Activate venv |
| `python --version` | Check Python (should be 3.12.x) |
| `pip install package` | Install package |
| `python script.py` | Run Python script |
| `deactivate` | Exit venv |

---

## 📝 Daily Workflow

```bash
# Morning: Start work
cd /Users/andrey.karazhev/Developer/spg/llm-multi-agent-system
source venv/bin/activate

# Your prompt changes to:
(venv) user@host:~/project$

# Work with your code
python examples/langgraph_feature_development.py
python main.py

# Install new package if needed
pip install package-name

# Evening: Done (optional)
deactivate
```

---

## 🐛 Troubleshooting

### Problem: "python3.12: command not found"

**You don't have Python 3.12 installed.**

**Solution:**
```bash
# macOS
brew install python@3.12

# Verify
python3.12 --version
```

### Problem: "Pydantic v1 not compatible with Python 3.14"

**You're using Python 3.14 (too new).**

**Solution:**
```bash
# Install Python 3.12
brew install python@3.12

# Remove old venv
rm -rf venv

# Create new venv with Python 3.12
python3.12 -m venv venv

# Activate and install
source venv/bin/activate
pip install -r requirements.txt
```

### Problem: "ModuleNotFoundError"

**Dependencies not installed or venv not activated.**

**Solution:**
```bash
# Make sure venv is activated
source venv/bin/activate

# Check Python version
python --version  # Must be 3.12.x

# Reinstall dependencies
pip install -r requirements.txt
```

### Problem: Wrong Python version inside venv

**Venv was created with wrong Python.**

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
python --version  # Verify 3.12.x
pip install -r requirements.txt
```

---

## 🚀 Quick Fix Script

If you have issues, run the auto-fix:

```bash
./scripts/fix_python_version.sh
```

This will:
- Find Python 3.12
- Recreate venv correctly
- Install dependencies
- Verify everything works

---

## ✅ Verification Checklist

Before running the project:

- [ ] Python 3.12 installed (`python3.12 --version`)
- [ ] Venv created with Python 3.12 (`python3.12 -m venv venv`)
- [ ] Venv activated (`source venv/bin/activate`)
- [ ] Python version correct (`python --version` shows 3.12.x)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Imports work (`python -c "import langgraph"`)

All checked? You're ready to go! 🎉

---

## 📚 Learn More

| Document | Purpose |
|----------|---------|
| `VENV_SETUP_GUIDE.md` | Complete virtual environment tutorial |
| `PYTHON_VERSION_COMPATIBILITY.md` | Why Python 3.12 is required |
| `LANGGRAPH_QUICK_START.md` | Start using LangGraph |
| `QUICK_REFERENCE.md` | One-page command reference |

---

## 🎯 Remember

| Context | Use This |
|---------|----------|
| **Creating venv** | `python3.12 -m venv venv` |
| **Inside venv** | `python` and `pip` |
| **Checking version** | `python --version` (inside venv) |

**Never use `python3` or `python3.14` - always use `python3.12` to create the venv!**

---

**Status:** ✅ Complete  
**Date:** January 13, 2026  
**Python:** 3.12.x (required)
