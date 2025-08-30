"""
Search Page Object for Monoxer App
Monoxer应用搜索页面对象
"""

import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from core.elements.page_object import PageObject
from core.utils.logger import Log
from datas.test_data import MonoxerTestData


class SearchPage(PageObject):
    """Monoxer应用搜索页面对象"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, MonoxerTestData.WAIT_TIME)
    
    def click_search_tab(self) -> bool:
        """
        点击搜索标签
        
        Returns:
            bool: 是否成功
        """
        try:
            search_tab = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ID, MonoxerTestData.Locators.SEARCH_TAB)
            ))
            search_tab.click()
            Log.info("Clicked search tab")
            time.sleep(2)  # 等待搜索页面加载
            return True
        except Exception as e:
            Log.error(f"Failed to click search tab: {str(e)}")
            return False
    
    def search_keyword(self, keyword: str) -> bool:
        """
        搜索关键词
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            bool: 是否成功
        """
        try:
            # 尝试多种方法找到搜索输入框
            search_input = None
            
            # 方法1: 尝试search_src_text ID
            try:
                search_input = self.wait.until(EC.element_to_be_clickable(
                    (AppiumBy.ID, MonoxerTestData.Locators.SEARCH_INPUT)
                ))
                Log.info("Found search input with search_src_text ID")
            except:
                # 方法2: 尝试search_view ID
                try:
                    search_input = self.wait.until(EC.element_to_be_clickable(
                        (AppiumBy.ID, MonoxerTestData.Locators.SEARCH_VIEW)
                    ))
                    Log.info("Found search input with search_view ID")
                except:
                    # 方法3: 尝试AutoCompleteTextView类
                    try:
                        search_input = self.driver.find_element(AppiumBy.CLASS_NAME, "android.widget.AutoCompleteTextView")
                        Log.info("Found search input with AutoCompleteTextView class")
                    except:
                        # 方法4: 尝试UiAutomator
                        try:
                            search_input = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 
                                'new UiSelector().className("android.widget.AutoCompleteTextView")')
                            Log.info("Found search input with UiAutomator")
                        except:
                            Log.error("Could not find search input field")
                            return False
            
            if search_input:
                # 点击搜索输入框
                search_input.click()
                Log.info("Clicked search input field")
                
                # 重新查找元素避免stale element reference
                try:
                    search_input = self.wait.until(EC.element_to_be_clickable(
                        (AppiumBy.ID, MonoxerTestData.Locators.SEARCH_INPUT)
                    ))
                    # 清空并输入搜索查询
                    search_input.clear()
                    search_input.send_keys(keyword)
                    Log.info(f"Typed search query: {keyword}")
                except:
                    # 尝试替代方法
                    try:
                        search_input = self.driver.find_element(AppiumBy.CLASS_NAME, "android.widget.AutoCompleteTextView")
                        search_input.clear()
                        search_input.send_keys(keyword)
                        Log.info(f"Typed search query: {keyword} (alternative method)")
                    except Exception as e:
                        Log.error(f"Failed to type in search field: {str(e)}")
                        return False
                
                # 等待搜索结果
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
        点击第一个搜索结果
        
        Returns:
            bool: 是否成功
        """
        try:
            first_result = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ID, MonoxerTestData.Locators.CARD_VIEW)
            ))
            first_result.click()
            Log.info("Clicked first search result")
            time.sleep(2)  # 等待详情页面加载
            return True
        except Exception as e:
            Log.error(f"Search result not found: {str(e)}")
            return False
    
    def click_contents_button(self) -> bool:
        """
        点击contents按钮
        
        Returns:
            bool: 是否成功
        """
        try:
            contents_btn = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ID, MonoxerTestData.Locators.CONTENTS_BTN)
            ))
            contents_btn.click()
            Log.info("Clicked contents button")
            time.sleep(2)  # 等待contents页面加载
            return True
        except Exception as e:
            Log.error(f"Contents button not found: {str(e)}")
            return False
    
    def click_back_multiple_times(self, times: int = 4) -> bool:
        """
        多次点击返回按钮
        
        Args:
            times: 点击次数
            
        Returns:
            bool: 是否成功
        """
        try:
            for i in range(times):
                try:
                    back_btn = self.wait.until(EC.element_to_be_clickable(
                        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Navigate up")')
                    ))
                    back_btn.click()
                    Log.info(f"Clicked back button ({i+1}/{times})")
                    time.sleep(1)  # 点击间隔等待
                except Exception as e:
                    Log.warning(f"Failed to click back button ({i+1}/{times}): {str(e)}")
                    break
            return True
        except Exception as e:
            Log.error(f"Failed to click back buttons: {str(e)}")
            return False
