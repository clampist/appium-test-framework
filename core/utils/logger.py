"""
Logger Utility
Logger utility class, providing unified logging functionality
"""

import os
import sys
from datetime import datetime
from typing import Optional
from loguru import logger


class Log:
    """Static logger utility class"""
    
    _initialized = False
    
    @classmethod
    def _get_caller_info(cls):
        """Get caller information"""
        import inspect
        
        # Get call stack
        stack = inspect.stack()
        
        # Find first non-logger caller
        caller_frame = None
        for frame_info in stack[1:]:  # Skip current frame
            if 'logger.py' not in frame_info.filename and 'core.utils.logger' not in frame_info.filename:
                caller_frame = frame_info
                break
        
        if caller_frame is None:
            # If not found, use second frame in stack (skip current method)
            caller_frame = stack[2] if len(stack) > 2 else stack[1]
        
        # Extract cleaner filename
        filename = caller_frame.filename
        if filename.endswith('.py'):
            filename = filename[:-3]  # Remove .py extension
        
        # Get relative path, remove project root directory
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        if filename.startswith(project_root):
            filename = filename[len(project_root):].lstrip('/')
        
        # Replace path separators with dots
        filename = filename.replace('/', '.').replace('\\', '.')
        
        return {
            'name': filename,
            'function': caller_frame.function,
            'line': caller_frame.lineno
        }
    
    @classmethod
    def _ensure_initialized(cls):
        """Ensure logging system is initialized"""
        if not cls._initialized:
            cls._setup_logger()
            cls._initialized = True
    
    @classmethod
    def _setup_logger(cls):
        """Setup logging configuration"""
        # Remove default log handlers
        logger.remove()
        
        # Create log directory
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        
        # Console output format
        console_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{extra[name]}</cyan>:<cyan>{extra[function]}</cyan>:<cyan>{extra[line]}</cyan> | "
            "<level>{message}</level>"
        )
        
        # File output format
        file_format = (
            "{time:YYYY-MM-DD HH:mm:ss} | "
            "{level: <8} | "
            "{extra[name]}:{extra[function]}:{extra[line]} | "
            "{message}"
        )
        
        # Add console handler
        logger.add(
            sys.stdout,
            format=console_format,
            level="INFO",
            colorize=True
        )
        
        # Add file handler (split by date)
        logger.add(
            f"{log_dir}/atf_{datetime.now().strftime('%Y%m%d')}.log",
            format=file_format,
            level="DEBUG",
            rotation="1 day",
            retention="30 days",
            compression="zip"
        )
        
        # Add error log file
        logger.add(
            f"{log_dir}/atf_error_{datetime.now().strftime('%Y%m%d')}.log",
            format=file_format,
            level="ERROR",
            rotation="1 day",
            retention="30 days",
            compression="zip"
        )
    
    @classmethod
    def debug(cls, message: str, *args, **kwargs):
        """Log debug message"""
        cls._ensure_initialized()
        caller_info = cls._get_caller_info()
        logger.bind(**caller_info).debug(message, *args, **kwargs)
    
    @classmethod
    def info(cls, message: str, *args, **kwargs):
        """Log info message"""
        cls._ensure_initialized()
        caller_info = cls._get_caller_info()
        logger.bind(**caller_info).info(message, *args, **kwargs)
    
    @classmethod
    def warning(cls, message: str, *args, **kwargs):
        """Log warning message"""
        cls._ensure_initialized()
        caller_info = cls._get_caller_info()
        logger.bind(**caller_info).warning(message, *args, **kwargs)
    
    @classmethod
    def warn(cls, message: str, *args, **kwargs):
        """Log warning message (alias)"""
        cls.warning(message, *args, **kwargs)
    
    @classmethod
    def error(cls, message: str, *args, **kwargs):
        """Log error message"""
        cls._ensure_initialized()
        caller_info = cls._get_caller_info()
        logger.bind(**caller_info).error(message, *args, **kwargs)
    
    @classmethod
    def critical(cls, message: str, *args, **kwargs):
        """Log critical error message"""
        cls._ensure_initialized()
        caller_info = cls._get_caller_info()
        logger.bind(**caller_info).critical(message, *args, **kwargs)
    
    @classmethod
    def exception(cls, message: str, *args, **kwargs):
        """Log exception message (includes stack trace)"""
        cls._ensure_initialized()
        caller_info = cls._get_caller_info()
        logger.bind(**caller_info).exception(message, *args, **kwargs)
    
    @classmethod
    def success(cls, message: str, *args, **kwargs):
        """Log success message"""
        cls._ensure_initialized()
        caller_info = cls._get_caller_info()
        logger.bind(**caller_info).success(message, *args, **kwargs)
    

    
    @classmethod
    def set_level(cls, level: str):
        """Set log level"""
        cls._ensure_initialized()
        logger.remove()
        cls._setup_logger()
        # Reset level
        for handler in logger._core.handlers.values():
            handler.levelno = logger.level(level).no
    
    @classmethod
    def add_file_handler(cls, filepath: str, level: str = "INFO", rotation: str = "1 day"):
        """Add file log handler"""
        cls._ensure_initialized()
        file_format = (
            "{time:YYYY-MM-DD HH:mm:ss} | "
            "{level: <8} | "
            "{name}:{function}:{line} | "
            "{message}"
        )
        
        logger.add(
            filepath,
            format=file_format,
            level=level,
            rotation=rotation,
            retention="30 days",
            compression="zip"
        )
