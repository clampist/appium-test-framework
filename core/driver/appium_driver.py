"""
Appium Driver Management
Appium驱动管理类
"""

import time
from typing import Dict, Any, Optional
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

from ..utils.logger import Log
from ..config.appium_config import AppiumConfig


class AppiumDriver:
    """Appium驱动管理类"""
    
    def __init__(self, config: AppiumConfig):
        """
        初始化Appium驱动
        
        Args:
            config: Appium配置对象
        """
        self.config = config
        self.driver: Optional[webdriver.Remote] = None
        self.wait: Optional[WebDriverWait] = None
        self._session_id: Optional[str] = None
        
    def start_driver(self) -> webdriver.Remote:
        """
        启动Appium驱动
        
        Returns:
            webdriver.Remote: Appium驱动实例
        """
        try:
            Log.info("Starting Appium driver...")
            
            # 构建capabilities
            capabilities = self.config.get_capabilities()
            
            # 创建驱动 - 使用新版本Selenium API
            from selenium.webdriver.common.options import ArgOptions
            
            # 创建Appium选项
            options = ArgOptions()
            for key, value in capabilities.items():
                options.set_capability(key, value)
            
            self.driver = webdriver.Remote(
                command_executor=self.config.server_url,
                options=options
            )
            
            # 设置显式等待
            self.wait = WebDriverWait(self.driver, self.config.timeout)
            
            # 获取会话ID
            self._session_id = self.driver.session_id
            
            Log.info(f"Appium driver started successfully. Session ID: {self._session_id}")
            return self.driver
            
        except Exception as e:
            Log.error(f"Failed to start Appium driver: {str(e)}")
            raise
    
    def quit_driver(self):
        """关闭Appium驱动"""
        if self.driver:
            try:
                Log.info("Quitting Appium driver...")
                self.driver.quit()
                self.driver = None
                self.wait = None
                self._session_id = None
                Log.info("Appium driver quit successfully")
            except Exception as e:
                Log.error(f"Error quitting driver: {str(e)}")
    
    def find_element(self, by: str, value: str, timeout: Optional[int] = None):
        """
        查找元素（带显式等待）
        
        Args:
            by: 定位方式
            value: 定位值
            timeout: 超时时间（秒）
            
        Returns:
            找到的元素
        """
        if not self.driver:
            raise WebDriverException("Driver not initialized")
        
        wait_time = timeout or self.config.timeout
        wait = WebDriverWait(self.driver, wait_time)
        
        try:
            element = wait.until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            Log.error(f"Element not found: {by}={value}")
            raise
    
    def find_elements(self, by: str, value: str, timeout: Optional[int] = None):
        """
        查找多个元素
        
        Args:
            by: 定位方式
            value: 定位值
            timeout: 超时时间（秒）
            
        Returns:
            找到的元素列表
        """
        if not self.driver:
            raise WebDriverException("Driver not initialized")
        
        wait_time = timeout or self.config.timeout
        wait = WebDriverWait(self.driver, wait_time)
        
        try:
            elements = wait.until(
                EC.presence_of_all_elements_located((by, value))
            )
            return elements
        except TimeoutException:
            Log.error(f"Elements not found: {by}={value}")
            raise
    
    def wait_for_element_clickable(self, by: str, value: str, timeout: Optional[int] = None):
        """
        等待元素可点击
        
        Args:
            by: 定位方式
            value: 定位值
            timeout: 超时时间（秒）
            
        Returns:
            可点击的元素
        """
        if not self.driver:
            raise WebDriverException("Driver not initialized")
        
        wait_time = timeout or self.config.timeout
        wait = WebDriverWait(self.driver, wait_time)
        
        try:
            element = wait.until(
                EC.element_to_be_clickable((by, value))
            )
            return element
        except TimeoutException:
            Log.error(f"Element not clickable: {by}={value}")
            raise
    
    def take_screenshot(self, filename: Optional[str] = None) -> str:
        """
        截图
        
        Args:
            filename: 文件名（可选）
            
        Returns:
            截图文件路径
        """
        if not self.driver:
            raise WebDriverException("Driver not initialized")
        
        if not filename:
            timestamp = int(time.time())
            filename = f"screenshot_{timestamp}.png"
        
        try:
            self.driver.save_screenshot(filename)
            Log.info(f"Screenshot saved: {filename}")
            return filename
        except Exception as e:
            Log.error(f"Failed to take screenshot: {str(e)}")
            raise
    
    def get_page_source(self) -> str:
        """获取页面源码"""
        if not self.driver:
            raise WebDriverException("Driver not initialized")
        
        return self.driver.page_source
    
    def get_current_activity(self) -> str:
        """获取当前Activity（Android）"""
        if not self.driver:
            raise WebDriverException("Driver not initialized")
        
        return self.driver.current_activity
    
    def get_current_package(self) -> str:
        """获取当前包名（Android）"""
        if not self.driver:
            raise WebDriverException("Driver not initialized")
        
        return self.driver.current_package
    
    def activate_app(self, app_package: str):
        """激活应用"""
        try:
            Log.info(f"Activating app: {app_package}")
            self.driver.activate_app(app_package)
            Log.info(f"App {app_package} activated successfully")
        except Exception as e:
            Log.error(f"Failed to activate app {app_package}: {str(e)}")
            raise
    
    def terminate_app(self, app_package: str):
        """终止应用"""
        try:
            Log.info(f"Terminating app: {app_package}")
            self.driver.terminate_app(app_package)
            Log.info(f"App {app_package} terminated successfully")
        except Exception as e:
            Log.error(f"Failed to terminate app {app_package}: {str(e)}")
            raise
    
    def tap(self, coordinates, count: int = 1):
        """
        点击屏幕指定坐标
        
        Args:
            coordinates: 坐标列表，格式为 [(x, y)] 或 [(x, y), (x2, y2), ...]
            count: 点击次数（默认为1）
        """
        try:
            Log.info(f"Tapping at coordinates {coordinates} {count} time(s)")
            self.driver.tap(coordinates, count)
            Log.info(f"Tap completed successfully")
        except Exception as e:
            Log.error(f"Failed to tap at coordinates {coordinates}: {str(e)}")
            raise
    
    @property
    def session_id(self) -> Optional[str]:
        """获取会话ID"""
        return self._session_id
    
    @property
    def is_driver_active(self) -> bool:
        """检查驱动是否活跃"""
        return self.driver is not None
