"""
Device Configuration
设备配置管理类
"""

import os
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field

from ..utils.logger import Log
from ..utils.file_utils import FileUtils


@dataclass
class DeviceConfig:
    """设备配置类"""
    
    # 设备基本信息
    device_id: str = ""
    device_name: str = ""
    platform: str = "Android"  # Android/iOS
    platform_version: str = ""
    manufacturer: str = ""
    model: str = ""
    
    # 屏幕配置
    screen_width: int = 0
    screen_height: int = 0
    screen_density: float = 0.0
    
    # 网络配置
    wifi_enabled: bool = True
    mobile_data_enabled: bool = True
    airplane_mode: bool = False
    
    # 语言和地区
    language: str = "en"
    country: str = "US"
    locale: str = "en_US"
    
    # 时区
    timezone: str = "UTC"
    
    # 其他配置
    additional_config: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """初始化后处理"""
        # 从环境变量加载配置
        self._load_from_env()
    
    def _load_from_env(self):
        """从环境变量加载配置"""
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
                # 处理数字类型
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
        获取设备信息
        
        Returns:
            Dict[str, Any]: 设备信息字典
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
        
        # 添加额外配置
        device_info.update(self.additional_config)
        
        return device_info
    
    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典
        
        Returns:
            Dict[str, Any]: 配置字典
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
        从字典创建配置对象
        
        Args:
            config_dict: 配置字典
            
        Returns:
            DeviceConfig: 配置对象
        """
        return cls(**config_dict)
    
    @classmethod
    def from_file(cls, filepath: str) -> 'DeviceConfig':
        """
        从文件加载配置
        
        Args:
            filepath: 配置文件路径
            
        Returns:
            DeviceConfig: 配置对象
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
        保存配置到文件
        
        Args:
            filepath: 文件路径
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
        验证配置
        
        Returns:
            bool: 配置是否有效
        """
        errors = []
        
        # 检查必需字段
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
        获取屏幕分辨率字符串
        
        Returns:
            str: 屏幕分辨率（如：1920x1080）
        """
        if self.screen_width and self.screen_height:
            return f"{self.screen_width}x{self.screen_height}"
        return "Unknown"
    
    def get_device_summary(self) -> str:
        """
        获取设备摘要信息
        
        Returns:
            str: 设备摘要
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
