#!/usr/bin/env python3
"""
Basic Usage Example
基本使用示例
"""

from core.driver.appium_driver import AppiumDriver
from core.config.appium_config import AppiumConfig
from core.utils.logger import Log


def main():
    """基本使用示例"""
    Log.info("Starting basic usage example")
    
    # 创建Appium配置
    config = AppiumConfig(
        server_url="http://localhost:4723",
        platform_name="Android",
        automation_name="UiAutomator2",
        app_package="com.honda.roadsync.duo",
        app_activity=".MainActivity",
        timeout=30
    )
    
    # 验证配置
    if not config.validate():
        Log.error("Invalid Appium configuration")
        return
    
    # 创建驱动
    driver = AppiumDriver(config)
    
    try:
        # 启动驱动
        driver.start_driver()
        Log.info("Driver started successfully")
        
        # 获取当前Activity
        current_activity = driver.get_current_activity()
        Log.info(f"Current activity: {current_activity}")
        
        # 获取当前包名
        current_package = driver.get_current_package()
        Log.info(f"Current package: {current_package}")
        
        # 截图
        screenshot_path = driver.take_screenshot("example_screenshot")
        Log.info(f"Screenshot saved: {screenshot_path}")
        
        # 获取页面源码
        page_source = driver.get_page_source()
        Log.info(f"Page source length: {len(page_source)}")
        
        Log.info("Basic usage example completed successfully")
        
    except Exception as e:
        Log.error(f"Basic usage example failed: {str(e)}")
        
    finally:
        # 关闭驱动
        driver.quit_driver()
        Log.info("Driver closed")


if __name__ == "__main__":
    main()
