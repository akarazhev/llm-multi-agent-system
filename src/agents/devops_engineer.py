from typing import Dict, Any
from .base_agent import BaseAgent, AgentRole, Task
import logging

logger = logging.getLogger(__name__)


class DevOpsEngineerAgent(BaseAgent):
    def __init__(self, agent_id: str, cursor_workspace: str, config: Dict[str, Any] = None):
        super().__init__(agent_id, AgentRole.DEVOPS_ENGINEER, cursor_workspace, config)
        self.platforms = config.get("platforms", ["docker", "kubernetes", "aws"]) if config else ["docker"]
    
    def get_system_prompt(self) -> str:
        return f"""You are an expert DevOps Engineer agent. Your responsibilities include:
        
        1. Infrastructure as Code: Create and manage infrastructure configurations
        2. CI/CD Pipelines: Design and implement automated deployment pipelines
        3. Containerization: Create Docker containers and orchestration configs
        4. Monitoring & Logging: Set up monitoring, alerting, and logging systems
        5. Security: Implement security best practices and compliance
        6. Performance Optimization: Optimize infrastructure for performance and cost
        
        Platforms: {', '.join(self.platforms)}
        
        When designing infrastructure:
        - Use infrastructure as code principles
        - Implement security best practices
        - Design for scalability and reliability
        - Automate everything possible
        - Include monitoring and observability
        - Document deployment procedures
        
        Provide production-ready infrastructure configurations."""
    
    async def process_task(self, task: Task) -> Dict[str, Any]:
        logger.info(f"[{self.agent_id}] Processing DevOps task: {task.description}")
        
        config_files = task.context.get("files", [])
        
        prompt = f"""
{self.get_system_prompt()}

Task: {task.description}

Context:
{self._format_context(task.context)}

Requirements:
{task.context.get('requirement', task.context.get('requirements', 'No specific requirements provided'))}

Please provide:
1. Infrastructure configuration files (Docker, K8s, Terraform, etc.)
2. CI/CD pipeline configuration
3. Deployment scripts and procedures
4. Monitoring and logging setup
5. Security configurations
6. Documentation for operations team

IMPORTANT: Format your configuration files using markdown code blocks with filenames:
```yaml:docker-compose.yml
# Your config here
```

Or specify files explicitly:
File: Dockerfile
# Your config here
"""
        
        result = await self.execute_cursor_command(
            prompt,
            files=config_files if config_files else None
        )
        
        if result.get("success"):
            infra_text = result.get("stdout", "")
            
            # Write infrastructure files from the LLM response
            created_files = []
            try:
                created_files = self.file_writer.write_code_blocks(
                    infra_text,
                    task.task_id,
                    self.role.value
                )
                
                if not created_files:
                    created_files = self.file_writer.write_file_structure(
                        infra_text,
                        task.task_id,
                        self.role.value
                    )
                
                logger.info(f"[{self.agent_id}] Created {len(created_files)} infrastructure files")
            except Exception as e:
                logger.warning(f"[{self.agent_id}] Failed to write infrastructure files: {e}")
            
            return {
                "status": "completed",
                "infrastructure": infra_text,
                "files_created": created_files,
                "config_files": config_files,
                "agent_role": self.role.value
            }
        else:
            raise Exception(f"Cursor command failed: {result.get('error', result.get('stderr'))}")
    
    def _format_context(self, context: Dict[str, Any]) -> str:
        lines = []
        for key, value in context.items():
            if key != "files":
                lines.append(f"- {key}: {value}")
        return "\n".join(lines)
