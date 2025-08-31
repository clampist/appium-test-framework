"""
Pytest configuration for Monoxer App tests
Pytest configuration for Monoxer App tests
"""

import sys
import os
import pytest
from appium import webdriver
from appium.options.common.base import AppiumOptions

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from core.utils.logger import Log
from datas.test_data import get_test_data
from configs.config_manager import get_appium_config, get_server_config


def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption(
        "--language", 
        action="store", 
        default="en", 
        choices=["en", "ja"],
        help="Language for testing (en/ja)"
    )


@pytest.fixture(scope="session")
def language(request):
    """Get language from command line option"""
    return request.config.getoption("--language")


@pytest.fixture(scope="session")
def test_data(language):
    """Get test data based on language"""
    return get_test_data(language)


@pytest.fixture(scope="session")
def appium_config(language):
    """Get Appium configuration based on language"""
    return get_appium_config(language)


@pytest.fixture(scope="session")
def driver(appium_config):
    """Create and manage Appium driver"""
    Log.info(f"Creating Appium driver with config: {appium_config}")
    
    options = AppiumOptions()
    options.load_capabilities(appium_config)
    
    # Get server configuration
    server_config = get_server_config()
    server_url = f"http://{server_config['host']}:{server_config['port']}{server_config['path']}"
    
    driver = webdriver.Remote(server_url, options=options)
    
    Log.info("Appium driver created successfully")
    
    yield driver
    
    Log.info("Closing Appium driver")
    driver.quit()


@pytest.fixture(autouse=True)
def allure_attachments(request, driver):
    """Automatically attach screenshots and page source on test failure"""
    yield
    
    # Check if test failed
    if request.node.rep_call.failed:
        from core.utils.allure_utils import attach_screenshot_on_failure, attach_page_source_on_failure
        
        test_name = request.node.name
        Log.info(f"Test '{test_name}' failed, attaching screenshots and page source to Allure report")
        
        try:
            # Attach screenshot
            attach_screenshot_on_failure(driver, test_name)
            
            # Attach page source
            attach_page_source_on_failure(driver, test_name)
            
        except Exception as e:
            Log.error(f"Failed to attach failure artifacts: {str(e)}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test result for failure handling"""
    outcome = yield
    rep = outcome.get_result()
    
    # Set the report attribute on the item
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(scope="session", autouse=True)
def setup_screenshot_management(language):
    """Setup screenshot management for Monoxer App tests"""
    from core.utils.screenshot_utils import ScreenshotUtils
    from core.utils.logger import Log
    
    app_package = "com.monoxer"
    
    # Clear current screenshot directory only at the beginning of session
    Log.info(f"Setting up screenshot management for Monoxer App tests (Language: {language})")
    ScreenshotUtils.clear_screenshot_directory(app_package)
    
    yield
    
    # Cleanup after test session
    Log.info("Cleaning up screenshot management for Monoxer App tests")
