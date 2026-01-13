# 🚀 START HERE - Python 3.12 Setup

## ⚡ Quick Setup (2 minutes)

```bash
# 1. Install Python 3.12
brew install python@3.12

# 2. Verify installation
python3.12 --version
# Should show: Python 3.12.x

# 3. Create virtual environment
python3.12 -m venv venv

# 4. Activate virtual environment
source venv/bin/activate

# 5. Verify Python inside venv
python --version
# Should show: Python 3.12.x

# 6. Install dependencies
pip install -r requirements.txt

# 7. Test installation
python -c "import langgraph; print('✅ Ready!')"

# 8. Run your first workflow
python examples/langgraph_feature_development.py
```

---

## 🎯 Key Rule

### Creating Virtual Environment
**Always use:** `python3.12 -m venv venv`

### Inside Virtual Environment
**Always use:** `python` and `pip` (NOT `python3.12` or `pip3.12`)

---

## 📚 Documentation

| Document | When to Read |
|----------|--------------|
| **START_HERE.md** (this file) | First time setup |
| **PYTHON_3.12_REQUIREMENT.md** | Quick reference |
| **VENV_SETUP_GUIDE.md** | Complete venv tutorial |
| **LANGGRAPH_QUICK_START.md** | Start using LangGraph |
| **QUICK_REFERENCE.md** | Daily commands cheat sheet |
| **README.md** | Full project documentation |

---

## 🐛 Troubleshooting

### "python3.12: command not found"

```bash
brew install python@3.12
```

### "Wrong Python version in venv"

```bash
rm -rf venv
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### "Module not found"

```bash
source venv/bin/activate
pip install -r requirements.txt
```

---

## ✅ Verification

After setup, verify everything:

```bash
source venv/bin/activate
python --version  # Must show 3.12.x
python -c "import langgraph; from src.orchestrator.langgraph_orchestrator import LangGraphOrchestrator; print('✅ All working!')"
```

---

## 🎉 You're Ready!

Run your first example:

```bash
source venv/bin/activate
python examples/langgraph_feature_development.py
```

---

**Need help?** Read `VENV_SETUP_GUIDE.md` or `QUICK_REFERENCE.md`

**Date:** January 13, 2026  
**Python Version:** 3.12.x (required)
