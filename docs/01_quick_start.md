# ATF Framework Quick Start Guide

## Overview

ATF (Appium Test Framework) is a Python testing framework based on Appium, specifically designed for mobile automation testing. This guide will help you get started quickly.

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Appium Server
- Android SDK (Android testing)
- Xcode (iOS testing)
- pyenv (recommended)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd atf

# Set up Python environment
pyenv activate atf
pip install -r requirements.txt

# Verify installation
python -c "import pytest, appium; print('Dependencies installed successfully')"
```

### Basic Usage

```python
from core.driver.appium_driver import AppiumDriver
from core.config.appium_config import AppiumConfig

# Create configuration
config = AppiumConfig(
    server_url="http://localhost:4723",
    platform_name="Android",
    app_package="com.example.app"
)

# Create driver
driver = AppiumDriver(config)
driver.start_driver()

# Execute test operations
# ...

# Close driver
driver.quit_driver()
```

### Running Tests

```bash
# Run all tests
python run_tests.py

# Run specific business path tests
python run_tests.py --test-path tests/com.honda.roadsync.duo/

# Run tests with markers
python run_tests.py --markers smoke regression

# Parallel test execution
python run_tests.py --parallel 4
```

### Using pytest Directly

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/com.honda.roadsync.duo/test_login.py

# Generate HTML report
pytest --html=reports/report.html tests/
```

## Writing Your First Test

### Page Object Pattern

```python
from core.elements.page_object import PageObject
from core.utils.logger import Log

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
        Log.info(f"Logging in with username: {username}")
        self.input_text("username_input", username)
        self.input_text("password_input", password)
        self.click_element("login_button")
```

### Test Case Example

```python
import pytest
from core.utils.logger import Log
from pages.login_page import LoginPage

class TestLogin:
    def test_successful_login(self, driver):
        """Test successful login flow"""
        Log.info("Starting login test")
        
        # Create page object
        login_page = LoginPage(driver)
        
        # Perform login
        login_page.login("testuser", "password")
        
        # Verify login success
        assert driver.get_current_activity() == ".MainActivity"
        
        Log.info("Login test completed successfully")
```

## Configuration Management

### Basic Configuration

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

### Environment-Specific Configuration

```python
from core.config.appium_config import AppiumConfig

# Load configuration
config = AppiumConfig.from_dict({
    "server_url": "http://localhost:4723",
    "platform_name": "Android",
    "app_package": "com.example.app"
})

# Validate configuration
if not config.validate():
    raise ValueError("Invalid configuration")
```

## Project Structure

```
atf/
├── core/                           # Core logic layer
│   ├── driver/                     # Appium driver management
│   ├── elements/                   # Element location and operations
│   ├── utils/                      # Utility classes
│   └── config/                     # Configuration management
├── api/                            # API interface layer
├── tests/                          # Test case layer
│   ├── com.honda.roadsync.duo/     # Business path 1
│   ├── com.honda.ms.dm.sab/        # Business path 2
│   └── common/                     # Common tests
├── examples/                       # Example code
├── config/                         # Configuration files
└── scripts/                        # Test runner scripts
```

## Next Steps

1. **Read the User Guide**: For detailed configuration and usage instructions
2. **Explore Architecture**: Understand the framework design principles
3. **Check Examples**: Review example code in the `examples/` directory
4. **Run Tests**: Try running existing test cases
5. **Write Your Own**: Create your first test case following the patterns shown

## Common Commands

```bash
# Environment setup
make install    # Install dependencies
make setup      # Setup environment

# Test running
make test-smoke     # Run smoke tests
make test-daily     # Run daily tests
make test-regression # Run regression tests

# Environment management
make check-env      # Check environment
make start-appium   # Start Appium server
make stop-appium    # Stop Appium server

# Cleanup
make clean          # Clean reports and logs
```

## Getting Help

- **Documentation**: Check the other guides in this docs directory
- **Examples**: Review code in the `examples/` directory
- **Issues**: Check the troubleshooting guide for common problems
- **Logs**: Check the `logs/` directory for detailed execution logs
