"""
Application Configuration
Application configuration management class
"""

import os
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field

from ..utils.logger import Log
from ..utils.file_utils import FileUtils


@dataclass
class AppConfig:
    """Application configuration class"""
    
    # Application basic information
    app_name: str = ""
    app_version: str = ""
    app_package: str = ""
    app_activity: str = ""  # Android
    app_bundle_id: str = ""  # iOS
    app_path: str = ""
    
    # Application type
    app_type: str = "native"  # native/web/hybrid
    
    # Launch configuration
    launch_timeout: int = 30
    startup_timeout: int = 60
    
    # Permission configuration
    auto_grant_permissions: bool = True
    permissions: List[str] = field(default_factory=list)
    
    # Data configuration
    no_reset: bool = False
    full_reset: bool = False
    clear_data: bool = False
    
    # Network configuration
    network_profile: str = ""
    proxy_settings: Dict[str, Any] = field(default_factory=dict)
    
    # Other configuration
    additional_config: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Post-initialization processing"""
        # Load configuration from environment variables
        self._load_from_env()
    
    def _load_from_env(self):
        """Load configuration from environment variables"""
        env_mappings = {
            'APP_NAME': 'app_name',
            'APP_VERSION': 'app_version',
            'APP_PACKAGE': 'app_package',
            'APP_ACTIVITY': 'app_activity',
            'APP_BUNDLE_ID': 'app_bundle_id',
            'APP_PATH': 'app_path',
            'APP_TYPE': 'app_type',
            'APP_LAUNCH_TIMEOUT': 'launch_timeout',
            'APP_STARTUP_TIMEOUT': 'startup_timeout',
        }
        
        for env_var, attr_name in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                # Handle numeric types
                if attr_name in ['launch_timeout', 'startup_timeout']:
                    try:
                        value = int(value)
                    except ValueError:
                        Log.warning(f"Invalid integer value for {env_var}: {value}")
                        continue
                
                setattr(self, attr_name, value)
                Log.info(f"Loaded {attr_name} from environment variable {env_var}: {value}")
    
    def get_app_info(self) -> Dict[str, Any]:
        """
        Get application information
        
        Returns:
            Dict[str, Any]: Application information dictionary
        """
        app_info = {
            'app_name': self.app_name,
            'app_version': self.app_version,
            'app_package': self.app_package,
            'app_activity': self.app_activity,
            'app_bundle_id': self.app_bundle_id,
            'app_path': self.app_path,
            'app_type': self.app_type,
            'launch_timeout': self.launch_timeout,
            'startup_timeout': self.startup_timeout,
        }
        
        # Add additional configuration
        app_info.update(self.additional_config)
        
        return app_info
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary
        
        Returns:
            Dict[str, Any]: Configuration dictionary
        """
        return {
            'app_name': self.app_name,
            'app_version': self.app_version,
            'app_package': self.app_package,
            'app_activity': self.app_activity,
            'app_bundle_id': self.app_bundle_id,
            'app_path': self.app_path,
            'app_type': self.app_type,
            'launch_timeout': self.launch_timeout,
            'startup_timeout': self.startup_timeout,
            'auto_grant_permissions': self.auto_grant_permissions,
            'permissions': self.permissions,
            'no_reset': self.no_reset,
            'full_reset': self.full_reset,
            'clear_data': self.clear_data,
            'network_profile': self.network_profile,
            'proxy_settings': self.proxy_settings,
            'additional_config': self.additional_config,
        }
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'AppConfig':
        """
        Create configuration object from dictionary
        
        Args:
            config_dict: Configuration dictionary
            
        Returns:
            AppConfig: Configuration object
        """
        return cls(**config_dict)
    
    @classmethod
    def from_file(cls, filepath: str) -> 'AppConfig':
        """
        Load configuration from file
        
        Args:
            filepath: Configuration file path
            
        Returns:
            AppConfig: Configuration object
        """
        try:
            if filepath.endswith('.json'):
                config_dict = FileUtils.read_json(filepath)
            elif filepath.endswith('.yaml') or filepath.endswith('.yml'):
                config_dict = FileUtils.read_yaml(filepath)
            else:
                raise ValueError(f"Unsupported file format: {filepath}")
            
            Log.info(f"Loaded app config from file: {filepath}")
            return cls.from_dict(config_dict)
            
        except Exception as e:
            Log.error(f"Failed to load app config from file {filepath}: {str(e)}")
            raise
    
    def save_to_file(self, filepath: str):
        """
        Save configuration to file
        
        Args:
            filepath: File path
        """
        try:
            config_dict = self.to_dict()
            
            if filepath.endswith('.json'):
                FileUtils.write_json(filepath, config_dict)
            elif filepath.endswith('.yaml') or filepath.endswith('.yml'):
                FileUtils.write_yaml(filepath, config_dict)
            else:
                raise ValueError(f"Unsupported file format: {filepath}")
            
            Log.info(f"Saved app config to file: {filepath}")
            
        except Exception as e:
            Log.error(f"Failed to save app config to file {filepath}: {str(e)}")
            raise
    
    def validate(self) -> bool:
        """
        Validate configuration
        
        Returns:
            bool: Whether configuration is valid
        """
        errors = []
        
        # Check application type
        if self.app_type not in ['native', 'web', 'hybrid']:
            errors.append("app_type must be 'native', 'web', or 'hybrid'")
        
        # Check application path
        if self.app_path and not FileUtils.file_exists(self.app_path):
            errors.append(f"App file not found: {self.app_path}")
        
        # Check timeout values
        if self.launch_timeout <= 0:
            errors.append("launch_timeout must be greater than 0")
        
        if self.startup_timeout <= 0:
            errors.append("startup_timeout must be greater than 0")
        
        if errors:
            for error in errors:
                Log.error(f"App configuration validation error: {error}")
            return False
        
        Log.info("App configuration validation passed")
        return True
    
    def get_app_identifier(self) -> str:
        """
        Get application identifier
        
        Returns:
            str: Application identifier
        """
        if self.app_package:
            return self.app_package
        elif self.app_bundle_id:
            return self.app_bundle_id
        elif self.app_name:
            return self.app_name
        else:
            return "Unknown"
    
    def get_app_summary(self) -> str:
        """
        Get application summary information
        
        Returns:
            str: Application summary
        """
        parts = []
        
        if self.app_name:
            parts.append(self.app_name)
        
        if self.app_version:
            parts.append(f"v{self.app_version}")
        
        if self.app_type:
            parts.append(f"({self.app_type})")
        
        if self.app_package or self.app_bundle_id:
            identifier = self.get_app_identifier()
            parts.append(f"[{identifier}]")
        
        return " ".join(parts)
    
    def add_permission(self, permission: str):
        """
        Add permission
        
        Args:
            permission: Permission name
        """
        if permission not in self.permissions:
            self.permissions.append(permission)
            Log.info(f"Added permission: {permission}")
    
    def remove_permission(self, permission: str):
        """
        Remove permission
        
        Args:
            permission: Permission name
        """
        if permission in self.permissions:
            self.permissions.remove(permission)
            Log.info(f"Removed permission: {permission}")
    
    def has_permission(self, permission: str) -> bool:
        """
        Check if has specified permission
        
        Args:
            permission: Permission name
            
        Returns:
            bool: Whether has permission
        """
        return permission in self.permissions
    
    def set_proxy(self, host: str, port: int, username: str = "", password: str = ""):
        """
        Set proxy
        
        Args:
            host: Proxy host
            port: Proxy port
            username: Username (optional)
            password: Password (optional)
        """
        self.proxy_settings = {
            'host': host,
            'port': port,
            'username': username,
            'password': password,
        }
        Log.info(f"Set proxy: {host}:{port}")
    
    def clear_proxy(self):
        """Clear proxy settings"""
        self.proxy_settings.clear()
        Log.info("Cleared proxy settings")
