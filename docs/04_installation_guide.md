# ATF Framework Installation Guide

## Overview

This guide provides comprehensive installation instructions for the ATF Framework, covering all supported platforms and installation scenarios.

## Prerequisites

### System Requirements

- **Operating System**: Linux, macOS, or Windows
- **Python**: 3.8 or higher
- **Appium Server**: 2.0 or higher
- **Android SDK**: For Android testing (optional but recommended)
- **Xcode**: For iOS testing (macOS only)
- **Git**: For cloning the repository
- **Memory**: Minimum 4GB RAM (8GB recommended)
- **Disk Space**: Minimum 2GB free space

### Python Environment

The framework requires Python 3.8 or higher. We recommend using pyenv for environment management:

```bash
# Check Python version
python --version

# Create virtual environment (using venv)
python -m venv atf_env
source atf_env/bin/activate  # Linux/macOS
# or
atf_env\Scripts\activate     # Windows

# Or using pyenv (recommended)
pyenv install 3.12.11
pyenv virtualenv 3.12.11 atf
pyenv activate atf
```

## Installation Methods

### Method 1: Standard Installation (Recommended)

#### 1. Clone the Repository

```bash
# Clone the repository
git clone <repository-url>
cd atf

# Or download and extract if you have the source code
```

#### 2. Install Python Dependencies

```bash
# Activate your Python environment
pyenv activate atf  # or your preferred method

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import pytest, appium, selenium; print('Dependencies installed successfully')"
```

#### 3. Set Up Appium Server

```bash
# Install Appium globally
npm install -g appium

# Install Appium Doctor for environment verification
npm install -g appium-doctor

# Verify Appium installation
appium --version

# Check environment setup
appium-doctor
```

#### 4. Set Up Android Environment (Optional)

```bash
# Install Android SDK
# Download from: https://developer.android.com/studio

# Set environment variables
export ANDROID_HOME=/path/to/android/sdk
export PATH=$PATH:$ANDROID_HOME/tools
export PATH=$PATH:$ANDROID_HOME/platform-tools

# Verify Android setup
adb devices
```

#### 5. Set Up iOS Environment (macOS only)

```bash
# Install Xcode from App Store
# Install Xcode Command Line Tools
xcode-select --install

# Install iOS Simulator
xcrun simctl list devices

# Verify iOS setup
xcrun simctl boot "iPhone 14"
```

#### 6. Verify Installation

```bash
# Validate configuration files
python -c "from core.config.appium_config import AppiumConfig; print('Configuration loaded successfully')"

# Run a simple test
python -m pytest tests/common/ -v

# Check environment
make check-env
```

### Method 2: Docker Installation

#### 1. Install Docker

```bash
# Install Docker Desktop
# Download from: https://www.docker.com/products/docker-desktop

# Verify Docker installation
docker --version
docker-compose --version
```

#### 2. Use Docker Compose

```bash
# Create docker-compose.yml
cat > docker-compose.yml << EOF
version: '3.8'
services:
  appium:
    image: appium/appium:latest
    ports:
      - "4723:4723"
    environment:
      - APPIUM_HOST=0.0.0.0
      - APPIUM_PORT=4723
    volumes:
      - /dev/bus/usb:/dev/bus/usb
    privileged: true
EOF

# Start Appium server
docker-compose up -d
```

### Method 3: CI/CD Environment Installation

#### 1. GitHub Actions Setup

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
        python -m pytest tests/ -v
```

#### 2. Jenkins Pipeline Setup

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.12'
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
                    python -m pytest tests/ -v
                '''
            }
        }
    }
}
```

## Configuration Setup

### 1. Environment Configuration

```bash
# Set environment variables
export ATF_ENV=local
export APPIUM_SERVER_URL=http://localhost:4723
export APPIUM_PLATFORM_NAME=Android
export APPIUM_APP_PACKAGE=com.example.app
export APPIUM_DEVICE_ID=emulator-5554
```

### 2. Configuration Files

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

### 3. Pyenv Environment Setup

```bash
# Create pyenv environment
pyenv install 3.12.11
pyenv virtualenv 3.12.11 atf
pyenv activate atf

# Install dependencies
pip install -r requirements.txt

# Set local Python version
pyenv local atf
```

## Verification Steps

### 1. Environment Check

```bash
# Check Python environment
python --version
pip list

# Check Appium installation
appium --version
appium-doctor

# Check Android environment
adb devices
adb version

# Check iOS environment (macOS only)
xcrun simctl list devices
```

### 2. Framework Verification

```bash
# Test framework imports
python -c "
from core.driver.appium_driver import AppiumDriver
from core.config.appium_config import AppiumConfig
from core.utils.logger import Log
print('Framework imports successful')
"

# Run basic tests
python -m pytest tests/common/ -v

# Check configuration
python -c "
from core.config.appium_config import AppiumConfig
config = AppiumConfig()
print('Configuration loaded:', config.server_url)
"
```

### 3. Device Connection Test

```bash
# List connected devices
adb devices

# Test device communication
adb shell getprop ro.build.version.release

# Test Appium connection
curl http://localhost:4723/status
```

## Troubleshooting

### Common Installation Issues

#### 1. Python Environment Issues

```bash
# Problem: Python version mismatch
# Solution: Use pyenv to manage Python versions
pyenv install 3.12.11
pyenv global 3.12.11

# Problem: Virtual environment not activated
# Solution: Activate the environment
pyenv activate atf
# or
source atf_env/bin/activate
```

#### 2. Appium Installation Issues

```bash
# Problem: Appium not found
# Solution: Install globally
npm install -g appium

# Problem: Appium Doctor shows issues
# Solution: Follow the recommendations
appium-doctor --android
appium-doctor --ios
```

#### 3. Android Environment Issues

```bash
# Problem: ADB not found
# Solution: Add to PATH
export ANDROID_HOME=/path/to/android/sdk
export PATH=$PATH:$ANDROID_HOME/platform-tools

# Problem: No devices found
# Solution: Enable USB debugging
# Settings > Developer options > USB debugging
```

#### 4. iOS Environment Issues (macOS)

```bash
# Problem: Xcode not found
# Solution: Install Xcode from App Store

# Problem: Command line tools not found
# Solution: Install command line tools
xcode-select --install

# Problem: Simulator not available
# Solution: Install simulator
xcrun simctl install booted com.apple.CoreSimulator.SimRuntime.iOS-16-0
```

### Environment-Specific Issues

#### Linux Issues

```bash
# Problem: Permission denied
# Solution: Use sudo or fix permissions
sudo npm install -g appium

# Problem: USB device access
# Solution: Add udev rules
echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="[vendor_id]", MODE="0666"' | sudo tee /etc/udev/rules.d/51-android.rules
```

#### Windows Issues

```bash
# Problem: Path issues
# Solution: Add to system PATH
# Control Panel > System > Environment Variables

# Problem: PowerShell execution policy
# Solution: Allow script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### macOS Issues

```bash
# Problem: Gatekeeper blocking
# Solution: Allow from identified developer
# System Preferences > Security & Privacy

# Problem: Homebrew conflicts
# Solution: Use pyenv instead of Homebrew Python
brew uninstall python
pyenv install 3.12.11
```

## Post-Installation Setup

### 1. IDE Configuration

#### VS Code Setup

```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": [
        "tests"
    ],
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true
}
```

#### PyCharm Setup

1. Open project in PyCharm
2. Go to File > Settings > Project > Python Interpreter
3. Add interpreter: Select pyenv environment
4. Configure pytest: Settings > Tools > Python Integrated Tools

### 2. Git Configuration

```bash
# Set up git hooks
cp scripts/pre-commit .git/hooks/
chmod +x .git/hooks/pre-commit

# Configure git ignore
echo "*.pyc" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "logs/" >> .gitignore
echo "reports/" >> .gitignore
```

### 3. Development Tools

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Set up linting
pip install black flake8 mypy
```

## Next Steps

After successful installation:

1. **Read the Quick Start Guide**: Get familiar with basic usage
2. **Explore Examples**: Review example code in the `examples/` directory
3. **Run Sample Tests**: Execute existing test cases
4. **Configure Your Environment**: Set up your specific test environment
5. **Write Your First Test**: Create a simple test case
6. **Join the Community**: Connect with other users and contributors

## Support

If you encounter issues during installation:

1. **Check the Troubleshooting Guide**: Common solutions to installation problems
2. **Review Logs**: Check installation logs for detailed error information
3. **Verify Prerequisites**: Ensure all system requirements are met
4. **Search Issues**: Look for similar issues in the project repository
5. **Ask for Help**: Create an issue with detailed information about your problem
