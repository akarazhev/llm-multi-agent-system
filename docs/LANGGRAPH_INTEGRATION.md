# LangGraph Integration Guide

## Overview

This multi-agent system now supports **LangGraph** for advanced workflow orchestration. LangGraph provides state persistence, parallel execution, conditional routing, and human-in-the-loop capabilities.

## Table of Contents

- [Why LangGraph?](#why-langgraph)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Features](#features)
- [Architecture](#architecture)
- [Usage Examples](#usage-examples)
- [Advanced Features](#advanced-features)
- [Migration Guide](#migration-guide)
- [API Reference](#api-reference)

## Why LangGraph?

### Before (Custom Orchestration)
- ❌ Sequential execution only
- ❌ No state persistence
- ❌ Manual dependency management
- ❌ Limited error recovery
- ❌ Difficult to visualize

### After (LangGraph)
- ✅ **Parallel execution** - QA and DevOps run simultaneously
- ✅ **State persistence** - Resume workflows after interruption
- ✅ **Automatic dependency resolution** - Handled by the graph
- ✅ **Conditional routing** - Smart error handling and branching
- ✅ **Workflow visualization** - See your workflows as diagrams
- ✅ **Time-travel debugging** - Inspect any point in workflow history
- ✅ **Human-in-the-loop** - Pause for approvals when needed

## Installation

### 1. Update Dependencies

```bash
pip install -r requirements.txt
```

New dependencies added:
- `langgraph>=0.2.0` - Graph-based workflow orchestration
- `langchain-core>=0.3.0` - Core LangChain primitives
- `aiosqlite>=0.19.0` - Async SQLite for checkpointing

### 2. Verify Installation

```bash
python -c "import langgraph; print('✓ LangGraph installed:', langgraph.__version__)"
```

## Quick Start

### Basic Usage

```python
import asyncio
from src.orchestrator.langgraph_orchestrator import LangGraphOrchestrator

async def main():
    # Create orchestrator
    orchestrator = LangGraphOrchestrator(
        cursor_workspace=".",
        config={"agents": {}}
    )
    
    # Execute workflow
    result = await orchestrator.execute_feature_development(
        requirement="Create a REST API for user management",
        context={
            "language": "python",
            "framework": "fastapi"
        }
    )
    
    print(f"Workflow completed: {result}")

asyncio.run(main())
```

### Run Example Scripts

```bash
# Feature development with parallel execution
python examples/langgraph_feature_development.py

# Bug fix workflow
python examples/langgraph_bug_fix.py

# Resume interrupted workflow
python examples/langgraph_resume_workflow.py

# Visualize workflow structure
python examples/visualize_workflow.py
```

## Features

### 1. Parallel Execution

**Before:** Tasks executed sequentially
```
Business Analyst → Developer → Developer → QA → DevOps → Writer
Total time: ~15-20 minutes
```

**After:** Parallel tasks reduce execution time
```
Business Analyst → Developer → Developer → [QA + DevOps] → Writer
                                              ↓        ↓
                                           PARALLEL EXECUTION
Total time: ~10-15 minutes (30-40% faster)
```

**Implementation:**
```python
# In the workflow graph
workflow.add_conditional_edges(
    "implementation",
    should_continue_after_implementation,
    {
        "continue": ["qa_testing", "infrastructure"],  # PARALLEL!
        "failed": END
    }
)
```

### 2. State Persistence

Workflows are automatically saved to SQLite checkpoints. If interrupted, resume from the last checkpoint:

```python
# Start workflow
result = await orchestrator.execute_feature_development(
    requirement="Build API",
    thread_id="my_workflow_001"
)

# [Process interrupted with Ctrl+C]

# Resume later with same thread_id
result = await orchestrator.execute_feature_development(
    requirement="Build API",  # Can be anything, state is restored
    thread_id="my_workflow_001"  # Same ID resumes from checkpoint
)
```

**Checkpoint Location:**
- Default: `./checkpoints.db`
- Custom: Pass `checkpoint_db` parameter to orchestrator

### 3. Conditional Routing

Smart decision making based on agent outputs:

```python
def should_continue_after_implementation(state):
    """Route based on implementation success"""
    if state.get("errors"):
        return "failed"  # Stop workflow
    
    if state["implementation"]["complexity"] == "high":
        return "review"  # Extra review step
    
    return "continue"  # Proceed with testing

# Add to graph
workflow.add_conditional_edges(
    "implementation",
    should_continue_after_implementation,
    {
        "continue": ["qa_testing", "infrastructure"],
        "review": "architecture_review",
        "failed": END
    }
)
```

### 4. Workflow Visualization

```python
# Generate Mermaid diagram
app = await orchestrator.build_feature_development_graph()
mermaid_code = app.get_graph().draw_mermaid()

print(mermaid_code)
# Copy to https://mermaid.live/ to visualize
```

**Generated Diagram:**
```mermaid
graph TD
    Start --> business_analyst
    business_analyst --> architecture_design
    architecture_design --> implementation
    implementation --> should_continue_after_implementation
    should_continue_after_implementation -->|continue| qa_testing
    should_continue_after_implementation -->|continue| infrastructure
    should_continue_after_implementation -->|failed| End
    qa_testing --> documentation
    infrastructure --> documentation
    documentation --> End
```

### 5. Time-Travel Debugging

Inspect any point in workflow history:

```python
app = await orchestrator.build_feature_development_graph()
config = {"configurable": {"thread_id": "workflow_123"}}

# Get all checkpoints
checkpoints = []
async for checkpoint in app.aget_state_history(config):
    checkpoints.append(checkpoint)
    print(f"Step: {checkpoint.values['current_step']}")
    print(f"Files: {checkpoint.values['files_created']}")

# Replay from specific checkpoint
state_at_step_3 = checkpoints[3]
result = await app.ainvoke(None, config={
    "configurable": {"thread_id": state_at_step_3.config["configurable"]["thread_id"]}
})
```

## Architecture

### State Management

```python
# MultiAgentState structure
{
    "requirement": "User's requirement",
    "workflow_type": "feature_development",
    "workflow_id": "workflow_20240115_143022",
    
    # Agent outputs (lists that auto-merge)
    "business_analysis": [result1],
    "architecture": [result1],
    "implementation": [result1],
    "tests": [result1],
    "infrastructure": [result1],
    "documentation": [result1],
    
    # Metadata
    "errors": [],
    "files_created": ["path/to/file1.py", "path/to/file2.py"],
    "current_step": "documentation",
    "completed_steps": ["business_analyst", "architecture_design", ...],
    "status": "completed",
    "started_at": "2024-01-15T14:30:22",
    "completed_at": "2024-01-15T14:45:10"
}
```

### Workflow Graph Structure

```
┌─────────────────────┐
│  Business Analyst   │
│  (Requirements)     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Developer          │
│  (Architecture)     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Developer          │
│  (Implementation)   │
└──────────┬──────────┘
           │
           ▼
    ┌──────┴──────┐
    │ Conditional │
    │   Routing   │
    └──────┬──────┘
           │
   ┌───────┴───────┐
   │               │
   ▼               ▼
┌──────────────┐  ┌──────────────┐
│ QA Engineer  │  │ DevOps Eng.  │
│  (Testing)   │  │ (Infra)      │
└──────┬───────┘  └──────┬───────┘
   │                 │
   └────────┬────────┘
            ▼
┌─────────────────────┐
│ Technical Writer    │
│  (Documentation)    │
└─────────────────────┘
```

## Usage Examples

### Example 1: Feature Development

```python
from src.orchestrator.langgraph_orchestrator import LangGraphOrchestrator

orchestrator = LangGraphOrchestrator(cursor_workspace=".")

result = await orchestrator.execute_feature_development(
    requirement="""
    Create a REST API for product catalog:
    - CRUD operations
    - Search and filtering
    - Category management
    """,
    context={
        "language": "python",
        "framework": "fastapi",
        "database": "postgresql"
    }
)

print(f"Status: {result['status']}")
print(f"Files created: {len(result['files_created'])}")
```

### Example 2: Bug Fix

```python
result = await orchestrator.execute_bug_fix(
    requirement="Fix authentication token expiration",
    bug_description="""
    Tokens not expiring correctly.
    Expected: Expire after 1 hour
    Actual: Remain valid indefinitely
    """
)
```

### Example 3: Resume Interrupted Workflow

```python
# Start workflow
try:
    result = await orchestrator.execute_feature_development(
        requirement="Build API",
        thread_id="api_build_001"
    )
except KeyboardInterrupt:
    print("Interrupted! State saved to checkpoint.")

# Resume later
result = await orchestrator.execute_feature_development(
    requirement="",  # Ignored, state restored
    thread_id="api_build_001"  # Same ID = resume
)
```

### Example 4: Monitor Progress

```python
app = await orchestrator.build_feature_development_graph()
config = {"configurable": {"thread_id": "workflow_123"}}

# Stream events for real-time progress
async for event in app.astream(initial_state, config):
    for node_name, node_state in event.items():
        print(f"✓ Completed: {node_name}")
        print(f"  Step: {node_state.get('current_step')}")
        print(f"  Files: {len(node_state.get('files_created', []))}")
```

## Advanced Features

### Human-in-the-Loop

Add approval steps to workflows:

```python
async def human_approval_node(state: MultiAgentState) -> Dict[str, Any]:
    """Pause for human approval"""
    print("\n" + "="*70)
    print("APPROVAL REQUIRED")
    print("="*70)
    print(f"\nArchitecture design complete.")
    print(f"Review the design before proceeding to implementation.")
    print("\nFiles created:")
    for file in state.get("files_created", []):
        print(f"  - {file}")
    
    approved = input("\nApprove? (yes/no): ").strip().lower() == "yes"
    
    return {
        "approved": approved,
        "requires_approval": False,
        "current_step": "human_approval"
    }

# Add to workflow
workflow.add_node("human_approval", human_approval_node)
workflow.add_edge("architecture_design", "human_approval")

workflow.add_conditional_edges(
    "human_approval",
    lambda s: "continue" if s.get("approved") else "rejected",
    {
        "continue": "implementation",
        "rejected": "architecture_design"  # Loop back for revision
    }
)
```

### Custom Workflows

Create your own workflow graphs:

```python
async def build_custom_workflow(self) -> Any:
    """Custom workflow: Analysis → Multiple Parallel Tasks → Synthesis"""
    
    async with AsyncSqliteSaver.from_conn_string(self.checkpoint_db) as checkpointer:
        workflow = StateGraph(MultiAgentState)
        
        # Initial analysis
        workflow.add_node("analysis", self.business_analyst_node)
        
        # Parallel investigation
        workflow.add_node("technical_analysis", self.developer_design_node)
        workflow.add_node("qa_analysis", self.qa_engineer_node)
        workflow.add_node("infra_analysis", self.devops_engineer_node)
        
        # Synthesis
        workflow.add_node("synthesis", self.technical_writer_node)
        
        # Build graph
        workflow.set_entry_point("analysis")
        
        # Fan-out to parallel nodes
        workflow.add_edge("analysis", "technical_analysis")
        workflow.add_edge("analysis", "qa_analysis")
        workflow.add_edge("analysis", "infra_analysis")
        
        # Fan-in to synthesis (waits for all)
        workflow.add_edge("technical_analysis", "synthesis")
        workflow.add_edge("qa_analysis", "synthesis")
        workflow.add_edge("infra_analysis", "synthesis")
        workflow.add_edge("synthesis", END)
        
        return workflow.compile(checkpointer=checkpointer)
```

### Error Recovery

Implement retry logic with exponential backoff:

```python
async def resilient_node(state: MultiAgentState) -> Dict[str, Any]:
    """Node with automatic retry"""
    max_retries = 3
    retry_count = state.get("retry_count", 0)
    
    try:
        # Execute task
        result = await execute_agent_task(state)
        return result
        
    except Exception as e:
        if retry_count < max_retries:
            delay = 2 ** retry_count  # Exponential backoff
            await asyncio.sleep(delay)
            
            return {
                "retry_count": retry_count + 1,
                "errors": [{
                    "step": "implementation",
                    "error": f"Retry {retry_count + 1}/{max_retries}: {str(e)}",
                    "timestamp": datetime.now().isoformat()
                }]
            }
        else:
            # Max retries exceeded
            return {
                "status": "failed",
                "errors": [{
                    "step": "implementation",
                    "error": f"Failed after {max_retries} retries: {str(e)}",
                    "timestamp": datetime.now().isoformat()
                }]
            }
```

## Migration Guide

### From Custom Orchestration to LangGraph

**Before (custom orchestration):**
```python
from src.orchestrator import AgentOrchestrator, WorkflowEngine

orchestrator = AgentOrchestrator(cursor_workspace=".")
workflow_engine = WorkflowEngine(orchestrator)

result = await workflow_engine.execute_workflow(
    workflow_type=WorkflowType.FEATURE_DEVELOPMENT,
    requirement="Build API",
    context={"language": "python"}
)
```

**After (LangGraph):**
```python
from src.orchestrator.langgraph_orchestrator import LangGraphOrchestrator

orchestrator = LangGraphOrchestrator(cursor_workspace=".")

result = await orchestrator.execute_feature_development(
    requirement="Build API",
    context={"language": "python"}
)
```

### Key Differences

| Feature | Custom | LangGraph |
|---------|--------|-----------|
| Parallel Execution | ❌ No | ✅ Yes |
| State Persistence | ❌ No | ✅ Yes |
| Resume Workflows | ❌ No | ✅ Yes |
| Conditional Routing | ⚠️ Manual | ✅ Automatic |
| Visualization | ❌ No | ✅ Yes |
| Time-Travel Debug | ❌ No | ✅ Yes |
| Performance | 15-20 min | 10-15 min |

### Backward Compatibility

Both orchestrators are available:
- **Custom**: `src.orchestrator.agent_orchestrator.AgentOrchestrator`
- **LangGraph**: `src.orchestrator.langgraph_orchestrator.LangGraphOrchestrator`

Your existing agents remain unchanged! LangGraph wraps them with no modifications needed.

## API Reference

### LangGraphOrchestrator

```python
class LangGraphOrchestrator:
    def __init__(
        self,
        cursor_workspace: str,
        config: Optional[Dict[str, Any]] = None,
        checkpoint_db: Optional[str] = None
    )
```

**Parameters:**
- `cursor_workspace`: Path to workspace directory
- `config`: Configuration dictionary (same as before)
- `checkpoint_db`: Path to SQLite checkpoint database (default: `./checkpoints.db`)

**Methods:**

#### execute_feature_development
```python
async def execute_feature_development(
    self,
    requirement: str,
    context: Optional[Dict[str, Any]] = None,
    thread_id: Optional[str] = None
) -> Dict[str, Any]
```

Execute feature development workflow with parallel QA/DevOps.

**Returns:** Final workflow state with all agent outputs

#### execute_bug_fix
```python
async def execute_bug_fix(
    self,
    requirement: str,
    bug_description: str,
    thread_id: Optional[str] = None
) -> Dict[str, Any]
```

Execute bug fix workflow.

#### build_feature_development_graph
```python
async def build_feature_development_graph(self) -> CompiledGraph
```

Build and compile the feature development workflow graph.

**Returns:** Compiled LangGraph application

## Performance Comparison

### Execution Time

| Workflow | Custom (Sequential) | LangGraph (Parallel) | Improvement |
|----------|---------------------|----------------------|-------------|
| Feature Development | 15-20 min | 10-15 min | 30-40% |
| Bug Fix | 8-12 min | 8-12 min | Same (no parallel) |
| Infrastructure | 10-15 min | 7-10 min | 30% |

### Resource Usage

- **Memory**: Similar (checkpoint adds ~10-20MB SQLite DB)
- **CPU**: Better utilized with parallel execution
- **Disk**: Checkpoint DB grows ~1-2MB per workflow

## Troubleshooting

### Issue: "No module named 'langgraph'"

**Solution:**
```bash
pip install langgraph langchain-core aiosqlite
```

### Issue: Checkpoint database locked

**Solution:**
```bash
# Delete checkpoint database (loses resume capability)
rm checkpoints.db

# Or specify different DB per workflow
orchestrator = LangGraphOrchestrator(
    cursor_workspace=".",
    checkpoint_db="./checkpoints_workflow2.db"
)
```

### Issue: Workflow stuck at parallel node

**Solution:**
LangGraph waits for ALL parallel branches to complete. Check logs for which node is stuck.

```python
# Add timeout to nodes
async def qa_engineer_node_with_timeout(state):
    try:
        return await asyncio.wait_for(
            self.qa_engineer_node(state),
            timeout=600  # 10 minutes
        )
    except asyncio.TimeoutError:
        return {
            "errors": [{"step": "qa_testing", "error": "Timeout"}],
            "status": "failed"
        }
```

## Best Practices

1. **Use Descriptive Thread IDs**
   ```python
   thread_id = f"feature_{feature_name}_{timestamp}"
   ```

2. **Monitor Checkpoint Database Size**
   - Grows ~1-2MB per workflow
   - Clean up old checkpoints periodically
   
3. **Handle Interruptions Gracefully**
   ```python
   try:
       result = await orchestrator.execute_feature_development(...)
   except KeyboardInterrupt:
       print("Workflow saved. Resume with same thread_id")
   ```

4. **Use Context for Configuration**
   ```python
   context = {
       "language": "python",
       "framework": "fastapi",
       "test_coverage": 80,
       "deployment": "kubernetes"
   }
   ```

5. **Leverage Parallel Execution**
   - Design workflows with parallel-compatible tasks
   - QA and DevOps naturally run in parallel
   - Documentation waits for both (join point)

## Examples Repository

All examples are in the `examples/` directory:

- `langgraph_feature_development.py` - Complete feature workflow
- `langgraph_bug_fix.py` - Bug fix workflow
- `langgraph_resume_workflow.py` - Resume interrupted workflow
- `visualize_workflow.py` - Generate workflow diagrams

Run any example:
```bash
python examples/langgraph_feature_development.py
```

## Next Steps

1. **Try the Examples**
   ```bash
   python examples/langgraph_feature_development.py
   ```

2. **Create Custom Workflows**
   - Copy an existing workflow graph
   - Modify nodes and edges
   - Add your own conditional routing

3. **Integrate with CI/CD**
   - Run workflows automatically on commits
   - Use thread_id for workflow tracking
   - Store checkpoints for audit trail

4. **Explore Advanced Features**
   - Human-in-the-loop approvals
   - Multi-level conditional routing
   - Custom error recovery strategies

## Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangGraph Tutorials](https://langchain-ai.github.io/langgraph/tutorials/)
- [Mermaid Diagram Editor](https://mermaid.live/)
- [Project Architecture](ARCHITECTURE.md)

---

**Built with ❤️ for developers who value efficiency and reliability.**

For questions or issues, please open a GitHub issue or check the troubleshooting section.
