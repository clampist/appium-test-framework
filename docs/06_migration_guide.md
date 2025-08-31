# ATF Framework Migration Guide

## Overview

This guide covers the migration process for existing test projects to the ATF Framework, including best practices, common patterns, and troubleshooting.

## Migration Overview

### What is Migration?

Migration involves adapting existing test code to work with the ATF Framework's architecture, patterns, and conventions. This includes:

- Restructuring test code to follow ATF patterns
- Adapting configuration management
- Implementing Page Object Model
- Setting up proper logging and reporting
- Integrating with ATF's utility classes

### Migration Benefits

1. **Standardized Architecture**: Consistent patterns across all test projects
2. **Enhanced Maintainability**: Better code organization and reusability
3. **Improved Reliability**: Robust error handling and resource management
4. **Better Reporting**: Integrated logging and reporting capabilities
5. **Easier Maintenance**: Centralized configuration and utility management

## Migration Process

### Phase 1: Assessment and Planning

#### 1. Analyze Current Test Structure

```bash
# Review existing test structure
tree tests/
ls -la *.py
cat requirements.txt
```

#### 2. Identify Migration Scope

- **Test Files**: Identify all test files to migrate
- **Dependencies**: List external dependencies and utilities
- **Configuration**: Document current configuration approach
- **Custom Utilities**: Identify custom utility functions

#### 3. Create Migration Plan

```markdown
# Migration Plan Template
## Project: [Project Name]
## Current Structure:
- Test files: [list]
- Dependencies: [list]
- Configuration: [description]

## Migration Tasks:
- [ ] Set up ATF project structure
- [ ] Migrate configuration management
- [ ] Implement Page Object Model
- [ ] Adapt test cases
- [ ] Update dependencies
- [ ] Test migration
- [ ] Update documentation
```

### Phase 2: Project Structure Setup

#### 1. Create ATF Project Structure

```bash
# Create ATF project structure
mkdir -p tests/{business_name}/{pages,datas}
mkdir -p config
mkdir -p scripts
mkdir -p logs
mkdir -p reports
mkdir -p screenshots/{business_name}/{base,cur}
```

#### 2. Set Up Configuration Files

```yaml
# config/appium_config.yaml
server:
  url: "http://localhost:4723"
  port: 4723

platform:
  name: "Android"
  version: "13"

device:
  id: "emulator-5554"
  name: "Android Emulator"

app:
  package: "com.example.app"
  activity: ".MainActivity"
  no_reset: true
```

#### 3. Install ATF Dependencies

```bash
# Install ATF framework
pip install -r requirements.txt

# Verify installation
python -c "from core.driver.appium_driver import AppiumDriver; print('ATF installed successfully')"
```

### Phase 3: Code Migration

#### 1. Migrate Configuration Management

**Before (Old Pattern)**:
```python
# Old configuration approach
APPIUM_SERVER = "http://localhost:4723"
PLATFORM_NAME = "Android"
APP_PACKAGE = "com.example.app"

capabilities = {
    "platformName": PLATFORM_NAME,
    "appPackage": APP_PACKAGE,
    "noReset": True
}
```

**After (ATF Pattern)**:
```python
# ATF configuration approach
from core.config.appium_config import AppiumConfig

config = AppiumConfig(
    server_url="http://localhost:4723",
    platform_name="Android",
    app_package="com.example.app",
    no_reset=True
)

# Validate configuration
if not config.validate():
    raise ValueError("Invalid configuration")

# Get capabilities
capabilities = config.get_capabilities()
```

#### 2. Implement Page Object Model

**Before (Old Pattern)**:
```python
# Old test approach
def test_login(self, driver):
    # Direct element interaction
    username_input = driver.find_element("id", "username")
    username_input.send_keys("testuser")
    
    password_input = driver.find_element("id", "password")
    password_input.send_keys("password")
    
    login_button = driver.find_element("id", "login")
    login_button.click()
```

**After (ATF Pattern)**:
```python
# ATF Page Object approach
from core.elements.page_object import PageObject

class LoginPage(PageObject):
    def __init__(self, driver):
        super().__init__(driver)
        self._init_elements()
    
    def _init_elements(self):
        """Initialize page elements"""
        self.add_element("username_input", "id", "username", "Username Input")
        self.add_element("password_input", "id", "password", "Password Input")
        self.add_element("login_button", "id", "login", "Login Button")
    
    def login(self, username, password):
        """Perform login operation"""
        self.input_text("username_input", username)
        self.input_text("password_input", password)
        self.click_element("login_button")

# Test using Page Object
def test_login(self, driver):
    login_page = LoginPage(driver)
    login_page.login("testuser", "password")
```

#### 3. Migrate Test Cases

**Before (Old Pattern)**:
```python
# Old test structure
import unittest
from selenium import webdriver

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Remote(
            command_executor="http://localhost:4723",
            desired_capabilities=capabilities
        )
    
    def test_successful_login(self):
        # Test implementation
        pass
    
    def tearDown(self):
        self.driver.quit()
```

**After (ATF Pattern)**:
```python
# ATF test structure
import pytest
from core.utils.logger import Log
from pages.login_page import LoginPage

class TestLogin:
    def setup_method(self, method):
        """Test method pre-processing"""
        Log.info(f"Starting test: {method.__name__}")
    
    def test_successful_login(self, driver):
        """Test successful login flow"""
        Log.info("Starting login test")
        
        login_page = LoginPage(driver)
        login_page.login("testuser", "password")
        
        # Verify login success
        assert driver.get_current_activity() == ".MainActivity"
        
        Log.info("Login test completed successfully")
    
    def teardown_method(self, method):
        """Test method post-processing"""
        Log.info(f"Completed test: {method.__name__}")
```

#### 4. Implement Logging

**Before (Old Pattern)**:
```python
# Old logging approach
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_example():
    logger.info("Starting test")
    # Test logic
    logger.info("Test completed")
```

**After (ATF Pattern)**:
```python
# ATF logging approach
from core.utils.logger import Log

def test_example():
    Log.info("Starting test")
    # Test logic
    Log.success("Test completed successfully")
```

### Phase 4: Testing and Validation

#### 1. Run Migration Tests

```bash
# Run migrated tests
pytest tests/migrated_project/ -v

# Run with detailed output
pytest tests/migrated_project/ -v --tb=long

# Run specific test
pytest tests/migrated_project/test_login.py::TestLogin::test_successful_login -v
```

#### 2. Validate Functionality

```bash
# Check test execution
python scripts/run_business_tests.py --business migrated_project

# Generate reports
pytest tests/migrated_project/ --html=reports/migration_report.html

# Check logs
tail -f logs/atf_$(date +%Y%m%d).log
```

#### 3. Performance Comparison

```bash
# Compare execution times
time pytest tests/old_project/ -v
time pytest tests/migrated_project/ -v

# Generate performance report
python scripts/generate_performance_report.py --old=old_project --new=migrated_project
```

## Migration Examples

### Example 1: Cocokara App Migration

#### Original Structure

```
cocokara/
├── test_cocokara.py          # Single test file
├── requirements.txt          # Dependencies
└── README.md                # Documentation
```

#### Migrated Structure

```
tests/jp.co.matsukiyococokara.app/
├── conftest.py              # pytest configuration
├── test_daily_challenge.py  # Test cases
├── datas/
│   └── test_data.py         # Test data
├── pages/
│   ├── main_page.py         # Main page object
│   ├── challenge_page.py    # Challenge page object
│   └── result_page.py       # Result page object
└── README.md               # Documentation
```

#### Key Migration Changes

1. **Configuration Management**:
   ```python
   # Before
   APP_PACKAGE = "jp.co.matsukiyococokara.app"
   
   # After
   from core.config.app_config import AppConfig
   app_config = AppConfig(app_package="jp.co.matsukiyococokara.app")
   ```

2. **Page Object Implementation**:
   ```python
   # Before
   def click_challenge_area(self, driver):
       element = driver.find_element("id", "challenge_area")
       element.click()
   
   # After
   class MainPage(PageObject):
       def _init_elements(self):
           self.add_element("challenge_area", "id", "challenge_area", "Challenge Area")
       
       def tap_challenge_area(self):
           self.click_element("challenge_area")
   ```

3. **Test Structure**:
   ```python
   # Before
   class TestCocokara(unittest.TestCase):
       def test_daily_challenge(self):
           # Test implementation
           pass
   
   # After
   class TestDailyChallenge:
       def test_daily_challenge_flow(self, driver):
           Log.info("Starting daily challenge test")
           # Test implementation
           Log.success("Daily challenge test completed")
   ```

### Example 2: Monoxer App Migration

#### Original Structure

```
examples/
└── monoxer_usage.py         # Single example file
```

#### Migrated Structure

```
tests/com.monoxer/
├── conftest.py              # pytest configuration
├── test_monoxer_features.py # Test cases
├── datas/
│   └── test_data.py         # Test data
├── pages/
│   ├── main_page.py         # Main page object
│   ├── search_page.py       # Search page object
│   └── library_page.py      # Library page object
└── README.md               # Documentation
```

#### Key Migration Changes

1. **Screenshot Management**:
   ```python
   # Before
   driver.save_screenshot("screenshot.png")
   
   # After
   from core.utils.screenshot_utils import ScreenshotUtils
   ScreenshotUtils.save_screenshot(driver, "com.monoxer", "feature_name", "01")
   ```

2. **Error Handling**:
   ```python
   # Before
   try:
       element.click()
   except Exception as e:
       print(f"Error: {e}")
   
   # After
   from core.utils.logger import Log
   try:
       element.click()
   except Exception as e:
       Log.error(f"Failed to click element: {e}")
       raise
   ```

## Migration Best Practices

### 1. Incremental Migration

- **Start Small**: Begin with a single test or feature
- **Validate Each Step**: Test after each migration phase
- **Maintain Functionality**: Ensure no regression in test behavior
- **Document Changes**: Keep track of all modifications

### 2. Code Quality

- **Follow ATF Patterns**: Use established ATF conventions
- **Implement Page Objects**: Separate UI logic from test logic
- **Use Proper Logging**: Implement comprehensive logging
- **Add Error Handling**: Include robust error handling

### 3. Testing Strategy

- **Parallel Testing**: Run old and new versions side by side
- **Regression Testing**: Ensure all functionality is preserved
- **Performance Testing**: Compare execution times
- **Integration Testing**: Test with other system components

### 4. Documentation

- **Update README**: Document new structure and usage
- **Code Comments**: Add comprehensive code comments
- **Migration Notes**: Document migration decisions and rationale
- **Troubleshooting**: Document common issues and solutions

## Common Migration Challenges

### 1. Configuration Complexity

**Challenge**: Complex configuration management in existing code

**Solution**:
```python
# Create configuration adapter
class ConfigAdapter:
    def __init__(self, old_config):
        self.old_config = old_config
    
    def to_atf_config(self):
        return AppiumConfig(
            server_url=self.old_config.get("server_url"),
            platform_name=self.old_config.get("platform_name"),
            app_package=self.old_config.get("app_package")
        )
```

### 2. Element Locator Changes

**Challenge**: Different element locator strategies

**Solution**:
```python
# Create locator adapter
class LocatorAdapter:
    @staticmethod
    def convert_locator(old_locator):
        """Convert old locator format to ATF format"""
        if old_locator.startswith("//"):
            return ("xpath", old_locator)
        elif old_locator.startswith("id="):
            return ("id", old_locator[3:])
        else:
            return ("id", old_locator)
```

### 3. Test Data Management

**Challenge**: Scattered test data across files

**Solution**:
```python
# Centralize test data
class TestDataManager:
    def __init__(self, data_file):
        self.data = FileUtils.read_json(data_file)
    
    def get_test_data(self, test_name):
        return self.data.get(test_name, {})
    
    def get_user_data(self, user_type):
        return self.data.get("users", {}).get(user_type, {})
```

## Migration Validation

### 1. Functional Validation

```bash
# Run all tests
pytest tests/migrated_project/ -v

# Compare results
python scripts/compare_test_results.py --old=old_results.json --new=new_results.json
```

### 2. Performance Validation

```bash
# Measure execution time
time pytest tests/migrated_project/ -v

# Generate performance report
python scripts/generate_performance_report.py --project=migrated_project
```

### 3. Code Quality Validation

```bash
# Run linting
flake8 tests/migrated_project/
black tests/migrated_project/
mypy tests/migrated_project/

# Generate coverage report
pytest tests/migrated_project/ --cov=core --cov-report=html
```

## Post-Migration Tasks

### 1. Cleanup

```bash
# Remove old files
rm -rf old_project/
rm -rf backup/

# Update documentation
git add docs/
git commit -m "Update documentation after migration"
```

### 2. Training

- **Team Training**: Train team members on new patterns
- **Code Reviews**: Establish code review process
- **Best Practices**: Document team-specific best practices
- **Troubleshooting**: Create troubleshooting guide

### 3. Monitoring

```bash
# Set up monitoring
python scripts/setup_monitoring.py --project=migrated_project

# Monitor test execution
python scripts/monitor_tests.py --project=migrated_project
```

## Troubleshooting

### Common Issues

#### 1. Import Errors

**Problem**: Module import errors after migration

**Solution**:
```python
# Add project root to Python path
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

#### 2. Configuration Issues

**Problem**: Configuration not loading correctly

**Solution**:
```python
# Verify configuration loading
from core.config.appium_config import AppiumConfig
config = AppiumConfig()
print(f"Server URL: {config.server_url}")
print(f"Platform: {config.platform_name}")
```

#### 3. Element Not Found

**Problem**: Elements not found after migration

**Solution**:
```python
# Add explicit waits
from core.utils.time_utils import TimeUtils

def wait_for_element(driver, locator, timeout=10):
    def condition():
        try:
            driver.find_element(*locator)
            return True
        except:
            return False
    
    return TimeUtils.wait_for_condition(condition, timeout)
```

### Getting Help

1. **Check Documentation**: Review ATF documentation
2. **Search Issues**: Look for similar issues in repository
3. **Ask Community**: Post questions in community forums
4. **Create Issue**: Create detailed issue with reproduction steps

## Conclusion

Migration to the ATF Framework provides significant benefits in terms of maintainability, reliability, and standardization. By following this guide and best practices, you can successfully migrate your existing test projects while maintaining functionality and improving code quality.

Remember to:
- Plan your migration carefully
- Test thoroughly at each step
- Document your changes
- Train your team on new patterns
- Monitor performance and stability
