"""
Device Configuration
Device configuration management class
"""

import os
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field

from ..utils.logger import Log
from ..utils.file_utils import FileUtils


@dataclass
class DeviceConfig:
    """Device configuration class"""
    
    # Device basic information
    device_id: str = ""
    device_name: str = ""
    platform: str = "Android"  # Android/iOS
    platform_version: str = ""
    manufacturer: str = ""
    model: str = ""
    
    # Screen configuration
    screen_width: int = 0
    screen_height: int = 0
    screen_density: float = 0.0
    
    # Network configuration
    wifi_enabled: bool = True
    mobile_data_enabled: bool = True
    airplane_mode: bool = False
    
    # Language and region
    language: str = "en"
    country: str = "US"
    locale: str = "en_US"
    
    # Timezone
    timezone: str = "UTC"
    
    # Other configuration
    additional_config: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Post-initialization processing"""
        # Load configuration from environment variables
        self._load_from_env()
    
    def _load_from_env(self):
        """Load configuration from environment variables"""
        env_mappings = {
            'DEVICE_ID': 'device_id',
            'DEVICE_NAME': 'device_name',
            'DEVICE_PLATFORM': 'platform',
            'DEVICE_PLATFORM_VERSION': 'platform_version',
            'DEVICE_MANUFACTURER': 'manufacturer',
            'DEVICE_MODEL': 'model',
            'DEVICE_SCREEN_WIDTH': 'screen_width',
            'DEVICE_SCREEN_HEIGHT': 'screen_height',
            'DEVICE_SCREEN_DENSITY': 'screen_density',
            'DEVICE_LANGUAGE': 'language',
            'DEVICE_COUNTRY': 'country',
            'DEVICE_LOCALE': 'locale',
            'DEVICE_TIMEZONE': 'timezone',
        }
        
        for env_var, attr_name in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                # Handle numeric types
                if attr_name in ['screen_width', 'screen_height']:
                    try:
                        value = int(value)
                    except ValueError:
                        Log.warning(f"Invalid integer value for {env_var}: {value}")
                        continue
                elif attr_name == 'screen_density':
                    try:
                        value = float(value)
                    except ValueError:
                        Log.warning(f"Invalid float value for {env_var}: {value}")
                        continue
                
                setattr(self, attr_name, value)
                Log.info(f"Loaded {attr_name} from environment variable {env_var}: {value}")
    
    def get_device_info(self) -> Dict[str, Any]:
        """
        Get device information
        
        Returns:
            Dict[str, Any]: Device information dictionary
        """
        device_info = {
            'device_id': self.device_id,
            'device_name': self.device_name,
            'platform': self.platform,
            'platform_version': self.platform_version,
            'manufacturer': self.manufacturer,
            'model': self.model,
            'screen_width': self.screen_width,
            'screen_height': self.screen_height,
            'screen_density': self.screen_density,
            'language': self.language,
            'country': self.country,
            'locale': self.locale,
            'timezone': self.timezone,
        }
        
        # Add additional configuration
        device_info.update(self.additional_config)
        
        return device_info
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary
        
        Returns:
            Dict[str, Any]: Configuration dictionary
        """
        return {
            'device_id': self.device_id,
            'device_name': self.device_name,
            'platform': self.platform,
            'platform_version': self.platform_version,
            'manufacturer': self.manufacturer,
            'model': self.model,
            'screen_width': self.screen_width,
            'screen_height': self.screen_height,
            'screen_density': self.screen_density,
            'wifi_enabled': self.wifi_enabled,
            'mobile_data_enabled': self.mobile_data_enabled,
            'airplane_mode': self.airplane_mode,
            'language': self.language,
            'country': self.country,
            'locale': self.locale,
            'timezone': self.timezone,
            'additional_config': self.additional_config,
        }
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'DeviceConfig':
        """
        Create configuration object from dictionary
        
        Args:
            config_dict: Configuration dictionary
            
        Returns:
            DeviceConfig: Configuration object
        """
        return cls(**config_dict)
    
    @classmethod
    def from_file(cls, filepath: str) -> 'DeviceConfig':
        """
        Load configuration from file
        
        Args:
            filepath: Configuration file path
            
        Returns:
            DeviceConfig: Configuration object
        """
        try:
            if filepath.endswith('.json'):
                config_dict = FileUtils.read_json(filepath)
            elif filepath.endswith('.yaml') or filepath.endswith('.yml'):
                config_dict = FileUtils.read_yaml(filepath)
            else:
                raise ValueError(f"Unsupported file format: {filepath}")
            
            Log.info(f"Loaded device config from file: {filepath}")
            return cls.from_dict(config_dict)
            
        except Exception as e:
            Log.error(f"Failed to load device config from file {filepath}: {str(e)}")
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
            
            Log.info(f"Saved device config to file: {filepath}")
            
        except Exception as e:
            Log.error(f"Failed to save device config to file {filepath}: {str(e)}")
            raise
    
    def validate(self) -> bool:
        """
        Validate configuration
        
        Returns:
            bool: Whether configuration is valid
        """
        errors = []
        
        # Check required fields
        if not self.platform:
            errors.append("platform is required")
        
        if self.platform.lower() not in ['android', 'ios']:
            errors.append("platform must be 'Android' or 'iOS'")
        
        if errors:
            for error in errors:
                Log.error(f"Device configuration validation error: {error}")
            return False
        
        Log.info("Device configuration validation passed")
        return True
    
    def get_screen_resolution(self) -> str:
        """
        Get screen resolution string
        
        Returns:
            str: Screen resolution (e.g., 1920x1080)
        """
        if self.screen_width and self.screen_height:
            return f"{self.screen_width}x{self.screen_height}"
        return "Unknown"
    
    def get_device_summary(self) -> str:
        """
        Get device summary information
        
        Returns:
            str: Device summary
        """
        parts = []
        
        if self.manufacturer and self.model:
            parts.append(f"{self.manufacturer} {self.model}")
        elif self.device_name:
            parts.append(self.device_name)
        
        if self.platform_version:
            parts.append(f"({self.platform} {self.platform_version})")
        else:
            parts.append(f"({self.platform})")
        
        if self.device_id:
            parts.append(f"[{self.device_id}]")
        
        return " ".join(parts)
