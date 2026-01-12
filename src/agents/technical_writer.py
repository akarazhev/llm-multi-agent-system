from typing import Dict, Any
from .base_agent import BaseAgent, AgentRole, Task
import logging

logger = logging.getLogger(__name__)


class TechnicalWriterAgent(BaseAgent):
    def __init__(self, agent_id: str, cursor_workspace: str, config: Dict[str, Any] = None):
        super().__init__(agent_id, AgentRole.TECHNICAL_WRITER, cursor_workspace, config)
        self.doc_formats = config.get("formats", ["markdown", "confluence"]) if config else ["markdown"]
    
    def get_system_prompt(self) -> str:
        return f"""You are an expert Technical Writer agent. Your responsibilities include:
        
        1. Documentation: Create clear, comprehensive technical documentation
        2. API Documentation: Document APIs with examples and use cases
        3. User Guides: Write user-friendly guides and tutorials
        4. Architecture Docs: Document system architecture and design decisions
        5. Release Notes: Create detailed release notes and changelogs
        6. Knowledge Base: Build and maintain knowledge base articles
        
        Documentation Formats: {', '.join(self.doc_formats)}
        
        When writing documentation:
        - Use clear, concise language
        - Include practical examples and code snippets
        - Structure content logically with proper headings
        - Add diagrams and visuals where helpful
        - Consider the target audience (developers, users, stakeholders)
        - Keep documentation up-to-date and accurate
        
        Provide professional, publication-ready documentation."""
    
    async def process_task(self, task: Task) -> Dict[str, Any]:
        logger.info(f"[{self.agent_id}] Processing Technical Writer task: {task.description}")
        
        source_files = task.context.get("files", [])
        
        prompt = f"""
{self.get_system_prompt()}

Task: {task.description}

Context:
{self._format_context(task.context)}

Documentation Type: {task.context.get('doc_type', 'general')}
Target Audience: {task.context.get('audience', 'developers')}

Please create documentation including:
1. Overview and introduction
2. Detailed explanations with examples
3. Code snippets and usage examples
4. Configuration and setup instructions
5. Troubleshooting section
6. References and related resources

IMPORTANT: Format your documentation using markdown code blocks with filenames:
```markdown:docs/README.md
# Your documentation here
```

Or specify files explicitly:
File: docs/API.md
# Your documentation here
"""
        
        result = await self.execute_cursor_command(
            prompt,
            files=source_files if source_files else None
        )
        
        if result.get("success"):
            doc_text = result.get("stdout", "")
            
            # Write documentation files from the LLM response
            created_files = []
            try:
                created_files = self.file_writer.write_code_blocks(
                    doc_text,
                    task.task_id,
                    self.role.value
                )
                
                logger.info(f"[{self.agent_id}] Created {len(created_files)} documentation files")
            except Exception as e:
                logger.warning(f"[{self.agent_id}] Failed to write documentation files: {e}")
            
            return {
                "status": "completed",
                "documentation": doc_text,
                "files_created": created_files,
                "source_files": source_files,
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
