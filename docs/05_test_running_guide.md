# ATF Framework Test Running Guide

## Overview

This guide covers all aspects of running tests with the ATF Framework, including local execution, CI/CD integration, parallel testing, and reporting.

## Test Execution Methods

### 1. Using Makefile (Recommended)

Makefile provides simplified commands for common test execution scenarios:

```bash
# View all available commands
make help

# Basic test running
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

### 2. Using Universal Test Runner

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

### 3. Using pytest Directly

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/com.honda.roadsync.duo/test_login.py

# Run specific test method
pytest tests/com.honda.roadsync.duo/test_login.py::TestLogin::test_successful_login

# Run tests with markers
pytest tests/ -m smoke
pytest tests/ -m "smoke and not slow"

# Generate HTML report
pytest --html=reports/report.html tests/

# Generate JUnit XML report
pytest --junitxml=reports/junit.xml tests/
```

### 4. Using Business-Specific Scripts

```bash
# Cocokara tests
./scripts/run_cocokara_tests.sh -m smoke daily
./scripts/run_cocokara_tests.sh --env ci -m smoke
./scripts/run_cocokara_tests.sh --allure
```

## Test Markers

### Marker Definitions

```python
import pytest

@pytest.mark.smoke        # Smoke tests - Quick verification of core functionality
@pytest.mark.daily        # Daily tests - Daily functionality verification
@pytest.mark.regression   # Regression tests - Complete functionality verification
@pytest.mark.integration  # Integration tests - System integration verification
@pytest.mark.unit         # Unit tests - Component-level testing
@pytest.mark.slow         # Slow tests - Long-running tests
@pytest.mark.android      # Android platform tests
@pytest.mark.ios          # iOS platform tests

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

### Marker Usage

```bash
# Run smoke tests
pytest tests/ -m smoke

# Run multiple markers
pytest tests/ -m "smoke and not slow"

# Exclude specific markers
pytest tests/ -m "not slow"

# Run specific business path
pytest tests/com.monoxer/ -m smoke

# Combine markers
pytest tests/ -m "smoke and android"
```

## Parallel Execution

### Local Parallel Execution

```bash
# Auto-detect CPU cores
pytest tests/ --parallel

# Specify worker count
pytest tests/ --parallel=4

# Disable parallel execution
pytest tests/ --no-parallel

# Using test runner
python scripts/run_business_tests.py --all --parallel 4
```

### CI/CD Parallel Execution

#### GitHub Actions

```yaml
# .github/workflows/ci-tests.yml
name: ATF Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.12']
        parallel: [4]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python scripts/run_business_tests.py --all --parallel ${{ matrix.parallel }}
```

#### Jenkins Pipeline

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    stages {
        stage('Parallel Tests') {
            parallel {
                stage('Smoke Tests') {
                    steps {
                        sh '''
                            pyenv activate atf
                            python scripts/run_business_tests.py --all --markers smoke --parallel 2
                        '''
                    }
                }
                stage('Regression Tests') {
                    steps {
                        sh '''
                            pyenv activate atf
                            python scripts/run_business_tests.py --all --markers regression --parallel 4
                        '''
                    }
                }
            }
        }
    }
}
```

## Environment Management

### Environment Types

1. **local**: Local development environment
2. **ci**: CI/CD environment
3. **staging**: Pre-release environment
4. **production**: Production environment

### Environment-Specific Configuration

```python
# scripts/run_business_tests.py
def adjust_config_for_environment(args):
    """Adjust configuration based on environment"""
    if args.env == "ci":
        if not args.parallel:
            args.parallel = 4  # CI environment default 4 parallel processes
        if not args.markers:
            args.markers = ["smoke"]  # CI environment default run smoke tests
    elif args.env == "local":
        if not args.parallel:
            args.parallel = 2  # Local environment default 2 parallel processes
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

# Check environment variables
echo $ATF_ENV
echo $APPIUM_SERVER_URL
echo $APPIUM_PLATFORM_NAME
```

## Test Organization

### Business Path Structure

```
tests/
├── com.honda.roadsync.duo/     # Business path 1
│   ├── conftest.py             # pytest configuration
│   ├── test_login.py           # Login tests
│   └── pages/                  # Page objects
├── com.honda.ms.dm.sab/        # Business path 2
│   ├── conftest.py             # pytest configuration
│   └── pages/                  # Page objects
├── com.monoxer/                # Business path 3
│   ├── conftest.py             # pytest configuration
│   ├── test_monoxer_features.py # Feature tests
│   └── pages/                  # Page objects
└── common/                     # Common tests
    └── __init__.py
```

### Running Tests by Business Path

```bash
# Run specific business path
pytest tests/com.honda.roadsync.duo/
pytest tests/com.monoxer/
pytest tests/jp.co.matsukiyococokara.app/

# Run with business-specific configuration
python scripts/run_business_tests.py --business com.monoxer
python scripts/run_business_tests.py --business jp.co.matsukiyococokara.app
```

## Reporting

### HTML Reports

```bash
# Generate HTML report
pytest tests/ --html=reports/report.html

# Generate detailed HTML report
pytest tests/ --html=reports/report.html --self-contained-html

# Generate HTML report with screenshots
pytest tests/ --html=reports/report.html --capture=no
```

### JUnit XML Reports

```bash
# Generate JUnit XML report
pytest tests/ --junitxml=reports/junit.xml

# Generate JUnit XML with test class names
pytest tests/ --junitxml=reports/junit.xml --junit-prefix=atf
```

### Allure Reports

```bash
# Generate Allure report
pytest tests/ --alluredir=reports/allure-results

# Serve Allure report
allure serve reports/allure-results

# Generate static Allure report
allure generate reports/allure-results --clean

# Open Allure report
allure open reports/allure-results
```

### Custom Reports

```bash
# Generate test summary
python scripts/generate_test_summary.py

# Generate performance report
python scripts/generate_performance_report.py

# Generate coverage report
pytest tests/ --cov=core --cov-report=html
```

## Performance Optimization

### Execution Time Optimization

1. **Parallel Execution**: Use multi-process parallel test running
2. **Test Grouping**: Group execution by business or functionality
3. **Resource Reuse**: Reuse drivers and sessions
4. **Caching**: Cache test data and configuration

### Resource Usage Optimization

1. **Memory Management**: Timely release of unnecessary resources
2. **Connection Pooling**: Reuse network connections
3. **Device Management**: Reasonable allocation of device resources
4. **Log Level**: Adjust log level based on environment

### Performance Monitoring

```bash
# Monitor test execution time
time pytest tests/ -m smoke

# Monitor memory usage
python scripts/monitor_performance.py

# Generate performance report
python scripts/generate_performance_report.py --output=reports/performance.html
```

## Error Handling and Recovery

### Error Handling Strategy

1. **Environment Check**: Check necessary environment before running
2. **Graceful Degradation**: Continue executing other tests when partially failed
3. **Retry Mechanism**: Automatic retry for network or temporary errors
4. **Resource Cleanup**: Clean up resources after test completion

### Recovery Mechanism

```bash
# Clean environment
make clean

# Restart Appium server
make stop-appium
make start-appium

# Re-run failed tests
pytest tests/ --lf  # Run last failed tests

# Re-run failed tests with more details
pytest tests/ --lf --tb=long

# Re-run specific failed test
pytest tests/ --lf -k "test_login"
```

### Common Error Solutions

#### Environment Issues

```bash
# Python environment issues
pyenv activate atf
pip install -r requirements.txt

# Appium server issues
pkill -f appium
appium --base-path /wd/hub &

# Device connection issues
adb devices
adb kill-server && adb start-server
```

#### Test Issues

```bash
# Test failures
pytest tests/ --lf --tb=short

# Timeout issues
pytest tests/ --timeout=300

# Memory issues
pytest tests/ --maxfail=5
```

#### Report Issues

```bash
# Report generation failures
make clean
make test-smoke

# Allure report issues
allure generate reports/allure-results --clean
allure serve reports/allure-results
```

## Monitoring and Alerting

### Monitoring Metrics

1. **Execution Time**: Total test execution time
2. **Success Rate**: Test pass rate
3. **Failure Rate**: Test failure rate
4. **Resource Usage**: CPU, memory, network usage

### Alerting Mechanism

1. **Failure Alerts**: Send notifications when tests fail
2. **Performance Alerts**: Alert when execution time exceeds threshold
3. **Resource Alerts**: Alert when resource usage is abnormal
4. **Trend Alerts**: Alert on rising failure rate trends

### Monitoring Setup

```bash
# Set up monitoring
python scripts/setup_monitoring.py

# Start monitoring
python scripts/monitor_tests.py &

# Check monitoring status
python scripts/check_monitoring.py

# Generate monitoring report
python scripts/generate_monitoring_report.py
```

## Best Practices

### Local Development

1. **Use Makefile**: Simplify commands, improve efficiency
2. **Environment Check**: Check environment status before running
3. **Quick Feedback**: Use smoke tests for quick verification
4. **Resource Management**: Timely cleanup of unnecessary resources

### CI/CD Integration

1. **Layered Testing**: Execute tests by importance layers
2. **Parallel Execution**: Fully utilize parallel capabilities
3. **Report Integration**: Generate multiple format reports
4. **Failure Handling**: Gracefully handle failure situations

### Maintenance and Extension

1. **Modular Design**: Maintain script modularity
2. **Configuration Management**: Centralized configuration management
3. **Documentation Updates**: Timely update related documentation
4. **Version Control**: Use version control to manage scripts

## Advanced Features

### Custom Test Runners

```python
# scripts/custom_test_runner.py
import argparse
import subprocess
from core.utils.logger import Log

class CustomTestRunner:
    def __init__(self, config):
        self.config = config
    
    def run_tests(self, test_path, markers=None, parallel=None):
        """Run tests with custom configuration"""
        cmd = ["pytest", test_path]
        
        if markers:
            cmd.extend(["-m", markers])
        
        if parallel:
            cmd.extend(["--parallel", str(parallel)])
        
        Log.info(f"Running command: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        return result.returncode == 0
```

### Test Data Management

```python
# scripts/test_data_manager.py
from core.utils.file_utils import FileUtils

class TestDataManager:
    def __init__(self, data_dir):
        self.data_dir = data_dir
    
    def load_test_data(self, test_name):
        """Load test data for specific test"""
        data_file = f"{self.data_dir}/{test_name}.json"
        return FileUtils.read_json(data_file)
    
    def save_test_results(self, test_name, results):
        """Save test results"""
        results_file = f"{self.data_dir}/{test_name}_results.json"
        FileUtils.write_json(results_file, results)
```

### Performance Testing

```python
# scripts/performance_test_runner.py
import time
from core.utils.logger import Log

class PerformanceTestRunner:
    def __init__(self):
        self.start_time = None
        self.end_time = None
    
    def start_test(self):
        """Start performance test"""
        self.start_time = time.time()
        Log.info("Performance test started")
    
    def end_test(self):
        """End performance test"""
        self.end_time = time.time()
        duration = self.end_time - self.start_time
        Log.info(f"Performance test completed in {duration:.2f} seconds")
        return duration
```
