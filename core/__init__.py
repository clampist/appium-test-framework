"""
ATF Core Package
核心逻辑层，提供Appium测试的基础功能
"""

__version__ = "1.0.0"
__author__ = "ATF Team"

from .driver.appium_driver import AppiumDriver
from .elements.base_element import BaseElement
from .utils.logger import Log
from .config.appium_config import AppiumConfig

__all__ = [
    "AppiumDriver",
    "BaseElement", 
    "Log",
    "AppiumConfig"
]
