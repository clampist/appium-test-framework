"""
Library Page Object for Monoxer App
Monoxer应用Library页面对象
"""

import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from core.elements.page_object import PageObject
from core.utils.logger import Log
from datas.test_data import MonoxerTestData


class LibraryPage(PageObject):
    """Monoxer应用Library页面对象"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, MonoxerTestData.WAIT_TIME)
    
    def click_library_tab(self) -> bool:
        """
        点击Library标签
        
        Returns:
            bool: 是否成功
        """
        try:
            library_tab = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ID, MonoxerTestData.Locators.LIBRARY_TAB)
            ))
            library_tab.click()
            Log.info("Clicked library tab")
            time.sleep(2)  # 等待Library页面加载
            return True
        except Exception as e:
            Log.error(f"Failed to click library tab: {str(e)}")
            return False
    
    def click_my_books_tab(self) -> bool:
        """
        点击My Books标签
        
        Returns:
            bool: 是否成功
        """
        try:
            my_books_tab = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ACCESSIBILITY_ID, MonoxerTestData.Locators.MY_BOOKS_TAB)
            ))
            my_books_tab.click()
            Log.info("Clicked 'My Books' tab")
            time.sleep(2)  # 等待My Books内容加载
            return True
        except Exception as e:
            Log.error(f"My Books tab not found: {str(e)}")
            return False
    
    def click_auto_test_title(self) -> bool:
        """
        点击auto_test标题
        
        Returns:
            bool: 是否成功
        """
        try:
            auto_test_title = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.XPATH, MonoxerTestData.Locators.AUTO_TEST_TITLE)
            ))
            auto_test_title.click()
            Log.info("Clicked 'auto_test' title")
            time.sleep(2)  # 等待页面加载
            return True
        except Exception as e:
            Log.error(f"Failed to click auto_test title: {str(e)}")
            return False
    
    def click_open_deck_button(self) -> bool:
        """
        点击open_deck按钮
        
        Returns:
            bool: 是否成功
        """
        try:
            open_deck_btn = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ID, MonoxerTestData.Locators.OPEN_DECK_BTN)
            ))
            open_deck_btn.click()
            Log.info("Clicked 'Open Deck' button")
            time.sleep(2)  # 等待deck打开
            return True
        except Exception as e:
            Log.error(f"Failed to click open_deck button: {str(e)}")
            return False
    
    def click_start_test_button(self) -> bool:
        """
        点击start_test按钮
        
        Returns:
            bool: 是否成功
        """
        try:
            # 尝试多种方法找到start_test按钮
            start_test_btn = None
            
            try:
                # 方法1: 尝试精确ID
                start_test_btn = self.wait.until(EC.element_to_be_clickable(
                    (AppiumBy.ID, MonoxerTestData.Locators.START_TEST_BTN)
                ))
                Log.info("Found start_test button with ID")
            except:
                try:
                    # 方法2: 尝试类名
                    start_test_btn = self.driver.find_element(AppiumBy.CLASS_NAME, "android.widget.Button")
                    Log.info("Found start_test button with class name")
                except:
                    try:
                        # 方法3: 尝试UiAutomator
                        start_test_btn = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 
                            'new UiSelector().resourceId("com.monoxer:id/start_test")')
                        Log.info("Found start_test button with UiAutomator")
                    except:
                        try:
                            # 方法4: 尝试XPath
                            start_test_btn = self.driver.find_element(AppiumBy.XPATH, 
                                '//android.widget.Button[@resource-id="com.monoxer:id/start_test"]')
                            Log.info("Found start_test button with XPath")
                        except:
                            try:
                                # 方法5: 尝试文本内容
                                start_test_btn = self.driver.find_element(AppiumBy.XPATH, "//*[@text='STUDY']")
                                Log.info("Found start_test button with text 'STUDY'")
                            except:
                                Log.error("Could not find start_test button")
                                return False
            
            if start_test_btn:
                start_test_btn.click()
                Log.info("Clicked 'Start Test' button")
                time.sleep(3)  # 等待STUDY页面加载
                return True
            else:
                return False
                
        except Exception as e:
            Log.error(f"Failed to click start_test button: {str(e)}")
            return False
    
    def answer_study_question(self, question_number: int = 1) -> bool:
        """
        回答STUDY问题
        
        Args:
            question_number: 问题编号
            
        Returns:
            bool: 是否成功
        """
        try:
            # 尝试找到choice1_text（选择题）
            try:
                choice1 = self.wait.until(EC.element_to_be_clickable(
                    (AppiumBy.ID, MonoxerTestData.Locators.CHOICE1_TEXT)
                ))
                choice1.click()
                Log.info(f"Clicked first choice for question {question_number} (multiple choice)")
                time.sleep(0.001)
                return True
                
            except Exception as choice_error:
                Log.info(f"No multiple choice found for question {question_number}, trying fill-in-the-blank...")
                
                # 尝试点击虚拟键盘上的Done按钮（填空题）
                try:
                    done_btn = self.wait.until(EC.element_to_be_clickable(
                        (AppiumBy.ANDROID_UIAUTOMATOR, MonoxerTestData.Locators.DONE_BTN)
                    ))
                    done_btn.click()
                    Log.info(f"Clicked 'Done' button for question {question_number} (fill-in-the-blank)")
                    
                except Exception as done_error:
                    try:
                        # 替代XPath方法
                        done_btn = self.driver.find_element(AppiumBy.XPATH, MonoxerTestData.Locators.DONE_BTN_XPATH)
                        done_btn.click()
                        Log.info(f"Clicked 'Done' button for question {question_number} (fill-in-the-blank) - XPath")
                        
                    except Exception as xpath_error:
                        Log.error(f"Could not find Done button for question {question_number}: {str(xpath_error)}")
                        return False
                
                time.sleep(0.001)
                return True
                
        except Exception as e:
            Log.error(f"Failed to answer question {question_number}: {str(e)}")
            return False
    
    def click_back_from_study(self) -> bool:
        """
        从STUDY模式点击返回按钮
        
        Returns:
            bool: 是否成功
        """
        try:
            back_btn = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ACCESSIBILITY_ID, MonoxerTestData.Locators.NAVIGATE_UP)
            ))
            back_btn.click()
            Log.info("Clicked back button from STUDY mode")
            time.sleep(2)  # 等待返回deck页面
            return True
        except Exception as e:
            Log.error(f"Failed to click back button from STUDY: {str(e)}")
            return False
