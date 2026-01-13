# ⚡ Quick Start - Mock Mode

## 🚀 One Command Start

```bash
./start-mock.sh
```

That's it! Browser will open with fully functional UI and mock data.

---

## 📦 First Time Setup

```bash
# 1. Go to frontend directory
cd frontend-ui

# 2. Install dependencies (only once)
npm install

# 3. Start mock mode
./start-mock.sh
```

---

## 🎭 What You'll See

### Dashboard
- 📊 **4 Stat Cards**: Total agents, active workflows, completed today, total workflows
- 🤖 **5 AI Agents**: All with different statuses (IDLE, WORKING, COMPLETED)
- 📋 **Recent Workflows**: Last 5 workflows with details

### Workflows Page
- 📑 **6 Sample Workflows**:
  - Feature Development (RUNNING) - JWT Auth API
  - Bug Fix (COMPLETED) - WebSocket memory leak
  - Infrastructure (COMPLETED) - Kubernetes setup
  - Documentation (COMPLETED) - API docs
  - Chat Feature (FAILED) - Real-time chat
  - Performance Analysis (COMPLETED) - DB optimization

### Workflow Details
- ✅ Completed steps list
- 📁 Files created (up to 8 files)
- 📊 Progress bar
- ❌ Error logs (for failed workflows)

### Agents Page
- 🎴 Beautiful cards for each agent
- 💼 Role descriptions
- 📈 Task completion counters

---

## 🎯 Features Available

✅ Full navigation  
✅ All pages functional  
✅ Realistic mock data  
✅ 500ms simulated API delay  
✅ No backend required  
✅ Perfect for development  

---

## 🛠️ Alternative Methods

### Using npm:
```bash
npm run start:mock
```

### Using Angular CLI:
```bash
ng serve --configuration=mock --open
```

---

## 📝 Mock Data Summary

| Type | Count | Details |
|------|-------|---------|
| **Agents** | 5 | BA, Developer, QA, DevOps, Writer |
| **Workflows** | 6 | Various types and statuses |
| **Files** | 30+ | Across all workflows |
| **Errors** | 1 | One failed workflow example |

---

## 🔧 Need Real Backend?

For production mode:

```bash
# 1. Start Python backend (from project root)
python main.py

# 2. Start frontend (in another terminal)
cd frontend-ui
npm start
```

---

## 📚 More Information

- Full guide: `MOCK_MODE.md`
- Setup instructions: `SETUP.md`
- Project documentation: `README.md`

---

## 💡 Quick Tips

1. **Check Console**: Look for 🎭 [MOCK] logs to verify mock mode
2. **Hot Reload**: Changes to code auto-reload the page
3. **Network Tab**: You'll see API calls in DevTools (F12)
4. **No Backend Needed**: Works completely offline after install

---

## 🎉 Enjoy!

The app should now be running at:

**http://localhost:4200**

Happy coding! 🚀
