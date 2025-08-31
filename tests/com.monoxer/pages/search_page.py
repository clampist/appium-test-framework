"""
Search Page Object for Monoxer App
Search page object for Monoxer App
"""

import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from core.elements.page_object import PageObject
from core.utils.logger import Log
from datas.test_data import MonoxerTestData


class SearchPage(PageObject):
    """Search page object for Monoxer App"""
    
    def __init__(self, driver, test_data=None):
        super().__init__(driver)
        self.test_data = test_data or MonoxerTestData
        self.wait = WebDriverWait(driver, self.test_data.WAIT_TIME)
    
    def click_search_tab(self) -> bool:
        """
        Click search tab
        
        Returns:
            bool: Whether successful
        """
        try:
            search_tab = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ID, self.test_data.Locators.SEARCH_TAB)
            ))
            search_tab.click()
            Log.info("Clicked search tab")
            time.sleep(2)  # Wait for search page to load
            return True
        except Exception as e:
            Log.error(f"Failed to click search tab: {str(e)}")
            return False
    
    def search_keyword(self, keyword: str) -> bool:
        """
        Search keyword
        
        Args:
            keyword: Search keyword
            
        Returns:
            bool: Whether successful
        """
        try:
            # Try multiple methods to find search input field
            search_input = None
            
            # Method 1: Try search_src_text ID
            try:
                search_input = self.wait.until(EC.element_to_be_clickable(
                    (AppiumBy.ID, self.test_data.Locators.SEARCH_INPUT)
                ))
                Log.info("Found search input with search_src_text ID")
            except:
                # Method 2: Try search_view ID
                try:
                    search_input = self.wait.until(EC.element_to_be_clickable(
                        (AppiumBy.ID, self.test_data.Locators.SEARCH_VIEW)
                    ))
                    Log.info("Found search input with search_view ID")
                except:
                    # Method 3: Try AutoCompleteTextView class
                    try:
                        search_input = self.driver.find_element(AppiumBy.CLASS_NAME, "android.widget.AutoCompleteTextView")
                        Log.info("Found search input with AutoCompleteTextView class")
                    except:
                        # Method 4: Try UiAutomator
                        try:
                            search_input = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 
                                'new UiSelector().className("android.widget.AutoCompleteTextView")')
                            Log.info("Found search input with UiAutomator")
                        except:
                            Log.error("Could not find search input field")
                            return False
            
            if search_input:
                # Click search input field
                search_input.click()
                Log.info("Clicked search input field")
                
                # Re-find element to avoid stale element reference
                try:
                    search_input = self.wait.until(EC.element_to_be_clickable(
                        (AppiumBy.ID, self.test_data.Locators.SEARCH_INPUT)
                    ))
                    # Clear and enter search query
                    search_input.clear()
                    search_input.send_keys(keyword)
                    Log.info(f"Typed search query: {keyword}")
                except:
                    # Try alternative method
                    try:
                        search_input = self.driver.find_element(AppiumBy.CLASS_NAME, "android.widget.AutoCompleteTextView")
                        search_input.clear()
                        search_input.send_keys(keyword)
                        Log.info(f"Typed search query: {keyword} (alternative method)")
                    except Exception as e:
                        Log.error(f"Failed to type in search field: {str(e)}")
                        return False
                
                # Wait for search results
                Log.info("Waiting for search results...")
                time.sleep(3)
                return True
            else:
                return False
                
        except Exception as e:
            Log.error(f"Error in search input interaction: {str(e)}")
            return False
    
    def click_first_result(self) -> bool:
        """
        Click first search result
        
        Returns:
            bool: Whether successful
        """
        try:
            first_result = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ID, self.test_data.Locators.CARD_VIEW)
            ))
            first_result.click()
            Log.info("Clicked first search result")
            time.sleep(2)  # Wait for detail page to load
            return True
        except Exception as e:
            Log.error(f"Search result not found: {str(e)}")
            return False
    
    def click_contents_button(self) -> bool:
        """
        Click contents button
        
        Returns:
            bool: Whether successful
        """
        try:
            contents_btn = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ID, self.test_data.Locators.CONTENTS_BTN)
            ))
            contents_btn.click()
            Log.info("Clicked contents button")
            time.sleep(2)  # Wait for contents page to load
            return True
        except Exception as e:
            Log.error(f"Contents button not found: {str(e)}")
            return False
    
    def click_back_multiple_times(self, times: int = 4) -> bool:
        """
        Click back button multiple times
        
        Args:
            times: Number of clicks
            
        Returns:
            bool: Whether successful
        """
        try:
            for i in range(times):
                try:
                    back_btn = self.wait.until(EC.element_to_be_clickable(
                        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Navigate up")')
                    ))
                    back_btn.click()
                    Log.info(f"Clicked back button ({i+1}/{times})")
                    time.sleep(1)  # Wait between clicks
                except Exception as e:
                    Log.warning(f"Failed to click back button ({i+1}/{times}): {str(e)}")
                    break
            return True
        except Exception as e:
            Log.error(f"Failed to click back buttons: {str(e)}")
            return False
