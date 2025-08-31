"""
Main Page Object for Monoxer App
Main page object for Monoxer App
"""

import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from core.elements.page_object import PageObject
from core.utils.logger import Log
from datas.test_data import MonoxerTestData


class MainPage(PageObject):
    """Main page object for Monoxer App"""
    
    def __init__(self, driver, test_data=None):
        super().__init__(driver)
        self.test_data = test_data or MonoxerTestData
        self.wait = WebDriverWait(driver, self.test_data.WAIT_TIME)
    
    def click_home_tab(self) -> bool:
        """
        Click Home tab
        
        Returns:
            bool: Whether successful
        """
        try:
            home_tab = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ID, self.test_data.Locators.HOME_TAB)
            ))
            home_tab.click()
            Log.info("Clicked home tab")
            time.sleep(2)  # Wait for page to load
            return True
        except Exception as e:
            Log.error(f"Failed to click home tab: {str(e)}")
            return False
    
    def open_sidebar(self) -> bool:
        """
        Open sidebar
        
        Returns:
            bool: Whether successful
        """
        try:
            header_selector = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ID, self.test_data.Locators.HEADER_SELECTOR)
            ))
            header_selector.click()
            Log.info("Sidebar opened successfully")
            time.sleep(2)  # Wait for sidebar animation
            return True
        except Exception as e:
            Log.error(f"Failed to open sidebar: {str(e)}")
            return False
    
    def click_invitation_code(self) -> bool:
        """
        Click invitation code button
        
        Returns:
            bool: Whether successful
        """
        try:
            invitation_code_btn = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ANDROID_UIAUTOMATOR, self.test_data.Locators.INVITATION_CODE_BTN)
            ))
            invitation_code_btn.click()
            Log.info("Clicked 'Enter invitation code'")
            return True
        except Exception as e:
            Log.error(f"Failed to click invitation code: {str(e)}")
            return False
    
    def click_sync_button(self) -> bool:
        """
        Click sync button
        
        Returns:
            bool: Whether successful
        """
        try:
            sync_btn = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ANDROID_UIAUTOMATOR, self.test_data.Locators.SYNC_BTN)
            ))
            sync_btn.click()
            Log.info("Clicked 'Sync' button")
            return True
        except Exception as e:
            Log.error(f"Failed to click sync button: {str(e)}")
            return False
    
    def click_linear_layout(self) -> bool:
        """
        Click linear_layout button
        
        Returns:
            bool: Whether successful
        """
        try:
            linear_layout_btn = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ID, self.test_data.Locators.LINEAR_LAYOUT)
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
        Click back button
        
        Returns:
            bool: Whether successful
        """
        try:
            back_btn = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ACCESSIBILITY_ID, self.test_data.Locators.NAVIGATE_UP)
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
        Check if page is loaded completely
        
        Returns:
            bool: Whether loaded completely
        """
        try:
            # Check if Home tab exists
            self.driver.find_element(AppiumBy.ID, self.test_data.Locators.HOME_TAB)
            return True
        except Exception:
            return False
