"""
Pytest configuration for RoadSync Duo tests
RoadSync Duo测试的pytest配置
"""

import pytest
from core.driver.appium_driver import AppiumDriver
from core.config.appium_config import AppiumConfig
from core.config.device_config import DeviceConfig
from core.config.app_config import AppConfig
from core.utils.logger import Log


@pytest.fixture(scope="session")
def appium_config():
    """Appium配置夹具"""
    config = AppiumConfig(
        server_url="http://localhost:4723",
        platform_name="Android",
        automation_name="UiAutomator2",
        app_package="com.honda.roadsync.duo",
        app_activity=".MainActivity",
        timeout=30,
        no_reset=True
    )
    
    Log.info("Created Appium config for RoadSync Duo")
    return config


@pytest.fixture(scope="session")
def device_config():
    """设备配置夹具"""
    config = DeviceConfig(
        device_name="Android Device",
        platform="Android",
        platform_version="11.0",
        manufacturer="Honda",
        model="Test Device"
    )
    
    Log.info("Created device config for RoadSync Duo")
    return config


@pytest.fixture(scope="session")
def app_config():
    """应用配置夹具"""
    config = AppConfig(
        app_name="RoadSync Duo",
        app_version="1.0.0",
        app_package="com.honda.roadsync.duo",
        app_activity=".MainActivity",
        app_type="native",
        launch_timeout=30,
        startup_timeout=60
    )
    
    Log.info("Created app config for RoadSync Duo")
    return config


@pytest.fixture(scope="function")
def driver(appium_config):
    """Appium驱动夹具"""
    driver = AppiumDriver(appium_config)
    
    try:
        Log.info("Starting Appium driver for test")
        driver.start_driver()
        yield driver
    finally:
        Log.info("Quitting Appium driver after test")
        driver.quit_driver()


@pytest.fixture(scope="function")
def test_data():
    """测试数据夹具"""
    return {
        "valid_username": "testuser@honda.com",
        "valid_password": "TestPassword123",
        "invalid_username": "invalid@test.com",
        "invalid_password": "WrongPassword",
        "test_vehicle_id": "TEST001",
        "test_trip_id": "TRIP001"
    }
