"""
Failure Demo Test Cases
Test cases designed to fail for demonstrating Allure report features
"""

import pytest
import allure
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from core.utils.allure_utils import AllureUtils
from datas.test_data import get_test_data


@allure.epic("Monoxer App")
@allure.feature("Failure Demo")
@allure.story("Element Not Found")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
This test is designed to fail by trying to find a non-existent element.
It demonstrates how Allure reports capture screenshots and page source on failure.

**Expected Behavior:**
- Test should fail with NoSuchElementException
- Screenshot should be attached to Allure report
- Page source should be attached to Allure report
- Test configuration should be attached to Allure report
""")
class TestFailureDemo:
    """Test cases designed to demonstrate failure handling and Allure reporting"""
    
    def setup_method(self, method):
        """Setup test data"""
        # Get test_data from fixture
        self.test_data = None  # Will be set in individual test methods
    
    @allure.step("Take initial screenshot")
    def take_initial_screenshot(self, driver):
        """Take initial screenshot for comparison"""
        AllureUtils.attach_screenshot(
            driver,
            "Initial State",
            "Screenshot taken at the beginning of the test"
        )
    
    @allure.step("Attempt to find non-existent element")
    def find_nonexistent_element(self, driver):
        """Try to find an element that doesn't exist"""
        from appium.webdriver.common.appiumby import AppiumBy
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        # Try to find an element that definitely doesn't exist
        non_existent_id = "com.monoxer:id/this_element_does_not_exist_12345"
        
        try:
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((AppiumBy.ID, non_existent_id))
            )
            return element
        except TimeoutException:
            # Take screenshot before raising exception
            AllureUtils.attach_screenshot(
                driver,
                "Before Exception",
                "Screenshot taken just before raising NoSuchElementException"
            )
            raise NoSuchElementException(f"Element with ID '{non_existent_id}' not found")
    
    @allure.step("Test element not found scenario")
    def test_element_not_found(self, driver, test_data):
        """Test that fails by trying to find a non-existent element"""
        self.test_data = test_data
        
        # Attach test configuration
        AllureUtils.attach_config(
            {
                "test_name": "test_element_not_found",
                "language": test_data.__name__,
                "expected_failure": True,
                "failure_type": "NoSuchElementException"
            },
            "Test Configuration"
        )
        
        # Take initial screenshot
        self.take_initial_screenshot(driver)
        
        # This will fail and trigger screenshot attachment
        self.find_nonexistent_element(driver)
    
    @allure.step("Test assertion failure scenario")
    def test_assertion_failure(self, driver, test_data):
        """Test that fails due to assertion failure"""
        self.test_data = test_data
        AllureUtils.add_parameter("Language", test_data.__name__)
        AllureUtils.add_parameter("Test Method", "test_assertion_failure")
        
        # Take initial screenshot
        self.take_initial_screenshot(driver)
        
        # This assertion will fail
        assert 1 == 2, "This is an intentional assertion failure for demo purposes"
    
    @allure.step("Test timeout scenario")
    def test_timeout_failure(self, driver, test_data):
        """Test that fails due to timeout"""
        self.test_data = test_data
        AllureUtils.add_parameter("Language", test_data.__name__)
        AllureUtils.add_parameter("Test Method", "test_timeout_failure")
        
        from appium.webdriver.common.appiumby import AppiumBy
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        # Take initial screenshot
        self.take_initial_screenshot(driver)
        
        # Try to wait for an element that will never appear (very short timeout)
        try:
            element = WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((AppiumBy.ID, "com.monoxer:id/never_appearing_element"))
            )
        except TimeoutException:
            # Take screenshot before raising exception
            AllureUtils.attach_screenshot(
                driver,
                "Timeout Failure",
                "Screenshot taken when timeout exception occurred"
            )
            raise TimeoutException("Element did not appear within the expected timeout")
    
    @allure.step("Test with multiple steps and failure")
    def test_multiple_steps_failure(self, driver, test_data):
        """Test with multiple steps that fails at the end"""
        self.test_data = test_data
        AllureUtils.add_parameter("Language", test_data.__name__)
        AllureUtils.add_parameter("Test Method", "test_multiple_steps_failure")
        
        with AllureUtils.add_step("Step 1: Take initial screenshot"):
            self.take_initial_screenshot(driver)
        
        with AllureUtils.add_step("Step 2: Wait a moment"):
            import time
            time.sleep(2)
        
        with AllureUtils.add_step("Step 3: Take another screenshot"):
            AllureUtils.attach_screenshot(
                driver,
                "Step 3 Screenshot",
                "Screenshot taken during step 3"
            )
        
        with AllureUtils.add_step("Step 4: Intentional failure"):
            # This will fail and trigger the failure handling
            assert False, "Intentional failure in step 4 for demonstration"


@allure.epic("Monoxer App")
@allure.feature("Failure Demo")
@allure.story("App State Issues")
@allure.severity(allure.severity_level.NORMAL)
class TestAppStateFailures:
    """Test cases that fail due to app state issues"""
    
    @allure.step("Test app not in expected state")
    def test_app_not_in_expected_state(self, driver, test_data):
        """Test that fails because app is not in the expected state"""
        
        # Try to find an element that should be present in a specific app state
        from appium.webdriver.common.appiumby import AppiumBy
        
        try:
            # Try to find an element that might not be present
            element = driver.find_element(AppiumBy.ID, "com.monoxer:id/some_specific_state_element")
            
            # If we find it, take a screenshot and fail anyway for demo
            AllureUtils.attach_screenshot(
                driver,
                "Unexpected State",
                "App is in an unexpected state"
            )
            assert False, "App is in an unexpected state for this test"
            
        except NoSuchElementException:
            # Take screenshot and fail
            AllureUtils.attach_screenshot(
                driver,
                "Missing Expected Element",
                "Expected element not found, app may not be in correct state"
            )
            raise NoSuchElementException("Expected element not found, app state issue")


@allure.epic("Monoxer App")
@allure.feature("Failure Demo")
@allure.story("Performance Issues")
@allure.severity(allure.severity_level.MINOR)
class TestPerformanceFailures:
    """Test cases that fail due to performance issues"""
    
    @allure.step("Test slow response time")
    def test_slow_response_time(self, driver, test_data):
        """Test that fails due to slow response time"""
        
        import time
        start_time = time.time()
        
        # Simulate a slow operation
        time.sleep(3)
        
        elapsed_time = time.time() - start_time
        
        # Take screenshot
        AllureUtils.attach_screenshot(
            driver,
            "Performance Test",
            f"Performance test completed in {elapsed_time:.2f} seconds"
        )
        
        # Fail if operation took too long
        assert elapsed_time < 2.0, f"Operation took too long: {elapsed_time:.2f} seconds"
