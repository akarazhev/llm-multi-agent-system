#!/usr/bin/env python3
"""
Workflow Visualization Utilities

Demonstrates how to visualize LangGraph workflows as diagrams.
Requires additional dependencies: matplotlib, pygraphviz or mermaid-py
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.orchestrator.langgraph_orchestrator import LangGraphOrchestrator
from src.config.settings import load_config
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def visualize_feature_development():
    """Generate visualization of feature development workflow"""
    
    print("=" * 70)
    print("Workflow Visualization Generator")
    print("=" * 70)
    print()
    
    # Load configuration
    try:
        config = load_config()
        workspace = config.workspace
    except Exception as e:
        logger.warning(f"Could not load config: {e}, using defaults")
        workspace = "."
        config = {
            "workspace": workspace,
            "agents": {}
        }
    
    # Create orchestrator
    print("Building workflow graph...")
    orchestrator = LangGraphOrchestrator(
        workspace=workspace,
        config=config.__dict__ if hasattr(config, '__dict__') else config
    )
    
    # Build the graph
    app = await orchestrator.build_feature_development_graph()
    
    print("✓ Graph built successfully")
    print()
    
    # Generate Mermaid diagram
    print("Generating Mermaid diagram...")
    print()
    
    try:
        mermaid_code = app.get_graph().draw_mermaid()
        
        print("Mermaid Diagram Code:")
        print("-" * 70)
        print(mermaid_code)
        print("-" * 70)
        print()
        
        # Save to file
        output_path = Path(workspace) / "output" / "workflow_diagram.mmd"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            f.write(mermaid_code)
        
        print(f"✓ Saved Mermaid diagram to: {output_path}")
        print()
        print("To visualize:")
        print("  1. Copy the Mermaid code above")
        print("  2. Paste into https://mermaid.live/")
        print("  3. Or use Mermaid CLI: mmdc -i workflow_diagram.mmd -o workflow.png")
        print()
        
    except Exception as e:
        print(f"✗ Could not generate Mermaid diagram: {e}")
        print()
    
    # Try to generate ASCII representation
    print("ASCII Workflow Representation:")
    print("-" * 70)
    print_workflow_ascii()
    print("-" * 70)
    print()
    
    # Display workflow structure
    print("Workflow Structure:")
    print("-" * 70)
    print_workflow_structure()
    print("-" * 70)
    print()


def print_workflow_ascii():
    """Print ASCII art representation of the workflow"""
    ascii_diagram = """
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
    """
    print(ascii_diagram)


def print_workflow_structure():
    """Print detailed workflow structure"""
    structure = """
Node: business_analyst
  ├─ Input: requirement, workflow_type
  ├─ Agent: Business Analyst
  ├─ Task: Requirements analysis, user stories
  └─ Output: business_analysis, files_created

Node: architecture_design
  ├─ Input: requirement, business_analysis
  ├─ Agent: Developer
  ├─ Task: System architecture design
  ├─ Depends on: business_analyst
  └─ Output: architecture, files_created

Node: implementation
  ├─ Input: requirement, architecture
  ├─ Agent: Developer
  ├─ Task: Feature implementation
  ├─ Depends on: architecture_design
  └─ Output: implementation, files_created

Conditional: should_continue_after_implementation
  ├─ Checks: implementation.status
  ├─ If success → [qa_testing, infrastructure] (PARALLEL)
  └─ If failed → END

Node: qa_testing (PARALLEL)
  ├─ Input: requirement, implementation
  ├─ Agent: QA Engineer
  ├─ Task: Test suite creation and execution
  ├─ Depends on: implementation (via conditional)
  └─ Output: tests, files_created

Node: infrastructure (PARALLEL)
  ├─ Input: requirement, implementation
  ├─ Agent: DevOps Engineer
  ├─ Task: Deployment infrastructure setup
  ├─ Depends on: implementation (via conditional)
  └─ Output: infrastructure, files_created

Node: documentation
  ├─ Input: requirement, implementation, tests, infrastructure
  ├─ Agent: Technical Writer
  ├─ Task: Comprehensive documentation
  ├─ Depends on: qa_testing AND infrastructure (join)
  └─ Output: documentation, files_created, status=completed
    """
    print(structure)


async def show_checkpoint_info():
    """Show information about workflow checkpoints"""
    
    print("\nCheckpoint Information:")
    print("=" * 70)
    print()
    print("LangGraph automatically saves checkpoints at each node completion.")
    print("This enables:")
    print()
    print("1. Resume Interrupted Workflows")
    print("   - If process crashes or is interrupted (Ctrl+C)")
    print("   - Resume from exact point where it stopped")
    print()
    print("2. Time-Travel Debugging")
    print("   - Inspect state at any point in workflow history")
    print("   - Replay from specific checkpoints")
    print()
    print("3. Branch Workflows")
    print("   - Create multiple variations from same checkpoint")
    print("   - Test different paths without re-running entire workflow")
    print()
    print("Checkpoints are stored in: checkpoints.db (SQLite)")
    print()
    print("Example Usage:")
    print("-" * 70)
    print("""
# Resume workflow
await orchestrator.execute_feature_development(
    requirement="...",
    thread_id="workflow_20240115_143022"  # ID of interrupted workflow
)

# Inspect checkpoints
app = await orchestrator.build_feature_development_graph()
config = {"configurable": {"thread_id": "workflow_123"}}

# Get all checkpoints for a workflow
checkpoints = []
async for checkpoint in app.aget_state_history(config):
    checkpoints.append(checkpoint)
    print(f"Step: {checkpoint.values.get('current_step')}")
    print(f"Files: {checkpoint.values.get('files_created')}")
    """)
    print("-" * 70)
    print()


async def main():
    """Main visualization demo"""
    
    try:
        await visualize_feature_development()
        await show_checkpoint_info()
        
        print("✓ Visualization complete!")
        print()
        
    except Exception as e:
        print(f"Error: {e}")
        logger.error(f"Visualization failed: {e}", exc_info=True)


if __name__ == "__main__":
    asyncio.run(main())
