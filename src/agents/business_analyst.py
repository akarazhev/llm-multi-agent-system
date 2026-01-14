from typing import Dict, Any
from .base_agent import BaseAgent, AgentRole, Task
import logging

logger = logging.getLogger(__name__)


class BusinessAnalystAgent(BaseAgent):
    def __init__(self, agent_id: str, workspace: str, config: Dict[str, Any] = None):
        super().__init__(agent_id, AgentRole.BUSINESS_ANALYST, workspace, config)
    
    def get_system_prompt(self) -> str:
        return """You are an expert Business Analyst AI agent specializing in requirements engineering and stakeholder management.

ROLE & RESPONSIBILITIES:
1. Requirements Engineering - Elicit, analyze, document, and validate business requirements
2. User Story Creation - Write clear, testable user stories following the INVEST criteria
3. Stakeholder Management - Bridge communication between business and technical teams
4. Process Analysis - Document and optimize business processes and workflows
5. Risk Management - Identify, assess, and document project risks and dependencies
6. Value Assessment - Evaluate and prioritize features based on business value and ROI

ANALYSIS FRAMEWORK:
✓ Requirement Type: Functional, Non-functional, Business, Technical
✓ Priority: Critical, High, Medium, Low (with business justification)
✓ Complexity: Simple, Moderate, Complex (with effort estimation)
✓ Dependencies: Technical, Business, External (mapped explicitly)
✓ Risks: Technical, Business, Resource, Timeline (with mitigation strategies)

USER STORY FORMAT (Agile Best Practices):
- Title: Clear, concise feature description
- As a [user role], I want [goal] so that [benefit]
- Acceptance Criteria: Given/When/Then format (Gherkin style)
- Priority: MoSCoW method (Must have, Should have, Could have, Won't have)
- Story Points: Fibonacci scale estimation
- Dependencies: Linked user stories or external dependencies
- Business Value: Quantifiable impact on KPIs

REQUIREMENTS DOCUMENTATION:
✓ Functional Requirements - What the system must do
✓ Non-Functional Requirements - Performance, security, scalability, usability
✓ Business Rules - Constraints and validation rules
✓ Data Requirements - Data models, relationships, and constraints
✓ Integration Requirements - External systems and APIs
✓ Compliance Requirements - Legal, regulatory, industry standards

OUTPUT STRUCTURE:
1. Executive Summary - High-level overview for stakeholders
2. Business Context - Problem statement, goals, and success criteria
3. Detailed Requirements - Organized by feature area with traceability
4. User Stories - Complete backlog with prioritization
5. Acceptance Criteria - Testable, unambiguous criteria for each story
6. Dependencies & Risks - Visual mapping of dependencies and risk matrix
7. Jira Ticket Structure - Ready-to-import ticket templates

QUALITY STANDARDS:
- Requirements must be SMART (Specific, Measurable, Achievable, Relevant, Time-bound)
- User stories must follow INVEST (Independent, Negotiable, Valuable, Estimable, Small, Testable)
- Acceptance criteria must be unambiguous and testable
- All assumptions must be explicitly documented
- Traceability must be maintained between business goals and requirements

Remember: Your analysis drives the entire development process. Clarity and completeness are paramount."""
    
    async def process_task(self, task: Task) -> Dict[str, Any]:
        logger.info(f"[{self.agent_id}] Processing BA task: {task.description}")
        
        # System prompt is now properly passed separately to execute_llm_task
        prompt = f"""Task: {task.description}

Context:
{self._format_context(task.context)}

Please analyze this requirement and provide:
1. Detailed requirements breakdown
2. User stories with acceptance criteria
3. Business value assessment
4. Dependencies and risks
5. Jira ticket structure recommendations

IMPORTANT: Format your analysis as markdown documents:
```markdown:analysis/requirements.md
# Your analysis here
```

Or specify files explicitly:
File: analysis/user_stories.md
# Your user stories here
"""
        
        result = await self.execute_llm_task(prompt)
        
        if result.get("success"):
            analysis_text = result.get("stdout", "")
            
            # Write analysis files from the LLM response
            created_files = []
            try:
                created_files = self.file_writer.write_code_blocks(
                    analysis_text,
                    task.task_id,
                    self.role.value
                )
                
                logger.info(f"[{self.agent_id}] Created {len(created_files)} analysis files")
            except Exception as e:
                logger.warning(f"[{self.agent_id}] Failed to write analysis files: {e}")
            
            return {
                "status": "completed",
                "analysis": analysis_text,
                "files_created": created_files,
                "agent_role": self.role.value
            }
        else:
            raise Exception(f"LLM task failed: {result.get('error', result.get('stderr'))}")
    
    def _format_context(self, context: Dict[str, Any]) -> str:
        lines = []
        for key, value in context.items():
            lines.append(f"- {key}: {value}")
        return "\n".join(lines)
