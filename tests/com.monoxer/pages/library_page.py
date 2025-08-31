"""
Library Page Object for Monoxer App
Library page object for Monoxer App
"""

import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from core.elements.page_object import PageObject
from core.utils.logger import Log
from datas.test_data import MonoxerTestData


class LibraryPage(PageObject):
    """Library page object for Monoxer App"""
    
    def __init__(self, driver, test_data=None):
        super().__init__(driver)
        self.test_data = test_data or MonoxerTestData
        self.wait = WebDriverWait(driver, self.test_data.WAIT_TIME)
    
    def click_library_tab(self) -> bool:
        """
        Click Library tab
        
        Returns:
            bool: Whether successful
        """
        try:
            library_tab = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ID, self.test_data.Locators.LIBRARY_TAB)
            ))
            library_tab.click()
            Log.info("Clicked library tab")
            time.sleep(2)  # Wait for Library page to load
            return True
        except Exception as e:
            Log.error(f"Failed to click library tab: {str(e)}")
            return False
    
    def click_my_books_tab(self) -> bool:
        """
        Click My Books tab
        
        Returns:
            bool: Whether successful
        """
        try:
            my_books_tab = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ACCESSIBILITY_ID, self.test_data.Locators.MY_BOOKS_TAB)
            ))
            my_books_tab.click()
            Log.info("Clicked 'My Books' tab")
            time.sleep(2)  # Wait for My Books content to load
            return True
        except Exception as e:
            Log.error(f"My Books tab not found: {str(e)}")
            return False
    
    def click_auto_test_title(self) -> bool:
        """
        Click auto_test title
        
        Returns:
            bool: Whether successful
        """
        try:
            auto_test_title = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.XPATH, self.test_data.Locators.AUTO_TEST_TITLE)
            ))
            auto_test_title.click()
            Log.info("Clicked 'auto_test' title")
            time.sleep(2)  # Wait for page to load
            return True
        except Exception as e:
            Log.error(f"Failed to click auto_test title: {str(e)}")
            return False
    
    def click_open_deck_button(self) -> bool:
        """
        Click open_deck button
        
        Returns:
            bool: Whether successful
        """
        try:
            open_deck_btn = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ID, self.test_data.Locators.OPEN_DECK_BTN)
            ))
            open_deck_btn.click()
            Log.info("Clicked 'Open Deck' button")
            time.sleep(2)  # Wait for deck to open
            return True
        except Exception as e:
            Log.error(f"Failed to click open_deck button: {str(e)}")
            return False
    
    def click_start_test_button(self) -> bool:
        """
        Click start_test button
        
        Returns:
            bool: Whether successful
        """
        try:
            # Try multiple methods to find start_test button
            start_test_btn = None
            
            try:
                # Method 1: Try exact ID
                start_test_btn = self.wait.until(EC.element_to_be_clickable(
                    (AppiumBy.ID, self.test_data.Locators.START_TEST_BTN)
                ))
                Log.info("Found start_test button with ID")
            except:
                try:
                    # Method 2: Try class name
                    start_test_btn = self.driver.find_element(AppiumBy.CLASS_NAME, "android.widget.Button")
                    Log.info("Found start_test button with class name")
                except:
                    try:
                        # Method 3: Try UiAutomator
                        start_test_btn = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 
                            'new UiSelector().resourceId("com.monoxer:id/start_test")')
                        Log.info("Found start_test button with UiAutomator")
                    except:
                        try:
                            # Method 4: Try XPath
                            start_test_btn = self.driver.find_element(AppiumBy.XPATH, 
                                '//android.widget.Button[@resource-id="com.monoxer:id/start_test"]')
                            Log.info("Found start_test button with XPath")
                        except:
                            try:
                                # Method 5: Try text content
                                start_test_btn = self.driver.find_element(AppiumBy.XPATH, "//*[@text='STUDY']")
                                Log.info("Found start_test button with text 'STUDY'")
                            except:
                                Log.error("Could not find start_test button")
                                return False
            
            if start_test_btn:
                start_test_btn.click()
                Log.info("Clicked 'Start Test' button")
                time.sleep(3)  # Wait for STUDY page to load
                return True
            else:
                return False
                
        except Exception as e:
            Log.error(f"Failed to click start_test button: {str(e)}")
            return False
    
    def answer_study_question(self, question_number: int = 1) -> bool:
        """
        Answer STUDY question
        
        Args:
            question_number: Question number
            
        Returns:
            bool: Whether successful
        """
        try:
            # Try to find choice1_text (multiple choice)
            try:
                choice1 = self.wait.until(EC.element_to_be_clickable(
                    (AppiumBy.ID, self.test_data.Locators.CHOICE1_TEXT)
                ))
                choice1.click()
                Log.info(f"Clicked first choice for question {question_number} (multiple choice)")
                time.sleep(0.001)
                return True
                
            except Exception as choice_error:
                Log.info(f"No multiple choice found for question {question_number}, trying fill-in-the-blank...")
                
                # Try to click Done button on virtual keyboard (fill-in-the-blank)
                try:
                    done_btn = self.wait.until(EC.element_to_be_clickable(
                        (AppiumBy.ANDROID_UIAUTOMATOR, self.test_data.Locators.DONE_BTN)
                    ))
                    done_btn.click()
                    Log.info(f"Clicked 'Done' button for question {question_number} (fill-in-the-blank)")
                    
                except Exception as done_error:
                    try:
                        # Alternative XPath method
                        done_btn = self.driver.find_element(AppiumBy.XPATH, self.test_data.Locators.DONE_BTN_XPATH)
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
        Click back button from STUDY mode
        
        Returns:
            bool: Whether successful
        """
        try:
            back_btn = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ACCESSIBILITY_ID, self.test_data.Locators.NAVIGATE_UP)
            ))
            back_btn.click()
            Log.info("Clicked back button from STUDY mode")
            time.sleep(2)  # Wait to return to deck page
            return True
        except Exception as e:
            Log.error(f"Failed to click back button from STUDY: {str(e)}")
            return False
