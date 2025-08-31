"""
Base Element Class
Base element class, encapsulating common element operation methods
"""

from typing import Optional, List
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import WebDriverException
from appium.webdriver.common.appiumby import AppiumBy

from ..utils.logger import Log


class BaseElement:
    """Base element class"""
    
    def __init__(self, driver, by: str, value: str, name: str = ""):
        """
        Initialize element
        
        Args:
            driver: Appium driver instance
            by: Locator method
            value: Locator value
            name: Element name (for logging)
        """
        self.driver = driver
        self.by = by
        self.value = value
        self.name = name or f"{by}={value}"
        self._element: Optional[WebElement] = None
    
    def find(self, timeout: Optional[int] = None) -> WebElement:
        """
        Find element
        
        Args:
            timeout: Timeout (seconds)
            
        Returns:
            WebElement: Found element
        """
        try:
            self._element = self.driver.find_element(self.by, self.value, timeout)
            Log.info(f"Found element: {self.name}")
            return self._element
        except Exception as e:
            Log.error(f"Failed to find element {self.name}: {str(e)}")
            raise
    
    def find_all(self, timeout: Optional[int] = None) -> List[WebElement]:
        """
        Find all matching elements
        
        Args:
            timeout: Timeout (seconds)
            
        Returns:
            List[WebElement]: List of found elements
        """
        try:
            elements = self.driver.find_elements(self.by, self.value, timeout)
            Log.info(f"Found {len(elements)} elements: {self.name}")
            return elements
        except Exception as e:
            Log.error(f"Failed to find elements {self.name}: {str(e)}")
            raise
    
    def click(self, timeout: Optional[int] = None):
        """
        Click element
        
        Args:
            timeout: Timeout (seconds)
        """
        try:
            element = self.find(timeout)
            element.click()
            Log.info(f"Clicked element: {self.name}")
        except Exception as e:
            Log.error(f"Failed to click element {self.name}: {str(e)}")
            raise
    
    def send_keys(self, text: str, timeout: Optional[int] = None):
        """
        Send text to element
        
        Args:
            text: Text to input
            timeout: Timeout (seconds)
        """
        try:
            element = self.find(timeout)
            element.clear()
            element.send_keys(text)
            Log.info(f"Sent keys '{text}' to element: {self.name}")
        except Exception as e:
            Log.error(f"Failed to send keys to element {self.name}: {str(e)}")
            raise
    
    def get_text(self, timeout: Optional[int] = None) -> str:
        """
        Get element text
        
        Args:
            timeout: Timeout (seconds)
            
        Returns:
            str: Element text
        """
        try:
            element = self.find(timeout)
            text = element.text
            Log.info(f"Got text '{text}' from element: {self.name}")
            return text
        except Exception as e:
            Log.error(f"Failed to get text from element {self.name}: {str(e)}")
            raise
    
    def get_attribute(self, attribute: str, timeout: Optional[int] = None) -> str:
        """
        Get element attribute
        
        Args:
            attribute: Attribute name
            timeout: Timeout (seconds)
            
        Returns:
            str: Attribute value
        """
        try:
            element = self.find(timeout)
            value = element.get_attribute(attribute)
            Log.info(f"Got attribute '{attribute}={value}' from element: {self.name}")
            return value
        except Exception as e:
            Log.error(f"Failed to get attribute from element {self.name}: {str(e)}")
            raise
    
    def is_displayed(self, timeout: Optional[int] = None) -> bool:
        """
        Check if element is visible
        
        Args:
            timeout: Timeout (seconds)
            
        Returns:
            bool: Whether visible
        """
        try:
            element = self.find(timeout)
            displayed = element.is_displayed()
            Log.info(f"Element {self.name} is {'displayed' if displayed else 'not displayed'}")
            return displayed
        except Exception as e:
            Log.error(f"Failed to check if element {self.name} is displayed: {str(e)}")
            return False
    
    def is_enabled(self, timeout: Optional[int] = None) -> bool:
        """
        Check if element is enabled
        
        Args:
            timeout: Timeout (seconds)
            
        Returns:
            bool: Whether enabled
        """
        try:
            element = self.find(timeout)
            enabled = element.is_enabled()
            Log.info(f"Element {self.name} is {'enabled' if enabled else 'disabled'}")
            return enabled
        except Exception as e:
            Log.error(f"Failed to check if element {self.name} is enabled: {str(e)}")
            return False
    
    def wait_for_clickable(self, timeout: Optional[int] = None) -> WebElement:
        """
        Wait for element to be clickable
        
        Args:
            timeout: Timeout (seconds)
            
        Returns:
            WebElement: Clickable element
        """
        try:
            element = self.driver.wait_for_element_clickable(self.by, self.value, timeout)
            Log.info(f"Element {self.name} is clickable")
            return element
        except Exception as e:
            Log.error(f"Failed to wait for element {self.name} to be clickable: {str(e)}")
            raise
    
    def scroll_to_element(self):
        """Scroll to element position"""
        try:
            element = self.find()
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            Log.info(f"Scrolled to element: {self.name}")
        except Exception as e:
            Log.error(f"Failed to scroll to element {self.name}: {str(e)}")
            raise
    
    def tap(self, x: Optional[int] = None, y: Optional[int] = None):
        """
        Tap element (supports coordinate offset)
        
        Args:
            x: X coordinate offset
            y: Y coordinate offset
        """
        try:
            element = self.find()
            if x is not None and y is not None:
                element.tap(x, y)
                Log.info(f"Tapped element {self.name} at offset ({x}, {y})")
            else:
                element.tap()
                Log.info(f"Tapped element: {self.name}")
        except Exception as e:
            Log.error(f"Failed to tap element {self.name}: {str(e)}")
            raise
    
    def long_press(self, duration: int = 2000):
        """
        Long press element
        
        Args:
            duration: Long press duration (milliseconds)
        """
        try:
            element = self.find()
            element.long_press(duration)
            Log.info(f"Long pressed element {self.name} for {duration}ms")
        except Exception as e:
            Log.error(f"Failed to long press element {self.name}: {str(e)}")
            raise
    
    @property
    def element(self) -> Optional[WebElement]:
        """Get current element instance"""
        return self._element
