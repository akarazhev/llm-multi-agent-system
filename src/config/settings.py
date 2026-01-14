import os
import yaml
import json
from typing import Dict, Any, Optional, List
from pathlib import Path
from dataclasses import dataclass, field
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)


class ConfigValidationError(Exception):
    """Raised when configuration validation fails"""
    pass


@dataclass
class Settings:
    workspace: str
    log_level: str = "INFO"
    log_file: Optional[str] = None
    
    agents: Dict[str, Any] = field(default_factory=dict)
    
    # LLM Configuration
    llm_timeout: int = 300
    llm_max_retries: int = 3
    llm_retry_initial_delay: float = 1.0
    llm_retry_max_delay: float = 60.0
    llm_circuit_breaker_threshold: int = 5
    llm_circuit_breaker_timeout: float = 60.0
    llm_stream_responses: bool = True
    
    # Orchestration Configuration
    max_concurrent_agents: int = 5
    task_retry_attempts: int = 3
    task_timeout: int = 600
    
    enable_message_bus: bool = True
    enable_task_persistence: bool = False
    enable_structured_logging: bool = True
    enable_metrics: bool = True
    
    output_directory: str = "./output"
    database_url: str = "postgresql+asyncpg://postgres:password@localhost:5432/llm_agents"
    keycloak: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate settings after initialization"""
        self.validate()
    
    def validate(self) -> None:
        """
        Validate configuration settings.
        
        Raises:
            ConfigValidationError: If validation fails
        """
        errors: List[str] = []
        
        # Validate workspace
        if not self.workspace:
            errors.append("workspace cannot be empty")
        elif not Path(self.workspace).exists():
            logger.warning(f"Workspace directory does not exist: {self.workspace}")
        
        # Validate log level
        valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if self.log_level.upper() not in valid_log_levels:
            errors.append(f"log_level must be one of {valid_log_levels}, got '{self.log_level}'")
        
        # Validate timeouts
        if self.llm_timeout <= 0:
            errors.append(f"llm_timeout must be positive, got {self.llm_timeout}")
        
        if self.task_timeout <= 0:
            errors.append(f"task_timeout must be positive, got {self.task_timeout}")
        
        # Validate retry configuration
        if self.llm_max_retries < 0:
            errors.append(f"llm_max_retries cannot be negative, got {self.llm_max_retries}")
        
        if self.llm_max_retries > 10:
            logger.warning(f"llm_max_retries is very high ({self.llm_max_retries}), consider reducing")
        
        if self.llm_retry_initial_delay <= 0:
            errors.append(f"llm_retry_initial_delay must be positive, got {self.llm_retry_initial_delay}")
        
        if self.llm_retry_max_delay <= self.llm_retry_initial_delay:
            errors.append(f"llm_retry_max_delay ({self.llm_retry_max_delay}) must be greater than llm_retry_initial_delay ({self.llm_retry_initial_delay})")
        
        # Validate circuit breaker configuration
        if self.llm_circuit_breaker_threshold <= 0:
            errors.append(f"llm_circuit_breaker_threshold must be positive, got {self.llm_circuit_breaker_threshold}")
        
        if self.llm_circuit_breaker_timeout <= 0:
            errors.append(f"llm_circuit_breaker_timeout must be positive, got {self.llm_circuit_breaker_timeout}")
        
        # Validate concurrent agents
        if self.max_concurrent_agents <= 0:
            errors.append(f"max_concurrent_agents must be positive, got {self.max_concurrent_agents}")
        
        if self.max_concurrent_agents > 20:
            logger.warning(f"max_concurrent_agents is very high ({self.max_concurrent_agents}), this may cause resource issues")
        
        # Validate task retry attempts
        if self.task_retry_attempts < 0:
            errors.append(f"task_retry_attempts cannot be negative, got {self.task_retry_attempts}")
        
        # Validate output directory
        if not self.output_directory:
            errors.append("output_directory cannot be empty")

        # Validate database URL
        if not self.database_url:
            errors.append("database_url cannot be empty")
        
        # Raise all errors at once
        if errors:
            raise ConfigValidationError(
                f"Configuration validation failed:\n" + "\n".join(f"  - {error}" for error in errors)
            )
    
    @classmethod
    def from_dict(cls, config: Dict[str, Any]) -> 'Settings':
        return cls(
            workspace=config.get('workspace', config.get('cursor_workspace', os.getcwd())),
            log_level=config.get('log_level', 'INFO'),
            log_file=config.get('log_file'),
            agents=config.get('agents', {}),
            llm_timeout=config.get('llm_timeout', config.get('cursor_timeout', 300)),
            llm_max_retries=config.get('llm_max_retries', 3),
            llm_retry_initial_delay=config.get('llm_retry_initial_delay', 1.0),
            llm_retry_max_delay=config.get('llm_retry_max_delay', 60.0),
            llm_circuit_breaker_threshold=config.get('llm_circuit_breaker_threshold', 5),
            llm_circuit_breaker_timeout=config.get('llm_circuit_breaker_timeout', 60.0),
            llm_stream_responses=config.get('llm_stream_responses', True),
            max_concurrent_agents=config.get('max_concurrent_agents', 5),
            task_retry_attempts=config.get('task_retry_attempts', 3),
            task_timeout=config.get('task_timeout', 600),
            enable_message_bus=config.get('enable_message_bus', True),
            enable_task_persistence=config.get('enable_task_persistence', False),
            enable_structured_logging=config.get('enable_structured_logging', True),
            enable_metrics=config.get('enable_metrics', True),
            output_directory=config.get('output_directory', './output'),
            database_url=config.get('database_url', 'postgresql+asyncpg://postgres:password@localhost:5432/llm_agents'),
            keycloak=config.get('keycloak', {})
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'workspace': self.workspace,
            'log_level': self.log_level,
            'log_file': self.log_file,
            'agents': self.agents,
            'llm_timeout': self.llm_timeout,
            'llm_max_retries': self.llm_max_retries,
            'llm_retry_initial_delay': self.llm_retry_initial_delay,
            'llm_retry_max_delay': self.llm_retry_max_delay,
            'llm_circuit_breaker_threshold': self.llm_circuit_breaker_threshold,
            'llm_circuit_breaker_timeout': self.llm_circuit_breaker_timeout,
            'llm_stream_responses': self.llm_stream_responses,
            'max_concurrent_agents': self.max_concurrent_agents,
            'task_retry_attempts': self.task_retry_attempts,
            'task_timeout': self.task_timeout,
            'enable_message_bus': self.enable_message_bus,
            'enable_task_persistence': self.enable_task_persistence,
            'enable_structured_logging': self.enable_structured_logging,
            'enable_metrics': self.enable_metrics,
            'output_directory': self.output_directory,
            'database_url': self.database_url,
            'keycloak': self.keycloak
        }


def load_config(config_path: Optional[str] = None) -> Settings:
    # Load .env file to make environment variables available
    load_dotenv()
    
    if config_path is None:
        config_path = os.getenv('AGENT_CONFIG_PATH', 'config.yaml')
    
    config_file = Path(config_path)
    
    if not config_file.exists():
        return Settings(workspace=os.getcwd())
    
    with open(config_file, 'r') as f:
        if config_file.suffix in ['.yaml', '.yml']:
            config_data = yaml.safe_load(f)
        elif config_file.suffix == '.json':
            config_data = json.load(f)
        else:
            raise ValueError(f"Unsupported config file format: {config_file.suffix}")
    
    # Resolve workspace path to absolute path
    workspace_key = 'workspace' if 'workspace' in config_data else 'cursor_workspace'
    if workspace_key in config_data:
        workspace_path = Path(config_data[workspace_key])
        if not workspace_path.is_absolute():
            # Resolve relative to config file location
            config_dir = config_file.parent.absolute()
            workspace_path = (config_dir / workspace_path).resolve()
        config_data['workspace'] = str(workspace_path)
        if 'cursor_workspace' in config_data:
            del config_data['cursor_workspace']
    
    # Also check environment variable for workspace
    env_workspace = os.getenv('WORKSPACE') or os.getenv('CURSOR_WORKSPACE')
    if env_workspace:
        workspace_path = Path(env_workspace)
        if not workspace_path.is_absolute():
            workspace_path = Path.cwd() / workspace_path
        config_data['workspace'] = str(workspace_path.resolve())
    
    return Settings.from_dict(config_data)


def save_config(settings: Settings, config_path: str = 'config.yaml') -> None:
    config_file = Path(config_path)
    
    with open(config_file, 'w') as f:
        if config_file.suffix in ['.yaml', '.yml']:
            yaml.dump(settings.to_dict(), f, default_flow_style=False)
        elif config_file.suffix == '.json':
            json.dump(settings.to_dict(), f, indent=2)
        else:
            raise ValueError(f"Unsupported config file format: {config_file.suffix}")
