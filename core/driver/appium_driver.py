"""
Appium Driver Management
Appium driver management class
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
    """Appium driver management class"""
    
    def __init__(self, config: AppiumConfig):
        """
        Initialize Appium driver
        
        Args:
            config: Appium configuration object
        """
        self.config = config
        self.driver: Optional[webdriver.Remote] = None
        self.wait: Optional[WebDriverWait] = None
        self._session_id: Optional[str] = None
        
    def start_driver(self) -> webdriver.Remote:
        """
        Start Appium driver
        
        Returns:
            webdriver.Remote: Appium driver instance
        """
        try:
            Log.info("Starting Appium driver...")
            
            # Build capabilities
            capabilities = self.config.get_capabilities()
            
            # Create driver - using new version Selenium API
            from selenium.webdriver.common.options import ArgOptions
            
            # Create Appium options
            options = ArgOptions()
            for key, value in capabilities.items():
                options.set_capability(key, value)
            
            self.driver = webdriver.Remote(
                command_executor=self.config.server_url,
                options=options
            )
            
            # Set explicit wait
            self.wait = WebDriverWait(self.driver, self.config.timeout)
            
            # Get session ID
            self._session_id = self.driver.session_id
            
            Log.info(f"Appium driver started successfully. Session ID: {self._session_id}")
            return self.driver
            
        except Exception as e:
            Log.error(f"Failed to start Appium driver: {str(e)}")
            raise
    
    def quit_driver(self):
        """Close Appium driver"""
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
        Find element (with explicit wait)
        
        Args:
            by: Locator method
            value: Locator value
            timeout: Timeout (seconds)
            
        Returns:
            Found element
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
        Find multiple elements
        
        Args:
            by: Locator method
            value: Locator value
            timeout: Timeout (seconds)
            
        Returns:
            List of found elements
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
        Wait for element to be clickable
        
        Args:
            by: Locator method
            value: Locator value
            timeout: Timeout (seconds)
            
        Returns:
            Clickable element
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
        Take screenshot
        
        Args:
            filename: Filename (optional)
            
        Returns:
            Screenshot file path
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
        """Get page source"""
        if not self.driver:
            raise WebDriverException("Driver not initialized")
        
        return self.driver.page_source
    
    def get_current_activity(self) -> str:
        """Get current activity (Android)"""
        if not self.driver:
            raise WebDriverException("Driver not initialized")
        
        return self.driver.current_activity
    
    def get_current_package(self) -> str:
        """Get current package name (Android)"""
        if not self.driver:
            raise WebDriverException("Driver not initialized")
        
        return self.driver.current_package
    
    def activate_app(self, app_package: str):
        """Activate app"""
        try:
            Log.info(f"Activating app: {app_package}")
            self.driver.activate_app(app_package)
            Log.info(f"App {app_package} activated successfully")
        except Exception as e:
            Log.error(f"Failed to activate app {app_package}: {str(e)}")
            raise
    
    def terminate_app(self, app_package: str):
        """Terminate app"""
        try:
            Log.info(f"Terminating app: {app_package}")
            self.driver.terminate_app(app_package)
            Log.info(f"App {app_package} terminated successfully")
        except Exception as e:
            Log.error(f"Failed to terminate app {app_package}: {str(e)}")
            raise
    
    def tap(self, coordinates, count: int = 1):
        """
        Tap at specified coordinates on screen
        
        Args:
            coordinates: Coordinate list, format as [(x, y)] or [(x, y), (x2, y2), ...]
            count: Number of taps (default 1)
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
        """Get session ID"""
        return self._session_id
    
    @property
    def is_driver_active(self) -> bool:
        """Check if driver is active"""
        return self.driver is not None
