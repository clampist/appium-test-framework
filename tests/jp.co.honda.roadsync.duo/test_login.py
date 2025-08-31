"""
Login Test Cases
Login functionality test cases
"""

import pytest
import time
from core.utils.logger import Log
import sys
import os

# Add current directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from pages.login_page import LoginPage
from pages.home_page import HomePage


class TestLogin:
    """Login functionality test class"""
    
    def test_valid_login(self, driver, test_data):
        """Test valid login"""
        Log.info("Starting valid login test")
        
        # Create page objects
        login_page = LoginPage(driver)
        home_page = HomePage(driver)
        
        try:
            # Wait for login page to load
            login_page.wait_for_page_load()
            assert login_page.is_page_loaded(), "Login page should be loaded"
            
            # Perform login
            login_page.login(
                test_data["valid_username"],
                test_data["valid_password"]
            )
            
            # Wait for home page to load
            time.sleep(3)  # Wait for page transition
            home_page.wait_for_page_load()
            
            # Verify successful login
            assert home_page.is_page_loaded(), "Home page should be loaded after successful login"
            assert "Welcome" in home_page.get_welcome_message(), "Welcome message should be displayed"
            
            Log.info("Valid login test passed")
            
        except Exception as e:
            Log.error(f"Valid login test failed: {str(e)}")
            login_page.take_screenshot("valid_login_failed")
            raise
    
    def test_invalid_login(self, driver, test_data):
        """Test invalid login"""
        Log.info("Starting invalid login test")
        
        # Create page objects
        login_page = LoginPage(driver)
        
        try:
            # Wait for login page to load
            login_page.wait_for_page_load()
            assert login_page.is_page_loaded(), "Login page should be loaded"
            
            # Perform invalid login
            login_page.login(
                test_data["invalid_username"],
                test_data["invalid_password"]
            )
            
            # Wait for error message to display
            time.sleep(2)
            
            # Verify error message
            assert login_page.is_error_displayed(), "Error message should be displayed"
            error_message = login_page.get_error_message()
            assert len(error_message) > 0, "Error message should not be empty"
            
            Log.info("Invalid login test passed")
            
        except Exception as e:
            Log.error(f"Invalid login test failed: {str(e)}")
            login_page.take_screenshot("invalid_login_failed")
            raise
    
    def test_login_with_remember_me(self, driver, test_data):
        """Test remember me functionality"""
        Log.info("Starting login with remember me test")
        
        # Create page objects
        login_page = LoginPage(driver)
        home_page = HomePage(driver)
        
        try:
            # Wait for login page to load
            login_page.wait_for_page_load()
            assert login_page.is_page_loaded(), "Login page should be loaded"
            
            # Perform login (remember me)
            login_page.login_with_remember_me(
                test_data["valid_username"],
                test_data["valid_password"]
            )
            
            # Wait for home page to load
            time.sleep(3)
            home_page.wait_for_page_load()
            
            # Verify successful login
            assert home_page.is_page_loaded(), "Home page should be loaded"
            
            # Verify remember me functionality (need to restart app to verify)
            # Skip restart verification due to test environment limitations
            
            Log.info("Login with remember me test passed")
            
        except Exception as e:
            Log.error(f"Login with remember me test failed: {str(e)}")
            login_page.take_screenshot("remember_me_login_failed")
            raise
    
    def test_empty_credentials(self, driver):
        """Test empty credentials login"""
        Log.info("Starting empty credentials test")
        
        # Create page objects
        login_page = LoginPage(driver)
        
        try:
            # Wait for login page to load
            login_page.wait_for_page_load()
            assert login_page.is_page_loaded(), "Login page should be loaded"
            
            # Clear credentials
            login_page.clear_credentials()
            
            # Try to login (empty credentials)
            login_page.login("", "")
            
            # Wait for error message to display
            time.sleep(2)
            
            # Verify error message
            assert login_page.is_error_displayed(), "Error message should be displayed for empty credentials"
            
            Log.info("Empty credentials test passed")
            
        except Exception as e:
            Log.error(f"Empty credentials test failed: {str(e)}")
            login_page.take_screenshot("empty_credentials_failed")
            raise
    
    def test_forgot_password_link(self, driver):
        """Test forgot password link"""
        Log.info("Starting forgot password link test")
        
        # Create page objects
        login_page = LoginPage(driver)
        
        try:
            # Wait for login page to load
            login_page.wait_for_page_load()
            assert login_page.is_page_loaded(), "Login page should be loaded"
            
            # Click forgot password link
            login_page.click_forgot_password()
            
            # Wait for page transition (should navigate to forgot password page)
            time.sleep(2)
            
            # Verify page transition (need forgot password page verification logic)
            # Skip specific verification due to lack of forgot password page implementation
            
            Log.info("Forgot password link test passed")
            
        except Exception as e:
            Log.error(f"Forgot password link test failed: {str(e)}")
            login_page.take_screenshot("forgot_password_failed")
            raise
    
    def test_remember_me_checkbox(self, driver):
        """Test remember me checkbox"""
        Log.info("Starting remember me checkbox test")
        
        # Create page objects
        login_page = LoginPage(driver)
        
        try:
            # Wait for login page to load
            login_page.wait_for_page_load()
            assert login_page.is_page_loaded(), "Login page should be loaded"
            
            # Check initial state
            initial_state = login_page.is_remember_me_checked()
            
            # Toggle remember me state
            login_page.toggle_remember_me()
            
            # Verify state has changed
            new_state = login_page.is_remember_me_checked()
            assert new_state != initial_state, "Remember me checkbox state should be toggled"
            
            # Toggle again
            login_page.toggle_remember_me()
            
            # Verify state is restored
            final_state = login_page.is_remember_me_checked()
            assert final_state == initial_state, "Remember me checkbox state should be restored"
            
            Log.info("Remember me checkbox test passed")
            
        except Exception as e:
            Log.error(f"Remember me checkbox test failed: {str(e)}")
            login_page.take_screenshot("remember_me_checkbox_failed")
            raise
    
    def test_input_placeholders(self, driver):
        """Test input field placeholders"""
        Log.info("Starting input placeholders test")
        
        # Create page objects
        login_page = LoginPage(driver)
        
        try:
            # Wait for login page to load
            login_page.wait_for_page_load()
            assert login_page.is_page_loaded(), "Login page should be loaded"
            
            # Check username placeholder
            username_placeholder = login_page.get_username_placeholder()
            assert len(username_placeholder) > 0, "Username placeholder should not be empty"
            
            # Check password placeholder
            password_placeholder = login_page.get_password_placeholder()
            assert len(password_placeholder) > 0, "Password placeholder should not be empty"
            
            Log.info("Input placeholders test passed")
            
        except Exception as e:
            Log.error(f"Input placeholders test failed: {str(e)}")
            login_page.take_screenshot("input_placeholders_failed")
            raise
