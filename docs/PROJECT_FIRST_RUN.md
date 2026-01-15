# First Project Guide (UI Only)

This guide shows how to create your first project entirely through the UI using the example **Inventory Tool**. It covers project creation, adding documentation links, attaching a repository reference, assigning agents, running a workflow, and reviewing communication and results.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Create the Project](#create-the-project)
- [Add Documentation Links](#add-documentation-links)
- [Attach the Repository Reference](#attach-the-repository-reference)
- [Assign Agents to the Project](#assign-agents-to-the-project)
- [Create and Run the Workflow](#create-and-run-the-workflow)
- [Watch Communication](#watch-communication)
- [Review Results](#review-results)
- [Troubleshooting](#troubleshooting)

## Prerequisites

- The UI is running and you can sign in.
- You can access **Projects** and **Workflows** in the left navigation.

If the UI is not running, follow `docs/FRONTEND_SETUP.md` and return here.

## Create the Project

Option A: Demo button (recommended for first run)

1. Open **Projects** from the left navigation.
2. Click **Create Demo Project**.
3. The app creates:
   - Inventory Tool project
   - Five demo agents
   - Inventory Tool MVP workflow
   - Demo communication messages
4. You are redirected to the workflow details page.

Option B: Manual project creation

1. Open **Projects** from the left navigation.
2. Click **New Project**.
3. Fill **Basic Information**:
   - **Project Name**: `Inventory Tool`
   - **Description**: short summary of the project (see example below)
   - **Icon**: `📦`
   - **Project Type**: `Web Application` (or `API/Backend` if backend-only)
   - **Initial Status**: `planning`
4. Click **Next**.
5. (Optional) Select tech stack:
   - Languages: `TypeScript`, `Python`
   - Frameworks: `Angular`, `FastAPI`
   - Databases: `PostgreSQL`
   - Tools: `Docker`
6. Click **Next** → **Create Project**.

Example description:

```
Inventory Tool for tracking stock, locations, and inbound/outbound operations.
```

## Add Documentation Links

Use the **Integrations** step during project creation (Option B):

1. In **Project Create → Integrations**, fill:
   - **Confluence Space URL**: `https://confluence.example.com/display/INV`
   - **Confluence Space Key**: `INV`
2. Finish the project creation flow.
3. Verify in **Project → Overview → Integrations** that Confluence is connected.

If you also keep file-based docs, include their link in the project description:

```
Files: https://drive.example.com/InventoryTool/Docs
```

## Attach the Repository Reference

Use the **Integrations** step during project creation (Option B):

1. In **Project Create → Integrations**, fill:
   - **Git Platform**: `GitHub` (or GitLab/Bitbucket)
   - **Git Repository URL**: `https://git.example.com/inventory-tool`
   - **Default Branch**: `main`
2. Finish the project creation flow.
3. Verify in **Project → Overview → Integrations** that Git is connected.

## Assign Agents to the Project

1. Open **Projects** → **Inventory Tool**.
2. Go to the **Team** tab.
3. Click **Configure Agents**.
4. Select the agents you want:
   - Business Analyst
   - Developer
   - QA Engineer
   - DevOps Engineer
   - Technical Writer
5. Save the selection.

## Create and Run the Workflow

1. Open **Workflows** in the left navigation.
2. Click **New Workflow**.
3. (Optional) choose a template such as **Feature Development**.
4. Fill **Workflow Details**:
   - **Workflow Name**: `Inventory Tool MVP`
   - **Description**: `Initial MVP for inventory tracking`
   - **Requirement**: use the sample below
   - **Workflow Type**: `Feature Development`
   - **Priority**: `Medium`
5. Click **Next**.
6. In **Configuration**:
   - **Assign to Project**: select `Inventory Tool`
   - **Assign Agents**: pick the same agents as in the project
   - **Tags**: `inventory, mvp, web`
7. Click **Create Workflow**.

Sample requirement (paste into **Requirement**):

```
Goal: Build an Inventory Tool MVP.

Documentation:
- Confluence: https://confluence.example.com/display/INV/Inventory+Tool
- Files: https://drive.example.com/InventoryTool/Docs

Repository:
- Git: https://git.example.com/inventory-tool (main)

Scope:
- Item catalog with SKU, name, category, and status.
- Stock levels by location.
- Simple inbound/outbound adjustments.
- Basic audit log for changes.

Deliverables:
- API endpoints (CRUD + adjustments).
- DB schema and migrations.
- Minimal UI for listing items and stock.
- Tests for critical flows.
```

## Watch Communication

1. Open the workflow from the **Workflows** list.
2. Go to the **Communication** tab.
3. Use **Chat View** for real-time messages.
4. Use **Threads** to follow decisions and Q&A.

## Review Results

1. In the workflow view, check:
   - **Steps** tab for progress and outputs.
   - **Artifacts** tab for generated files.
   - **Metrics** tab for duration and counts.
2. Click any artifact to review its content or path.

## Troubleshooting

- If communication is empty, wait for the workflow to start or click **Refresh**.
- If you do not see agents in the list, create agents first or refresh the page.
- If the workflow is not linked to a project, edit the workflow by creating a new one with the correct project assignment.

