"""
Page Object Base Class
Page object base class, implementing Page Object Model pattern
"""

from typing import Dict, Any, Optional
from appium.webdriver.common.appiumby import AppiumBy

from .base_element import BaseElement
from ..utils.logger import Log


class PageObject:
    """Page object base class"""
    
    def __init__(self, driver):
        """
        Initialize page object
        
        Args:
            driver: Appium driver instance
        """
        self.driver = driver
        self.elements: Dict[str, BaseElement] = {}
        self._init_elements()
    
    def _init_elements(self):
        """Initialize page elements, subclasses need to override this method"""
        pass
    
    def add_element(self, name: str, by: str, value: str, element_name: str = ""):
        """
        Add page element
        
        Args:
            name: Element name
            by: Locator method
            value: Locator value
            element_name: Element display name
        """
        self.elements[name] = BaseElement(
            self.driver, by, value, element_name or name
        )
    
    def get_element(self, name: str) -> BaseElement:
        """
        Get page element
        
        Args:
            name: Element name
            
        Returns:
            BaseElement: Page element
        """
        if name not in self.elements:
            raise KeyError(f"Element '{name}' not found in page object")
        return self.elements[name]
    
    def wait_for_page_load(self, timeout: Optional[int] = None):
        """
        Wait for page to load completely
        
        Args:
            timeout: Timeout (seconds)
        """
        # Subclasses can override this method to implement specific page loading wait logic
        Log.info("Waiting for page to load...")
    
    def is_page_loaded(self) -> bool:
        """
        Check if page is loaded completely
        
        Returns:
            bool: Whether page is loaded completely
        """
        # Subclasses can override this method to implement specific page loading check logic
        return True
    
    def take_screenshot(self, name: str = ""):
        """
        Page screenshot
        
        Args:
            name: Screenshot name
        """
        try:
            filename = f"{self.__class__.__name__}_{name}.png" if name else f"{self.__class__.__name__}.png"
            self.driver.take_screenshot(filename)
            Log.info(f"Page screenshot saved: {filename}")
        except Exception as e:
            Log.error(f"Failed to take page screenshot: {str(e)}")
    
    def get_page_title(self) -> str:
        """
        Get page title
        
        Returns:
            str: Page title
        """
        try:
            # Try to get page title, specific implementation depends on application type
            if hasattr(self.driver, 'title'):
                return self.driver.title
            else:
                # For mobile apps, may need to get title through specific elements
                return "Mobile App Page"
        except Exception as e:
            Log.error(f"Failed to get page title: {str(e)}")
            return ""
    
    def scroll_to_element(self, element_name: str):
        """
        Scroll to specified element
        
        Args:
            element_name: Element name
        """
        element = self.get_element(element_name)
        element.scroll_to_element()
    
    def wait_for_element(self, element_name: str, timeout: Optional[int] = None):
        """
        Wait for element to appear
        
        Args:
            element_name: Element name
            timeout: Timeout (seconds)
        """
        element = self.get_element(element_name)
        element.find(timeout)
    
    def click_element(self, element_name: str, timeout: Optional[int] = None):
        """
        Click element
        
        Args:
            element_name: Element name
            timeout: Timeout (seconds)
        """
        element = self.get_element(element_name)
        element.click(timeout)
    
    def input_text(self, element_name: str, text: str, timeout: Optional[int] = None):
        """
        Input text to element
        
        Args:
            element_name: Element name
            text: Text to input
            timeout: Timeout (seconds)
        """
        element = self.get_element(element_name)
        element.send_keys(text, timeout)
    
    def get_element_text(self, element_name: str, timeout: Optional[int] = None) -> str:
        """
        Get element text
        
        Args:
            element_name: Element name
            timeout: Timeout (seconds)
            
        Returns:
            str: Element text
        """
        element = self.get_element(element_name)
        return element.get_text(timeout)
    
    def is_element_displayed(self, element_name: str, timeout: Optional[int] = None) -> bool:
        """
        Check if element is visible
        
        Args:
            element_name: Element name
            timeout: Timeout (seconds)
            
        Returns:
            bool: Whether visible
        """
        element = self.get_element(element_name)
        return element.is_displayed(timeout)
    
    def is_element_enabled(self, element_name: str, timeout: Optional[int] = None) -> bool:
        """
        Check if element is enabled
        
        Args:
            element_name: Element name
            timeout: Timeout (seconds)
            
        Returns:
            bool: Whether enabled
        """
        element = self.get_element(element_name)
        return element.is_enabled(timeout)
    
    def wait_for_element_clickable(self, element_name: str, timeout: Optional[int] = None):
        """
        Wait for element to be clickable
        
        Args:
            element_name: Element name
            timeout: Timeout (seconds)
        """
        element = self.get_element(element_name)
        element.wait_for_clickable(timeout)
    
    def tap_element(self, element_name: str, x: Optional[int] = None, y: Optional[int] = None):
        """
        Tap element (supports coordinate offset)
        
        Args:
            element_name: Element name
            x: X coordinate offset
            y: Y coordinate offset
        """
        element = self.get_element(element_name)
        element.tap(x, y)
    
    def long_press_element(self, element_name: str, duration: int = 2000):
        """
        Long press element
        
        Args:
            element_name: Element name
            duration: Long press duration (milliseconds)
        """
        element = self.get_element(element_name)
        element.long_press(duration)
