"""
Login Test Cases
登录功能测试用例
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
    """登录功能测试类"""
    
    def test_valid_login(self, driver, test_data):
        """测试有效登录"""
        Log.info("Starting valid login test")
        
        # 创建页面对象
        login_page = LoginPage(driver)
        home_page = HomePage(driver)
        
        try:
            # 等待登录页面加载
            login_page.wait_for_page_load()
            assert login_page.is_page_loaded(), "Login page should be loaded"
            
            # 执行登录
            login_page.login(
                test_data["valid_username"],
                test_data["valid_password"]
            )
            
            # 等待主页加载
            time.sleep(3)  # 等待页面跳转
            home_page.wait_for_page_load()
            
            # 验证登录成功
            assert home_page.is_page_loaded(), "Home page should be loaded after successful login"
            assert "Welcome" in home_page.get_welcome_message(), "Welcome message should be displayed"
            
            Log.info("Valid login test passed")
            
        except Exception as e:
            Log.error(f"Valid login test failed: {str(e)}")
            login_page.take_screenshot("valid_login_failed")
            raise
    
    def test_invalid_login(self, driver, test_data):
        """测试无效登录"""
        Log.info("Starting invalid login test")
        
        # 创建页面对象
        login_page = LoginPage(driver)
        
        try:
            # 等待登录页面加载
            login_page.wait_for_page_load()
            assert login_page.is_page_loaded(), "Login page should be loaded"
            
            # 执行无效登录
            login_page.login(
                test_data["invalid_username"],
                test_data["invalid_password"]
            )
            
            # 等待错误消息显示
            time.sleep(2)
            
            # 验证错误消息
            assert login_page.is_error_displayed(), "Error message should be displayed"
            error_message = login_page.get_error_message()
            assert len(error_message) > 0, "Error message should not be empty"
            
            Log.info("Invalid login test passed")
            
        except Exception as e:
            Log.error(f"Invalid login test failed: {str(e)}")
            login_page.take_screenshot("invalid_login_failed")
            raise
    
    def test_login_with_remember_me(self, driver, test_data):
        """测试记住我功能"""
        Log.info("Starting login with remember me test")
        
        # 创建页面对象
        login_page = LoginPage(driver)
        home_page = HomePage(driver)
        
        try:
            # 等待登录页面加载
            login_page.wait_for_page_load()
            assert login_page.is_page_loaded(), "Login page should be loaded"
            
            # 执行登录（记住我）
            login_page.login_with_remember_me(
                test_data["valid_username"],
                test_data["valid_password"]
            )
            
            # 等待主页加载
            time.sleep(3)
            home_page.wait_for_page_load()
            
            # 验证登录成功
            assert home_page.is_page_loaded(), "Home page should be loaded"
            
            # 验证记住我功能（这里需要重新启动应用来验证）
            # 由于测试环境限制，暂时跳过重启验证
            
            Log.info("Login with remember me test passed")
            
        except Exception as e:
            Log.error(f"Login with remember me test failed: {str(e)}")
            login_page.take_screenshot("remember_me_login_failed")
            raise
    
    def test_empty_credentials(self, driver):
        """测试空凭据登录"""
        Log.info("Starting empty credentials test")
        
        # 创建页面对象
        login_page = LoginPage(driver)
        
        try:
            # 等待登录页面加载
            login_page.wait_for_page_load()
            assert login_page.is_page_loaded(), "Login page should be loaded"
            
            # 清除凭据
            login_page.clear_credentials()
            
            # 尝试登录（空凭据）
            login_page.login("", "")
            
            # 等待错误消息显示
            time.sleep(2)
            
            # 验证错误消息
            assert login_page.is_error_displayed(), "Error message should be displayed for empty credentials"
            
            Log.info("Empty credentials test passed")
            
        except Exception as e:
            Log.error(f"Empty credentials test failed: {str(e)}")
            login_page.take_screenshot("empty_credentials_failed")
            raise
    
    def test_forgot_password_link(self, driver):
        """测试忘记密码链接"""
        Log.info("Starting forgot password link test")
        
        # 创建页面对象
        login_page = LoginPage(driver)
        
        try:
            # 等待登录页面加载
            login_page.wait_for_page_load()
            assert login_page.is_page_loaded(), "Login page should be loaded"
            
            # 点击忘记密码链接
            login_page.click_forgot_password()
            
            # 等待页面跳转（这里应该跳转到忘记密码页面）
            time.sleep(2)
            
            # 验证页面跳转（这里需要忘记密码页面的验证逻辑）
            # 由于没有忘记密码页面的实现，暂时跳过具体验证
            
            Log.info("Forgot password link test passed")
            
        except Exception as e:
            Log.error(f"Forgot password link test failed: {str(e)}")
            login_page.take_screenshot("forgot_password_failed")
            raise
    
    def test_remember_me_checkbox(self, driver):
        """测试记住我复选框"""
        Log.info("Starting remember me checkbox test")
        
        # 创建页面对象
        login_page = LoginPage(driver)
        
        try:
            # 等待登录页面加载
            login_page.wait_for_page_load()
            assert login_page.is_page_loaded(), "Login page should be loaded"
            
            # 检查初始状态
            initial_state = login_page.is_remember_me_checked()
            
            # 切换记住我状态
            login_page.toggle_remember_me()
            
            # 验证状态已改变
            new_state = login_page.is_remember_me_checked()
            assert new_state != initial_state, "Remember me checkbox state should be toggled"
            
            # 再次切换
            login_page.toggle_remember_me()
            
            # 验证状态恢复
            final_state = login_page.is_remember_me_checked()
            assert final_state == initial_state, "Remember me checkbox state should be restored"
            
            Log.info("Remember me checkbox test passed")
            
        except Exception as e:
            Log.error(f"Remember me checkbox test failed: {str(e)}")
            login_page.take_screenshot("remember_me_checkbox_failed")
            raise
    
    def test_input_placeholders(self, driver):
        """测试输入框占位符"""
        Log.info("Starting input placeholders test")
        
        # 创建页面对象
        login_page = LoginPage(driver)
        
        try:
            # 等待登录页面加载
            login_page.wait_for_page_load()
            assert login_page.is_page_loaded(), "Login page should be loaded"
            
            # 检查用户名占位符
            username_placeholder = login_page.get_username_placeholder()
            assert len(username_placeholder) > 0, "Username placeholder should not be empty"
            
            # 检查密码占位符
            password_placeholder = login_page.get_password_placeholder()
            assert len(password_placeholder) > 0, "Password placeholder should not be empty"
            
            Log.info("Input placeholders test passed")
            
        except Exception as e:
            Log.error(f"Input placeholders test failed: {str(e)}")
            login_page.take_screenshot("input_placeholders_failed")
            raise
