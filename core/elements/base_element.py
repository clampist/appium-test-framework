"""
Base Element Class
基础元素类，封装常用的元素操作方法
"""

from typing import Optional, List
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import WebDriverException
from appium.webdriver.common.appiumby import AppiumBy

from ..utils.logger import Log


class BaseElement:
    """基础元素类"""
    
    def __init__(self, driver, by: str, value: str, name: str = ""):
        """
        初始化元素
        
        Args:
            driver: Appium驱动实例
            by: 定位方式
            value: 定位值
            name: 元素名称（用于日志）
        """
        self.driver = driver
        self.by = by
        self.value = value
        self.name = name or f"{by}={value}"
        self._element: Optional[WebElement] = None
    
    def find(self, timeout: Optional[int] = None) -> WebElement:
        """
        查找元素
        
        Args:
            timeout: 超时时间（秒）
            
        Returns:
            WebElement: 找到的元素
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
        查找所有匹配的元素
        
        Args:
            timeout: 超时时间（秒）
            
        Returns:
            List[WebElement]: 找到的元素列表
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
        点击元素
        
        Args:
            timeout: 超时时间（秒）
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
        向元素输入文本
        
        Args:
            text: 要输入的文本
            timeout: 超时时间（秒）
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
        获取元素文本
        
        Args:
            timeout: 超时时间（秒）
            
        Returns:
            str: 元素文本
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
        获取元素属性
        
        Args:
            attribute: 属性名
            timeout: 超时时间（秒）
            
        Returns:
            str: 属性值
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
        检查元素是否可见
        
        Args:
            timeout: 超时时间（秒）
            
        Returns:
            bool: 是否可见
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
        检查元素是否启用
        
        Args:
            timeout: 超时时间（秒）
            
        Returns:
            bool: 是否启用
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
        等待元素可点击
        
        Args:
            timeout: 超时时间（秒）
            
        Returns:
            WebElement: 可点击的元素
        """
        try:
            element = self.driver.wait_for_element_clickable(self.by, self.value, timeout)
            Log.info(f"Element {self.name} is clickable")
            return element
        except Exception as e:
            Log.error(f"Failed to wait for element {self.name} to be clickable: {str(e)}")
            raise
    
    def scroll_to_element(self):
        """滚动到元素位置"""
        try:
            element = self.find()
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            Log.info(f"Scrolled to element: {self.name}")
        except Exception as e:
            Log.error(f"Failed to scroll to element {self.name}: {str(e)}")
            raise
    
    def tap(self, x: Optional[int] = None, y: Optional[int] = None):
        """
        点击元素（支持坐标偏移）
        
        Args:
            x: X坐标偏移
            y: Y坐标偏移
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
        长按元素
        
        Args:
            duration: 长按持续时间（毫秒）
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
        """获取当前元素实例"""
        return self._element
