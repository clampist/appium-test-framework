# ATF Framework User Guide

## Overview

This guide covers all the features that users directly interact with when using the ATF Framework, including configuration management, test execution, logging, and reporting.

## 🔧 Configuration Management

### Appium Configuration

The framework uses dataclass-based configuration for Appium settings:

```python
from core.config.appium_config import AppiumConfig

# Create configuration
config = AppiumConfig(
    server_url="http://localhost:4723",
    platform_name="Android",
    app_package="com.example.app",
    app_activity=".MainActivity",
    device_id="emulator-5554",
    no_reset=True,
    new_command_timeout=3600
)

# Validate configuration
if not config.validate():
    raise ValueError("Invalid configuration")

# Get capabilities
capabilities = config.get_capabilities()
```

### Device Configuration

```python
from core.config.device_config import DeviceConfig

device_config = DeviceConfig(
    device_id="emulator-5554",
    platform="Android",
    platform_version="13",
    device_name="Android Emulator",
    screen_width=1080,
    screen_height=1920,
    language="en",
    timezone="UTC"
)
```

### Application Configuration

```python
from core.config.app_config import AppConfig

app_config = AppConfig(
    app_name="Test App",
    app_package="com.example.app",
    app_activity=".MainActivity",
    app_path="/path/to/app.apk",
    app_type="native",
    launch_timeout=30,
    auto_grant_permissions=True
)
```

### Environment Variable Override

All configurations support environment variable override:

```bash
# Set environment variables
export APPIUM_SERVER_URL=http://localhost:4723
export APPIUM_PLATFORM_NAME=Android
export APPIUM_APP_PACKAGE=com.example.app
export APPIUM_DEVICE_ID=emulator-5554
```

## 📊 Logging and Tracing

### Unified Logging Interface

The framework provides a unified logging interface:

```python
from core.utils.logger import Log

# Different log levels
Log.debug("Debug information")
Log.info("General information")
Log.warning("Warning message")
Log.error("Error message")
Log.critical("Critical error")
Log.success("Success message")

# Exception logging
try:
    # Some operation
    pass
except Exception as e:
    Log.exception("Operation failed")
```

### Automatic Caller Information

Logs automatically include caller information:

```
2024-01-15 10:30:45 | INFO | tests.com.monoxer.test_features | Test started
2024-01-15 10:30:46 | INFO | pages.main_page | Clicking login button
2024-01-15 10:30:47 | SUCCESS | tests.com.monoxer.test_features | Test completed
```

### File Logging Configuration

```python
# Add custom file handler
Log.add_file_handler(
    filepath="logs/custom.log",
    level="DEBUG",
    rotation="1 day"
)

# Set log level
Log.set_level("DEBUG")
```

## 🗄️ Page Object Pattern

### Creating Page Objects

```python
from core.elements.page_object import PageObject
from core.elements.base_element import BaseElement

class LoginPage(PageObject):
    def __init__(self, driver):
        super().__init__(driver)
        self._init_elements()
    
    def _init_elements(self):
        """Initialize page elements"""
        self.add_element("username_input", "id", "username", "Username Input")
        self.add_element("password_input", "id", "password", "Password Input")
        self.add_element("login_button", "id", "login", "Login Button")
        self.add_element("error_message", "id", "error", "Error Message")
    
    def login(self, username, password):
        """Perform login operation"""
        self.input_text("username_input", username)
        self.input_text("password_input", password)
        self.click_element("login_button")
    
    def get_error_message(self):
        """Get error message text"""
        return self.get_element_text("error_message")
    
    def is_error_displayed(self):
        """Check if error message is displayed"""
        return self.is_element_displayed("error_message")
```

### Element Operations

```python
# Basic operations
page.click_element("button_name")
page.input_text("input_name", "text")
page.get_element_text("element_name")
page.is_element_displayed("element_name")
page.is_element_enabled("element_name")

# Advanced operations
page.wait_for_element("element_name", timeout=10)
page.wait_for_element_clickable("element_name", timeout=10)
page.tap_element("element_name", x=10, y=20)
page.long_press_element("element_name", duration=2000)
page.scroll_to_element("element_name")
```

## ⚡ Test Execution

### Test Markers

```python
import pytest

@pytest.mark.smoke        # Smoke tests - Quick verification of core functionality
@pytest.mark.daily        # Daily tests - Daily functionality verification
@pytest.mark.regression   # Regression tests - Complete functionality verification
@pytest.mark.integration  # Integration tests - System integration verification
@pytest.mark.android      # Android platform tests
@pytest.mark.ios          # iOS platform tests
@pytest.mark.slow         # Slow tests - Long-running tests

class TestLogin:
    @pytest.mark.smoke
    def test_successful_login(self):
        """Smoke test for login functionality"""
        pass
    
    @pytest.mark.regression
    def test_login_validation(self):
        """Regression test for login validation"""
        pass
```

### Running Tests with Markers

```bash
# Run smoke tests
pytest tests/ -m smoke

# Run multiple markers
pytest tests/ -m "smoke and not slow"

# Exclude specific markers
pytest tests/ -m "not slow"

# Run specific business path
pytest tests/com.monoxer/ -m smoke
```

### Parallel Execution

```bash
# Auto-detect CPU cores
pytest tests/ --parallel

# Specify worker count
pytest tests/ --parallel=4

# Disable parallel execution
pytest tests/ --no-parallel
```

## 📱 Screenshot Management

### Automatic Screenshots

```python
from core.utils.screenshot_utils import ScreenshotUtils

# Take screenshot
ScreenshotUtils.save_screenshot(driver, "com.example.app", "login_page", "01")

# Compare screenshots
ScreenshotUtils.compare_screenshots("com.example.app", "login_page")

# Set baseline screenshots
ScreenshotUtils.set_base_screenshots("com.example.app")

# Clear screenshot directory
ScreenshotUtils.clear_screenshot_directory("com.example.app")
```

### Screenshot Directory Structure

```
screenshots/
├── com.example.app/
│   ├── base/                    # Baseline screenshots
│   │   ├── login_page_01.png
│   │   └── home_page_01.png
│   └── cur/                     # Current test screenshots
│       ├── login_page_01.png
│       └── home_page_01.png
```

## 🔧 Test Data Management

### Data-Driven Testing

```python
from core.utils.file_utils import FileUtils

class TestData:
    @staticmethod
    def load_test_data(file_path):
        """Load test data from JSON/YAML file"""
        return FileUtils.read_json(file_path)
    
    @staticmethod
    def save_test_data(file_path, data):
        """Save test data to file"""
        FileUtils.write_json(file_path, data)

# Usage
test_data = TestData.load_test_data("tests/data/login_data.json")
```

### Test Data Example

```json
{
  "valid_users": [
    {
      "username": "testuser1",
      "password": "password123",
      "expected_result": "success"
    },
    {
      "username": "testuser2",
      "password": "password456",
      "expected_result": "success"
    }
  ],
  "invalid_users": [
    {
      "username": "invalid",
      "password": "wrong",
      "expected_result": "error"
    }
  ]
}
```

## 🚀 Test Runner Scripts

### Using Makefile

```bash
# Environment setup
make install    # Install dependencies
make setup      # Setup environment

# Test running
make test-smoke     # Run smoke tests
make test-daily     # Run daily tests
make test-regression # Run regression tests
make test-cocokara  # Run Cocokara tests

# Advanced usage
make test-business BUSINESS=jp.co.matsukiyococokara.app
make test-markers MARKERS=smoke daily
make test-parallel PARALLEL=4

# Environment management
make check-env      # Check environment
make start-appium   # Start Appium server
make stop-appium    # Stop Appium server

# Cleanup
make clean          # Clean reports and logs
make show-reports   # Show reports
```

### Using Universal Test Runner

```bash
# Run all business tests
python scripts/run_business_tests.py --all

# Run specific business tests
python scripts/run_business_tests.py --business jp.co.matsukiyococokara.app

# Run tests with specific markers
python scripts/run_business_tests.py --all --markers smoke daily

# Parallel running
python scripts/run_business_tests.py --all --parallel 4

# Generate Allure reports
python scripts/run_business_tests.py --all --allure
```

### Using Business-Specific Scripts

```bash
# Cocokara tests
./scripts/run_cocokara_tests.sh -m smoke daily
./scripts/run_cocokara_tests.sh --env ci -m smoke
./scripts/run_cocokara_tests.sh --allure
```

## 📊 Reporting

### HTML Reports

```bash
# Generate HTML report
pytest tests/ --html=reports/report.html

# Generate detailed HTML report
pytest tests/ --html=reports/report.html --self-contained-html
```

### JUnit XML Reports

```bash
# Generate JUnit XML report
pytest tests/ --junitxml=reports/junit.xml
```

### Allure Reports

```bash
# Generate Allure report
pytest tests/ --alluredir=reports/allure-results

# Serve Allure report
allure serve reports/allure-results

# Generate static Allure report
allure generate reports/allure-results --clean
```

## 🔍 Environment Management

### Environment Types

1. **local**: Local development environment
2. **ci**: CI/CD environment
3. **staging**: Pre-release environment
4. **production**: Production environment

### Environment-Specific Configuration

```python
# CI environment automatic configuration
if args.env == "ci":
    if not args.parallel:
        args.parallel = 4  # CI environment default 4 parallel processes
    if not args.markers:
        args.markers = ["smoke"]  # CI environment default run smoke tests
```

### Environment Check

```bash
# Check Python environment
make check-env

# Check device connections
make check-devices

# Start Appium server
make start-appium

# Stop Appium server
make stop-appium
```

## 📝 Best Practices

### 1. Page Object Pattern
- Encapsulate page elements and operations in PageObject classes
- Use meaningful element names
- Implement page status verification methods

### 2. Configuration Management
- Use configuration files instead of hardcoding
- Support environment variable override
- Validate configuration effectiveness

### 3. Error Handling
- Use try-catch to wrap critical operations
- Record detailed error information
- Save screenshots on failure

### 4. Test Organization
- Organize test cases by business path
- Use descriptive test method names
- Reasonably use test markers

### 5. Logging
- Use unified Log interface
- Record critical operation steps
- Set appropriate log levels

## 🔧 Common Patterns

### Test Setup and Teardown

```python
import pytest
from core.utils.logger import Log

class TestExample:
    def setup_method(self, method):
        """Test method pre-processing"""
        Log.info(f"Starting test: {method.__name__}")
    
    def teardown_method(self, method):
        """Test method post-processing"""
        Log.info(f"Completed test: {method.__name__}")
    
    def test_example(self):
        """Example test method"""
        Log.info("Executing test logic")
        # Test implementation
```

### Resource Management

```python
from core.driver.appium_driver import AppiumDriver

def test_with_driver():
    driver = None
    try:
        # Create and start driver
        driver = AppiumDriver(config)
        driver.start_driver()
        
        # Test logic
        # ...
        
    finally:
        # Ensure driver is closed
        if driver:
            driver.quit_driver()
```

### Wait Strategies

```python
from core.utils.time_utils import TimeUtils

# Wait for condition
def wait_for_element_visible(driver, element_id, timeout=10):
    def condition():
        try:
            element = driver.find_element("id", element_id)
            return element.is_displayed()
        except:
            return False
    
    return TimeUtils.wait_for_condition(condition, timeout, condition_name="element visible")
```
