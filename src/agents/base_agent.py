import asyncio
import subprocess
import json
from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class AgentRole(Enum):
    BUSINESS_ANALYST = "business_analyst"
    DEVELOPER = "developer"
    QA_ENGINEER = "qa_engineer"
    DEVOPS_ENGINEER = "devops_engineer"
    TECHNICAL_WRITER = "technical_writer"


class AgentStatus(Enum):
    IDLE = "idle"
    WORKING = "working"
    WAITING = "waiting"
    COMPLETED = "completed"
    ERROR = "error"


@dataclass
class Task:
    task_id: str
    description: str
    context: Dict[str, Any]
    priority: int = 1
    dependencies: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


@dataclass
class AgentMessage:
    from_agent: str
    to_agent: Optional[str]
    message_type: str
    content: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)


class BaseAgent(ABC):
    def __init__(
        self,
        agent_id: str,
        role: AgentRole,
        cursor_workspace: str,
        config: Optional[Dict[str, Any]] = None
    ):
        self.agent_id = agent_id
        self.role = role
        self.cursor_workspace = cursor_workspace
        self.config = config or {}
        self.cursor_cli_path = self.config.get('cursor_cli_path', 'cursor')
        self.status = AgentStatus.IDLE
        self.current_task: Optional[Task] = None
        self.task_history: List[Task] = []
        self.message_queue: asyncio.Queue = asyncio.Queue()
        
    @abstractmethod
    async def process_task(self, task: Task) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        pass
    
    async def execute_cursor_command(
        self,
        prompt: str,
        files: Optional[List[str]] = None,
        timeout: int = 300
    ) -> Dict[str, Any]:
        """
        Execute AI task using cursor-agent-tools SDK or direct OpenAI client.
        Supports Claude, OpenAI, Ollama, and local llama-server.
        """
        try:
            import os
            
            # Read file contents if files are specified
            file_contents = {}
            if files:
                for file_path in files:
                    try:
                        with open(file_path, 'r') as f:
                            file_contents[file_path] = f.read()
                    except Exception as e:
                        logger.warning(f"[{self.agent_id}] Could not read file {file_path}: {e}")
            
            # Build enhanced prompt with system context and files
            system_prompt = self.get_system_prompt()
            full_prompt = prompt
            
            if file_contents:
                full_prompt += "\n\nRelevant Files:\n"
                for path, content in file_contents.items():
                    full_prompt += f"\n--- {path} ---\n{content[:2000]}\n"  # Limit file content
            
            # Enforce local llama-server usage only
            api_base = os.getenv('OPENAI_API_BASE')
            if not api_base:
                error_msg = (
                    "OPENAI_API_BASE not configured. This system requires a local llama-server.\n"
                    "Please set OPENAI_API_BASE in your .env file:\n"
                    "  OPENAI_API_BASE=http://127.0.0.1:8080/v1\n"
                    "  OPENAI_API_KEY=not-needed\n"
                    "  OPENAI_API_MODEL=devstral\n\n"
                    "Start llama-server with: ./scripts/start_llama_server.sh"
                )
                logger.error(f"[{self.agent_id}] {error_msg}")
                return {
                    "success": False,
                    "error": error_msg
                }
            
            logger.info(f"[{self.agent_id}] Using local llama-server at {api_base}")
            return await self._call_local_llama_server(system_prompt, full_prompt, timeout)
            
        except asyncio.TimeoutError:
            logger.error(f"[{self.agent_id}] Task timed out after {timeout} seconds")
            return {
                "success": False,
                "error": f"Task timed out after {timeout} seconds"
            }
        except Exception as e:
            logger.error(f"[{self.agent_id}] Error executing task: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _call_local_llama_server(self, system_prompt: str, user_prompt: str, timeout: int) -> Dict[str, Any]:
        """Call local llama-server using OpenAI-compatible API"""
        try:
            import os
            from openai import AsyncOpenAI
            
            api_base = os.getenv('OPENAI_API_BASE', 'http://127.0.0.1:8080/v1')
            model = os.getenv('OPENAI_API_MODEL', 'devstral')
            
            # Create OpenAI client with custom base URL
            client = AsyncOpenAI(
                base_url=api_base,
                api_key="not-needed"  # Local server doesn't need real API key
            )
            
            logger.info(f"[{self.agent_id}] Calling local llama-server with model: {model}")
            
            # Make the API call
            response = await asyncio.wait_for(
                client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.7,
                    max_tokens=4096
                ),
                timeout=timeout
            )
            
            content = response.choices[0].message.content
            
            return {
                "success": True,
                "stdout": content,
                "stderr": "",
                "returncode": 0
            }
            
        except asyncio.TimeoutError:
            return {
                "success": False,
                "error": f"Local llama-server request timed out after {timeout} seconds"
            }
        except Exception as e:
            logger.error(f"[{self.agent_id}] Error calling local llama-server: {e}")
            return {
                "success": False,
                "error": f"Local llama-server error: {str(e)}"
            }
    
    async def run_task(self, task: Task) -> Task:
        self.current_task = task
        self.status = AgentStatus.WORKING
        
        try:
            logger.info(f"[{self.agent_id}] Starting task: {task.task_id}")
            result = await self.process_task(task)
            
            task.result = result
            task.completed_at = datetime.now()
            self.status = AgentStatus.COMPLETED
            
            logger.info(f"[{self.agent_id}] Completed task: {task.task_id}")
            
        except Exception as e:
            logger.error(f"[{self.agent_id}] Error processing task {task.task_id}: {e}")
            task.error = str(e)
            self.status = AgentStatus.ERROR
        
        finally:
            self.task_history.append(task)
            self.current_task = None
            
        return task
    
    async def send_message(self, message: AgentMessage):
        await self.message_queue.put(message)
    
    async def receive_message(self) -> AgentMessage:
        return await self.message_queue.get()
    
    def get_status(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "role": self.role.value,
            "status": self.status.value,
            "current_task": self.current_task.task_id if self.current_task else None,
            "completed_tasks": len(self.task_history)
        }
