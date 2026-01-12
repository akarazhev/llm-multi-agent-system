# Path Configuration Guide

The project has been refactored to use **relative paths** instead of hardcoded absolute paths, making it portable across different systems and users.

## How Paths Work

### Configuration Files

**config.yaml:**
```yaml
cursor_workspace: "."  # Current directory (project root)
```

**.env:**
```bash
CURSOR_WORKSPACE=.  # Current directory
```

### Path Resolution

The system automatically resolves relative paths to absolute paths:

1. **Relative paths** (e.g., `.`, `./output`) are resolved relative to:
   - Config file location for `config.yaml`
   - Current working directory for `.env`

2. **Absolute paths** are used as-is

3. **Dynamic resolution** happens at runtime in `src/config/settings.py`

## Usage in Code

### Test Scripts

```python
from pathlib import Path

# Get project root dynamically
PROJECT_ROOT = Path(__file__).parent.absolute()

# Use it for workspace
agent = DeveloperAgent(
    agent_id="dev_001",
    cursor_workspace=str(PROJECT_ROOT),
    config={'cursor_cli_path': 'cursor'}
)
```

### Example Scripts

```python
from src.config import load_config

# Load config (automatically resolves paths)
config = load_config()

# Use resolved workspace path
orchestrator = AgentOrchestrator(
    cursor_workspace=config.cursor_workspace,
    config=config.to_dict()
)
```

## Benefits

✅ **Portable** - Works on any system without modification  
✅ **Team-friendly** - No hardcoded user paths  
✅ **Flexible** - Can be run from any directory  
✅ **Clean** - No absolute paths in version control  

## File Locations

### Files Updated:
- `test_agent.py` - Uses `PROJECT_ROOT`
- `simple_test.py` - Uses `PROJECT_ROOT`
- `examples/custom_workflow.py` - Uses `PROJECT_ROOT`
- `config.yaml` - Uses relative path `.`
- `.env` - Uses relative path `.`
- `.env.example` - Updated with relative path
- `src/config/settings.py` - Added path resolution logic

### Files Using Config:
- `examples/simple_workflow.py` - Uses `config.cursor_workspace`
- `examples/task_management_api.py` - Uses `config.cursor_workspace`
- `examples/ecommerce_catalog.py` - Uses `config.cursor_workspace`
- `examples/blog_platform.py` - Uses `config.cursor_workspace`
- `examples/agent_status_monitor.py` - Uses `config.cursor_workspace`

## Migration Guide

If you have old absolute paths, update them:

### Before:
```python
cursor_workspace="/Users/username/project"
```

### After:
```python
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.absolute()
cursor_workspace=str(PROJECT_ROOT)
```

Or use config:
```python
from src.config import load_config
config = load_config()
cursor_workspace=config.cursor_workspace
```

## Environment Variables

The `.env` file now uses relative paths:

```bash
# Old (absolute)
CURSOR_WORKSPACE=/Users/username/Developer/project

# New (relative)
CURSOR_WORKSPACE=.
```

## Testing

Verify paths are working:

```bash
# Run from project root
python test_agent.py

# Run from any directory
cd /tmp
python /path/to/project/test_agent.py  # Still works!
```

## Troubleshooting

### Issue: "No such file or directory"
**Solution:** Ensure you're running from the project root or using absolute paths in `.env`

### Issue: Config not found
**Solution:** Set `AGENT_CONFIG_PATH` environment variable or run from project root

### Issue: Workspace path incorrect
**Solution:** Check that `.env` has `CURSOR_WORKSPACE=.` and config.yaml has `cursor_workspace: "."`

## Best Practices

1. **Always use relative paths** in config files
2. **Use `PROJECT_ROOT`** in standalone scripts
3. **Use `config.cursor_workspace`** in examples
4. **Don't commit** absolute paths to git
5. **Document** any path assumptions in README

## Summary

The project now uses a flexible path system that:
- Resolves relative paths automatically
- Works across different systems
- Maintains backward compatibility with absolute paths
- Makes the codebase more maintainable

All paths are resolved at runtime, ensuring the system works regardless of where it's installed or who is running it.
