"""
Pytest configuration for Monoxer App tests
Monoxer应用测试的pytest配置
"""

import os
import sys
import pytest

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from core.driver.appium_driver import AppiumDriver
from core.config.appium_config import AppiumConfig
from core.config.device_config import DeviceConfig
from core.config.app_config import AppConfig
from core.utils.logger import Log


@pytest.fixture(scope="session")
def appium_config():
    """Appium configuration fixture for Monoxer App"""
    config = AppiumConfig(
        server_url="http://127.0.0.1:4723",
        platform_name="Android",
        platform_version="13",
        device_name="emulator-5554",
        automation_name="UiAutomator2",
        app_package="com.monoxer",
        app_activity="com.monoxer.view.main.MainActivity",
        timeout=15,
        no_reset=True,
        additional_capabilities={
            "ensureWebviewsHavePages": True,
            "nativeWebScreenshot": True,
            "newCommandTimeout": 3600,
            "connectHardwareKeyboard": True
        }
    )
    
    Log.info("Created Appium config for Monoxer App")
    return config


@pytest.fixture(scope="session")
def device_config():
    """Device configuration fixture for Monoxer App"""
    config = DeviceConfig(
        device_name="emulator-5554",
        platform="Android",
        platform_version="13",
        manufacturer="Google",
        model="Android Emulator"
    )
    
    Log.info("Created device config for Monoxer App")
    return config


@pytest.fixture(scope="session")
def app_config():
    """Application configuration fixture for Monoxer App"""
    config = AppConfig(
        app_name="Monoxer",
        app_version="1.0.0",
        app_package="com.monoxer",
        app_activity="com.monoxer.view.main.MainActivity",
        app_type="native",
        launch_timeout=30,
        startup_timeout=60
    )
    
    Log.info("Created app config for Monoxer App")
    return config


@pytest.fixture(scope="function")
def driver(appium_config):
    """Appium driver fixture for Monoxer App"""
    driver = AppiumDriver(appium_config)
    
    try:
        Log.info("Starting Appium driver for Monoxer App test")
        driver.start_driver()
        yield driver
    finally:
        Log.info("Quitting Appium driver after Monoxer App test")
        driver.quit_driver()


@pytest.fixture(scope="function")
def test_data():
    """Test data fixture for Monoxer App"""
    return {
        "app_package": "com.monoxer",
        "wait_time": 15,
        "popup_timeout": 5,
        "screenshot_dir": "screenshots"
    }


@pytest.fixture(scope="session", autouse=True)
def setup_screenshot_management():
    """Setup screenshot management for Monoxer App tests"""
    from core.utils.screenshot_utils import ScreenshotUtils
    from core.utils.logger import Log
    
    app_package = "com.monoxer"
    
    # Clear current screenshot directory only at the beginning of session
    Log.info("Setting up screenshot management for Monoxer App tests")
    ScreenshotUtils.clear_screenshot_directory(app_package)
    
    yield
    
    # 测试会话结束后的清理工作
    Log.info("Cleaning up screenshot management for Monoxer App tests")
