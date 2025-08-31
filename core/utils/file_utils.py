"""
File Utilities
File utility class, providing file operation related functionality
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
    """File utility class"""
    
    @staticmethod
    def ensure_dir(directory: str) -> str:
        """
        Ensure directory exists, create if not exists
        
        Args:
            directory: Directory path
            
        Returns:
            str: Directory path
        """
        Path(directory).mkdir(parents=True, exist_ok=True)
        return directory
    
    @staticmethod
    def read_json(filepath: str) -> Dict[str, Any]:
        """
        Read JSON file
        
        Args:
            filepath: File path
            
        Returns:
            Dict[str, Any]: JSON data
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
        Write JSON file
        
        Args:
            filepath: File path
            data: Data to write
            indent: Indentation spaces
        """
        try:
            # Ensure directory exists
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
        Read YAML file
        
        Args:
            filepath: File path
            
        Returns:
            Dict[str, Any]: YAML data
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
        Write YAML file
        
        Args:
            filepath: File path
            data: Data to write
        """
        try:
            # Ensure directory exists
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
        Read text file
        
        Args:
            filepath: File path
            
        Returns:
            str: File content
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
        Write text file
        
        Args:
            filepath: File path
            content: Content to write
        """
        try:
            # Ensure directory exists
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
        Copy file
        
        Args:
            src: Source file path
            dst: Destination file path
        """
        try:
            # Ensure destination directory exists
            FileUtils.ensure_dir(os.path.dirname(dst))
            
            shutil.copy2(src, dst)
            Log.info(f"Successfully copied file from {src} to {dst}")
        except Exception as e:
            Log.error(f"Failed to copy file from {src} to {dst}: {str(e)}")
            raise
    
    @staticmethod
    def move_file(src: str, dst: str):
        """
        Move file
        
        Args:
            src: Source file path
            dst: Destination file path
        """
        try:
            # Ensure destination directory exists
            FileUtils.ensure_dir(os.path.dirname(dst))
            
            shutil.move(src, dst)
            Log.info(f"Successfully moved file from {src} to {dst}")
        except Exception as e:
            Log.error(f"Failed to move file from {src} to {dst}: {str(e)}")
            raise
    
    @staticmethod
    def delete_file(filepath: str):
        """
        Delete file
        
        Args:
            filepath: File path
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
        List files in directory
        
        Args:
            directory: Directory path
            pattern: File matching pattern
            
        Returns:
            List[str]: List of file paths
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
        Check if file exists
        
        Args:
            filepath: File path
            
        Returns:
            bool: Whether file exists
        """
        return os.path.exists(filepath)
    
    @staticmethod
    def get_file_size(filepath: str) -> int:
        """
        Get file size
        
        Args:
            filepath: File path
            
        Returns:
            int: File size (bytes)
        """
        try:
            return os.path.getsize(filepath)
        except Exception as e:
            Log.error(f"Failed to get file size for {filepath}: {str(e)}")
            return 0
    
    @staticmethod
    def get_file_modified_time(filepath: str) -> datetime:
        """
        Get file modified time
        
        Args:
            filepath: File path
            
        Returns:
            datetime: Modified time
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
        Create file backup
        
        Args:
            filepath: Original file path
            backup_dir: Backup directory
            
        Returns:
            str: Backup file path
        """
        try:
            if not FileUtils.file_exists(filepath):
                raise FileNotFoundError(f"File not found: {filepath}")
            
            # Create backup directory
            FileUtils.ensure_dir(backup_dir)
            
            # Generate backup filename
            filename = os.path.basename(filepath)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"{timestamp}_{filename}"
            backup_path = os.path.join(backup_dir, backup_filename)
            
            # Copy file
            FileUtils.copy_file(filepath, backup_path)
            
            Log.info(f"Created backup: {backup_path}")
            return backup_path
            
        except Exception as e:
            Log.error(f"Failed to create backup for {filepath}: {str(e)}")
            raise
