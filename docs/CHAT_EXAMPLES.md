# Interactive Chat Examples

Visual examples showing exactly what the interactive chat display looks like in action.

## Table of Contents

- [Basic Workflow Flow](#basic-workflow-flow)
- [Feature Development Example](#feature-development-example)
- [Bug Fix Workflow](#bug-fix-workflow)
- [Error Handling](#error-handling)
- [Progress Tracking](#progress-tracking)

---

## Basic Workflow Flow

### Starting a Workflow

```
================================================================================
               Multi-Agent Feature Development Workflow
================================================================================

🚀 System: Starting workflow: workflow_20260113_120000

🤔 Business Analyst:
  Starting requirements analysis...
  
  Requirement: Create a task management API with user authentication

⚙️ Business Analyst is analyzing requirements and creating user stories
  Identifying stakeholders, use cases, and acceptance criteria
```

### Agent Completion

```
✅ Business Analyst completed task
  Requirements analysis complete. Identified 8 user stories and 24 acceptance criteria.
  📄 Files created: 2
    • requirements.md
    • user_stories.md
```

### Inter-Agent Handoff

```
🔄 Business Analyst → Developer
  Handoff: Requirements and user stories are ready for architecture design
```

### Next Agent Starts

```
🤔 Developer:
  Reviewing requirements and designing system architecture...
  Planning components, services, and data models.

⚙️ Developer is designing system architecture
  Creating architecture diagrams, API specifications, and data models
```

---

## Feature Development Example

### Complete Workflow Output

```
================================================================================
               Multi-Agent Feature Development Workflow
================================================================================

🚀 System: Starting workflow: workflow_20260113_120000

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Business Analyst Phase
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🤔 Business Analyst:
  Analyzing requirements for task management API...
  
  Requirements:
  - User authentication with JWT
  - CRUD operations for tasks
  - Task assignment to users
  - Task status tracking
  - Due date management

⚙️ Business Analyst is creating user stories and requirements documentation
  Identifying 8 user stories and 24 acceptance criteria

✅ Business Analyst completed task
  Requirements analysis complete. Identified 8 user stories, 24 acceptance 
  criteria, and 3 data models.
  📄 Files created: 3
    • requirements.md
    • user_stories.md
    • data_models.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Architecture Design Phase
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔄 Business Analyst → Developer
  Handoff: Requirements and user stories are ready for architecture design

🤔 Developer:
  Reviewing requirements and designing system architecture...
  Planning components, services, and data models.

⚙️ Developer is designing system architecture
  Creating architecture diagrams, API specifications, and data models

✅ Developer completed task
  Architecture design complete. Defined 12 API endpoints, 5 database tables, 
  and JWT authentication flow.
  📄 Files created: 4
    • architecture/system_design.md
    • architecture/database_schema.sql
    • architecture/api_endpoints.yaml
    • architecture/auth_flow.md

ℹ️  Workflow Status
  ID: workflow_20260113_120000
  Status: running
  Current Step: architecture_design
  Progress: 2 steps completed
  ████████████░░░░░░░░░░░░░░░░░░░░░░░░░░ 33%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Implementation Phase
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🤔 Developer:
  Starting implementation based on architecture design...
  Writing code, creating modules, and setting up project structure.

⚙️ Developer is implementing the feature
  Writing source code, configuration files, and setting up dependencies

✅ Developer completed task
  Implementation complete. Created FastAPI endpoints, SQLAlchemy models, 
  JWT authentication, and Pydantic schemas.
  📄 Files created: 12
    • src/main.py
    • src/api/auth.py
    • src/api/tasks.py
    • src/models/user.py
    • src/models/task.py
    ... and 7 more

ℹ️  Workflow Status
  ID: workflow_20260113_120000
  Status: running
  Current Step: implementation
  Progress: 3 steps completed
  ████████████████████░░░░░░░░░░░░░░░░░░ 50%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Parallel Execution: QA + DevOps
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ℹ️  System: Implementation complete. Starting parallel QA and DevOps tasks...

🔄 Developer → QA Engineer
  Handoff: Implementation complete. Ready for testing and quality assurance.

🔄 Developer → DevOps Engineer
  Handoff: Implementation complete. Ready for deployment infrastructure setup.

🤔 QA Engineer:
  Reviewing implementation and creating test suite...
  Planning unit tests, integration tests, and end-to-end tests.

🤔 DevOps Engineer:
  Setting up deployment infrastructure...
  Configuring CI/CD pipelines, containers, and cloud resources.

⚙️ QA Engineer is creating comprehensive test suite
  Writing test cases, test fixtures, and test automation scripts

⚙️ DevOps Engineer is setting up deployment infrastructure
  Creating Docker containers, Kubernetes configs, and CI/CD pipelines

✅ QA Engineer completed task
  Test suite complete. Created 45 unit tests, 15 integration tests, and 
  12 API endpoint tests. Code coverage: 94%.
  📄 Files created: 8
    • tests/test_auth.py
    • tests/test_tasks.py
    • tests/test_api_endpoints.py
    • tests/test_integration.py
    ... and 4 more

✅ DevOps Engineer completed task
  Infrastructure setup complete. Docker containerization, Kubernetes 
  deployment configs, and CI/CD pipeline configured.
  📄 Files created: 6
    • Dockerfile
    • docker-compose.yml
    • kubernetes/deployment.yaml
    • .github/workflows/ci.yml
    ... and 2 more

ℹ️  Workflow Status
  ID: workflow_20260113_120000
  Status: running
  Current Step: qa_testing
  Progress: 5 steps completed
  ████████████████████████████░░░░░░░░░░ 83%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Documentation Phase
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ℹ️  System: QA and DevOps completed in parallel. Moving to documentation...

🔄 System → Technical Writer
  Handoff: All development, testing, and infrastructure work completed. 
  Ready for documentation.

🤔 Technical Writer:
  Creating comprehensive documentation...
  Writing API docs, user guides, and deployment instructions.

⚙️ Technical Writer is creating comprehensive documentation
  Writing README, API documentation, and user guides

✅ Technical Writer completed task
  Documentation complete. Created README, API documentation, deployment guide, 
  and user manual.
  📄 Files created: 5
    • README.md
    • docs/API_REFERENCE.md
    • docs/DEPLOYMENT_GUIDE.md
    • docs/USER_MANUAL.md
    • docs/QUICK_START.md

✨ System: Workflow completed successfully! All agents have finished their tasks.

ℹ️  Workflow Status
  ID: workflow_20260113_120000
  Status: completed
  Current Step: documentation
  Progress: 6 steps completed
  ████████████████████████████████████████ 100%

════════════════════════════════════════
  Conversation Summary
════════════════════════════════════════

Total messages: 24

Messages per agent:
  Developer: 8
  Business Analyst: 6
  QA Engineer: 5
  DevOps Engineer: 3
  Technical Writer: 2

📄 Chat log saved to: output/chat_log_workflow_20260113_120000.json

================================================================================
📊 WORKFLOW SUMMARY
================================================================================

✓ Workflow ID: workflow_20260113_120000
✓ Status: COMPLETED
✓ Completed Steps: 6
✓ Files Created: 38

📄 Files Created:
   1. requirements.md
   2. user_stories.md
   3. data_models.md
   4. architecture/system_design.md
   5. architecture/database_schema.sql
   6. src/main.py
   7. src/api/auth.py
   8. tests/test_auth.py
   9. Dockerfile
   10. README.md
   ... and 28 more files

📁 Results saved to:
   - Workflow data: output/langgraph_workflow_20260113_120000.json
   - Chat log: output/chat_log_workflow_20260113_120000.json

================================================================================
✨ Workflow completed! Check the output directory for all generated files.
================================================================================
```

---

## Bug Fix Workflow

### Bug Analysis Phase

```
🤔 QA Engineer:
  Analyzing bug report...
  
  Bug: User authentication fails with 401 error on valid credentials
  Steps to reproduce identified.

⚙️ QA Engineer is analyzing and reproducing the bug
  Creating test case to reproduce the issue

✅ QA Engineer completed task
  Bug analysis complete. Issue identified in JWT token validation logic.
  📄 Files created: 2
    • bug_reports/bug_analysis_001.md
    • tests/test_bug_reproduction.py

🔄 QA Engineer → Developer
  Bug analysis complete. Root cause identified. Ready for fix implementation.
```

### Bug Fix Implementation

```
🤔 Developer:
  Reviewing bug analysis and planning fix...
  Issue: JWT token expiration check has off-by-one error.

⚙️ Developer is fixing the bug
  Updating JWT validation logic and adding edge case handling

✅ Developer completed task
  Bug fix complete. Updated JWT validation and added expiration buffer.
  📄 Files created: 3
    • src/auth/jwt_validator.py (updated)
    • tests/test_jwt_edge_cases.py
    • CHANGELOG.md (updated)
```

---

## Error Handling

### Agent Error Example

```
⚙️ Developer is implementing database migrations
  Creating SQLAlchemy migration scripts

❌ Developer encountered an error
  Database connection failed: Connection timeout after 30 seconds
  
  Error details:
  - Database: postgresql://localhost:5432/taskdb
  - Timeout: 30s
  - Suggestion: Check if PostgreSQL service is running

ℹ️  Workflow Status
  ID: workflow_20260113_120000
  Status: failed
  Current Step: implementation
  Errors: 1
```

### Recovery Message

```
ℹ️  System: Retrying after error...

🤔 Developer:
  Checking database connection before retry...
  Database service confirmed running. Retrying connection.

✅ Developer completed task
  Database migrations completed successfully on retry.
```

---

## Progress Tracking

### Progress at Different Stages

**20% Complete:**
```
Progress: ████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 20%
Current: requirements_analysis

ℹ️  Workflow Status
  ID: workflow_20260113_120000
  Status: running
  Current Step: requirements_analysis
  Progress: 1 steps completed
  ████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 17%
```

**50% Complete:**
```
Progress: ████████████████████░░░░░░░░░░░░░░░░ 50%
Current: implementation

ℹ️  Workflow Status
  ID: workflow_20260113_120000
  Status: running
  Current Step: implementation
  Progress: 3 steps completed
  ████████████████████░░░░░░░░░░░░░░░░░░ 50%
```

**83% Complete:**
```
Progress: █████████████████████████████████░░░ 83%
Current: testing

ℹ️  Workflow Status
  ID: workflow_20260113_120000
  Status: running
  Current Step: testing
  Progress: 5 steps completed
  ████████████████████████████░░░░░░░░░░ 83%
```

**100% Complete:**
```
Progress: ████████████████████████████████████ 100%
Current: documentation

✨ System: Workflow completed successfully!

ℹ️  Workflow Status
  ID: workflow_20260113_120000
  Status: completed
  Current Step: documentation
  Progress: 6 steps completed
  ████████████████████████████████████████ 100%
```

---

## File Operation Examples

### Single File Creation

```
✅ Developer created: src/api/tasks.py
```

### Multiple Files

```
✅ Developer completed task
  Implementation phase complete
  📄 Files created: 8
    • src/main.py
    • src/api/auth.py
    • src/api/tasks.py
    • src/models/user.py
    • src/models/task.py
    • src/schemas/task.py
    • src/schemas/user.py
    • src/database.py
```

### Many Files (Truncated)

```
✅ Technical Writer completed task
  Complete documentation suite created
  📄 Files created: 15
    • README.md
    • docs/QUICK_START.md
    • docs/API_REFERENCE.md
    • docs/ARCHITECTURE.md
    • docs/DEPLOYMENT.md
    ... and 10 more
```

---

## System Messages

### Workflow Start

```
🚀 System: Starting workflow: workflow_20260113_120000
```

### Phase Transition

```
ℹ️  System: QA and DevOps completed in parallel. Moving to documentation...
```

### Workflow Complete

```
✨ System: Workflow completed successfully! All agents have finished their tasks.
```

### Error State

```
⚠️  System: Implementation failed. Workflow paused.
```

---

## Custom Workflows

### Analysis Workflow

```
🤔 Business Analyst:
  Conducting feasibility analysis...
  Evaluating technical requirements and constraints.

⚙️ Business Analyst is analyzing technical feasibility
  Assessing resource requirements, timeline, and risks

✅ Business Analyst completed task
  Feasibility analysis complete. Project estimated at 6 weeks with 3 developers.
  📄 Files created: 2
    • analysis/feasibility_report.md
    • analysis/resource_plan.md
```

---

## Tips for Reading Chat Output

### Color Legend (as displayed in terminal)

- **Cyan text** = Business Analyst
- **Green text** = Developer
- **Yellow text** = QA Engineer
- **Magenta text** = DevOps Engineer
- **Blue text** = Technical Writer
- **White text** = System messages

### Icon Quick Reference

- 🚀 = Starting
- 🤔 = Thinking/Planning
- ⚙️ = Working
- ✅ = Success
- ❌ = Error
- 🔄 = Handoff
- ℹ️ = Status
- 📄 = Files
- 📊 = Progress

### Reading Workflow Status

```
ℹ️  Workflow Status
  ID: workflow_20260113_120000      ← Unique workflow identifier
  Status: running                    ← Current state (running/completed/failed)
  Current Step: implementation       ← What's happening now
  Progress: 3 steps completed        ← How many steps done
  ████████████████░░░░░░░░░░░░       ← Visual progress bar
```

---

## Next Steps

- **Try the demo**: `python examples/interactive_chat_workflow.py`
- **Read the guide**: [INTERACTIVE_CHAT.md](INTERACTIVE_CHAT.md)
- **Quick reference**: [CHAT_QUICK_REFERENCE.md](CHAT_QUICK_REFERENCE.md)

---

These examples show the actual format and style of the interactive chat display. When you run workflows, you'll see output similar to these examples, color-coded and formatted for easy reading in your terminal.
