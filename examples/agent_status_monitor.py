import asyncio
import sys
from pathlib import Path
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(Path(__file__).parent.parent / '.env')

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.orchestrator import AgentOrchestrator
from src.config import load_config


async def monitor_agents():
    config = load_config()
    
    orchestrator = AgentOrchestrator(
        cursor_workspace=config.cursor_workspace,
        config=config.to_dict()
    )
    
    print("Agent Status Monitor")
    print("="*80)
    
    status = orchestrator.get_system_status()
    
    print(f"\nTotal Agents: {status['total_agents']}")
    print(f"Total Tasks Completed: {status['total_tasks_completed']}")
    print(f"Timestamp: {status['timestamp']}")
    
    print("\nAgent Details:")
    print("-"*80)
    
    for agent_id, agent_status in status['agents'].items():
        print(f"\nAgent ID: {agent_id}")
        print(f"  Role: {agent_status['role']}")
        print(f"  Status: {agent_status['status']}")
        print(f"  Current Task: {agent_status['current_task'] or 'None'}")
        print(f"  Completed Tasks: {agent_status['completed_tasks']}")
    
    print("\n" + "="*80)
    
    output_file = Path("output") / "agent_status.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(status, f, indent=2)
    
    print(f"\nStatus saved to: {output_file}")


if __name__ == "__main__":
    asyncio.run(monitor_agents())
