# ATF - Appium Test Framework

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Appium](https://img.shields.io/badge/Appium-2.0+-green.svg)](http://appium.io/)
[![Pytest](https://img.shields.io/badge/Pytest-6.2+-orange.svg)](https://docs.pytest.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Documentation](https://img.shields.io/badge/Documentation-8%20Guides-brightgreen.svg)](docs/)

A modern, pytest-based mobile automation testing framework built on Appium. Features layered architecture design, flexible configuration management, comprehensive logging, screenshot management, and cross-platform support for Android and iOS applications.

## ✨ Key Features

- 🏗️ **Layered Architecture**: Clear separation of concerns with core, API, and test layers
- 🔧 **Flexible Configuration**: Dataclass-based configuration supporting multiple platforms and environments
- 📊 **Comprehensive Logging**: Unified logging interface with automatic caller information
- 📱 **Screenshot Management**: Automatic screenshot capture, comparison, and baseline management
- ⚡ **Parallel Testing**: Built-in support for parallel test execution
- 📈 **Rich Reporting**: HTML, JUnit XML, and Allure reports
- 🎯 **Page Object Pattern**: Robust page object implementation for maintainable tests
- 🛠️ **Command Line Interface**: Easy-to-use Makefile commands for test execution
- 🔄 **Cross-Platform Support**: Android and iOS testing capabilities
- 🗄️ **API Integration**: RESTful API client and server for test data management

## 🎬 Demo

Watch ATF Framework in action with our TikTok app automation demo:

![TikTok Appium Demo](https://github.com/your-repo/raw/main/demo/tiktok-appium-example.gif)

*This demo showcases automated testing of TikTok app features including video browsing, user interactions, and content discovery using the ATF Framework.*

## 📚 Documentation

- **[Quick Start Guide](docs/01_quick_start.md)** - Get up and running in minutes
- **[User Guide](docs/02_user_guide.md)** - Comprehensive usage instructions
- **[Architecture Guide](docs/03_architecture_guide.md)** - Design principles and system architecture
- **[Installation Guide](docs/04_installation_guide.md)** - Detailed installation instructions
- **[Test Running Guide](docs/05_test_running_guide.md)** - Test execution and best practices
- **[Migration Guide](docs/06_migration_guide.md)** - Migrating existing tests to ATF
- **[Troubleshooting Guide](docs/07_troubleshooting_guide.md)** - Common issues and solutions
- **[Reporting Guide](docs/08_reporting_guide.md)** - Test reporting and Allure integration

## 🏗️ Architecture

### Layered Architecture Design

The ATF Framework follows a clear layered architecture design:

```
┌─────────────────────────────────────────────────────────────┐
│                    Test Layer (tests/)                      │
│  ┌─────────────────────────────────────────────────────┐   │
│  │           API Interface Layer (api/)                │   │
│  │  ┌─────────────────────────────────────────────┐   │   │
│  │  │         Core Framework Layer                │   │   │
│  │  │              (core/)                        │   │   │
│  │  └─────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Layer Responsibilities

- **Core Layer (`core/`)**: Universal framework functionality, driver management, element operations, utilities
- **API Layer (`api/`)**: HTTP client wrapper, test data management, and API server functionality
- **Test Layer (`tests/`)**: Test case writing using core and API layer functionality

### Project Structure

```
atf/
├── core/                    # Core framework layer
│   ├── driver/             # Appium driver management
│   │   └── appium_driver.py # Appium driver wrapper
│   ├── elements/           # Element location and operations
│   │   ├── base_element.py # Base element class
│   │   └── page_object.py  # Page object pattern
│   ├── utils/              # Utility classes
│   │   ├── logger.py       # Unified logging interface
│   │   ├── file_utils.py   # File operations
│   │   ├── time_utils.py   # Time utilities
│   │   └── screenshot_utils.py # Screenshot management
│   └── config/             # Configuration management
│       ├── appium_config.py # Appium configuration
│       ├── device_config.py # Device configuration
│       └── app_config.py   # Application configuration
├── api/                    # API interface layer
│   ├── client/             # API client
│   │   └── api_client.py   # RESTful API client
│   ├── server/             # API server
│   │   └── api_server.py   # Flask-based API server
│   └── models/             # Data models
│       ├── test_case.py    # Test case model
│       └── test_result.py  # Test result model
├── tests/                  # Test case layer
│   ├── com.honda.roadsync.duo/    # Business path 1
│   ├── com.honda.ms.dm.sab/       # Business path 2
│   ├── com.monoxer/               # Business path 3
│   ├── jp.co.matsukiyococokara.app/ # Business path 4
│   └── common/                    # Common tests
├── examples/               # Example code
│   └── basic_usage.py      # Basic usage examples
├── config/                 # Configuration files
│   └── appium_config.yaml  # Appium configuration
├── scripts/                # Utility scripts
│   ├── run_business_tests.py # Universal test runner
│   └── manage_screenshots.py # Screenshot management
├── docs/                   # Documentation
├── logs/                   # Log files
├── reports/                # Test reports
├── screenshots/            # Screenshot storage
├── requirements.txt        # Dependencies
├── setup.py               # Installation configuration
├── pytest.ini            # Pytest configuration
├── run_tests.py           # Test runner script
├── Makefile               # Build and test commands
└── README.md              # Project documentation
```

### Data Flow Architecture

#### Test Execution Flow
```
Test Case → Page Object → Element Operations → Appium Driver → Mobile Device
    ↓            ↓              ↓                ↓              ↓
  Logging → Page Logging → Element Logging → Driver Logging → Device Response
```

#### Configuration Flow
```
Environment Variables → Config Manager → Appium Config → Device Config → App Config
        ↓                    ↓              ↓            ↓              ↓
    Override Values → Merged Configuration → Driver Setup → Session Creation
```

#### Screenshot Management Flow
```
Test Execution → Screenshot Utils → Save Screenshot → Compare with Baseline → Generate Report
      ↓              ↓                ↓                ↓                    ↓
   Test Step → Screenshot Capture → File Storage → Image Comparison → Report Integration
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Appium Server 2.0+
- Android SDK (for Android testing)
- Xcode (for iOS testing, macOS only)
- pyenv (recommended)

### Quick Installation

```bash
# Clone the repository
git clone <repository-url>
cd atf

# Set up Python environment
pyenv activate atf
pip install -r requirements.txt

# Verify installation
python -c "from core.driver.appium_driver import AppiumDriver; print('ATF installed successfully')"
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

# Create and start driver
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
pytest tests/

# Run specific business path tests
pytest tests/com.monoxer/

# Run tests with markers
pytest tests/ -m smoke

# Generate HTML report
pytest tests/ --html=reports/report.html

# Parallel execution
pytest tests/ --parallel=4
```

### Using Makefile Commands

```bash
# View all available commands
make help

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

## 📱 Supported Platforms

### Android
- **Platform**: Android 8.0+
- **Automation**: UiAutomator2
- **Devices**: Physical devices and emulators
- **Features**: Native apps, hybrid apps, web apps

### iOS
- **Platform**: iOS 12.0+
- **Automation**: XCUITest
- **Devices**: Physical devices and simulators
- **Features**: Native apps, hybrid apps, web apps

## 🔧 Configuration

### Appium Configuration

```python
from core.config.appium_config import AppiumConfig

config = AppiumConfig(
    server_url="http://localhost:4723",
    platform_name="Android",
    app_package="com.example.app",
    app_activity=".MainActivity",
    device_id="emulator-5554",
    no_reset=True,
    new_command_timeout=3600
)
```

### Environment Variables

```bash
export APPIUM_SERVER_URL=http://localhost:4723
export APPIUM_PLATFORM_NAME=Android
export APPIUM_APP_PACKAGE=com.example.app
export APPIUM_DEVICE_ID=emulator-5554
```

## 📊 Reporting

### HTML Reports
```bash
pytest tests/ --html=reports/report.html --self-contained-html
```

### JUnit XML Reports
```bash
pytest tests/ --junitxml=reports/junit.xml
```

### Allure Reports
```bash
pytest tests/ --alluredir=reports/allure-results
allure serve reports/allure-results
```

## 🛠️ Development

### Project Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Set up pre-commit hooks
pre-commit install

# Run linting
black core/ tests/
flake8 core/ tests/
mypy core/ tests/
```

### Running Examples

```bash
# Run basic usage example
python examples/basic_usage.py

# Run Cocokara example
python examples/cocokara_usage.py
```

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the project
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

### Development Guidelines

- Follow the existing code style and patterns
- Add comprehensive tests for new features
- Update documentation for any changes
- Ensure all tests pass before submitting

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check our comprehensive [documentation](docs/)
- **Issues**: Report bugs and request features via [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: Join our [GitHub Discussions](https://github.com/your-repo/discussions)
- **Examples**: Review example code in the `examples/` directory

## 🏆 Success Stories

- **Honda RoadSync**: Comprehensive mobile app testing for Honda's connected vehicle platform
- **Monoxer**: Japanese language learning app automation with complex UI interactions
- **Cocokara**: Daily challenge app testing with popup handling and result verification

---

**ATF Framework** - Mobile Automation Testing Made Simple 📱🚀
