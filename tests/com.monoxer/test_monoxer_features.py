"""
Monoxer App Feature Tests
"""

import pytest
import time
from core.utils.logger import Log
from core.utils.screenshot_utils import ScreenshotUtils
from datas.test_data import MonoxerTestData
from pages.main_page import MainPage
from pages.search_page import SearchPage
from pages.library_page import LibraryPage


@pytest.mark.monoxer
class TestMonoxerFeatures:
    """Monoxer App feature test class"""
    
    def _initialize_app_and_take_initial_screenshot(self, driver, test_data, feature_name: str = "common"):
        """
        Initialize app and take initial screenshot
        
        Args:
            driver: Appium driver instance
            test_data: Test data class for current language
            feature_name: Feature name for screenshot naming
        """
        # Activate app
        driver.activate_app(test_data.APP_PACKAGE)
        Log.info("App activated")
        
        # Wait for app to load
        time.sleep(5)
        
        # Ensure we start from home page
        main_page = MainPage(driver, test_data)
        main_page.click_home_tab()
        
        # Take initial screenshot with feature name
        ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, f"{feature_name}_initial", "01")
    
    def setup_method(self, method):
        """Test method setup"""
        Log.info(f"Starting test: {method.__name__}")
        # No longer clear screenshot directory, maintain session-level screenshots
    
    def teardown_method(self, method):
        """Test method teardown"""
        Log.info(f"Completed test: {method.__name__}")
        # Screenshot comparison
        Log.info("Comparing screenshots...")
        ScreenshotUtils.compare_screenshots("com.monoxer")
        # Auto set base screenshots
        ScreenshotUtils.auto_set_base_if_successful("com.monoxer")
    
    def test_invitation_code_feature(self, driver, test_data):
        """Test invitation code feature"""
        Log.info("Testing invitation code feature")
        
        # Create page objects
        main_page = MainPage(driver, test_data)
        
        try:
            # Use common initialization method
            self._initialize_app_and_take_initial_screenshot(driver, test_data, "invitation")
            
            # Open sidebar
            assert main_page.open_sidebar(), "Should open sidebar successfully"
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "invitation_sidebar_opened", "02")
            
            # Click invitation code button
            assert main_page.click_invitation_code(), "Should click invitation code successfully"
            time.sleep(1)
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "invitation_code_page", "03a")
            
            # Click back button
            assert main_page.click_navigate_up(), "Should click navigate up successfully"
            
            # Ensure we return to home page
            main_page.click_home_tab()
            
            # Completion screenshot
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "invitation_code_completed", "04")
            
            Log.info("Invitation code feature test completed successfully")
            
        except Exception as e:
            Log.error(f"Invitation code feature test failed: {str(e)}")
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "invitation_code_failed", "04")
            raise
        
        finally:
            # Close app
            try:
                driver.terminate_app(test_data.APP_PACKAGE)
                Log.info("App terminated")
            except Exception as e:
                Log.warning(f"Failed to terminate app: {str(e)}")
    
    def test_sync_feature(self, driver, test_data):
        """Test sync feature"""
        Log.info("Testing sync feature")
        
        # Create page objects
        main_page = MainPage(driver, test_data)
        
        try:
            # Use common initialization method
            self._initialize_app_and_take_initial_screenshot(driver, test_data, "sync")
            
            # Open sidebar
            assert main_page.open_sidebar(), "Should open sidebar successfully"
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "sync_sidebar_opened", "05")
            
            # Click sync button
            assert main_page.click_sync_button(), "Should click sync button successfully"
            time.sleep(1)
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "sync_button_clicked", "05a")
            
            # Wait for sync operation to complete
            Log.info("Waiting for sync operation...")
            time.sleep(3)
            
            # Check for "Synced" toast message
            try:
                synced_toast = driver.find_element("xpath", "//*[contains(@text, 'Synced')]")
                if synced_toast.is_displayed():
                    Log.info("'Synced' toast message detected")
                else:
                    Log.info("Sync operation completed (toast may have disappeared)")
            except:
                Log.info("Sync operation completed")
            
            # Click linear_layout to return to main page
            main_page.click_linear_layout()
            
            # Ensure we return to Home page
            main_page.click_home_tab()
            
            # Completion screenshot
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "sync_completed", "06")
            
            Log.info("Sync feature test completed successfully")
            
        except Exception as e:
            Log.error(f"Sync feature test failed: {str(e)}")
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "sync_failed", "06")
            raise
        
        finally:
            # Close app
            try:
                driver.terminate_app(test_data.APP_PACKAGE)
                Log.info("App terminated")
            except Exception as e:
                Log.warning(f"Failed to terminate app: {str(e)}")
    
    def test_search_feature(self, driver, test_data):
        """Test search feature"""
        Log.info("Testing search feature")
        
        # Create page objects
        main_page = MainPage(driver, test_data)
        search_page = SearchPage(driver, test_data)
        
        try:
            # Use common initialization method
            self._initialize_app_and_take_initial_screenshot(driver, test_data, "search")
            
            # Click search tab
            assert search_page.click_search_tab(), "Should click search tab successfully"
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "search_page_opened", "07")
            
            # Search keyword
            assert search_page.search_keyword(test_data.TestData.SEARCH_KEYWORD), "Should search keyword successfully"
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "search_results", "08")
            
            # Click first search result
            assert search_page.click_first_result(), "Should click first search result successfully"
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "search_result_detail", "09")
            
            # Click contents button
            assert search_page.click_contents_button(), "Should click contents button successfully"
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "search_contents_page", "10")
            
            # Click back button multiple times
            search_page.click_back_multiple_times(4)
            
            # Click Home tab to return to main page
            main_page.click_home_tab()
            
            # Completion screenshot
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "search_completed", "11")
            
            Log.info("Search feature test completed successfully")
            
        except Exception as e:
            Log.error(f"Search feature test failed: {str(e)}")
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "search_failed", "11")
            raise
        
        finally:
            # Close app
            try:
                driver.terminate_app(test_data.APP_PACKAGE)
                Log.info("App terminated")
            except Exception as e:
                Log.warning(f"Failed to terminate app: {str(e)}")
    
    def test_library_feature(self, driver, test_data):
        """Test library feature"""
        Log.info("Testing library feature")
        
        # Create page objects
        main_page = MainPage(driver, test_data)
        library_page = LibraryPage(driver, test_data)
        
        try:
            # Use common initialization method
            self._initialize_app_and_take_initial_screenshot(driver, test_data, "library")
            
            # Click library tab
            assert library_page.click_library_tab(), "Should click library tab successfully"
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "library_page_opened", "12")
            
            # Click My Books tab
            assert library_page.click_my_books_tab(), "Should click My Books tab successfully"
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "library_my_books_tab_selected", "13")
            
            # Try to click open_deck button directly
            try:
                assert library_page.click_open_deck_button(), "Should click open_deck button directly"
                Log.info("Clicked 'Open Deck' button directly")
            except Exception as e:
                Log.info("Open deck button not found directly, trying to click auto_test title first...")
                
                # If open_deck not found, click auto_test title first
                assert library_page.click_auto_test_title(), "Should click auto_test title successfully"
                ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "auto_test_selected", "14a")
                
                # Now try to click open_deck button
                assert library_page.click_open_deck_button(), "Should click open_deck button after selecting auto_test"
            
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "deck_opened", "14")
            
            # Click back button
            assert main_page.click_navigate_up(), "Should click back button successfully"
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "returned_to_library", "15")
            
            # Test STUDY mode
            assert library_page.click_start_test_button(), "Should click start_test button successfully"
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "study_page_opened", "17")
            
            # Answer first question
            assert library_page.answer_study_question(1), "Should answer first question successfully"
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "question1_answered", "18")
            
            # Wait 5 seconds
            Log.info("Waiting 5 seconds...")
            time.sleep(5)
            
            # Answer second question
            assert library_page.answer_study_question(2), "Should answer second question successfully"
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "question2_answered", "19")
            
            # Click back from STUDY mode
            assert library_page.click_back_from_study(), "Should click back from STUDY mode successfully"
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "returned_from_study", "20")
            
            # Ensure we return to home page
            main_page.click_home_tab()
            
            # Completion screenshot
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "library_completed", "16")
            
            Log.info("Library feature test completed successfully")
            
        except Exception as e:
            Log.error(f"Library feature test failed: {str(e)}")
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "library_failed", "16")
            raise
        
        finally:
            # Close app
            try:
                driver.terminate_app(test_data.APP_PACKAGE)
                Log.info("App terminated")
            except Exception as e:
                Log.warning(f"Failed to terminate app: {str(e)}")
