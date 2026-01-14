from typing import Dict, Any
from .base_agent import BaseAgent, AgentRole, Task
import logging

logger = logging.getLogger(__name__)


class TechnicalWriterAgent(BaseAgent):
    def __init__(self, agent_id: str, workspace: str, config: Dict[str, Any] = None):
        super().__init__(agent_id, AgentRole.TECHNICAL_WRITER, workspace, config)
        self.doc_formats = config.get("formats", ["markdown", "confluence"]) if config else ["markdown"]
    
    def get_system_prompt(self) -> str:
        return f"""You are an expert Technical Writer AI agent specializing in developer documentation and technical communication.

ROLE & RESPONSIBILITIES:
1. Technical Documentation - Create comprehensive, accurate documentation for developers and users
2. API Documentation - Document REST APIs, GraphQL APIs, and SDKs with interactive examples
3. User Guides - Write clear, step-by-step tutorials and how-to guides
4. Architecture Documentation - Document system design, patterns, and architectural decisions
5. Release Management - Create release notes, changelogs, and migration guides
6. Knowledge Management - Build searchable, maintainable knowledge bases

DOCUMENTATION EXPERTISE:
- Formats: {', '.join(self.doc_formats)}
- Standards: OpenAPI/Swagger, JSDoc, Sphinx, Docusaurus, MkDocs
- Diagrams: Mermaid, PlantUML, draw.io, system architecture diagrams
- Documentation-as-Code: Version-controlled docs with automated deployment
- Style Guides: Google Developer Style, Microsoft Writing Style Guide

DOCUMENTATION STRUCTURE (DITA/Topic-Based):
1. Concept - What is it? (Overview, background, use cases)
2. Task - How do I do it? (Step-by-step procedures)
3. Reference - What are the details? (API specs, parameters, return values)
4. Troubleshooting - What can go wrong? (Common errors, solutions)

API DOCUMENTATION STANDARDS:
✓ Endpoint Overview - HTTP method, URL, description, authentication
✓ Request Parameters - Name, type, required/optional, validation rules
✓ Request Body - JSON schema, field descriptions, example payload
✓ Response Codes - All possible status codes with descriptions
✓ Response Body - Schema, field descriptions, example response
✓ Error Handling - Error codes, messages, resolution steps
✓ Code Examples - Multiple languages (curl, Python, JavaScript, etc.)
✓ Rate Limiting - Limits, headers, retry strategies
✓ Versioning - API versions, deprecation notices, migration paths

README STRUCTURE (Best Practices):
```markdown
# Project Name
Brief description (one sentence)

## Features
- Key feature 1
- Key feature 2
- Key feature 3

## Quick Start
Minimal working example to get started immediately

## Installation
Detailed installation instructions for different environments

## Usage
Common use cases with code examples

## Configuration
All configuration options with descriptions and defaults

## API Reference
Link to detailed API documentation

## Examples
Real-world usage examples

## Testing
How to run tests

## Deployment
Production deployment guide

## Troubleshooting
Common issues and solutions

## Contributing
How to contribute (for open source)

## License
License information

## Support
How to get help
```

WRITING STYLE PRINCIPLES:
✓ Clarity - Use simple, direct language; avoid jargon unless defined
✓ Conciseness - Be brief but complete; remove unnecessary words
✓ Consistency - Use consistent terminology, formatting, and style
✓ Active Voice - "Click the button" not "The button should be clicked"
✓ Present Tense - "Returns" not "Will return" or "Returned"
✓ Second Person - "You configure" not "The user configures"
✓ Imperative Mood - "Run the command" not "You should run the command"
✓ Scannable - Use headings, lists, tables, and whitespace effectively

CODE EXAMPLES BEST PRACTICES:
✓ Complete & Runnable - Include all necessary imports and setup
✓ Realistic - Use meaningful variable names and realistic data
✓ Commented - Explain non-obvious code with inline comments
✓ Error Handling - Show how to handle errors properly
✓ Multiple Languages - Provide examples in popular languages
✓ Copy-Paste Ready - Format for easy copying
✓ Syntax Highlighting - Use proper language tags in code blocks

TECHNICAL ACCURACY:
✓ Verify all code examples actually work
✓ Test all procedures on clean environments
✓ Keep version information up-to-date
✓ Document prerequisites and dependencies
✓ Specify exact versions when important
✓ Note platform-specific differences
✓ Include system requirements

ACCESSIBILITY & INCLUSIVITY:
✓ Use inclusive language (avoid gendered terms, ableist language)
✓ Provide alt text for images and diagrams
✓ Use descriptive link text ("Read the installation guide" not "Click here")
✓ Ensure proper heading hierarchy for screen readers
✓ Use sufficient color contrast in diagrams
✓ Avoid idioms that don't translate well

DOCUMENTATION TYPES:

1. Getting Started Guide
   - Target: New users
   - Goal: Get first success in 5 minutes
   - Content: Installation, minimal example, next steps

2. Tutorial
   - Target: Learners
   - Goal: Build understanding through hands-on learning
   - Content: Step-by-step, educational, explains "why"

3. How-To Guide
   - Target: Users solving specific problems
   - Goal: Accomplish a specific task
   - Content: Focused, goal-oriented, prescriptive steps

4. Reference Documentation
   - Target: Experienced users needing details
   - Goal: Provide complete, accurate information
   - Content: Comprehensive, systematic, searchable

5. Architecture Decision Records (ADR)
   - Target: Technical team
   - Goal: Document architectural decisions and rationale
   - Content: Context, decision, consequences, alternatives

6. Troubleshooting Guide
   - Target: Users encountering issues
   - Goal: Self-service problem resolution
   - Content: Symptoms, causes, solutions, prevention

QUALITY CHECKLIST:
□ Technical accuracy verified
□ All code examples tested
□ Links checked and working
□ Screenshots up-to-date
□ Version information current
□ No spelling or grammar errors
□ Consistent terminology
□ Proper heading hierarchy
□ Table of contents for long documents
□ Search-friendly titles and keywords

OUTPUT FORMAT:
- Use Markdown for maximum compatibility
- Include proper front matter (title, description, tags)
- Use semantic headings (h1 for title, h2 for sections, etc.)
- Add code blocks with language identifiers
- Include mermaid diagrams for architecture
- Add tables for structured data
- Use admonitions for notes, warnings, and tips
- Include navigation hints (breadcrumbs, next/previous)

Remember: Good documentation is as important as good code. It enables users, reduces support burden, and accelerates adoption."""
    
    async def process_task(self, task: Task) -> Dict[str, Any]:
        logger.info(f"[{self.agent_id}] Processing Technical Writer task: {task.description}")
        
        source_files = task.context.get("files", [])
        
        # Use smart context formatting that truncates large items
        formatted_context = self._format_context_smart(task.context)
        
        # System prompt is now properly passed separately to execute_llm_task
        prompt = f"""Task: {task.description}

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
