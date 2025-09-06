"""
Main Page Object for TikTok App
"""

import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from core.elements.page_object import PageObject
from core.utils.logger import Log
from datas.test_data import BaseTikTokTestData


class MainPage(PageObject):
    """Main page object for TikTok App - handles navigation and permissions"""
    
    def __init__(self, driver, test_data=None):
        super().__init__(driver)
        self.test_data = test_data or BaseTikTokTestData()
        self.wait = WebDriverWait(driver, self.test_data.WAIT_TIME)
    
    def click_home_tab(self) -> bool:
        """Click Home tab"""
        try:
            home_tab = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ID, self.test_data.CommonLocators.HOME_TAB)
            ))
            home_tab.click()
            Log.info("Clicked home tab")
            time.sleep(self.test_data.CommonTestData.ANIMATION_WAIT_TIME)
            return True
        except Exception as e:
            Log.error(f"Failed to click home tab: {str(e)}")
            return False
    
    def click_friends_tab(self) -> bool:
        """Click Friends tab"""
        try:
            friends_tab = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ID, self.test_data.CommonLocators.FRIENDS_TAB)
            ))
            friends_tab.click()
            Log.info("Clicked friends tab")
            time.sleep(self.test_data.CommonTestData.ANIMATION_WAIT_TIME)
            return True
        except Exception as e:
            Log.error(f"Failed to click friends tab: {str(e)}")
            return False
    
    
    def click_inbox_tab(self) -> bool:
        """Click Inbox tab"""
        try:
            inbox_tab = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ID, self.test_data.CommonLocators.INBOX_TAB)
            ))
            inbox_tab.click()
            Log.info("Clicked inbox tab")
            time.sleep(self.test_data.CommonTestData.ANIMATION_WAIT_TIME)
            return True
        except Exception as e:
            Log.error(f"Failed to click inbox tab: {str(e)}")
            return False
    
    def click_profile_tab(self) -> bool:
        """Click Profile tab"""
        try:
            profile_tab = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ID, self.test_data.CommonLocators.PROFILE_TAB)
            ))
            profile_tab.click()
            Log.info("Clicked profile tab")
            time.sleep(self.test_data.CommonTestData.ANIMATION_WAIT_TIME)
            return True
        except Exception as e:
            Log.error(f"Failed to click profile tab: {str(e)}")
            return False
    
    def handle_permission_dialog(self, allow: bool = True) -> bool:
        """Handle permission dialog"""
        try:
            if allow:
                allow_btn = self.wait.until(EC.element_to_be_clickable(
                    (AppiumBy.ID, self.test_data.CommonLocators.PERMISSION_ALLOW_BTN)
                ))
                allow_btn.click()
                Log.info("Allowed permission")
            else:
                deny_btn = self.wait.until(EC.element_to_be_clickable(
                    (AppiumBy.ID, self.test_data.CommonLocators.PERMISSION_DENY_BTN)
                ))
                deny_btn.click()
                Log.info("Denied permission")
            
            time.sleep(1)
            return True
        except Exception as e:
            Log.warning(f"Permission dialog not found or already handled: {str(e)}")
            return True


    def click_create_tab_and_close(self) -> bool:
        """Click create tab and then close it"""
        try:
            # Click create tab
            create_tab = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ID, self.test_data.CommonLocators.CREATE_TAB)
            ))
            create_tab.click()
            Log.info("Clicked create tab")
            time.sleep(self.test_data.CommonTestData.ANIMATION_WAIT_TIME)
            
            # Close create tab
            close_btn = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ID, self.test_data.CommonLocators.CREATE_CLOSE_BTN)
            ))
            close_btn.click()
            Log.info("Closed create tab")
            time.sleep(self.test_data.CommonTestData.ANIMATION_WAIT_TIME)
            
            Log.info("Successfully clicked and closed create tab")
            return True
        except Exception as e:
            Log.error(f"Failed to click and close create tab: {str(e)}")
            return False

