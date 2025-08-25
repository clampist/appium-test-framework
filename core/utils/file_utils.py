"""
File Utilities
文件工具类，提供文件操作相关功能
"""

import os
import json
import yaml
import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

from .logger import Log


class FileUtils:
    """文件工具类"""
    
    @staticmethod
    def ensure_dir(directory: str) -> str:
        """
        确保目录存在，如果不存在则创建
        
        Args:
            directory: 目录路径
            
        Returns:
            str: 目录路径
        """
        Path(directory).mkdir(parents=True, exist_ok=True)
        return directory
    
    @staticmethod
    def read_json(filepath: str) -> Dict[str, Any]:
        """
        读取JSON文件
        
        Args:
            filepath: 文件路径
            
        Returns:
            Dict[str, Any]: JSON数据
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            Log.info(f"Successfully read JSON file: {filepath}")
            return data
        except Exception as e:
            Log.error(f"Failed to read JSON file {filepath}: {str(e)}")
            raise
    
    @staticmethod
    def write_json(filepath: str, data: Dict[str, Any], indent: int = 2):
        """
        写入JSON文件
        
        Args:
            filepath: 文件路径
            data: 要写入的数据
            indent: 缩进空格数
        """
        try:
            # 确保目录存在
            FileUtils.ensure_dir(os.path.dirname(filepath))
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=indent, ensure_ascii=False)
            Log.info(f"Successfully wrote JSON file: {filepath}")
        except Exception as e:
            Log.error(f"Failed to write JSON file {filepath}: {str(e)}")
            raise
    
    @staticmethod
    def read_yaml(filepath: str) -> Dict[str, Any]:
        """
        读取YAML文件
        
        Args:
            filepath: 文件路径
            
        Returns:
            Dict[str, Any]: YAML数据
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            Log.info(f"Successfully read YAML file: {filepath}")
            return data or {}
        except Exception as e:
            Log.error(f"Failed to read YAML file {filepath}: {str(e)}")
            raise
    
    @staticmethod
    def write_yaml(filepath: str, data: Dict[str, Any]):
        """
        写入YAML文件
        
        Args:
            filepath: 文件路径
            data: 要写入的数据
        """
        try:
            # 确保目录存在
            FileUtils.ensure_dir(os.path.dirname(filepath))
            
            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
            Log.info(f"Successfully wrote YAML file: {filepath}")
        except Exception as e:
            Log.error(f"Failed to write YAML file {filepath}: {str(e)}")
            raise
    
    @staticmethod
    def read_text(filepath: str) -> str:
        """
        读取文本文件
        
        Args:
            filepath: 文件路径
            
        Returns:
            str: 文件内容
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            Log.info(f"Successfully read text file: {filepath}")
            return content
        except Exception as e:
            Log.error(f"Failed to read text file {filepath}: {str(e)}")
            raise
    
    @staticmethod
    def write_text(filepath: str, content: str):
        """
        写入文本文件
        
        Args:
            filepath: 文件路径
            content: 要写入的内容
        """
        try:
            # 确保目录存在
            FileUtils.ensure_dir(os.path.dirname(filepath))
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            Log.info(f"Successfully wrote text file: {filepath}")
        except Exception as e:
            Log.error(f"Failed to write text file {filepath}: {str(e)}")
            raise
    
    @staticmethod
    def copy_file(src: str, dst: str):
        """
        复制文件
        
        Args:
            src: 源文件路径
            dst: 目标文件路径
        """
        try:
            # 确保目标目录存在
            FileUtils.ensure_dir(os.path.dirname(dst))
            
            shutil.copy2(src, dst)
            Log.info(f"Successfully copied file from {src} to {dst}")
        except Exception as e:
            Log.error(f"Failed to copy file from {src} to {dst}: {str(e)}")
            raise
    
    @staticmethod
    def move_file(src: str, dst: str):
        """
        移动文件
        
        Args:
            src: 源文件路径
            dst: 目标文件路径
        """
        try:
            # 确保目标目录存在
            FileUtils.ensure_dir(os.path.dirname(dst))
            
            shutil.move(src, dst)
            Log.info(f"Successfully moved file from {src} to {dst}")
        except Exception as e:
            Log.error(f"Failed to move file from {src} to {dst}: {str(e)}")
            raise
    
    @staticmethod
    def delete_file(filepath: str):
        """
        删除文件
        
        Args:
            filepath: 文件路径
        """
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                Log.info(f"Successfully deleted file: {filepath}")
            else:
                Log.warning(f"File does not exist: {filepath}")
        except Exception as e:
            Log.error(f"Failed to delete file {filepath}: {str(e)}")
            raise
    
    @staticmethod
    def list_files(directory: str, pattern: str = "*") -> List[str]:
        """
        列出目录中的文件
        
        Args:
            directory: 目录路径
            pattern: 文件匹配模式
            
        Returns:
            List[str]: 文件路径列表
        """
        try:
            files = []
            for file_path in Path(directory).glob(pattern):
                if file_path.is_file():
                    files.append(str(file_path))
            Log.info(f"Found {len(files)} files in {directory}")
            return files
        except Exception as e:
            Log.error(f"Failed to list files in {directory}: {str(e)}")
            return []
    
    @staticmethod
    def file_exists(filepath: str) -> bool:
        """
        检查文件是否存在
        
        Args:
            filepath: 文件路径
            
        Returns:
            bool: 文件是否存在
        """
        return os.path.exists(filepath)
    
    @staticmethod
    def get_file_size(filepath: str) -> int:
        """
        获取文件大小
        
        Args:
            filepath: 文件路径
            
        Returns:
            int: 文件大小（字节）
        """
        try:
            return os.path.getsize(filepath)
        except Exception as e:
            Log.error(f"Failed to get file size for {filepath}: {str(e)}")
            return 0
    
    @staticmethod
    def get_file_modified_time(filepath: str) -> datetime:
        """
        获取文件修改时间
        
        Args:
            filepath: 文件路径
            
        Returns:
            datetime: 修改时间
        """
        try:
            timestamp = os.path.getmtime(filepath)
            return datetime.fromtimestamp(timestamp)
        except Exception as e:
            Log.error(f"Failed to get file modified time for {filepath}: {str(e)}")
            raise
    
    @staticmethod
    def create_backup(filepath: str, backup_dir: str = "backups") -> str:
        """
        创建文件备份
        
        Args:
            filepath: 原文件路径
            backup_dir: 备份目录
            
        Returns:
            str: 备份文件路径
        """
        try:
            if not FileUtils.file_exists(filepath):
                raise FileNotFoundError(f"File not found: {filepath}")
            
            # 创建备份目录
            FileUtils.ensure_dir(backup_dir)
            
            # 生成备份文件名
            filename = os.path.basename(filepath)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"{timestamp}_{filename}"
            backup_path = os.path.join(backup_dir, backup_filename)
            
            # 复制文件
            FileUtils.copy_file(filepath, backup_path)
            
            Log.info(f"Created backup: {backup_path}")
            return backup_path
            
        except Exception as e:
            Log.error(f"Failed to create backup for {filepath}: {str(e)}")
            raise
