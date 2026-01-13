# Python 3.12 Requirement - Final Summary

## ✅ Project Standard: Python 3.12

**This project requires and only supports Python 3.12.x**

---

## 🎯 Quick Reference

| What | Command |
|------|---------|
| **Install Python 3.12** | `brew install python@3.12` |
| **Create venv** | `python3.12 -m venv venv` |
| **Activate venv** | `source venv/bin/activate` |
| **Install deps** | `pip install -r requirements.txt` |
| **Run project** | `python script.py` |

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| **PYTHON_VERSION_COMPATIBILITY.md** | Why Python 3.12, installation guide |
| **VENV_SETUP_GUIDE.md** | Complete virtual environment tutorial |
| **LANGGRAPH_QUICK_START.md** | Quick start with LangGraph |
| **QUICK_REFERENCE.md** | One-page cheat sheet |
| **README.md** | Main project documentation |

---

## 🚀 Quick Setup

```bash
# 1. Install Python 3.12
brew install python@3.12

# 2. Create and activate venv
python3.12 -m venv venv
source venv/bin/activate

# 3. Verify Python version
python --version  # Must show 3.12.x

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run example
python examples/langgraph_feature_development.py
```

---

## ⚠️ Why Python 3.12 Only?

### Compatibility Table

| Python Version | Status | Reason |
|----------------|--------|--------|
| **3.12.x** | ✅ **Required** | Only tested and supported version |
| 3.11.x | ⚠️ Not tested | May work but not supported |
| 3.14.x | ❌ Broken | Pydantic v1 incompatible |

### Python 3.14 Issues

Python 3.14 breaks:
- Pydantic v1 (used by LangChain)
- LangGraph imports
- LangChain core functionality

Error with Python 3.14:
```
UserWarning: Core Pydantic V1 functionality isn't compatible with Python 3.14
ModuleNotFoundError: No module named 'langgraph.checkpoint.aiosqlite'
```

---

## 🔧 If You Have Wrong Python Version

### Automated Fix

```bash
./scripts/fix_python_version.sh
```

### Manual Fix

```bash
# 1. Install Python 3.12
brew install python@3.12

# 2. Remove old venv
rm -rf venv

# 3. Create new venv with Python 3.12
python3.12 -m venv venv

# 4. Activate
source venv/bin/activate

# 5. Verify
python --version  # Must show 3.12.x

# 6. Install
pip install -r requirements.txt
```

---

## ✅ Verification Checklist

- [ ] Python 3.12 installed (`python3.12 --version`)
- [ ] Venv created with Python 3.12 (`python3.12 -m venv venv`)
- [ ] Venv activated (`source venv/bin/activate`)
- [ ] Python version correct (`python --version` shows 3.12.x)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Imports work (`python -c "import langgraph"`)

---

## 📝 Files Updated for Python 3.12

### Scripts (2 files)
- ✅ `scripts/setup_env.sh` - Uses python3.12
- ✅ `scripts/setup_langgraph.sh` - Uses python3.12

### Documentation (6 files)
- ✅ `README.md` - Python 3.12 requirement
- ✅ `VENV_SETUP_GUIDE.md` - Python 3.12 tutorial
- ✅ `LANGGRAPH_QUICK_START.md` - Python 3.12 quick start
- ✅ `QUICK_REFERENCE.md` - Python 3.12 commands
- ✅ `PYTHON_VERSION_COMPATIBILITY.md` - Why Python 3.12
- ✅ `requirements.txt` - Python 3.12 note

### Helper Scripts
- ✅ `scripts/fix_python_version.sh` - Auto-fix for wrong version

---

## 🎯 Key Points

1. **Only Python 3.12** - No other version supported
2. **Use `python3.12`** - To create venv
3. **Inside venv use `python`** - Not `python3.12`
4. **Verify version** - Always check `python --version` shows 3.12.x
5. **Read the docs** - Check PYTHON_VERSION_COMPATIBILITY.md for details

---

## 🆘 Need Help?

### Quick Links
- Installation issues → `PYTHON_VERSION_COMPATIBILITY.md`
- Virtual env help → `VENV_SETUP_GUIDE.md`
- Quick commands → `QUICK_REFERENCE.md`
- Getting started → `LANGGRAPH_QUICK_START.md`

### Common Issues

**"python3.12 not found"**
```bash
brew install python@3.12
```

**"Wrong Python in venv"**
```bash
rm -rf venv && python3.12 -m venv venv
```

**"Module not found"**
```bash
source venv/bin/activate && pip install -r requirements.txt
```

---

## 📊 Summary

| Aspect | Value |
|--------|-------|
| **Required Python** | 3.12.x only |
| **Installation** | `brew install python@3.12` |
| **Create venv** | `python3.12 -m venv venv` |
| **Activate** | `source venv/bin/activate` |
| **Inside venv** | Use `python` and `pip` |
| **Verify** | `python --version` shows 3.12.x |

---

**Status:** ✅ Complete - All documentation updated for Python 3.12  
**Date:** January 13, 2026  
**Standard:** Python 3.12.x required
