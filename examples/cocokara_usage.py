#!/usr/bin/env python3
"""
Cocokara App Usage Example
Cocokara应用使用示例
"""

from core.driver.appium_driver import AppiumDriver
from core.config.appium_config import AppiumConfig
from core.utils.logger import Log
from tests.jp.co.matsukiyococokara.app.pages.main_page import MainPage
from tests.jp.co.matsukiyococokara.app.pages.challenge_page import ChallengePage
from tests.jp.co.matsukiyococokara.app.pages.result_page import ResultPage
from tests.jp.co.matsukiyococokara.app.datas.test_data import CocokaraTestData


def main():
    """Cocokara应用使用示例"""
    Log.info("Starting Cocokara app usage example")
    
    # 创建Appium配置
    config = AppiumConfig(
        server_url="http://127.0.0.1:4723",
        platform_name="Android",
        platform_version="14",
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
        
        # 创建页面对象
        main_page = MainPage(driver)
        challenge_page = ChallengePage(driver)
        result_page = ResultPage(driver)
        
        # 启动应用
        driver.activate_app(CocokaraTestData.APP_PACKAGE)
        Log.info("App activated")
        
        # 等待主页面加载
        main_page.wait_for_page_load()
        Log.info("Main page loaded")
        
        # 处理弹窗
        main_page.wait_for_popup()
        main_page.close_popup()
        Log.info("Popup handled")
        
        # 点击挑战区域
        main_page.tap_challenge_area()
        Log.info("Challenge area tapped")
        
        # 开始挑战
        challenge_page.start_challenge()
        Log.info("Challenge started")
        
        # 检查结果
        result_page.wait_for_page_load()
        result_type = result_page.check_result()
        Log.info(f"Challenge result: {result_type}")
        
        # 处理结果
        result_page.handle_result()
        Log.info("Result handled")
        
        # 截图
        driver.take_screenshot("cocokara_example")
        Log.info("Screenshot taken")
        
        # 关闭弹窗
        main_page.close_imageview_popup()
        Log.info("Popup closed")
        
        Log.info("Cocokara app usage example completed successfully")
        
    except Exception as e:
        Log.error(f"Cocokara app usage example failed: {str(e)}")
        
    finally:
        # 关闭应用
        try:
            driver.terminate_app(CocokaraTestData.APP_PACKAGE)
            Log.info("App terminated")
        except Exception as e:
            Log.warning(f"Failed to terminate app: {str(e)}")
        
        # 关闭驱动
        driver.quit_driver()
        Log.info("Driver closed")


if __name__ == "__main__":
    main()
