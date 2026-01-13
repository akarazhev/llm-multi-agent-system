import os
import yaml
import json
from typing import Dict, Any, Optional
from pathlib import Path
from dataclasses import dataclass, field
from dotenv import load_dotenv


@dataclass
class Settings:
    cursor_workspace: str
    log_level: str = "INFO"
    log_file: Optional[str] = None
    
    agents: Dict[str, Any] = field(default_factory=dict)
    
    llm_timeout: int = 300
    
    max_concurrent_agents: int = 5
    task_retry_attempts: int = 3
    task_timeout: int = 600
    
    enable_message_bus: bool = True
    enable_task_persistence: bool = False
    
    output_directory: str = "./output"
    
    @classmethod
    def from_dict(cls, config: Dict[str, Any]) -> 'Settings':
        return cls(
            cursor_workspace=config.get('cursor_workspace', os.getcwd()),
            log_level=config.get('log_level', 'INFO'),
            log_file=config.get('log_file'),
            agents=config.get('agents', {}),
            llm_timeout=config.get('llm_timeout', config.get('cursor_timeout', 300)),
            max_concurrent_agents=config.get('max_concurrent_agents', 5),
            task_retry_attempts=config.get('task_retry_attempts', 3),
            task_timeout=config.get('task_timeout', 600),
            enable_message_bus=config.get('enable_message_bus', True),
            enable_task_persistence=config.get('enable_task_persistence', False),
            output_directory=config.get('output_directory', './output')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'cursor_workspace': self.cursor_workspace,
            'log_level': self.log_level,
            'log_file': self.log_file,
            'agents': self.agents,
            'llm_timeout': self.llm_timeout,
            'max_concurrent_agents': self.max_concurrent_agents,
            'task_retry_attempts': self.task_retry_attempts,
            'task_timeout': self.task_timeout,
            'enable_message_bus': self.enable_message_bus,
            'enable_task_persistence': self.enable_task_persistence,
            'output_directory': self.output_directory
        }


def load_config(config_path: Optional[str] = None) -> Settings:
    # Load .env file to make environment variables available
    load_dotenv()
    
    if config_path is None:
        config_path = os.getenv('AGENT_CONFIG_PATH', 'config.yaml')
    
    config_file = Path(config_path)
    
    if not config_file.exists():
        return Settings(cursor_workspace=os.getcwd())
    
    with open(config_file, 'r') as f:
        if config_file.suffix in ['.yaml', '.yml']:
            config_data = yaml.safe_load(f)
        elif config_file.suffix == '.json':
            config_data = json.load(f)
        else:
            raise ValueError(f"Unsupported config file format: {config_file.suffix}")
    
    # Resolve cursor_workspace path to absolute path
    if 'cursor_workspace' in config_data:
        workspace_path = Path(config_data['cursor_workspace'])
        if not workspace_path.is_absolute():
            # Resolve relative to config file location
            config_dir = config_file.parent.absolute()
            workspace_path = (config_dir / workspace_path).resolve()
        config_data['cursor_workspace'] = str(workspace_path)
    
    # Also check environment variable for workspace
    env_workspace = os.getenv('CURSOR_WORKSPACE')
    if env_workspace:
        workspace_path = Path(env_workspace)
        if not workspace_path.is_absolute():
            workspace_path = Path.cwd() / workspace_path
        config_data['cursor_workspace'] = str(workspace_path.resolve())
    
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
