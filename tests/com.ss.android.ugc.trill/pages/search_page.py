"""
Search Page Object for TikTok App
"""

import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from core.elements.page_object import PageObject
from core.utils.logger import Log
from datas.test_data import BaseTikTokTestData


class SearchPage(PageObject):
    """Search page object for TikTok App"""
    
    def __init__(self, driver, test_data=None):
        super().__init__(driver)
        self.test_data = test_data or BaseTikTokTestData()
        self.wait = WebDriverWait(driver, self.test_data.WAIT_TIME)
    
    def click_search_bar(self) -> bool:
        """Click search bar to open search"""
        try:
            search_bar = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ID, self.test_data.CommonLocators.SEARCH_BAR)
            ))
            search_bar.click()
            Log.info("Clicked search bar")
            time.sleep(self.test_data.CommonTestData.ANIMATION_WAIT_TIME)
            return True
        except Exception as e:
            Log.error(f"Failed to click search bar: {str(e)}")
            return False
    
    def enter_search_keyword(self, keyword: str) -> bool:
        """Enter search keyword"""
        try:
            search_input = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ID, self.test_data.CommonLocators.SEARCH_INPUT)
            ))
            search_input.clear()
            search_input.send_keys(keyword)
            Log.info(f"Entered search keyword: {keyword}")
            time.sleep(1)
            return True
        except Exception as e:
            Log.error(f"Failed to enter search keyword: {str(e)}")
            return False
    
    def click_search_button(self) -> bool:
        """Click search button"""
        try:
            search_btn = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ID, self.test_data.CommonLocators.SEARCH_BTN)
            ))
            search_btn.click()
            Log.info("Clicked search button")
            time.sleep(self.test_data.CommonTestData.LOADING_WAIT_TIME)
            return True
        except Exception as e:
            Log.error(f"Failed to click search button: {str(e)}")
            return False
    
    def search_for_keyword(self, keyword: str) -> bool:
        """Complete search flow for a keyword"""
        try:
            # Click search bar
            if not self.click_search_bar():
                return False
            
            # Enter keyword
            if not self.enter_search_keyword(keyword):
                return False
            
            # Click search button
            if not self.click_search_button():
                return False
            
            Log.info(f"Successfully searched for: {keyword}")
            return True
        except Exception as e:
            Log.error(f"Search flow failed: {str(e)}")
            return False
    
    def click_trending_tab(self) -> bool:
        """Click trending tab"""
        try:
            trending_tab = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ANDROID_UIAUTOMATOR, self.test_data.Locators.TRENDING_TEXT)
            ))
            trending_tab.click()
            Log.info("Clicked trending tab")
            time.sleep(self.test_data.CommonTestData.ANIMATION_WAIT_TIME)
            return True
        except Exception as e:
            Log.error(f"Failed to click trending tab: {str(e)}")
            return False
    
    def click_first_search_result(self) -> bool:
        """Click first search result"""
        try:
            # Try to find first video result
            first_result = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.CLASS_NAME, "android.widget.FrameLayout")
            ))
            first_result.click()
            Log.info("Clicked first search result")
            time.sleep(self.test_data.CommonTestData.ANIMATION_WAIT_TIME)
            return True
        except Exception as e:
            Log.error(f"Failed to click first search result: {str(e)}")
            return False
    
    def click_back_button(self) -> bool:
        """Click back button to return from search"""
        try:
            back_btn = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ID, self.test_data.CommonLocators.BACK_BTN)
            ))
            back_btn.click()
            Log.info("Clicked back button")
            time.sleep(self.test_data.CommonTestData.ANIMATION_WAIT_TIME)
            return True
        except Exception as e:
            Log.error(f"Failed to click back button: {str(e)}")
            return False
    
    def is_search_results_loaded(self) -> bool:
        """Check if search results are loaded"""
        try:
            # Wait for search results to appear
            self.wait.until(EC.presence_of_element_located(
                (AppiumBy.CLASS_NAME, "android.widget.FrameLayout")
            ))
            Log.info("Search results loaded successfully")
            return True
        except Exception as e:
            Log.error(f"Search results not loaded: {str(e)}")
            return False

