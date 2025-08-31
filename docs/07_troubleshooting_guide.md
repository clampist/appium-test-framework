# ATF Framework Troubleshooting Guide

## Overview

This guide provides solutions to common issues encountered when using the ATF Framework, including installation problems, test execution issues, and configuration errors.

## Quick Diagnosis

### Environment Check

```bash
# Check Python environment
python --version
pip list | grep -E "(pytest|appium|selenium)"

# Check Appium installation
appium --version
appium-doctor

# Check device connections
adb devices
adb version

# Check framework installation
python -c "from core.driver.appium_driver import AppiumDriver; print('ATF installed successfully')"
```

### Basic Health Check

```bash
# Run basic health check
make check-env

# Check configuration
python -c "
from core.config.appium_config import AppiumConfig
config = AppiumConfig()
print(f'Server URL: {config.server_url}')
print(f'Platform: {config.platform_name}')
print(f'App Package: {config.app_package}')
"

# Test basic functionality
python -m pytest tests/common/ -v
```

## Common Issues and Solutions

### 1. Installation Issues

#### Python Environment Problems

**Problem**: Python version mismatch or virtual environment not activated

**Symptoms**:
```
ImportError: No module named 'core'
ModuleNotFoundError: No module named 'pytest'
```

**Solutions**:
```bash
# Check Python version
python --version

# Activate correct environment
pyenv activate atf
# or
source atf_env/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Verify installation
python -c "import pytest, appium, selenium; print('Dependencies OK')"
```

#### Appium Installation Issues

**Problem**: Appium not found or version incompatible

**Symptoms**:
```
Command 'appium' not found
Appium version 1.x.x is not compatible
```

**Solutions**:
```bash
# Install Appium globally
npm install -g appium

# Install specific version
npm install -g appium@2.0.0

# Verify installation
appium --version

# Check environment
appium-doctor
```

#### Android Environment Issues

**Problem**: Android SDK not configured or devices not detected

**Symptoms**:
```
adb: command not found
No devices found
```

**Solutions**:
```bash
# Set Android environment variables
export ANDROID_HOME=/path/to/android/sdk
export PATH=$PATH:$ANDROID_HOME/platform-tools

# Verify ADB installation
adb version
adb devices

# Enable USB debugging on device
# Settings > Developer options > USB debugging
```

### 2. Configuration Issues

#### Configuration Loading Errors

**Problem**: Configuration files not found or invalid

**Symptoms**:
```
FileNotFoundError: config/appium_config.yaml
YAMLError: Invalid YAML format
```

**Solutions**:
```python
# Check configuration file existence
import os
config_file = "config/appium_config.yaml"
if not os.path.exists(config_file):
    print(f"Configuration file not found: {config_file}")

# Validate YAML format
import yaml
try:
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    print("YAML format is valid")
except yaml.YAMLError as e:
    print(f"YAML format error: {e}")
```

#### Environment Variable Issues

**Problem**: Environment variables not set or not recognized

**Symptoms**:
```
Configuration not loaded from environment variables
Default values being used instead of environment values
```

**Solutions**:
```bash
# Set environment variables
export APPIUM_SERVER_URL=http://localhost:4723
export APPIUM_PLATFORM_NAME=Android
export APPIUM_APP_PACKAGE=com.example.app

# Verify environment variables
echo $APPIUM_SERVER_URL
echo $APPIUM_PLATFORM_NAME
echo $APPIUM_APP_PACKAGE

# Test configuration loading
python -c "
from core.config.appium_config import AppiumConfig
config = AppiumConfig()
print(f'Server URL: {config.server_url}')
print(f'Platform: {config.platform_name}')
print(f'App Package: {config.app_package}')
"
```

### 3. Test Execution Issues

#### Driver Connection Problems

**Problem**: Cannot connect to Appium server or device

**Symptoms**:
```
ConnectionRefusedError: [Errno 61] Connection refused
WebDriverException: Message: An unknown server-side error occurred
```

**Solutions**:
```bash
# Check Appium server status
curl http://localhost:4723/status

# Start Appium server
appium --base-path /wd/hub &

# Check device connections
adb devices

# Verify device is ready
adb shell getprop ro.build.version.release
```

#### Element Not Found Errors

**Problem**: Elements cannot be located on the page

**Symptoms**:
```
NoSuchElementException: Message: An element could not be located
ElementNotInteractableException: Message: element not interactable
```

**Solutions**:
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
    
    return TimeUtils.wait_for_condition(condition, timeout, "element visible")

# Use multiple locator strategies
def find_element_with_fallback(driver, locators):
    for locator in locators:
        try:
            return driver.find_element(*locator)
        except:
            continue
    raise Exception("Element not found with any locator")
```

#### Test Timeout Issues

**Problem**: Tests taking too long to execute or timing out

**Symptoms**:
```
TimeoutException: Message: timeout
Test execution taking longer than expected
```

**Solutions**:
```python
# Increase timeout values
from core.config.appium_config import AppiumConfig

config = AppiumConfig(
    timeout=60,  # Increase from default 30
    new_command_timeout=7200  # Increase from default 3600
)

# Add explicit waits with longer timeouts
from core.utils.time_utils import TimeUtils

TimeUtils.wait_for_condition(condition_func, timeout=60, interval=1.0)
```

### 4. Logging and Reporting Issues

#### Log File Problems

**Problem**: Log files not created or not writable

**Symptoms**:
```
PermissionError: [Errno 13] Permission denied
Log files not appearing in logs directory
```

**Solutions**:
```bash
# Check directory permissions
ls -la logs/
chmod 755 logs/

# Create logs directory if missing
mkdir -p logs

# Check disk space
df -h

# Test log writing
python -c "
from core.utils.logger import Log
Log.info('Test log message')
"
```

#### Report Generation Issues

**Problem**: Test reports not generated or incomplete

**Symptoms**:
```
HTML report not created
Allure report generation failed
```

**Solutions**:
```bash
# Generate HTML report
pytest tests/ --html=reports/report.html --self-contained-html

# Generate Allure report
pytest tests/ --alluredir=reports/allure-results
allure generate reports/allure-results --clean

# Check report directory
ls -la reports/

# Verify report content
cat reports/report.html | head -20
```

### 5. Screenshot Management Issues

#### Screenshot Directory Problems

**Problem**: Screenshots not saved or directory not found

**Symptoms**:
```
FileNotFoundError: screenshots directory not found
Screenshots not appearing in expected location
```

**Solutions**:
```python
# Check screenshot directory structure
from core.utils.screenshot_utils import ScreenshotUtils

# Ensure directory exists
import os
screenshot_dir = "screenshots/com.example.app/cur"
os.makedirs(screenshot_dir, exist_ok=True)

# Test screenshot functionality
ScreenshotUtils.save_screenshot(driver, "com.example.app", "test", "01")
```

#### Screenshot Comparison Issues

**Problem**: Screenshot comparison failing or inaccurate

**Symptoms**:
```
Screenshot comparison always fails
Baseline screenshots not found
```

**Solutions**:
```python
# Set baseline screenshots
ScreenshotUtils.set_base_screenshots("com.example.app")

# Compare screenshots with tolerance
ScreenshotUtils.compare_screenshots("com.example.app", "test", tolerance=0.95)

# Check screenshot files
import os
base_dir = "screenshots/com.example.app/base"
cur_dir = "screenshots/com.example.app/cur"
print(f"Base screenshots: {os.listdir(base_dir)}")
print(f"Current screenshots: {os.listdir(cur_dir)}")
```

### 6. Performance Issues

#### Memory Leaks

**Problem**: Tests consuming too much memory

**Symptoms**:
```
Memory usage increasing over time
Tests becoming slower with each run
```

**Solutions**:
```python
# Proper resource cleanup
def test_with_cleanup(self, driver):
    try:
        # Test logic
        pass
    finally:
        # Clean up resources
        driver.quit()
        driver = None

# Monitor memory usage
import psutil
import os

def log_memory_usage():
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    Log.info(f"Memory usage: {memory_info.rss / 1024 / 1024:.2f} MB")
```

#### Slow Test Execution

**Problem**: Tests taking too long to execute

**Symptoms**:
```
Test execution time increasing
Individual test steps taking too long
```

**Solutions**:
```python
# Optimize element location
# Use more specific locators
element = driver.find_element("id", "specific_id")  # Better
element = driver.find_element("xpath", "//*[contains(@class, 'generic')]")  # Worse

# Reduce wait times where appropriate
from core.utils.time_utils import TimeUtils
TimeUtils.wait_for_condition(condition_func, timeout=5, interval=0.5)

# Use parallel execution
pytest tests/ --parallel=4
```

### 7. CI/CD Issues

#### Jenkins Pipeline Problems

**Problem**: Tests failing in Jenkins environment

**Symptoms**:
```
Tests pass locally but fail in Jenkins
Environment differences causing issues
```

**Solutions**:
```groovy
// Jenkinsfile
pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.12'
        ATF_ENV = 'ci'
    }
    
    stages {
        stage('Setup') {
            steps {
                sh '''
                    pyenv install ${PYTHON_VERSION}
                    pyenv virtualenv ${PYTHON_VERSION} atf
                    pyenv activate atf
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Start Appium') {
            steps {
                sh '''
                    npm install -g appium
                    appium --base-path /wd/hub &
                    sleep 10
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                sh '''
                    pyenv activate atf
                    python scripts/run_business_tests.py --all --parallel 4
                '''
            }
        }
    }
}
```

#### GitHub Actions Issues

**Problem**: Tests failing in GitHub Actions

**Symptoms**:
```
Workflow failing due to environment issues
Tests timing out in CI environment
```

**Solutions**:
```yaml
# .github/workflows/ci-tests.yml
name: ATF Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Start Appium Server
      run: |
        npm install -g appium
        appium --base-path /wd/hub &
        sleep 10
    
    - name: Run tests
      run: |
        python scripts/run_business_tests.py --all --parallel 4
      timeout-minutes: 30
```

## Debugging Techniques

### 1. Verbose Logging

```python
# Enable debug logging
from core.utils.logger import Log
Log.set_level("DEBUG")

# Add detailed logging
Log.debug("Element locator: %s", locator)
Log.debug("Page source: %s", driver.page_source)
```

### 2. Screenshot Debugging

```python
# Take screenshots at key points
def debug_test(self, driver, step_name):
    ScreenshotUtils.save_screenshot(driver, "com.example.app", f"debug_{step_name}", "01")
    Log.info(f"Debug screenshot saved for step: {step_name}")
```

### 3. Element Inspection

```python
# Inspect element properties
def inspect_element(self, driver, locator):
    try:
        element = driver.find_element(*locator)
        Log.info(f"Element found: {element}")
        Log.info(f"Element text: {element.text}")
        Log.info(f"Element attributes: {element.get_attribute('class')}")
    except Exception as e:
        Log.error(f"Element not found: {e}")
```

### 4. Page Source Analysis

```python
# Analyze page source
def analyze_page(self, driver):
    page_source = driver.page_source
    Log.debug("Page source length: %d", len(page_source))
    
    # Search for specific elements
    if "target_element" in page_source:
        Log.info("Target element found in page source")
    else:
        Log.warning("Target element not found in page source")
```

## Performance Monitoring

### 1. Test Execution Monitoring

```python
# Monitor test execution time
import time
from core.utils.logger import Log

def monitor_test_execution():
    start_time = time.time()
    
    def log_execution_time():
        end_time = time.time()
        duration = end_time - start_time
        Log.info(f"Test execution time: {duration:.2f} seconds")
    
    return log_execution_time
```

### 2. Resource Usage Monitoring

```python
# Monitor system resources
import psutil
import os

def monitor_resources():
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    cpu_percent = process.cpu_percent()
    
    Log.info(f"Memory usage: {memory_info.rss / 1024 / 1024:.2f} MB")
    Log.info(f"CPU usage: {cpu_percent:.2f}%")
```

## Getting Help

### 1. Self-Diagnosis

```bash
# Run comprehensive health check
make check-env
make check-devices
python scripts/diagnose_environment.py
```

### 2. Collecting Information

When reporting issues, collect the following information:

```bash
# System information
uname -a
python --version
pip list

# Framework information
python -c "from core.driver.appium_driver import AppiumDriver; print('ATF version info')"

# Test execution logs
tail -n 100 logs/atf_$(date +%Y%m%d).log

# Configuration
cat config/appium_config.yaml
echo $APPIUM_SERVER_URL
echo $APPIUM_PLATFORM_NAME
```

### 3. Reporting Issues

When creating an issue report, include:

1. **Problem Description**: Clear description of the issue
2. **Steps to Reproduce**: Detailed steps to reproduce the problem
3. **Expected vs Actual Behavior**: What you expected vs what happened
4. **Environment Information**: System, Python, Appium versions
5. **Logs and Screenshots**: Relevant logs and screenshots
6. **Configuration**: Relevant configuration files
7. **Test Code**: Minimal test case that reproduces the issue

### 4. Community Resources

- **Documentation**: Check the ATF documentation
- **Examples**: Review example code in the `examples/` directory
- **Issues**: Search existing issues in the repository
- **Discussions**: Participate in community discussions

## Prevention

### 1. Regular Maintenance

```bash
# Regular cleanup
make clean
rm -rf logs/*
rm -rf reports/*
rm -rf screenshots/*/cur/*

# Update dependencies
pip install -r requirements.txt --upgrade

# Check for updates
git pull origin main
```

### 2. Best Practices

1. **Use Explicit Waits**: Always use explicit waits instead of implicit waits
2. **Proper Resource Management**: Ensure proper cleanup in finally blocks
3. **Comprehensive Logging**: Log important steps and error conditions
4. **Regular Testing**: Run tests regularly to catch issues early
5. **Environment Consistency**: Maintain consistent environments across development and CI

### 3. Monitoring Setup

```bash
# Set up monitoring
python scripts/setup_monitoring.py

# Regular health checks
crontab -e
# Add: 0 */6 * * * cd /path/to/atf && make check-env
```

## Conclusion

This troubleshooting guide covers the most common issues encountered with the ATF Framework. By following these solutions and best practices, you can resolve most problems quickly and maintain a stable testing environment.

Remember to:
- Always check the environment first
- Use comprehensive logging for debugging
- Collect detailed information when reporting issues
- Follow best practices to prevent issues
- Keep the framework and dependencies updated
