"""
Login Page Object
登录页面对象
"""

from appium.webdriver.common.appiumby import AppiumBy
from core.elements.page_object import PageObject
from core.utils.logger import Log


class LoginPage(PageObject):
    """登录页面对象"""
    
    def _init_elements(self):
        """初始化页面元素"""
        # 用户名输入框
        self.add_element(
            "username_input",
            AppiumBy.ID,
            "com.honda.roadsync.duo:id/username_input",
            "Username Input"
        )
        
        # 密码输入框
        self.add_element(
            "password_input",
            AppiumBy.ID,
            "com.honda.roadsync.duo:id/password_input",
            "Password Input"
        )
        
        # 登录按钮
        self.add_element(
            "login_button",
            AppiumBy.ID,
            "com.honda.roadsync.duo:id/login_button",
            "Login Button"
        )
        
        # 忘记密码链接
        self.add_element(
            "forgot_password_link",
            AppiumBy.ID,
            "com.honda.roadsync.duo:id/forgot_password_link",
            "Forgot Password Link"
        )
        
        # 错误消息
        self.add_element(
            "error_message",
            AppiumBy.ID,
            "com.honda.roadsync.duo:id/error_message",
            "Error Message"
        )
        
        # 记住我复选框
        self.add_element(
            "remember_me_checkbox",
            AppiumBy.ID,
            "com.honda.roadsync.duo:id/remember_me_checkbox",
            "Remember Me Checkbox"
        )
    
    def wait_for_page_load(self, timeout=None):
        """等待页面加载完成"""
        Log.info("Waiting for login page to load...")
        self.wait_for_element("username_input", timeout)
        self.wait_for_element("password_input", timeout)
        self.wait_for_element("login_button", timeout)
    
    def is_page_loaded(self) -> bool:
        """检查页面是否加载完成"""
        try:
            return (self.is_element_displayed("username_input") and
                    self.is_element_displayed("password_input") and
                    self.is_element_displayed("login_button"))
        except Exception:
            return False
    
    def login(self, username: str, password: str):
        """
        执行登录操作
        
        Args:
            username: 用户名
            password: 密码
        """
        Log.info(f"Attempting to login with username: {username}")
        
        # 输入用户名
        self.input_text("username_input", username)
        
        # 输入密码
        self.input_text("password_input", password)
        
        # 点击登录按钮
        self.click_element("login_button")
        
        Log.info("Login attempt completed")
    
    def login_with_remember_me(self, username: str, password: str):
        """
        执行登录操作（记住我）
        
        Args:
            username: 用户名
            password: 密码
        """
        Log.info(f"Attempting to login with remember me: {username}")
        
        # 输入用户名
        self.input_text("username_input", username)
        
        # 输入密码
        self.input_text("password_input", password)
        
        # 勾选记住我
        self.click_element("remember_me_checkbox")
        
        # 点击登录按钮
        self.click_element("login_button")
        
        Log.info("Login with remember me attempt completed")
    
    def get_error_message(self) -> str:
        """
        获取错误消息
        
        Returns:
            str: 错误消息
        """
        try:
            return self.get_element_text("error_message")
        except Exception:
            return ""
    
    def is_error_displayed(self) -> bool:
        """
        检查是否显示错误消息
        
        Returns:
            bool: 是否显示错误
        """
        try:
            return self.is_element_displayed("error_message")
        except Exception:
            return False
    
    def click_forgot_password(self):
        """点击忘记密码链接"""
        Log.info("Clicking forgot password link")
        self.click_element("forgot_password_link")
    
    def clear_credentials(self):
        """清除输入的用户名和密码"""
        Log.info("Clearing login credentials")
        
        # 清除用户名
        username_element = self.get_element("username_input")
        username_element.find().clear()
        
        # 清除密码
        password_element = self.get_element("password_input")
        password_element.find().clear()
    
    def is_remember_me_checked(self) -> bool:
        """
        检查记住我是否被勾选
        
        Returns:
            bool: 是否被勾选
        """
        try:
            element = self.get_element("remember_me_checkbox")
            return element.get_attribute("checked") == "true"
        except Exception:
            return False
    
    def toggle_remember_me(self):
        """切换记住我状态"""
        Log.info("Toggling remember me checkbox")
        self.click_element("remember_me_checkbox")
    
    def get_username_placeholder(self) -> str:
        """
        获取用户名输入框的占位符文本
        
        Returns:
            str: 占位符文本
        """
        try:
            element = self.get_element("username_input")
            return element.get_attribute("content-desc") or element.get_attribute("hint")
        except Exception:
            return ""
    
    def get_password_placeholder(self) -> str:
        """
        获取密码输入框的占位符文本
        
        Returns:
            str: 占位符文本
        """
        try:
            element = self.get_element("password_input")
            return element.get_attribute("content-desc") or element.get_attribute("hint")
        except Exception:
            return ""
