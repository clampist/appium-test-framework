"""
Appium Configuration
Appium configuration management class
"""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass, field

from ..utils.logger import Log
from ..utils.file_utils import FileUtils


@dataclass
class AppiumConfig:
    """Appium configuration class"""
    
    # Server configuration
    server_url: str = "http://localhost:4723"
    server_host: str = "localhost"
    server_port: int = 4723
    
    # Session configuration
    timeout: int = 30
    implicit_wait: int = 10
    new_command_timeout: int = 60
    
    # Platform configuration
    platform_name: str = "Android"
    platform_version: str = ""
    device_name: str = ""
    automation_name: str = "UiAutomator2"
    
    # Application configuration
    app_package: str = ""
    app_activity: str = ""
    app_path: str = ""
    app_bundle_id: str = ""  # iOS
    
    # Other configuration
    no_reset: bool = False
    full_reset: bool = False
    auto_grant_permissions: bool = True
    auto_accept_alerts: bool = True
    
    # Advanced configuration
    additional_capabilities: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Post-initialization processing"""
        # Load configuration from environment variables
        self._load_from_env()
        
        # Build server URL
        if not self.server_url.startswith("http"):
            self.server_url = f"http://{self.server_host}:{self.server_port}"
    
    def _load_from_env(self):
        """Load configuration from environment variables"""
        env_mappings = {
            'APPIUM_SERVER_URL': 'server_url',
            'APPIUM_SERVER_HOST': 'server_host',
            'APPIUM_SERVER_PORT': 'server_port',
            'APPIUM_TIMEOUT': 'timeout',
            'APPIUM_PLATFORM_NAME': 'platform_name',
            'APPIUM_PLATFORM_VERSION': 'platform_version',
            'APPIUM_DEVICE_NAME': 'device_name',
            'APPIUM_AUTOMATION_NAME': 'automation_name',
            'APPIUM_APP_PACKAGE': 'app_package',
            'APPIUM_APP_ACTIVITY': 'app_activity',
            'APPIUM_APP_PATH': 'app_path',
            'APPIUM_APP_BUNDLE_ID': 'app_bundle_id',
        }
        
        for env_var, attr_name in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                # Handle numeric types
                if attr_name in ['server_port', 'timeout', 'implicit_wait', 'new_command_timeout']:
                    try:
                        value = int(value)
                    except ValueError:
                        Log.warning(f"Invalid integer value for {env_var}: {value}")
                        continue
                
                setattr(self, attr_name, value)
                Log.info(f"Loaded {attr_name} from environment variable {env_var}: {value}")
    
    def get_capabilities(self) -> Dict[str, Any]:
        """
        Get Appium capabilities
        
        Returns:
            Dict[str, Any]: Capabilities dictionary
        """
        capabilities = {
            'platformName': self.platform_name,
            'automationName': self.automation_name,
            'newCommandTimeout': self.new_command_timeout,
            'autoGrantPermissions': self.auto_grant_permissions,
            'autoAcceptAlerts': self.auto_accept_alerts,
            'noReset': self.no_reset,
            'fullReset': self.full_reset,
        }
        
        # Add platform-specific configuration
        if self.platform_name.lower() == 'android':
            if self.platform_version:
                capabilities['platformVersion'] = self.platform_version
            if self.device_name:
                capabilities['deviceName'] = self.device_name
            if self.app_package:
                capabilities['appPackage'] = self.app_package
            if self.app_activity:
                capabilities['appActivity'] = self.app_activity
            if self.app_path:
                capabilities['app'] = self.app_path
        elif self.platform_name.lower() == 'ios':
            if self.platform_version:
                capabilities['platformVersion'] = self.platform_version
            if self.device_name:
                capabilities['deviceName'] = self.device_name
            if self.app_bundle_id:
                capabilities['bundleId'] = self.app_bundle_id
            if self.app_path:
                capabilities['app'] = self.app_path
        
        # Add additional configuration
        capabilities.update(self.additional_capabilities)
        
        Log.info(f"Generated capabilities: {capabilities}")
        return capabilities
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary
        
        Returns:
            Dict[str, Any]: Configuration dictionary
        """
        return {
            'server_url': self.server_url,
            'server_host': self.server_host,
            'server_port': self.server_port,
            'timeout': self.timeout,
            'implicit_wait': self.implicit_wait,
            'new_command_timeout': self.new_command_timeout,
            'platform_name': self.platform_name,
            'platform_version': self.platform_version,
            'device_name': self.device_name,
            'automation_name': self.automation_name,
            'app_package': self.app_package,
            'app_activity': self.app_activity,
            'app_path': self.app_path,
            'app_bundle_id': self.app_bundle_id,
            'no_reset': self.no_reset,
            'full_reset': self.full_reset,
            'auto_grant_permissions': self.auto_grant_permissions,
            'auto_accept_alerts': self.auto_accept_alerts,
            'additional_capabilities': self.additional_capabilities,
        }
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'AppiumConfig':
        """
        Create configuration object from dictionary
        
        Args:
            config_dict: Configuration dictionary
            
        Returns:
            AppiumConfig: Configuration object
        """
        return cls(**config_dict)
    
    @classmethod
    def from_file(cls, filepath: str) -> 'AppiumConfig':
        """
        Load configuration from file
        
        Args:
            filepath: Configuration file path
            
        Returns:
            AppiumConfig: Configuration object
        """
        try:
            if filepath.endswith('.json'):
                config_dict = FileUtils.read_json(filepath)
            elif filepath.endswith('.yaml') or filepath.endswith('.yml'):
                config_dict = FileUtils.read_yaml(filepath)
            else:
                raise ValueError(f"Unsupported file format: {filepath}")
            
            Log.info(f"Loaded Appium config from file: {filepath}")
            return cls.from_dict(config_dict)
            
        except Exception as e:
            Log.error(f"Failed to load Appium config from file {filepath}: {str(e)}")
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
            
            Log.info(f"Saved Appium config to file: {filepath}")
            
        except Exception as e:
            Log.error(f"Failed to save Appium config to file {filepath}: {str(e)}")
            raise
    
    def validate(self) -> bool:
        """
        Validate configuration
        
        Returns:
            bool: Whether configuration is valid
        """
        errors = []
        
        # Check required fields
        if not self.platform_name:
            errors.append("platform_name is required")
        
        if not self.automation_name:
            errors.append("automation_name is required")
        
        # Check platform-specific fields
        if self.platform_name.lower() == 'android':
            if not self.app_package and not self.app_path:
                errors.append("Either app_package or app_path is required for Android")
        elif self.platform_name.lower() == 'ios':
            if not self.app_bundle_id and not self.app_path:
                errors.append("Either app_bundle_id or app_path is required for iOS")
        
        if errors:
            for error in errors:
                Log.error(f"Configuration validation error: {error}")
            return False
        
        Log.info("Appium configuration validation passed")
        return True
