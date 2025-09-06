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
    
    def tap_screen_center(self) -> bool:
        """Tap screen center to activate app interface"""
        try:
            # Get screen dimensions
            screen_size = self.driver.get_window_size()
            center_x = screen_size['width'] // 2
            center_y = screen_size['height'] // 2
            
            # Tap at screen center
            self.driver.tap([(center_x, center_y)], 1)
            Log.info(f"Tapped screen center at ({center_x}, {center_y})")
            time.sleep(0.5)  # Short wait after tap
            return True
            
        except Exception as e:
            Log.error(f"Failed to tap screen center: {str(e)}")
            return False

    def debug_app_state(self) -> None:
        """Debug method to check app state and available elements (ultra-optimized)"""
        try:
            Log.info("=== App State Debug Info ===")
            
            # Get current activity (fast operation)
            current_activity = self.driver.current_activity
            Log.info(f"Current activity: {current_activity}")
            
            # Skip all element checks as they are very slow
            Log.info("Skipping all element checks (too slow)")
            Log.info("App appears to be responsive based on activity")
            
            Log.info("=== End Debug Info ===")
            
        except Exception as e:
            Log.error(f"Debug method failed: {str(e)}")
    
    def click_home_tab(self) -> bool:
        """Click Home tab (ultra-optimized)"""
        try:
            Log.info(f"Looking for home tab with ID: {self.test_data.CommonLocators.HOME_TAB}")
            
            # Use progressive wait strategy: 1s, 2s, 3s
            for timeout in [1, 2, 3]:
                try:
                    Log.info(f"Trying with {timeout}s timeout...")
                    short_wait = WebDriverWait(self.driver, timeout)
                    home_tab = short_wait.until(EC.element_to_be_clickable(
                        (AppiumBy.ID, self.test_data.CommonLocators.HOME_TAB)
                    ))
                    
                    Log.info("Home tab element found, attempting to click...")
                    home_tab.click()
                    Log.info("Clicked home tab")
                    time.sleep(self.test_data.CommonTestData.ANIMATION_WAIT_TIME)
                    return True
                    
                except Exception as e:
                    Log.warning(f"Timeout {timeout}s failed: {str(e)}")
                    if timeout == 3:  # Last attempt
                        raise e
                    continue
            
        except Exception as e:
            Log.error(f"All timeout attempts failed: {str(e)}")
            return False
    
    def click_friends_tab(self) -> bool:
        """Click Friends tab (optimized)"""
        try:
            # Use shorter wait time for faster failure detection
            short_wait = WebDriverWait(self.driver, 3)  # 3 second timeout
            
            friends_tab = short_wait.until(EC.element_to_be_clickable(
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
        """Click Inbox tab (optimized)"""
        try:
            # Use shorter wait time for faster failure detection
            short_wait = WebDriverWait(self.driver, 3)  # 3 second timeout
            
            inbox_tab = short_wait.until(EC.element_to_be_clickable(
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
        """Click Profile tab (optimized)"""
        try:
            # Use shorter wait time for faster failure detection
            short_wait = WebDriverWait(self.driver, 3)  # 3 second timeout
            
            profile_tab = short_wait.until(EC.element_to_be_clickable(
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
        """Click create tab and then close it (optimized)"""
        try:
            # Use shorter wait time for faster failure detection
            short_wait = WebDriverWait(self.driver, 3)  # 3 second timeout
            
            # Click create tab
            create_tab = short_wait.until(EC.element_to_be_clickable(
                (AppiumBy.ID, self.test_data.CommonLocators.CREATE_TAB)
            ))
            create_tab.click()
            Log.info("Clicked create tab")
            time.sleep(self.test_data.CommonTestData.ANIMATION_WAIT_TIME)
            
            # Close create tab
            close_btn = short_wait.until(EC.element_to_be_clickable(
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

