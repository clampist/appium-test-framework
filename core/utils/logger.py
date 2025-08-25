"""
Logger Utility
日志工具类，提供统一的日志记录功能
"""

import os
import sys
from datetime import datetime
from typing import Optional
from loguru import logger


class Log:
    """静态日志工具类"""
    
    _initialized = False
    
    @classmethod
    def _ensure_initialized(cls):
        """确保日志系统已初始化"""
        if not cls._initialized:
            cls._setup_logger()
            cls._initialized = True
    
    @classmethod
    def _setup_logger(cls):
        """设置日志配置"""
        # 移除默认的日志处理器
        logger.remove()
        
        # 创建日志目录
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        
        # 控制台输出格式
        console_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        )
        
        # 文件输出格式
        file_format = (
            "{time:YYYY-MM-DD HH:mm:ss} | "
            "{level: <8} | "
            "{name}:{function}:{line} | "
            "{message}"
        )
        
        # 添加控制台处理器
        logger.add(
            sys.stdout,
            format=console_format,
            level="INFO",
            colorize=True
        )
        
        # 添加文件处理器（按日期分割）
        logger.add(
            f"{log_dir}/atf_{datetime.now().strftime('%Y%m%d')}.log",
            format=file_format,
            level="DEBUG",
            rotation="1 day",
            retention="30 days",
            compression="zip"
        )
        
        # 添加错误日志文件
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
        """记录调试日志"""
        cls._ensure_initialized()
        logger.debug(message, *args, **kwargs)
    
    @classmethod
    def info(cls, message: str, *args, **kwargs):
        """记录信息日志"""
        cls._ensure_initialized()
        logger.info(message, *args, **kwargs)
    
    @classmethod
    def warning(cls, message: str, *args, **kwargs):
        """记录警告日志"""
        cls._ensure_initialized()
        logger.warning(message, *args, **kwargs)
    
    @classmethod
    def warn(cls, message: str, *args, **kwargs):
        """记录警告日志（别名）"""
        cls.warning(message, *args, **kwargs)
    
    @classmethod
    def error(cls, message: str, *args, **kwargs):
        """记录错误日志"""
        cls._ensure_initialized()
        logger.error(message, *args, **kwargs)
    
    @classmethod
    def critical(cls, message: str, *args, **kwargs):
        """记录严重错误日志"""
        cls._ensure_initialized()
        logger.critical(message, *args, **kwargs)
    
    @classmethod
    def exception(cls, message: str, *args, **kwargs):
        """记录异常日志（包含堆栈信息）"""
        cls._ensure_initialized()
        logger.exception(message, *args, **kwargs)
    
    @classmethod
    def success(cls, message: str, *args, **kwargs):
        """记录成功日志"""
        cls._ensure_initialized()
        logger.success(message, *args, **kwargs)
    

    
    @classmethod
    def set_level(cls, level: str):
        """设置日志级别"""
        cls._ensure_initialized()
        logger.remove()
        cls._setup_logger()
        # 重新设置级别
        for handler in logger._core.handlers.values():
            handler.levelno = logger.level(level).no
    
    @classmethod
    def add_file_handler(cls, filepath: str, level: str = "INFO", rotation: str = "1 day"):
        """添加文件日志处理器"""
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
