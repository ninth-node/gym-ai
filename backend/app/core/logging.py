"""
Centralized logging configuration for the application.
Provides structured JSON logging with rotation and different handlers.
"""

import os
import json
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from datetime import datetime
from typing import Any, Dict, Optional
from pythonjsonlogger import jsonlogger


# Create logs directory if it doesn't exist
LOGS_DIR = Path("/app/logs")
LOGS_DIR.mkdir(exist_ok=True)


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Custom JSON formatter with additional context."""

    def add_fields(self, log_record: Dict[str, Any], record: logging.LogRecord, message_dict: Dict[str, Any]):
        super().add_fields(log_record, record, message_dict)

        # Add timestamp
        log_record['timestamp'] = datetime.utcnow().isoformat()

        # Add log level
        log_record['level'] = record.levelname

        # Add logger name
        log_record['logger'] = record.name

        # Add file and line number
        log_record['file'] = record.filename
        log_record['line'] = record.lineno

        # Add function name
        if record.funcName:
            log_record['function'] = record.funcName

        # Add environment
        log_record['environment'] = os.getenv('ENVIRONMENT', 'development')


def setup_logging(
    log_level: str = None,
    enable_console: bool = True,
    enable_file: bool = True,
    enable_json: bool = True
) -> logging.Logger:
    """
    Setup application logging with multiple handlers.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        enable_console: Enable console output
        enable_file: Enable file output
        enable_json: Use JSON formatting

    Returns:
        Configured logger instance
    """
    # Determine log level from environment or parameter
    if log_level is None:
        log_level = os.getenv('LOG_LEVEL', 'INFO').upper()

    level = getattr(logging, log_level, logging.INFO)

    # Create root logger
    logger = logging.getLogger()
    logger.setLevel(level)

    # Remove existing handlers
    logger.handlers.clear()

    # Create formatters
    if enable_json:
        formatter = CustomJsonFormatter(
            '%(timestamp)s %(level)s %(logger)s %(message)s'
        )
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    # Console handler (stdout)
    if enable_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # File handlers
    if enable_file:
        # General application log (rotating by size)
        app_log_file = LOGS_DIR / "app.log"
        file_handler = RotatingFileHandler(
            app_log_file,
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Error log (only errors and critical)
        error_log_file = LOGS_DIR / "error.log"
        error_handler = RotatingFileHandler(
            error_log_file,
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        logger.addHandler(error_handler)

        # AI agent log (for agent-specific logging)
        agent_log_file = LOGS_DIR / "agents.log"
        agent_handler = TimedRotatingFileHandler(
            agent_log_file,
            when='midnight',
            interval=1,
            backupCount=30  # Keep 30 days
        )
        agent_handler.setLevel(level)
        agent_handler.setFormatter(formatter)

        # Create named logger for agents
        agent_logger = logging.getLogger('agents')
        agent_logger.addHandler(agent_handler)

    logger.info("Logging configured successfully", extra={
        'log_level': log_level,
        'console_enabled': enable_console,
        'file_enabled': enable_file,
        'json_enabled': enable_json
    })

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the given name.

    Args:
        name: Logger name (usually __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(name)


class StructuredLogger:
    """
    Helper class for structured logging with context.
    """

    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.context: Dict[str, Any] = {}

    def add_context(self, **kwargs):
        """Add context that will be included in all log messages."""
        self.context.update(kwargs)

    def clear_context(self):
        """Clear all context."""
        self.context.clear()

    def _log(self, level: int, message: str, **kwargs):
        """Internal log method with context."""
        extra = {**self.context, **kwargs}
        self.logger.log(level, message, extra=extra)

    def debug(self, message: str, **kwargs):
        """Log debug message."""
        self._log(logging.DEBUG, message, **kwargs)

    def info(self, message: str, **kwargs):
        """Log info message."""
        self._log(logging.INFO, message, **kwargs)

    def warning(self, message: str, **kwargs):
        """Log warning message."""
        self._log(logging.WARNING, message, **kwargs)

    def error(self, message: str, **kwargs):
        """Log error message."""
        self._log(logging.ERROR, message, **kwargs)

    def critical(self, message: str, **kwargs):
        """Log critical message."""
        self._log(logging.CRITICAL, message, **kwargs)

    def exception(self, message: str, **kwargs):
        """Log exception with traceback."""
        extra = {**self.context, **kwargs}
        self.logger.exception(message, extra=extra)


# Initialize logging on module import
setup_logging()
