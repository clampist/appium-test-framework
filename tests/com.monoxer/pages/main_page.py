"""
Main Page Object for Monoxer App
Monoxer应用主页面对象
"""

import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from core.elements.page_object import PageObject
from core.utils.logger import Log
from datas.test_data import MonoxerTestData


class MainPage(PageObject):
    """Monoxer应用主页面对象"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, MonoxerTestData.WAIT_TIME)
    
    def click_home_tab(self) -> bool:
        """
        点击Home标签
        
        Returns:
            bool: 是否成功
        """
        try:
            home_tab = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ID, MonoxerTestData.Locators.HOME_TAB)
            ))
            home_tab.click()
            Log.info("Clicked home tab")
            time.sleep(2)  # 等待页面加载
            return True
        except Exception as e:
            Log.error(f"Failed to click home tab: {str(e)}")
            return False
    
    def open_sidebar(self) -> bool:
        """
        打开侧边栏
        
        Returns:
            bool: 是否成功
        """
        try:
            header_selector = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ID, MonoxerTestData.Locators.HEADER_SELECTOR)
            ))
            header_selector.click()
            Log.info("Sidebar opened successfully")
            time.sleep(2)  # 等待侧边栏动画
            return True
        except Exception as e:
            Log.error(f"Failed to open sidebar: {str(e)}")
            return False
    
    def click_invitation_code(self) -> bool:
        """
        点击邀请码按钮
        
        Returns:
            bool: 是否成功
        """
        try:
            invitation_code_btn = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ANDROID_UIAUTOMATOR, MonoxerTestData.Locators.INVITATION_CODE_BTN)
            ))
            invitation_code_btn.click()
            Log.info("Clicked 'Enter invitation code'")
            return True
        except Exception as e:
            Log.error(f"Failed to click invitation code: {str(e)}")
            return False
    
    def click_sync_button(self) -> bool:
        """
        点击同步按钮
        
        Returns:
            bool: 是否成功
        """
        try:
            sync_btn = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ANDROID_UIAUTOMATOR, MonoxerTestData.Locators.SYNC_BTN)
            ))
            sync_btn.click()
            Log.info("Clicked 'Sync' button")
            return True
        except Exception as e:
            Log.error(f"Failed to click sync button: {str(e)}")
            return False
    
    def click_linear_layout(self) -> bool:
        """
        点击linear_layout按钮
        
        Returns:
            bool: 是否成功
        """
        try:
            linear_layout_btn = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ID, MonoxerTestData.Locators.LINEAR_LAYOUT)
            ))
            linear_layout_btn.click()
            Log.info("Clicked linear_layout to return to main page")
            time.sleep(2)
            return True
        except Exception as e:
            Log.error(f"Failed to click linear_layout: {str(e)}")
            return False
    
    def click_navigate_up(self) -> bool:
        """
        点击返回按钮
        
        Returns:
            bool: 是否成功
        """
        try:
            back_btn = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ACCESSIBILITY_ID, MonoxerTestData.Locators.NAVIGATE_UP)
            ))
            back_btn.click()
            Log.info("Clicked 'Navigate up' button")
            time.sleep(2)
            return True
        except Exception as e:
            Log.error(f"Failed to click navigate up: {str(e)}")
            return False
    
    def is_page_loaded(self) -> bool:
        """
        检查页面是否加载完成
        
        Returns:
            bool: 是否加载完成
        """
        try:
            # 检查Home标签是否存在
            self.driver.find_element(AppiumBy.ID, MonoxerTestData.Locators.HOME_TAB)
            return True
        except Exception:
            return False
