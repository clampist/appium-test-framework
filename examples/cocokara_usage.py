#!/usr/bin/env python3
"""
Cocokara App Usage Example
Cocokara app usage example
"""

from core.driver.appium_driver import AppiumDriver
from core.config.appium_config import AppiumConfig
from core.utils.logger import Log
from tests.jp.co.matsukiyococokara.app.pages.main_page import MainPage
from tests.jp.co.matsukiyococokara.app.pages.challenge_page import ChallengePage
from tests.jp.co.matsukiyococokara.app.pages.result_page import ResultPage
from tests.jp.co.matsukiyococokara.app.datas.test_data import CocokaraTestData


def main():
    """Cocokara app usage example"""
    Log.info("Starting Cocokara app usage example")
    
    # Create Appium configuration
    config = AppiumConfig(
        server_url="http://127.0.0.1:4723",
        platform_name="Android",
        platform_version="13",
        device_name="emulator-5554",
        automation_name="UiAutomator2",
        app_package=CocokaraTestData.APP_PACKAGE,
        app_activity=CocokaraTestData.APP_ACTIVITY,
        timeout=CocokaraTestData.WAIT_TIME,
        no_reset=True,
        additional_capabilities={
            "ensureWebviewsHavePages": True,
            "nativeWebScreenshot": True,
            "newCommandTimeout": 3600,
            "connectHardwareKeyboard": True
        }
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
        
        # Create page objects
        main_page = MainPage(driver)
        challenge_page = ChallengePage(driver)
        result_page = ResultPage(driver)
        
        # Activate app
        driver.activate_app(CocokaraTestData.APP_PACKAGE)
        Log.info("App activated")
        
        # Wait for main page to load
        main_page.wait_for_page_load()
        Log.info("Main page loaded")
        
        # Handle popup
        main_page.wait_for_popup()
        main_page.close_popup()
        Log.info("Popup handled")
        
        # Tap challenge area
        main_page.tap_challenge_area()
        Log.info("Challenge area tapped")
        
        # Start challenge
        challenge_page.start_challenge()
        Log.info("Challenge started")
        
        # Check result
        result_page.wait_for_page_load()
        result_type = result_page.check_result()
        Log.info(f"Challenge result: {result_type}")
        
        # Handle result
        result_page.handle_result()
        Log.info("Result handled")
        
        # Take screenshot
        driver.take_screenshot("cocokara_example")
        Log.info("Screenshot taken")
        
        # Close popup
        main_page.close_imageview_popup()
        Log.info("Popup closed")
        
        Log.info("Cocokara app usage example completed successfully")
        
    except Exception as e:
        Log.error(f"Cocokara app usage example failed: {str(e)}")
        
    finally:
        # Terminate app
        try:
            driver.terminate_app(CocokaraTestData.APP_PACKAGE)
            Log.info("App terminated")
        except Exception as e:
            Log.warning(f"Failed to terminate app: {str(e)}")
        
        # Close driver
        driver.quit_driver()
        Log.info("Driver closed")


if __name__ == "__main__":
    main()
