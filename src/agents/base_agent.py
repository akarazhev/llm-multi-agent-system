import asyncio
import subprocess
import json
from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import logging
from ..utils import FileWriter

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
        workspace: str,
        config: Optional[Dict[str, Any]] = None
    ):
        self.agent_id = agent_id
        self.role = role
        self.workspace = workspace
        self.config = config or {}
        self.status = AgentStatus.IDLE
        self.current_task: Optional[Task] = None
        self.task_history: List[Task] = []
        self.message_queue: asyncio.Queue = asyncio.Queue()
        self.file_writer = FileWriter(workspace)
        
    @abstractmethod
    async def process_task(self, task: Task) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        pass
    
    async def execute_llm_task(
        self,
        prompt: str,
        files: Optional[List[str]] = None,
        timeout: int = 300
    ) -> Dict[str, Any]:
        """
        Execute AI task using local llama-server.
        All processing happens locally via OpenAI-compatible API.
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
                # Reduce per-file limit to accommodate smaller context windows
                per_file_limit = 1000 if len(file_contents) > 1 else 1500
                for path, content in file_contents.items():
                    truncated_content = content[:per_file_limit]
                    if len(content) > per_file_limit:
                        truncated_content += f"\n... [truncated {len(content) - per_file_limit} chars]"
                    full_prompt += f"\n--- {path} ---\n{truncated_content}\n"
            
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
    
    def _truncate_prompt_to_fit(self, system_prompt: str, user_prompt: str, max_context_tokens: int, max_completion_tokens: int = 1024) -> tuple[str, str, bool]:
        """
        Truncate prompts to fit within context size limits.
        
        Args:
            system_prompt: The system prompt
            user_prompt: The user prompt
            max_context_tokens: Maximum context size in tokens (e.g., 4096)
            max_completion_tokens: Tokens reserved for completion (default 1024)
            
        Returns:
            Tuple of (truncated_system_prompt, truncated_user_prompt, was_truncated)
        """
        # Rough estimation: 1 token ≈ 4 characters
        CHARS_PER_TOKEN = 4
        
        # Calculate available tokens for prompt (reserve space for completion)
        available_prompt_tokens = max_context_tokens - max_completion_tokens
        available_chars = available_prompt_tokens * CHARS_PER_TOKEN
        
        system_chars = len(system_prompt)
        user_chars = len(user_prompt)
        total_chars = system_chars + user_chars
        
        # If it fits, return as-is
        if total_chars <= available_chars:
            return system_prompt, user_prompt, False
        
        # Truncation needed - prioritize user prompt over system prompt
        # Keep system prompt mostly intact (use 30% of available space)
        # Use remaining 70% for user prompt
        system_budget = int(available_chars * 0.3)
        user_budget = available_chars - system_budget
        
        truncated_system = system_prompt
        truncated_user = user_prompt
        
        # Truncate system prompt if needed
        if system_chars > system_budget:
            truncated_system = system_prompt[:system_budget] + "\n\n[System prompt truncated to fit context...]"
            logger.warning(f"[{self.agent_id}] System prompt truncated from {system_chars} to {len(truncated_system)} chars")
        
        # Truncate user prompt if needed
        if user_chars > user_budget:
            truncated_user = user_prompt[:user_budget] + "\n\n[User prompt truncated to fit context...]"
            logger.warning(f"[{self.agent_id}] User prompt truncated from {user_chars} to {len(truncated_user)} chars")
        
        logger.info(f"[{self.agent_id}] Prompt truncation: {total_chars} -> {len(truncated_system) + len(truncated_user)} chars (est {(len(truncated_system) + len(truncated_user))//CHARS_PER_TOKEN} tokens)")
        
        return truncated_system, truncated_user, True
    
    async def _call_local_llama_server(self, system_prompt: str, user_prompt: str, timeout: int, retry_count: int = 0) -> Dict[str, Any]:
        """Call local llama-server using OpenAI-compatible API with automatic retry on context size errors"""
        try:
            import os
            import re
            from openai import AsyncOpenAI
            
            api_base = os.getenv('OPENAI_API_BASE', 'http://127.0.0.1:8080/v1')
            model = os.getenv('OPENAI_API_MODEL', 'devstral')
            
            # Create OpenAI client with custom base URL
            client = AsyncOpenAI(
                base_url=api_base,
                api_key="not-needed"  # Local server doesn't need real API key
            )
            
            logger.info(f"[{self.agent_id}] Calling local llama-server with model: {model} (attempt {retry_count + 1})")
            
            # Make the API call
            response = await asyncio.wait_for(
                client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1024  # Reduced to leave more room for prompt
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
            error_str = str(e)
            
            # Check if this is a context size error
            if "exceed_context_size" in error_str or "exceeds the available context size" in error_str:
                logger.warning(f"[{self.agent_id}] Context size exceeded, attempting to truncate and retry...")
                
                # Extract context size from error message if possible
                # Error format: "request (4476 tokens) exceeds the available context size (4096 tokens)"
                match = re.search(r'available context size \((\d+) tokens\)', error_str)
                max_context_tokens = int(match.group(1)) if match else 4096
                
                # Extract actual prompt tokens from error
                match_prompt = re.search(r'request \((\d+) tokens\)', error_str)
                actual_prompt_tokens = int(match_prompt.group(1)) if match_prompt else None
                
                logger.info(f"[{self.agent_id}] Detected context limit: {max_context_tokens} tokens, prompt was: {actual_prompt_tokens} tokens")
                
                # Only retry once to avoid infinite loops
                if retry_count == 0:
                    # Truncate prompts to fit
                    truncated_system, truncated_user, was_truncated = self._truncate_prompt_to_fit(
                        system_prompt, user_prompt, max_context_tokens, max_completion_tokens=1024
                    )
                    
                    if was_truncated:
                        logger.info(f"[{self.agent_id}] Retrying with truncated prompts...")
                        # Retry with truncated prompts
                        return await self._call_local_llama_server(
                            truncated_system, truncated_user, timeout, retry_count=1
                        )
                else:
                    logger.error(f"[{self.agent_id}] Context size error persisted after truncation")
                    return {
                        "success": False,
                        "error": f"Context size error persisted after truncation. Server limit: {max_context_tokens} tokens. Consider increasing LLAMA_CTX_SIZE or reducing prompt complexity."
                    }
            
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
