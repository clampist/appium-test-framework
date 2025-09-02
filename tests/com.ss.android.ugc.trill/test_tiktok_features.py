"""
TikTok App Feature Tests
TikTok App automated test suite for core features
"""

import pytest
import time
from core.utils.logger import Log
from core.utils.screenshot_utils import ScreenshotUtils
from datas.test_data import get_test_data
from pages.main_page import MainPage
from pages.search_page import SearchPage
from pages.profile_page import ProfilePage
from pages.video_page import VideoPage


@pytest.mark.tiktok
class TestTikTokFeatures:
    """TikTok App feature test class"""
    
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
        Log.info("TikTok app activated")
        
        # Wait for app to load
        time.sleep(5)
        
        # Handle permission dialogs if they appear
        main_page = MainPage(driver, test_data)
        main_page.handle_permission_dialog(allow=True)
        
        # Ensure we start from home page
        main_page.click_home_tab()
        
        # Take initial screenshot with feature name
        ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, f"{feature_name}_initial", "01")
    
    def setup_method(self, method):
        """Test method setup"""
        Log.info(f"Starting test: {method.__name__}")
    
    def teardown_method(self, method):
        """Test method teardown"""
        Log.info(f"Completed test: {method.__name__}")
        # Screenshot comparison
        Log.info("Comparing screenshots...")
        ScreenshotUtils.compare_screenshots("com.ss.android.ugc.trill")
        # Auto set base screenshots
        ScreenshotUtils.auto_set_base_if_successful("com.ss.android.ugc.trill")
    
    def test_app_launch_and_navigation(self, driver, test_data):
        """Test app launch and basic navigation"""
        Log.info("Testing app launch and navigation")
        
        # Create page objects
        main_page = MainPage(driver, test_data)
        
        try:
            # Use common initialization method
            self._initialize_app_and_take_initial_screenshot(driver, test_data, "navigation")
            
            # Test navigation to different tabs
            assert main_page.click_friends_tab(), "Should navigate to friends tab successfully"
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "navigation_friends_tab", "02")
            
            assert main_page.click_create_tab_and_close(), "Should navigate to create tab successfully"
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "navigation_create_tab", "03")
            
            assert main_page.click_inbox_tab(), "Should navigate to inbox tab successfully"
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "navigation_inbox_tab", "04")
            
            assert main_page.click_profile_tab(), "Should navigate to profile tab successfully"
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "navigation_profile_tab", "05")
            
            # Return to home tab
            assert main_page.click_home_tab(), "Should return to home tab successfully"
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "navigation_home_return", "06")
            
            Log.info("App launch and navigation test completed successfully")
            
        except Exception as e:
            Log.error(f"App launch and navigation test failed: {str(e)}")
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "navigation_failed", "06")
            raise
        
        finally:
            # Close app
            try:
                driver.terminate_app(test_data.APP_PACKAGE)
                Log.info("App terminated")
            except Exception as e:
                Log.warning(f"Failed to terminate app: {str(e)}")
    
    def test_video_interaction_features(self, driver, test_data):
        """Test video interaction features (like, comment, share, bookmark)"""
        Log.info("Testing video interaction features")
        
        # Create page objects
        main_page = MainPage(driver, test_data)
        video_page = VideoPage(driver, test_data)
        
        try:
            # Use common initialization method
            self._initialize_app_and_take_initial_screenshot(driver, test_data, "video_interaction")
            
            # Wait for video to load
            assert video_page.wait_for_video_load(), "Should load video successfully"
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "video_interaction_loaded", "02")
            
            # Test like button using VideoPage
            assert video_page.click_like_button(), "Should click like button successfully"
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "video_interaction_liked", "03")
            
            # Test comment button using VideoPage
            assert video_page.click_comment_button(), "Should click comment button successfully"
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "video_interaction_comment", "04")
            
            # Go back from comment section
            assert video_page.click_close_button(), "Should close comment section successfully"
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "video_interaction_comment_closed", "05")
            
            # Test share button using VideoPage
            assert video_page.click_share_button(), "Should click share button successfully"
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "video_interaction_share", "06")
            
            # Close share dialog
            assert video_page.click_close_button(), "Should close share dialog successfully"
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "video_interaction_share_closed", "07")
            
            # Test bookmark button using VideoPage
            assert video_page.click_bookmark_button(), "Should click bookmark button successfully"
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "video_interaction_bookmarked", "08")
            
            Log.info("Video interaction features test completed successfully")
            
        except Exception as e:
            Log.error(f"Video interaction features test failed: {str(e)}")
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "video_interaction_failed", "08")
            raise
        
        finally:
            # Close app
            try:
                driver.terminate_app(test_data.APP_PACKAGE)
                Log.info("App terminated")
            except Exception as e:
                Log.warning(f"Failed to terminate app: {str(e)}")
    
    def test_video_navigation(self, driver, test_data):
        """Test video navigation (swipe up/down)"""
        Log.info("Testing video navigation")
        
        # Create page objects
        main_page = MainPage(driver, test_data)
        video_page = VideoPage(driver, test_data)
        
        try:
            # Use common initialization method
            self._initialize_app_and_take_initial_screenshot(driver, test_data, "video_navigation")
            
            # Wait for video to load
            assert video_page.wait_for_video_load(), "Should load video successfully"
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "video_navigation_initial", "02")
            
            # Swipe to next video using VideoPage
            assert video_page.swipe_to_next_video(), "Should swipe to next video successfully"
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "video_navigation_next", "03")
            
            # Swipe to previous video using VideoPage
            assert video_page.swipe_to_previous_video(), "Should swipe to previous video successfully"
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "video_navigation_previous", "04")
            
            # Swipe to next video again using VideoPage
            assert video_page.swipe_to_next_video(), "Should swipe to next video again successfully"
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "video_navigation_next_again", "05")
            
            Log.info("Video navigation test completed successfully")
            
        except Exception as e:
            Log.error(f"Video navigation test failed: {str(e)}")
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "video_navigation_failed", "05")
            raise
        
        finally:
            # Close app
            try:
                driver.terminate_app(test_data.APP_PACKAGE)
                Log.info("App terminated")
            except Exception as e:
                Log.warning(f"Failed to terminate app: {str(e)}")
    
    def test_advanced_video_features(self, driver, test_data):
        """Test advanced video features (double tap, long press)"""
        Log.info("Testing advanced video features")
        
        # Create page objects
        main_page = MainPage(driver, test_data)
        video_page = VideoPage(driver, test_data)
        
        try:
            # Use common initialization method
            self._initialize_app_and_take_initial_screenshot(driver, test_data, "advanced_video")
            
            # Wait for video to load
            assert video_page.wait_for_video_load(), "Should load video successfully"
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "advanced_video_loaded", "02")
            
            # Test double tap to like
            assert video_page.double_tap_to_like(), "Should double tap video to like successfully"
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "advanced_video_double_tap", "03")
            
            # Test long press on video
            assert video_page.long_press_video(duration=2000), "Should long press video successfully"
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "advanced_video_long_press", "04")
            
            # Check video playing status
            assert video_page.is_video_playing(), "Video should be playing"
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "advanced_video_status", "05")
            
            Log.info("Advanced video features test completed successfully")
            
        except Exception as e:
            Log.error(f"Advanced video features test failed: {str(e)}")
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "advanced_video_failed", "05")
            raise
        
        finally:
            # Close app
            try:
                driver.terminate_app(test_data.APP_PACKAGE)
                Log.info("App terminated")
            except Exception as e:
                Log.warning(f"Failed to terminate app: {str(e)}")
    
    def test_search_functionality(self, driver, test_data):
        """Test search functionality"""
        Log.info("Testing search functionality")
        
        # Create page objects
        main_page = MainPage(driver, test_data)
        search_page = SearchPage(driver, test_data)
        
        try:
            # Use common initialization method
            self._initialize_app_and_take_initial_screenshot(driver, test_data, "search")
            
            # Perform search
            assert search_page.search_for_keyword(test_data.TestData.SEARCH_KEYWORD), "Should search successfully"
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "search_results", "02")
            
            # Check if search results are loaded
            assert search_page.is_search_results_loaded(), "Should load search results successfully"
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "search_results_loaded", "03")
            
            # Click first search result
            assert search_page.click_first_search_result(), "Should click first search result successfully"
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "search_result_selected", "04")
            
            # Go back to search results
            assert search_page.click_back_button(), "Should go back to search results successfully"
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "search_back_to_results", "05")
            
            # Go back to main page
            assert search_page.click_back_button(), "Should go back to main page successfully"
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "search_back_to_main", "06")
            
            Log.info("Search functionality test completed successfully")
            
        except Exception as e:
            Log.error(f"Search functionality test failed: {str(e)}")
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "search_failed", "06")
            raise
        
        finally:
            # Close app
            try:
                driver.terminate_app(test_data.APP_PACKAGE)
                Log.info("App terminated")
            except Exception as e:
                Log.warning(f"Failed to terminate app: {str(e)}")
    
    def test_profile_page_features(self, driver, test_data):
        """Test profile page features"""
        Log.info("Testing profile page features")
        
        # Create page objects
        main_page = MainPage(driver, test_data)
        profile_page = ProfilePage(driver, test_data)
        
        try:
            # Use common initialization method
            self._initialize_app_and_take_initial_screenshot(driver, test_data, "profile")
            
            # Navigate to profile tab using MainPage
            assert main_page.click_profile_tab(), "Should navigate to profile tab successfully"
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "profile_tab_opened", "02")
            
            # Check if profile page is loaded
            assert profile_page.is_profile_page_loaded(), "Should load profile page successfully"
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "profile_page_loaded", "03")
            
            # Get username
            username = profile_page.get_username()
            if username:
                Log.info(f"Profile username: {username}")
                ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "profile_username_displayed", "04")
            
            # Click profile avatar
            assert profile_page.click_profile_avatar(), "Should click profile avatar successfully"
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "profile_avatar_clicked", "05")
            
            # Go back to profile page
            assert profile_page.click_back_button(), "Should go back to profile page successfully"
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "profile_back_to_page", "06")
            
            # Return to home tab using MainPage
            assert main_page.click_home_tab(), "Should return to home tab successfully"
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "profile_back_to_home", "07")
            
            Log.info("Profile page features test completed successfully")
            
        except Exception as e:
            Log.error(f"Profile page features test failed: {str(e)}")
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "profile_failed", "07")
            raise
        
        finally:
            # Close app
            try:
                driver.terminate_app(test_data.APP_PACKAGE)
                Log.info("App terminated")
            except Exception as e:
                Log.warning(f"Failed to terminate app: {str(e)}")
    
    def test_app_permissions(self, driver, test_data):
        """Test app permission handling"""
        Log.info("Testing app permission handling")
        
        # Create page objects
        main_page = MainPage(driver, test_data)
        
        try:
            # Use common initialization method
            self._initialize_app_and_take_initial_screenshot(driver, test_data, "permissions")
            
            # Test permission dialog handling (allow)
            assert main_page.handle_permission_dialog(allow=True), "Should handle permission dialog successfully"
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "permissions_allowed", "02")
            
            # Navigate to create tab (might trigger more permissions)
            assert main_page.click_create_tab_and_close(), "Should navigate to create tab successfully"
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "permissions_create_tab", "03")
            
            # Handle any additional permissions
            assert main_page.handle_permission_dialog(allow=True), "Should handle additional permissions successfully"
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "permissions_additional", "04")
            
            # Return to home tab
            assert main_page.click_home_tab(), "Should return to home tab successfully"
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "permissions_back_to_home", "05")
            
            Log.info("App permissions test completed successfully")
            
        except Exception as e:
            Log.error(f"App permissions test failed: {str(e)}")
            ScreenshotUtils.save_screenshot(driver, test_data.APP_PACKAGE, "permissions_failed", "05")
            raise
        
        finally:
            # Close app
            try:
                driver.terminate_app(test_data.APP_PACKAGE)
                Log.info("App terminated")
            except Exception as e:
                Log.warning(f"Failed to terminate app: {str(e)}")

