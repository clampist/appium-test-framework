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
    def _get_caller_info(cls):
        """获取调用者信息"""
        import inspect
        
        # 获取调用栈
        stack = inspect.stack()
        
        # 查找第一个非logger的调用者
        caller_frame = None
        for frame_info in stack[1:]:  # 跳过当前帧
            if 'logger.py' not in frame_info.filename and 'core.utils.logger' not in frame_info.filename:
                caller_frame = frame_info
                break
        
        if caller_frame is None:
            # 如果找不到，使用栈中的第二个帧（跳过当前方法）
            caller_frame = stack[2] if len(stack) > 2 else stack[1]
        
        # 提取更清晰的文件名
        filename = caller_frame.filename
        if filename.endswith('.py'):
            filename = filename[:-3]  # 移除.py后缀
        
        # 获取相对路径，去掉项目根目录
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        if filename.startswith(project_root):
            filename = filename[len(project_root):].lstrip('/')
        
        # 将路径分隔符替换为点
        filename = filename.replace('/', '.').replace('\\', '.')
        
        return {
            'name': filename,
            'function': caller_frame.function,
            'line': caller_frame.lineno
        }
    
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
            "<cyan>{extra[name]}</cyan>:<cyan>{extra[function]}</cyan>:<cyan>{extra[line]}</cyan> | "
            "<level>{message}</level>"
        )
        
        # 文件输出格式
        file_format = (
            "{time:YYYY-MM-DD HH:mm:ss} | "
            "{level: <8} | "
            "{extra[name]}:{extra[function]}:{extra[line]} | "
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
        caller_info = cls._get_caller_info()
        logger.bind(**caller_info).debug(message, *args, **kwargs)
    
    @classmethod
    def info(cls, message: str, *args, **kwargs):
        """记录信息日志"""
        cls._ensure_initialized()
        caller_info = cls._get_caller_info()
        logger.bind(**caller_info).info(message, *args, **kwargs)
    
    @classmethod
    def warning(cls, message: str, *args, **kwargs):
        """记录警告日志"""
        cls._ensure_initialized()
        caller_info = cls._get_caller_info()
        logger.bind(**caller_info).warning(message, *args, **kwargs)
    
    @classmethod
    def warn(cls, message: str, *args, **kwargs):
        """记录警告日志（别名）"""
        cls.warning(message, *args, **kwargs)
    
    @classmethod
    def error(cls, message: str, *args, **kwargs):
        """记录错误日志"""
        cls._ensure_initialized()
        caller_info = cls._get_caller_info()
        logger.bind(**caller_info).error(message, *args, **kwargs)
    
    @classmethod
    def critical(cls, message: str, *args, **kwargs):
        """记录严重错误日志"""
        cls._ensure_initialized()
        caller_info = cls._get_caller_info()
        logger.bind(**caller_info).critical(message, *args, **kwargs)
    
    @classmethod
    def exception(cls, message: str, *args, **kwargs):
        """记录异常日志（包含堆栈信息）"""
        cls._ensure_initialized()
        caller_info = cls._get_caller_info()
        logger.bind(**caller_info).exception(message, *args, **kwargs)
    
    @classmethod
    def success(cls, message: str, *args, **kwargs):
        """记录成功日志"""
        cls._ensure_initialized()
        caller_info = cls._get_caller_info()
        logger.bind(**caller_info).success(message, *args, **kwargs)
    

    
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
