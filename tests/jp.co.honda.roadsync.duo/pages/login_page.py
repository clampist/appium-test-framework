"""
Login Page Object
Login page object
"""

from appium.webdriver.common.appiumby import AppiumBy
from core.elements.page_object import PageObject
from core.utils.logger import Log


class LoginPage(PageObject):
    """Login page object"""
    
    def _init_elements(self):
        """Initialize page elements"""
        # Username input field
        self.add_element(
            "username_input",
            AppiumBy.ID,
            "com.honda.roadsync.duo:id/username_input",
            "Username Input"
        )
        
        # Password input field
        self.add_element(
            "password_input",
            AppiumBy.ID,
            "com.honda.roadsync.duo:id/password_input",
            "Password Input"
        )
        
        # Login button
        self.add_element(
            "login_button",
            AppiumBy.ID,
            "com.honda.roadsync.duo:id/login_button",
            "Login Button"
        )
        
        # Forgot password link
        self.add_element(
            "forgot_password_link",
            AppiumBy.ID,
            "com.honda.roadsync.duo:id/forgot_password_link",
            "Forgot Password Link"
        )
        
        # Error message
        self.add_element(
            "error_message",
            AppiumBy.ID,
            "com.honda.roadsync.duo:id/error_message",
            "Error Message"
        )
        
        # Remember me checkbox
        self.add_element(
            "remember_me_checkbox",
            AppiumBy.ID,
            "com.honda.roadsync.duo:id/remember_me_checkbox",
            "Remember Me Checkbox"
        )
    
    def wait_for_page_load(self, timeout=None):
        """Wait for page to load completely"""
        Log.info("Waiting for login page to load...")
        self.wait_for_element("username_input", timeout)
        self.wait_for_element("password_input", timeout)
        self.wait_for_element("login_button", timeout)
    
    def is_page_loaded(self) -> bool:
        """Check if page is loaded completely"""
        try:
            return (self.is_element_displayed("username_input") and
                    self.is_element_displayed("password_input") and
                    self.is_element_displayed("login_button"))
        except Exception:
            return False
    
    def login(self, username: str, password: str):
        """
        Perform login operation
        
        Args:
            username: Username
            password: Password
        """
        Log.info(f"Attempting to login with username: {username}")
        
        # Enter username
        self.input_text("username_input", username)
        
        # Enter password
        self.input_text("password_input", password)
        
        # Click login button
        self.click_element("login_button")
        
        Log.info("Login attempt completed")
    
    def login_with_remember_me(self, username: str, password: str):
        """
        Perform login operation (remember me)
        
        Args:
            username: Username
            password: Password
        """
        Log.info(f"Attempting to login with remember me: {username}")
        
        # Enter username
        self.input_text("username_input", username)
        
        # Enter password
        self.input_text("password_input", password)
        
        # Check remember me
        self.click_element("remember_me_checkbox")
        
        # Click login button
        self.click_element("login_button")
        
        Log.info("Login with remember me attempt completed")
    
    def get_error_message(self) -> str:
        """
        Get error message
        
        Returns:
            str: Error message
        """
        try:
            return self.get_element_text("error_message")
        except Exception:
            return ""
    
    def is_error_displayed(self) -> bool:
        """
        Check if error message is displayed
        
        Returns:
            bool: Whether error is displayed
        """
        try:
            return self.is_element_displayed("error_message")
        except Exception:
            return False
    
    def click_forgot_password(self):
        """Click forgot password link"""
        Log.info("Clicking forgot password link")
        self.click_element("forgot_password_link")
    
    def clear_credentials(self):
        """Clear entered username and password"""
        Log.info("Clearing login credentials")
        
        # Clear username
        username_element = self.get_element("username_input")
        username_element.find().clear()
        
        # Clear password
        password_element = self.get_element("password_input")
        password_element.find().clear()
    
    def is_remember_me_checked(self) -> bool:
        """
        Check if remember me is checked
        
        Returns:
            bool: Whether checked
        """
        try:
            element = self.get_element("remember_me_checkbox")
            return element.get_attribute("checked") == "true"
        except Exception:
            return False
    
    def toggle_remember_me(self):
        """Toggle remember me state"""
        Log.info("Toggling remember me checkbox")
        self.click_element("remember_me_checkbox")
    
    def get_username_placeholder(self) -> str:
        """
        Get username input field placeholder text
        
        Returns:
            str: Placeholder text
        """
        try:
            element = self.get_element("username_input")
            return element.get_attribute("content-desc") or element.get_attribute("hint")
        except Exception:
            return ""
    
    def get_password_placeholder(self) -> str:
        """
        Get password input field placeholder text
        
        Returns:
            str: Placeholder text
        """
        try:
            element = self.get_element("password_input")
            return element.get_attribute("content-desc") or element.get_attribute("hint")
        except Exception:
            return ""
