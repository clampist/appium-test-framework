"""
Profile Page Object for TikTok App
"""

import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from core.elements.page_object import PageObject
from core.utils.logger import Log
from datas.test_data import BaseTikTokTestData


class ProfilePage(PageObject):
    """Profile page object for TikTok App"""
    
    def __init__(self, driver, test_data=None):
        super().__init__(driver)
        self.test_data = test_data or BaseTikTokTestData()
        self.wait = WebDriverWait(driver, self.test_data.WAIT_TIME)
    
    def click_profile_avatar(self) -> bool:
        """Click profile avatar"""
        try:
            avatar = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ID, self.test_data.CommonLocators.PROFILE_AVATAR)
            ))
            avatar.click()
            Log.info("Clicked profile avatar")
            time.sleep(self.test_data.CommonTestData.ANIMATION_WAIT_TIME)
            return True
        except Exception as e:
            Log.error(f"Failed to click profile avatar: {str(e)}")
            return False
    
    def get_username(self) -> str:
        """Get username text"""
        try:
            username_element = self.wait.until(EC.presence_of_element_located(
                (AppiumBy.ID, self.test_data.CommonLocators.USERNAME_TEXT)
            ))
            username = username_element.text
            Log.info(f"Username: {username}")
            return username
        except Exception as e:
            Log.error(f"Failed to get username: {str(e)}")
            return ""
    
    def is_profile_page_loaded(self) -> bool:
        """Check if profile page is loaded"""
        try:
            # Wait for profile elements to appear
            self.wait.until(EC.presence_of_element_located(
                (AppiumBy.ID, self.test_data.CommonLocators.PROFILE_AVATAR)
            ))
            Log.info("Profile page loaded successfully")
            return True
        except Exception as e:
            Log.error(f"Profile page not loaded: {str(e)}")
            return False
    
    def click_back_button(self) -> bool:
        """Click back button to return from profile"""
        try:
            # 首先尝试点击普通的返回按钮
            try:
                back_btn = self.wait.until(EC.element_to_be_clickable(
                    (AppiumBy.ID, self.test_data.CommonLocators.BACK_BTN)
                ))
                back_btn.click()
                Log.info("Clicked back button")
                time.sleep(self.test_data.CommonTestData.ANIMATION_WAIT_TIME)
                return True
            except Exception:
                Log.info("Back button not found, trying close icon button")
            
            # 如果普通返回按钮不存在，尝试点击关闭图标按钮
            try:
                close_btn = self.wait.until(EC.element_to_be_clickable(
                    (AppiumBy.ANDROID_UIAUTOMATOR, self.test_data.CommonLocators.CLOSE_ICON_BTN)
                ))
                close_btn.click()
                Log.info("Clicked close icon button")
                time.sleep(self.test_data.CommonTestData.ANIMATION_WAIT_TIME)
                return True
            except Exception:
                Log.info("Close icon button not found, trying alternative methods")
            
            # 如果上述方法都失败，尝试使用 XPath 定位
            try:
                close_xpath = '//android.widget.ImageView[@content-desc="Close"]'
                close_btn = self.wait.until(EC.element_to_be_clickable(
                    (AppiumBy.XPATH, close_xpath)
                ))
                close_btn.click()
                Log.info("Clicked close button using XPath")
                time.sleep(self.test_data.CommonTestData.ANIMATION_WAIT_TIME)
                return True
            except Exception as e:
                Log.error(f"All back/close button methods failed: {str(e)}")
                return False
                
        except Exception as e:
            Log.error(f"Failed to click back/close button: {str(e)}")
            return False

