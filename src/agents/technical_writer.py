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
        
        # Use smart context formatting that truncates large items
        formatted_context = self._format_context_smart(task.context)
        
        prompt = f"""
{self.get_system_prompt()}

Task: {task.description}

Context:
{formatted_context}

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
        
        result = await self.execute_llm_task(
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
            raise Exception(f"LLM task failed: {result.get('error', result.get('stderr'))}")
    
    def _format_context(self, context: Dict[str, Any]) -> str:
        lines = []
        for key, value in context.items():
            if key != "files":
                lines.append(f"- {key}: {value}")
        return "\n".join(lines)
    
    def _format_context_smart(self, context: Dict[str, Any], max_size_per_item: int = 1000) -> str:
        """
        Format context with smart truncation to avoid exceeding token limits.
        Large items (implementation, tests, infrastructure) are summarized.
        """
        lines = []
        
        for key, value in context.items():
            if key == "files":
                continue
            
            # For simple string values, include as-is
            if isinstance(value, str):
                if len(value) > max_size_per_item:
                    lines.append(f"- {key}: {value[:max_size_per_item]}... (truncated, {len(value)} chars total)")
                else:
                    lines.append(f"- {key}: {value}")
            
            # For dict values (implementation, tests, infrastructure), summarize
            elif isinstance(value, dict):
                # Extract key information: files_created, status, summary
                summary_parts = []
                
                if "files_created" in value:
                    files = value["files_created"]
                    if isinstance(files, list):
                        summary_parts.append(f"Files created: {len(files)} files")
                        if files:
                            summary_parts.append(f"File paths: {', '.join(files[:5])}")
                            if len(files) > 5:
                                summary_parts.append(f"... and {len(files) - 5} more files")
                    else:
                        summary_parts.append(f"Files: {files}")
                
                if "status" in value:
                    summary_parts.append(f"Status: {value['status']}")
                
                # Include a small snippet of the main content if available
                if "code" in value:
                    code_snippet = str(value["code"])[:200]
                    summary_parts.append(f"Code snippet: {code_snippet}...")
                elif "documentation" in value:
                    doc_snippet = str(value["documentation"])[:200]
                    summary_parts.append(f"Content snippet: {doc_snippet}...")
                elif "analysis" in value:
                    analysis_snippet = str(value["analysis"])[:200]
                    summary_parts.append(f"Analysis snippet: {analysis_snippet}...")
                
                # If no specific fields, just show it's a dict with keys
                if not summary_parts:
                    keys = list(value.keys())[:5]
                    summary_parts.append(f"Contains: {', '.join(keys)}")
                    if len(value) > 5:
                        summary_parts.append(f"... and {len(value) - 5} more keys")
                
                lines.append(f"- {key}: {' | '.join(summary_parts)}")
            
            # For list values, summarize
            elif isinstance(value, list):
                if len(value) > 0:
                    lines.append(f"- {key}: List with {len(value)} items")
                    # Show first item summary if it's a dict
                    if isinstance(value[0], dict):
                        first_keys = list(value[0].keys())[:3]
                        lines.append(f"  First item keys: {', '.join(first_keys)}")
                else:
                    lines.append(f"- {key}: []")
            
            # For other types, convert to string with truncation
            else:
                value_str = str(value)
                if len(value_str) > max_size_per_item:
                    lines.append(f"- {key}: {value_str[:max_size_per_item]}... (truncated)")
                else:
                    lines.append(f"- {key}: {value_str}")
        
        return "\n".join(lines)
