"""
Page Object Base Class
页面对象基类，实现Page Object Model模式
"""

from typing import Dict, Any, Optional
from appium.webdriver.common.appiumby import AppiumBy

from .base_element import BaseElement
from ..utils.logger import Log


class PageObject:
    """页面对象基类"""
    
    def __init__(self, driver):
        """
        初始化页面对象
        
        Args:
            driver: Appium驱动实例
        """
        self.driver = driver
        self.elements: Dict[str, BaseElement] = {}
        self._init_elements()
    
    def _init_elements(self):
        """初始化页面元素，子类需要重写此方法"""
        pass
    
    def add_element(self, name: str, by: str, value: str, element_name: str = ""):
        """
        添加页面元素
        
        Args:
            name: 元素名称
            by: 定位方式
            value: 定位值
            element_name: 元素显示名称
        """
        self.elements[name] = BaseElement(
            self.driver, by, value, element_name or name
        )
    
    def get_element(self, name: str) -> BaseElement:
        """
        获取页面元素
        
        Args:
            name: 元素名称
            
        Returns:
            BaseElement: 页面元素
        """
        if name not in self.elements:
            raise KeyError(f"Element '{name}' not found in page object")
        return self.elements[name]
    
    def wait_for_page_load(self, timeout: Optional[int] = None):
        """
        等待页面加载完成
        
        Args:
            timeout: 超时时间（秒）
        """
        # 子类可以重写此方法实现具体的页面加载等待逻辑
        Log.info("Waiting for page to load...")
    
    def is_page_loaded(self) -> bool:
        """
        检查页面是否加载完成
        
        Returns:
            bool: 页面是否加载完成
        """
        # 子类可以重写此方法实现具体的页面加载检查逻辑
        return True
    
    def take_screenshot(self, name: str = ""):
        """
        页面截图
        
        Args:
            name: 截图名称
        """
        try:
            filename = f"{self.__class__.__name__}_{name}.png" if name else f"{self.__class__.__name__}.png"
            self.driver.take_screenshot(filename)
            Log.info(f"Page screenshot saved: {filename}")
        except Exception as e:
            Log.error(f"Failed to take page screenshot: {str(e)}")
    
    def get_page_title(self) -> str:
        """
        获取页面标题
        
        Returns:
            str: 页面标题
        """
        try:
            # 尝试获取页面标题，具体实现取决于应用类型
            if hasattr(self.driver, 'title'):
                return self.driver.title
            else:
                # 对于移动应用，可能需要通过特定元素获取标题
                return "Mobile App Page"
        except Exception as e:
            Log.error(f"Failed to get page title: {str(e)}")
            return ""
    
    def scroll_to_element(self, element_name: str):
        """
        滚动到指定元素
        
        Args:
            element_name: 元素名称
        """
        element = self.get_element(element_name)
        element.scroll_to_element()
    
    def wait_for_element(self, element_name: str, timeout: Optional[int] = None):
        """
        等待元素出现
        
        Args:
            element_name: 元素名称
            timeout: 超时时间（秒）
        """
        element = self.get_element(element_name)
        element.find(timeout)
    
    def click_element(self, element_name: str, timeout: Optional[int] = None):
        """
        点击元素
        
        Args:
            element_name: 元素名称
            timeout: 超时时间（秒）
        """
        element = self.get_element(element_name)
        element.click(timeout)
    
    def input_text(self, element_name: str, text: str, timeout: Optional[int] = None):
        """
        向元素输入文本
        
        Args:
            element_name: 元素名称
            text: 要输入的文本
            timeout: 超时时间（秒）
        """
        element = self.get_element(element_name)
        element.send_keys(text, timeout)
    
    def get_element_text(self, element_name: str, timeout: Optional[int] = None) -> str:
        """
        获取元素文本
        
        Args:
            element_name: 元素名称
            timeout: 超时时间（秒）
            
        Returns:
            str: 元素文本
        """
        element = self.get_element(element_name)
        return element.get_text(timeout)
    
    def is_element_displayed(self, element_name: str, timeout: Optional[int] = None) -> bool:
        """
        检查元素是否可见
        
        Args:
            element_name: 元素名称
            timeout: 超时时间（秒）
            
        Returns:
            bool: 是否可见
        """
        element = self.get_element(element_name)
        return element.is_displayed(timeout)
    
    def is_element_enabled(self, element_name: str, timeout: Optional[int] = None) -> bool:
        """
        检查元素是否启用
        
        Args:
            element_name: 元素名称
            timeout: 超时时间（秒）
            
        Returns:
            bool: 是否启用
        """
        element = self.get_element(element_name)
        return element.is_enabled(timeout)
    
    def wait_for_element_clickable(self, element_name: str, timeout: Optional[int] = None):
        """
        等待元素可点击
        
        Args:
            element_name: 元素名称
            timeout: 超时时间（秒）
        """
        element = self.get_element(element_name)
        element.wait_for_clickable(timeout)
    
    def tap_element(self, element_name: str, x: Optional[int] = None, y: Optional[int] = None):
        """
        点击元素（支持坐标偏移）
        
        Args:
            element_name: 元素名称
            x: X坐标偏移
            y: Y坐标偏移
        """
        element = self.get_element(element_name)
        element.tap(x, y)
    
    def long_press_element(self, element_name: str, duration: int = 2000):
        """
        长按元素
        
        Args:
            element_name: 元素名称
            duration: 长按持续时间（毫秒）
        """
        element = self.get_element(element_name)
        element.long_press(duration)
