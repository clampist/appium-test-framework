#!/usr/bin/env python3
"""
Basic Usage Example
Basic usage example
"""

from core.driver.appium_driver import AppiumDriver
from core.config.appium_config import AppiumConfig
from core.utils.logger import Log


def main():
    """Basic usage example"""
    Log.info("Starting basic usage example")
    
    # Create Appium configuration
    config = AppiumConfig(
        server_url="http://localhost:4723",
        platform_name="Android",
        automation_name="UiAutomator2",
        app_package="com.honda.roadsync.duo",
        app_activity=".MainActivity",
        timeout=30
    )
    
    # Validate configuration
    if not config.validate():
        Log.error("Invalid Appium configuration")
        return
    
    # Create driver
    driver = AppiumDriver(config)
    
    try:
        # Start driver
        driver.start_driver()
        Log.info("Driver started successfully")
        
        # Get current activity
        current_activity = driver.get_current_activity()
        Log.info(f"Current activity: {current_activity}")
        
        # Get current package name
        current_package = driver.get_current_package()
        Log.info(f"Current package: {current_package}")
        
        # Take screenshot
        screenshot_path = driver.take_screenshot("example_screenshot")
        Log.info(f"Screenshot saved: {screenshot_path}")
        
        # Get page source
        page_source = driver.get_page_source()
        Log.info(f"Page source length: {len(page_source)}")
        
        Log.info("Basic usage example completed successfully")
        
    except Exception as e:
        Log.error(f"Basic usage example failed: {str(e)}")
        
    finally:
        # Close driver
        driver.quit_driver()
        Log.info("Driver closed")


if __name__ == "__main__":
    main()
