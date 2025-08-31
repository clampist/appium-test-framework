"""
Path Utilities
Path management utility class for detecting project structure
"""

import os
from typing import Optional


class PathUtils:
    """Path utility class for project structure detection"""
    
    @staticmethod
    def get_project_root() -> str:
        """
        Get project root directory
        
        Returns:
            str: Project root directory path
        """
        # First check environment variable
        project_root = os.environ.get('ATF_PROJECT_ROOT')
        if project_root:
            return project_root
        
        # Auto-detect by looking for project markers
        current_dir = os.getcwd()
        while current_dir != os.path.dirname(current_dir):  # Stop at filesystem root
            # Check for common project root indicators
            project_indicators = [
                'pytest.ini',
                'setup.py', 
                'pyproject.toml',
                'requirements.txt',
                'Makefile'
            ]
            
            for indicator in project_indicators:
                if os.path.exists(os.path.join(current_dir, indicator)):
                    return current_dir
            
            current_dir = os.path.dirname(current_dir)
        
        # Fallback to current directory
        return os.getcwd()
    
    @staticmethod
    def get_relative_path_from_root(relative_path: str) -> str:
        """
        Get absolute path from project root
        
        Args:
            relative_path: Relative path from project root
            
        Returns:
            str: Absolute path
        """
        project_root = PathUtils.get_project_root()
        return os.path.join(project_root, relative_path)
    
    @staticmethod
    def ensure_directory_exists(path: str) -> None:
        """
        Ensure directory exists, create if not
        
        Args:
            path: Directory path to ensure
        """
        os.makedirs(path, exist_ok=True)
