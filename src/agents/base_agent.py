import asyncio
import subprocess
import json
from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, List, Optional, Any, Callable, AsyncIterator
from dataclasses import dataclass, field
from datetime import datetime
import logging
import os
from ..utils import FileWriter
from ..utils.retry import retry_with_exponential_backoff, CircuitBreaker, CircuitBreakerError
from ..utils.llm_client_pool import get_llm_client

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
        
        # Production-ready enhancements
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=int(os.getenv('LLM_CIRCUIT_BREAKER_THRESHOLD', '5')),
            recovery_timeout=float(os.getenv('LLM_CIRCUIT_BREAKER_TIMEOUT', '60.0')),
            half_open_attempts=int(os.getenv('LLM_CIRCUIT_BREAKER_HALF_OPEN', '3'))
        )
        self.max_retries = int(os.getenv('LLM_MAX_RETRIES', '3'))
        self.retry_initial_delay = float(os.getenv('LLM_RETRY_INITIAL_DELAY', '1.0'))
        self.retry_max_delay = float(os.getenv('LLM_RETRY_MAX_DELAY', '60.0'))
        
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
        timeout: int = 300,
        stream: bool = True,
        stream_callback: Optional[Callable[[str], None]] = None
    ) -> Dict[str, Any]:
        """
        Execute AI task using local llama-server.
        All processing happens locally via OpenAI-compatible API.
        
        Args:
            prompt: The user prompt
            files: Optional list of file paths to include in context
            timeout: Timeout in seconds
            stream: Whether to use streaming responses (default: True for better UX)
            stream_callback: Optional callback function for streaming chunks
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
                    "Ensure your local LLM server is running on port 8080"
                )
                logger.error(f"[{self.agent_id}] {error_msg}")
                return {
                    "success": False,
                    "error": error_msg
                }
            
            logger.info(f"[{self.agent_id}] Using local llama-server at {api_base}")
            
            # Wrap with retry logic and circuit breaker
            try:
                return await retry_with_exponential_backoff(
                    self.circuit_breaker.call(self._call_local_llama_server),
                    system_prompt,
                    full_prompt,
                    timeout,
                    0,  # retry_count
                    stream,
                    stream_callback,
                    max_attempts=self.max_retries,
                    initial_delay=self.retry_initial_delay,
                    max_delay=self.retry_max_delay,
                    retriable_exceptions=(asyncio.TimeoutError, ConnectionError, OSError),
                    non_retriable_exceptions=(CircuitBreakerError, ValueError, TypeError)
                )
            except CircuitBreakerError as e:
                logger.error(f"[{self.agent_id}] Circuit breaker is open: {e}")
                return {
                    "success": False,
                    "error": f"LLM service is temporarily unavailable (circuit breaker open). Please try again later."
                }
            
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
    
    async def _call_local_llama_server(self, system_prompt: str, user_prompt: str, timeout: int, retry_count: int = 0, stream: bool = False, stream_callback: Optional[Callable[[str], None]] = None) -> Dict[str, Any]:
        """Call local llama-server using OpenAI-compatible API with automatic retry on context size errors and streaming support"""
        try:
            import re
            
            api_base = os.getenv('OPENAI_API_BASE', 'http://127.0.0.1:8080/v1')
            model = os.getenv('OPENAI_API_MODEL', 'devstral')
            temperature = float(os.getenv('OPENAI_TEMPERATURE', '0.7'))
            max_tokens = int(os.getenv('OPENAI_MAX_TOKENS', '2048'))
            
            # Get client from connection pool
            client = await get_llm_client(
                api_base=api_base,
                timeout=timeout
            )
            
            logger.info(f"[{self.agent_id}] Calling local llama-server with model: {model} (attempt {retry_count + 1}, stream: {stream})")
            
            # Make the API call
            if stream:
                # Streaming response
                response = await asyncio.wait_for(
                    client.chat.completions.create(
                        model=model,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ],
                        temperature=temperature,
                        max_tokens=max_tokens,
                        stream=True
                    ),
                    timeout=timeout
                )
                
                # Collect streamed chunks
                content_chunks = []
                async for chunk in response:
                    if chunk.choices[0].delta.content:
                        chunk_content = chunk.choices[0].delta.content
                        content_chunks.append(chunk_content)
                        
                        # Call stream callback if provided
                        if stream_callback:
                            try:
                                stream_callback(chunk_content)
                            except Exception as e:
                                logger.warning(f"[{self.agent_id}] Stream callback error: {e}")
                        
                        # Yield to allow other coroutines to process
                        await asyncio.sleep(0)
                
                content = ''.join(content_chunks)
            else:
                # Non-streaming response
                response = await asyncio.wait_for(
                    client.chat.completions.create(
                        model=model,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ],
                        temperature=temperature,
                        max_tokens=max_tokens
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
                            truncated_system, truncated_user, timeout, retry_count=1, stream=stream, stream_callback=stream_callback
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
