"""
Configuration manager for TikTok App tests
"""

import os
import yaml
from typing import Dict, Any


def get_appium_config(language: str = "en") -> Dict[str, Any]:
    """
    Get Appium configuration for TikTok App
    
    Args:
        language: Language code (en/zh)
        
    Returns:
        Appium capabilities dictionary
    """
    base_config = {
        "platformName": "Android",
        "automationName": "UiAutomator2",
        "appPackage": "com.ss.android.ugc.trill",
        "appActivity": "com.ss.android.ugc.aweme.splash.SplashActivity",
        "noReset": True,
        "autoGrantPermissions": True,
        "newCommandTimeout": 300,
        "adbExecTimeout": 60000,
        "uiautomator2ServerLaunchTimeout": 60000,
        "uiautomator2ServerInstallTimeout": 60000,
        "androidInstallTimeout": 90000,
        "avdLaunchTimeout": 60000,
        "avdReadyTimeout": 60000,
        "androidDeviceReadyTimeout": 60000,
        "systemPort": 8200
    }
    
    # Add language-specific settings
    if language == "zh":
        base_config.update({
            "locale": "zh_CN",
            "language": "zh"
        })
    else:
        # For English, only set language, let device use default locale
        base_config.update({
            "language": "en"
            # Removed locale setting to avoid compatibility issues
        })
    
    return base_config


def get_server_config() -> Dict[str, Any]:
    """
    Get Appium server configuration
    
    Returns:
        Server configuration dictionary
    """
    return {
        "host": "localhost",
        "port": 4723,
        "path": "/wd/hub"
    }

