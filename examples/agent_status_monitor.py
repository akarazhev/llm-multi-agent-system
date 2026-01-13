import asyncio
import sys
from pathlib import Path
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(Path(__file__).parent.parent / '.env')

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.orchestrator import LangGraphOrchestrator
from src.config import load_config


async def monitor_agents():
    config = load_config()
    
    orchestrator = LangGraphOrchestrator(
        workspace=config.workspace,
        config=config.to_dict()
    )
    
    print("Agent Status Monitor")
    print("="*80)
    
    print(f"\nTotal Agents: {len(orchestrator.agents)}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    print("\nAgent Details:")
    print("-"*80)
    
    for agent_name, agent in orchestrator.agents.items():
        print(f"\nAgent: {agent_name}")
        print(f"  ID: {agent.agent_id}")
        print(f"  Role: {agent.role}")
        status = agent.get_status() if hasattr(agent, 'get_status') else {}
        print(f"  Status: {status.get('status', 'active')}")
        print(f"  Current Task: {status.get('current_task', 'None')}")
        print(f"  Completed Tasks: {status.get('completed_tasks', 0)}")
    
    print("\n" + "="*80)
    
    status = {
        "total_agents": len(orchestrator.agents),
        "agents": {
            name: {
                "agent_id": agent.agent_id,
                "role": agent.role.value if hasattr(agent.role, 'value') else str(agent.role),
                "status": agent.get_status().get('status', 'active') if hasattr(agent, 'get_status') else 'active'
            }
            for name, agent in orchestrator.agents.items()
        },
        "timestamp": datetime.now().isoformat()
    }
    
    output_file = Path("output") / "agent_status.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(status, f, indent=2)
    
    print(f"\nStatus saved to: {output_file}")


if __name__ == "__main__":
    asyncio.run(monitor_agents())
