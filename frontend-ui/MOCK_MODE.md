# 🎭 Mock Mode - Quick Start Guide

## Overview

Mock mode allows you to run and test the UI **without a backend**. All API calls are intercepted and return realistic mock data.

Perfect for:
- ✅ Frontend development
- ✅ UI/UX testing
- ✅ Demos and presentations
- ✅ Quick prototyping

---

## 🚀 Quick Start

### Option 1: Using the Script (Recommended)

```bash
./start-mock.sh
```

This will:
1. Check and install dependencies if needed
2. Start dev server on port 4200
3. Auto-open browser with mock data
4. Show colorful startup info

### Option 2: Using npm

```bash
npm run start:mock
```

### Option 3: Manual

```bash
ng serve --configuration=mock --port 4200 --open
```

---

## 📊 Mock Data Available

### Agents (5)

| Agent | Role | Status | Completed Tasks |
|-------|------|--------|----------------|
| ba_001 | Business Analyst | IDLE | 15 |
| dev_001 | Developer | WORKING | 28 |
| qa_001 | QA Engineer | COMPLETED | 22 |
| devops_001 | DevOps Engineer | WORKING | 19 |
| writer_001 | Technical Writer | IDLE | 12 |

### Workflows (6)

1. **Feature Development** (RUNNING)
   - JWT Authentication API
   - 30 minutes in progress
   - 2 steps completed
   - 8 files created

2. **Bug Fix** (COMPLETED)
   - WebSocket memory leak fix
   - Completed 45 min ago
   - 4 steps completed
   - 3 files created

3. **Infrastructure** (COMPLETED)
   - Kubernetes cluster setup
   - Completed 3 hours ago
   - 4 steps completed
   - 8 files created

4. **Documentation** (COMPLETED)
   - API documentation
   - Completed yesterday
   - 3 steps completed
   - 4 files created

5. **Chat Feature** (FAILED)
   - Real-time chat implementation
   - Failed during QA testing
   - Error: WebSocket timeout

6. **Performance Analysis** (COMPLETED)
   - Database optimization study
   - Completed 28 hours ago
   - 4 steps completed

---

## 🎯 What's Mocked?

### API Endpoints

All these endpoints return realistic data:

```
✅ GET  /api/agents
✅ GET  /api/agents/{id}
✅ GET  /api/workflows
✅ GET  /api/workflows/{id}
✅ POST /api/workflows
✅ POST /api/workflows/{id}/cancel
✅ POST /api/workflows/{id}/resume
```

### Features That Work

- ✅ Dashboard with stats
- ✅ View all agents
- ✅ View all workflows
- ✅ View workflow details
- ✅ See progress bars
- ✅ View created files
- ✅ See error logs
- ✅ All navigation
- ✅ Responsive design

### Features Not Available in Mock

- ❌ Creating real workflows
- ❌ Actual workflow execution
- ❌ WebSocket real-time updates
- ❌ File downloads
- ❌ Authentication

---

## 🔧 How It Works

### Architecture

```
Browser Request
     │
     ▼
HTTP Interceptor
     │
     ├─ matches /api/agents? ───┐
     ├─ matches /api/workflows? ─┤
     └─ other? ─────────────────┘
                                 │
                                 ▼
                          Return Mock Data
                          (with 500ms delay)
```

### Key Files

```
frontend-ui/
├── src/
│   ├── app/
│   │   └── mocks/
│   │       ├── mock-data.ts        # 📊 All mock data
│   │       └── mock.interceptor.ts # 🎭 HTTP interceptor
│   ├── main.mock.ts                # 🚀 Mock bootstrap
│   └── environments/
│       └── environment.mock.ts     # ⚙️ Mock config
├── start-mock.sh                   # 🎬 Startup script
└── MOCK_MODE.md                    # 📖 This file
```

### Mock Data Details

**Agents** (`mock-data.ts`):
- 5 agents with realistic IDs
- Different statuses (IDLE, WORKING, COMPLETED)
- Task counts (12-28 tasks)
- Current tasks for active agents

**Workflows** (`mock-data.ts`):
- 6 workflows spanning 24+ hours
- All workflow types represented
- Various statuses (RUNNING, COMPLETED, FAILED)
- Realistic file paths
- Error examples

**Interceptor** (`mock.interceptor.ts`):
- Catches all `/api/*` requests
- Returns appropriate mock data
- Simulates 500ms network delay
- Logs all intercepted calls with 🎭 prefix

---

## 🎨 Customizing Mock Data

### Add More Workflows

Edit `src/app/mocks/mock-data.ts`:

```typescript
export const MOCK_WORKFLOWS: Workflow[] = [
  // ... existing workflows
  {
    workflow_id: 'workflow_custom_001',
    workflow_type: WorkflowType.FEATURE_DEVELOPMENT,
    requirement: 'Your custom workflow',
    status: WorkflowStatus.RUNNING,
    // ... more fields
  }
];
```

### Change Agent Statuses

```typescript
export const MOCK_AGENTS: Agent[] = [
  {
    agent_id: 'ba_001',
    role: AgentRole.BUSINESS_ANALYST,
    status: AgentStatus.WORKING, // Change here
    completed_tasks: 99,          // Change here
  }
];
```

### Adjust Network Delay

In `mock.interceptor.ts`:

```typescript
const MOCK_DELAY = 1000; // Change from 500ms to 1000ms
```

### Add More Endpoints

In `mock.interceptor.ts`:

```typescript
// Add your custom endpoint
if (url.includes('/api/custom') && req.method === 'GET') {
  return of(new HttpResponse({
    status: 200,
    body: { your: 'data' }
  })).pipe(delay(MOCK_DELAY));
}
```

---

## 🐛 Debugging

### Enable Verbose Logging

All mock requests are logged with 🎭 prefix:

```
🎭 [MOCK] GET /api/agents
🎭 [MOCK] GET /api/workflows
🎭 [MOCK] GET /api/workflows/workflow_123
```

Check browser console (F12) for these logs.

### Disable Mock Mode

Just use regular start:

```bash
npm start
# or
ng serve
```

This will use real API endpoints from `environment.ts`.

---

## 📱 Testing Checklist

Use this to test all features in mock mode:

### Dashboard
- [ ] Stats cards show correct numbers
- [ ] Agents list displays all 5 agents
- [ ] Agent statuses show colors
- [ ] Recent workflows show 5 items
- [ ] Refresh button works
- [ ] Links navigate correctly

### Workflows Page
- [ ] Table shows all 6 workflows
- [ ] Status chips are colored correctly
- [ ] Can click on workflow to view details
- [ ] Empty state (delete mock data to test)
- [ ] Action buttons visible

### Workflow Detail
- [ ] Progress bar shows correctly
- [ ] Workflow info displays
- [ ] Completed steps list shows
- [ ] Files created list shows
- [ ] Errors display (check FAILED workflow)
- [ ] Back button works

### Agents Page
- [ ] All 5 agents display as cards
- [ ] Icons match roles
- [ ] Status chips colored
- [ ] Task counts show
- [ ] Responsive grid works

### Navigation
- [ ] Sidenav links work
- [ ] Active route highlights
- [ ] All routes load correctly

---

## 🎯 Performance

Mock mode is optimized for development:

- **Initial load**: ~2-3 seconds
- **API response**: 500ms (simulated)
- **Navigation**: Instant
- **No backend**: 100% frontend

---

## 🔄 Switching Between Modes

### Development (Real Backend)
```bash
npm start
# Uses environment.ts
# Connects to http://localhost:8000
```

### Mock (No Backend)
```bash
npm run start:mock
# or ./start-mock.sh
# Uses mock.interceptor.ts
# No backend needed
```

### Production
```bash
npm run build:prod
# Builds for production
# Uses environment.prod.ts
```

---

## 💡 Tips & Tricks

1. **Quick Demo**: Use mock mode for presentations - no setup required!

2. **Parallel Development**: Frontend devs can work without waiting for backend

3. **Testing Edge Cases**: Easily test error states, empty states, loading states

4. **Screenshot/Video**: Perfect for documentation and tutorials

5. **UI/UX Iteration**: Fast feedback loop for design changes

---

## 🚨 Common Issues

### Port Already in Use

If port 4200 is busy:

```bash
ng serve --configuration=mock --port 4300
```

### Interceptor Not Working

Check if `app.config.mock.ts` is being used:

```typescript
// Should include mockInterceptor
withInterceptors([mockInterceptor])
```

### Mock Data Not Showing

1. Check browser console for 🎭 logs
2. Verify you're using `start:mock` script
3. Clear cache: Ctrl+Shift+R (hard reload)

### Wrong Environment

Make sure `environment.mock.ts` is loaded:

```typescript
// In main.mock.ts
import { environment } from './environments/environment.mock';
console.log('Mock mode:', environment.mock); // Should be true
```

---

## 📚 Learn More

- **Mock Data**: `src/app/mocks/mock-data.ts`
- **Interceptor**: `src/app/mocks/mock.interceptor.ts`
- **Interfaces**: `src/app/core/interfaces/`
- **Components**: `src/app/pages/`

---

## 🎉 Ready to Go!

Start mock mode now:

```bash
./start-mock.sh
```

Browser will open at: `http://localhost:4200`

**Happy testing! 🚀**
