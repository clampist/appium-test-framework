"""
Application Configuration
应用配置管理类
"""

import os
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field

from ..utils.logger import Log
from ..utils.file_utils import FileUtils


@dataclass
class AppConfig:
    """应用配置类"""
    
    # 应用基本信息
    app_name: str = ""
    app_version: str = ""
    app_package: str = ""
    app_activity: str = ""  # Android
    app_bundle_id: str = ""  # iOS
    app_path: str = ""
    
    # 应用类型
    app_type: str = "native"  # native/web/hybrid
    
    # 启动配置
    launch_timeout: int = 30
    startup_timeout: int = 60
    
    # 权限配置
    auto_grant_permissions: bool = True
    permissions: List[str] = field(default_factory=list)
    
    # 数据配置
    no_reset: bool = False
    full_reset: bool = False
    clear_data: bool = False
    
    # 网络配置
    network_profile: str = ""
    proxy_settings: Dict[str, Any] = field(default_factory=dict)
    
    # 其他配置
    additional_config: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """初始化后处理"""
        # 从环境变量加载配置
        self._load_from_env()
    
    def _load_from_env(self):
        """从环境变量加载配置"""
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
                # 处理数字类型
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
        获取应用信息
        
        Returns:
            Dict[str, Any]: 应用信息字典
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
        
        # 添加额外配置
        app_info.update(self.additional_config)
        
        return app_info
    
    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典
        
        Returns:
            Dict[str, Any]: 配置字典
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
        从字典创建配置对象
        
        Args:
            config_dict: 配置字典
            
        Returns:
            AppConfig: 配置对象
        """
        return cls(**config_dict)
    
    @classmethod
    def from_file(cls, filepath: str) -> 'AppConfig':
        """
        从文件加载配置
        
        Args:
            filepath: 配置文件路径
            
        Returns:
            AppConfig: 配置对象
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
            
            Log.info(f"Saved app config to file: {filepath}")
            
        except Exception as e:
            Log.error(f"Failed to save app config to file {filepath}: {str(e)}")
            raise
    
    def validate(self) -> bool:
        """
        验证配置
        
        Returns:
            bool: 配置是否有效
        """
        errors = []
        
        # 检查应用类型
        if self.app_type not in ['native', 'web', 'hybrid']:
            errors.append("app_type must be 'native', 'web', or 'hybrid'")
        
        # 检查应用路径
        if self.app_path and not FileUtils.file_exists(self.app_path):
            errors.append(f"App file not found: {self.app_path}")
        
        # 检查超时时间
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
        获取应用标识符
        
        Returns:
            str: 应用标识符
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
        获取应用摘要信息
        
        Returns:
            str: 应用摘要
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
        添加权限
        
        Args:
            permission: 权限名称
        """
        if permission not in self.permissions:
            self.permissions.append(permission)
            Log.info(f"Added permission: {permission}")
    
    def remove_permission(self, permission: str):
        """
        移除权限
        
        Args:
            permission: 权限名称
        """
        if permission in self.permissions:
            self.permissions.remove(permission)
            Log.info(f"Removed permission: {permission}")
    
    def has_permission(self, permission: str) -> bool:
        """
        检查是否有指定权限
        
        Args:
            permission: 权限名称
            
        Returns:
            bool: 是否有权限
        """
        return permission in self.permissions
    
    def set_proxy(self, host: str, port: int, username: str = "", password: str = ""):
        """
        设置代理
        
        Args:
            host: 代理主机
            port: 代理端口
            username: 用户名（可选）
            password: 密码（可选）
        """
        self.proxy_settings = {
            'host': host,
            'port': port,
            'username': username,
            'password': password,
        }
        Log.info(f"Set proxy: {host}:{port}")
    
    def clear_proxy(self):
        """清除代理设置"""
        self.proxy_settings.clear()
        Log.info("Cleared proxy settings")
