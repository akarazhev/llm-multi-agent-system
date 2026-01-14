"""
Structured logging utilities for production-ready observability.
"""
import logging
import json
import sys
from typing import Any, Dict, Optional
from datetime import datetime
import uuid
from contextvars import ContextVar

# Context variable for correlation ID
correlation_id_ctx: ContextVar[Optional[str]] = ContextVar('correlation_id', default=None)


class StructuredFormatter(logging.Formatter):
    """
    JSON formatter for structured logging.
    Outputs logs in JSON format for easy parsing by log aggregation systems.
    """
    
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }
        
        # Add correlation ID if available
        correlation_id = correlation_id_ctx.get()
        if correlation_id:
            log_data['correlation_id'] = correlation_id
        
        # Add extra fields
        if hasattr(record, 'agent_id'):
            log_data['agent_id'] = record.agent_id
        
        if hasattr(record, 'task_id'):
            log_data['task_id'] = record.task_id
        
        if hasattr(record, 'workflow_id'):
            log_data['workflow_id'] = record.workflow_id
        
        if hasattr(record, 'duration_ms'):
            log_data['duration_ms'] = record.duration_ms
        
        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = {
                'type': record.exc_info[0].__name__ if record.exc_info[0] else None,
                'message': str(record.exc_info[1]) if record.exc_info[1] else None,
                'traceback': self.formatException(record.exc_info)
            }
        
        # Add any custom extra fields
        for key, value in record.__dict__.items():
            if key not in ['name', 'msg', 'args', 'created', 'filename', 'funcName',
                          'levelname', 'lineno', 'module', 'msecs', 'message',
                          'pathname', 'process', 'processName', 'relativeCreated',
                          'thread', 'threadName', 'exc_info', 'exc_text', 'stack_info',
                          'agent_id', 'task_id', 'workflow_id', 'duration_ms']:
                if not key.startswith('_'):
                    try:
                        # Only include JSON-serializable values
                        json.dumps({key: value})
                        log_data[key] = value
                    except (TypeError, ValueError):
                        pass
        
        return json.dumps(log_data)


class ColoredConsoleFormatter(logging.Formatter):
    """
    Colored formatter for console output.
    Makes logs more readable during development.
    """
    
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record: logging.LogRecord) -> str:
        # Add color to level name
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{self.RESET}"
        
        # Format the message
        formatted = super().format(record)
        
        # Reset levelname for future formatters
        record.levelname = levelname
        
        return formatted


def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    json_format: bool = False,
    colored_console: bool = True
) -> None:
    """
    Setup production-ready logging configuration.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path for file logging
        json_format: Use JSON format for structured logging
        colored_console: Use colored output for console (dev mode)
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))
    
    # Remove existing handlers
    root_logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper()))
    
    if json_format:
        console_handler.setFormatter(StructuredFormatter())
    elif colored_console:
        console_handler.setFormatter(ColoredConsoleFormatter(
            fmt='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        ))
    else:
        console_handler.setFormatter(logging.Formatter(
            fmt='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        ))
    
    root_logger.addHandler(console_handler)
    
    # File handler (always JSON for easy parsing)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(getattr(logging, level.upper()))
        file_handler.setFormatter(StructuredFormatter())
        root_logger.addHandler(file_handler)
    
    logging.info(f"Logging configured: level={level}, file={log_file}, json={json_format}")


def set_correlation_id(correlation_id: Optional[str] = None) -> str:
    """
    Set correlation ID for the current context.
    Useful for tracking requests across multiple services/agents.
    
    Args:
        correlation_id: Optional correlation ID (generates UUID if not provided)
    
    Returns:
        The correlation ID that was set
    """
    if correlation_id is None:
        correlation_id = str(uuid.uuid4())
    
    correlation_id_ctx.set(correlation_id)
    return correlation_id


def get_correlation_id() -> Optional[str]:
    """Get the current correlation ID"""
    return correlation_id_ctx.get()


def clear_correlation_id():
    """Clear the correlation ID"""
    correlation_id_ctx.set(None)


class ContextLogger:
    """
    Logger with automatic context injection (agent_id, task_id, etc.).
    """
    
    def __init__(self, name: str, **default_context):
        self.logger = logging.getLogger(name)
        self.default_context = default_context
    
    def _log(self, level: int, msg: str, **extra_context):
        """Internal logging method with context injection"""
        context = {**self.default_context, **extra_context}
        
        # Create LogRecord with extra fields
        if context:
            self.logger.log(level, msg, extra=context)
        else:
            self.logger.log(level, msg)
    
    def debug(self, msg: str, **extra_context):
        self._log(logging.DEBUG, msg, **extra_context)
    
    def info(self, msg: str, **extra_context):
        self._log(logging.INFO, msg, **extra_context)
    
    def warning(self, msg: str, **extra_context):
        self._log(logging.WARNING, msg, **extra_context)
    
    def error(self, msg: str, exc_info=None, **extra_context):
        if exc_info:
            self.logger.error(msg, exc_info=exc_info, extra=extra_context)
        else:
            self._log(logging.ERROR, msg, **extra_context)
    
    def critical(self, msg: str, exc_info=None, **extra_context):
        if exc_info:
            self.logger.critical(msg, exc_info=exc_info, extra=extra_context)
        else:
            self._log(logging.CRITICAL, msg, **extra_context)
