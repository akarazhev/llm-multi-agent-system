# Example Programs

This directory contains ready-to-run examples demonstrating the multi-agent system's capabilities.

## Available Examples

### 1. Task Management API (`task_management_api.py`)

**Complexity:** Medium  
**Build Time:** ~10-15 minutes

**Features:**
- User authentication with JWT
- Full CRUD operations for tasks
- Real-time WebSocket notifications
- Task assignment and status tracking
- PostgreSQL database
- Docker deployment

**Run:**
```bash
source venv/bin/activate
python examples/task_management_api.py
```

**Tech Stack:**
- Backend: Python + FastAPI
- Database: PostgreSQL
- Auth: JWT
- WebSockets: FastAPI WebSocket
- Testing: pytest
- Deployment: Docker

---

### 2. E-commerce Product Catalog (`ecommerce_catalog.py`)

**Complexity:** High  
**Build Time:** ~15-20 minutes

**Features:**
- Product management with search and filters
- Shopping cart and checkout
- Stripe payment integration
- Order tracking and management
- React frontend with Tailwind CSS
- Admin dashboard
- User reviews and ratings

**Run:**
```bash
source venv/bin/activate
python examples/ecommerce_catalog.py
```

**Tech Stack:**
- Backend: Python + FastAPI
- Frontend: React + TypeScript + Tailwind CSS
- Database: PostgreSQL
- Payment: Stripe
- Caching: Redis
- Testing: pytest + React Testing Library
- Deployment: Docker + Nginx

---

### 3. Blog Platform with CMS (`blog_platform.py`)

**Complexity:** Medium  
**Build Time:** ~10-15 minutes

**Features:**
- Rich markdown editor with auto-save
- Categories, tags, and SEO optimization
- Comment system with moderation
- User roles and permissions (admin, editor, author)
- Media management
- Admin dashboard
- RSS feed and sitemap generation

**Run:**
```bash
source venv/bin/activate
python examples/blog_platform.py
```

**Tech Stack:**
- Backend: Python + FastAPI
- Frontend: React + TypeScript + Tailwind CSS
- Database: PostgreSQL
- Editor: Markdown with rich text
- SEO: Meta tags, sitemap, RSS
- Testing: pytest + React Testing Library
- Deployment: Docker + Nginx

---

## Other Examples

### Simple Workflow (`simple_workflow.py`)
Basic example showing how to execute a predefined workflow.

### Custom Workflow (`custom_workflow.py`)
Example of creating a custom workflow with specific task dependencies.

### Agent Status Monitor (`agent_status_monitor.py`)
Monitor the status of all agents in the system.

---

## How to Run

1. **Activate virtual environment:**
   ```bash
   source venv/bin/activate
   ```

2. **Choose an example:**
   ```bash
   python examples/task_management_api.py
   # or
   python examples/ecommerce_catalog.py
   # or
   python examples/blog_platform.py
   ```

3. **Wait for completion:**
   The multi-agent system will:
   - Analyze requirements (Business Analyst)
   - Design architecture (Developer)
   - Implement code (Developer)
   - Create tests (QA Engineer)
   - Set up infrastructure (DevOps Engineer)
   - Write documentation (Technical Writer)

4. **Review results:**
   - Check the `output/` directory for detailed results
   - Review generated code in your workspace
   - Check logs in `logs/agent_system.log`

---

## What Each Agent Does

### Business Analyst
- Analyzes requirements
- Creates user stories with acceptance criteria
- Identifies dependencies and risks
- Recommends Jira ticket structure

### Developer
- Designs system architecture
- Implements features following best practices
- Writes clean, production-ready code
- Includes error handling and logging

### QA Engineer
- Creates comprehensive test suites
- Writes unit, integration, and e2e tests
- Ensures 80%+ code coverage
- Documents test scenarios

### DevOps Engineer
- Creates Docker configurations
- Sets up CI/CD pipelines
- Configures deployment infrastructure
- Implements monitoring and logging

### Technical Writer
- Creates API documentation (OpenAPI/Swagger)
- Writes user guides and README files
- Documents architecture decisions
- Creates setup instructions

---

## Expected Output

After running an example, you'll find:

1. **Console Output:**
   - Real-time progress updates
   - Task completion status
   - Summary of results

2. **Generated Files:**
   - Source code in your workspace
   - Tests in `tests/` directory
   - Docker configurations
   - Documentation files

3. **Output Directory:**
   - JSON file with detailed workflow results
   - Task execution details
   - Agent outputs

4. **Logs:**
   - Detailed execution logs in `logs/agent_system.log`

---

## Tips

- **Be Patient:** Complex examples may take 15-20 minutes
- **Check Logs:** Monitor `logs/agent_system.log` for detailed progress
- **Review Output:** Always review generated code before using in production
- **Customize:** Modify the examples to fit your specific needs

---

## Troubleshooting

**If an example fails:**
1. Check `logs/agent_system.log` for detailed error messages
2. Verify llama-server is running: `curl http://127.0.0.1:8080/health`
3. Ensure virtual environment is activated
4. Check that all dependencies are installed: `pip list`
5. Verify .env file is configured with OPENAI_API_BASE

**If execution is slow:**
- This is normal for complex examples
- Each agent needs time to analyze and generate quality output
- Monitor logs to see progress

**If you want to stop:**
- Press `Ctrl+C` to interrupt
- The system will gracefully shut down
- Partial results may be available in the output directory

---

## Creating Your Own Examples

You can create custom examples by:

1. Copy an existing example file
2. Modify the `requirement` string with your specifications
3. Update the `context` dictionary with your tech stack
4. Run your custom example

Example structure:
```python
requirement = """
Your detailed requirement here...
"""

context = {
    "language": "python",
    "framework": "fastapi",
    "database": "postgresql",
    # ... other context
}

result = await workflow_engine.execute_workflow(
    workflow_type=WorkflowType.FEATURE_DEVELOPMENT,
    requirement=requirement,
    context=context
)
```

---

## Next Steps

After running an example:
1. Review the generated code
2. Run the tests: `pytest`
3. Start the application: `docker-compose up`
4. Access the API documentation
5. Customize and extend as needed

Happy building! 🚀
