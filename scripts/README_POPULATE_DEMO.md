# Populate Demo Projects Script

This script populates the database with demo projects based on the examples in the `examples/` directory.

## Prerequisites

1. **Database must be running and accessible**
   - Ensure PostgreSQL is running
   - Database connection configured in `.env` or `config.yaml`
   - Database schema must be initialized (run Alembic migrations)

2. **Dependencies installed**
   ```bash
   source venv/bin/activate
   pip install -r requirements.txt
   ```

## Usage

### For Podman/Docker Environment (Recommended)

If you're running the application in Podman/Docker containers:

```bash
./scripts/populate_demo_podman.sh
```

Or with a custom owner ID:

```bash
./scripts/populate_demo_podman.sh your-username
```

This script will:
1. Check if the backend container is running
2. Copy the populate script into the container
3. Execute it with the correct database configuration
4. Clean up after execution

### For Local Development

If you're running the application locally:

```bash
source venv/bin/activate
python scripts/populate_demo_projects.py
```

Or with a custom owner ID:

```bash
python scripts/populate_demo_projects.py your-username
```

## What It Does

The script creates 4 demo projects based on your examples:

1. **Task Management API** 📋
   - Status: Active
   - Type: API
   - Tech Stack: Python, FastAPI, PostgreSQL
   - Features: JWT auth, WebSockets, Docker

2. **E-commerce Product Catalog** 🛒
   - Status: Active
   - Type: Web App
   - Tech Stack: Python, React, TypeScript, PostgreSQL, Redis
   - Features: Stripe integration, Admin dashboard

3. **Blog Platform with CMS** 📝
   - Status: Completed
   - Type: Web App
   - Tech Stack: Python, React, TypeScript, PostgreSQL
   - Features: Markdown editor, SEO, Comments

4. **Interactive Chat Workflow** 💬
   - Status: Active
   - Type: Workflow
   - Tech Stack: Python, FastAPI, LangGraph
   - Features: Real-time communication, Progress tracking

## Project Data Included

Each project includes:
- ✅ Name, description, and icon
- ✅ Status and type
- ✅ Tech stack (languages, frameworks, databases, tools)
- ✅ Integrations (Git, Jira, Confluence, Slack)
- ✅ Statistics (workflows, team size, files generated, etc.)
- ✅ AI agents assigned
- ✅ Team members
- ✅ Realistic timestamps

## Verification

After running the script, you can verify the projects were created:

1. **Check the UI**: Projects should appear in the projects list
2. **Check the database**: Query the `projects` table
3. **Check logs**: The script prints success messages

## Troubleshooting

### Error: "Container 'llm_agents_backend' is not running"
**Solution**: Start the Podman containers first
```bash
./scripts/start_podman.sh
```

### Error: "ModuleNotFoundError: No module named 'sqlalchemy'"
**Solution**: 
- **For Podman**: The container should already have dependencies. Rebuild if needed:
  ```bash
  podman compose build backend
  ```
- **For Local**: Install dependencies
  ```bash
  source venv/bin/activate
  pip install -r requirements.txt
  ```

### Error: "Connection refused" or database errors
**Solution**: 
1. **For Podman**: Ensure all containers are running:
   ```bash
   podman ps
   ```
   Check that `llm_agents_postgres` and `llm_agents_backend` are running.

2. **For Local**: 
   - Ensure PostgreSQL is running
   - Check database URL in `.env` or `config.yaml`
   - Verify database schema is initialized:
     ```bash
     alembic upgrade head
     ```

### Projects already exist
The script will ask if you want to proceed. It will skip projects with duplicate names.

## Notes

- Projects are created with owner_id "demo-user" by default
- You can customize the owner_id by passing it as an argument
- Projects have realistic timestamps (created at different times)
- Last activity dates are set to show recent activity
