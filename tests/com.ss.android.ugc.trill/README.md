# TikTok App Test Suite

TikTok App automated test suite for `com.ss.android.ugc.trill/com.ss.android.ugc.aweme.splash.SplashActivity`

## Overview

This test suite provides comprehensive automated testing for TikTok App core features including:

- App launch and navigation
- Video interaction features (like, comment, share, bookmark)
- Video navigation (swipe up/down)
- Advanced video features (double tap, long press)
- Search functionality
- Profile page features
- App permission handling

## Test Structure

```
tests/com.ss.android.ugc.trill/
├── __init__.py                 # Package initialization
├── conftest.py                 # Pytest configuration and fixtures
├── test_tiktok_features.py     # Main test cases
├── datas/
│   ├── __init__.py
│   └── test_data.py           # Test data definitions (EN/CN)
├── configs/
│   ├── __init__.py
│   └── config_manager.py      # Appium configuration
├── pages/
│   ├── __init__.py
│   ├── main_page.py           # Navigation and permissions
│   ├── search_page.py         # Search functionality
│   ├── profile_page.py        # Profile management
│   └── video_page.py          # Video operations and interactions
└── README.md                  # This file
```

## Features Tested

### 1. App Launch and Navigation
- App activation and initialization
- Navigation between tabs (Home, Friends, Create, Inbox, Profile)
- Permission dialog handling

### 2. Video Interaction Features
- Like button functionality
- Comment button and comment section
- Share button and share dialog
- Bookmark button functionality

### 3. Video Navigation
- Swipe up to next video
- Swipe down to previous video
- Video loading verification

### 4. Advanced Video Features
- Double tap to like
- Long press for additional options
- Video status checking
- Video duration and mute status

### 5. Search Functionality
- Search bar interaction
- Keyword search
- Search results navigation
- Trending tab access

### 6. Profile Page Features
- Profile page loading
- Username display
- Profile avatar interaction
- Navigation back to main page

### 7. App Permissions
- Permission dialog handling
- Camera and storage permissions
- Permission flow testing

## Language Support

The test suite supports both English and Chinese languages:

- **English**: Default language for testing
- **Chinese**: Use `--language zh` parameter

## Running Tests

### Prerequisites

1. Ensure Appium server is running
2. Android device/emulator is connected
3. TikTok app is installed on the device
4. Python environment is activated

### Basic Test Execution

```bash
# Run all TikTok tests
pytest tests/com.ss.android.ugc.trill/ -v

# Run with English language (default)
pytest tests/com.ss.android.ugc.trill/ --language=en -v

# Run with Chinese language
pytest tests/com.ss.android.ugc.trill/ --language=zh -v
```

### Running Specific Tests

```bash
# Run specific test class
pytest tests/com.ss.android.ugc.trill/test_tiktok_features.py::TestTikTokFeatures -v

# Run specific test method
pytest tests/com.ss.android.ugc.trill/test_tiktok_features.py::TestTikTokFeatures::test_app_launch_and_navigation -v

# Run tests with specific marker
pytest tests/com.ss.android.ugc.trill/ -m tiktok -v
```

### Test Execution with Allure Reports

```bash
# Run tests with Allure reporting
pytest tests/com.ss.android.ugc.trill/ --alluredir=reports/allure-results -v

# Generate Allure report
allure serve reports/allure-results
```

## Configuration

### Appium Configuration

The test suite uses the following Appium capabilities:

```python
{
    "platformName": "Android",
    "automationName": "UiAutomator2",
    "appPackage": "com.ss.android.ugc.trill",
    "appActivity": "com.ss.android.ugc.aweme.splash.SplashActivity",
    "noReset": True,
    "autoGrantPermissions": True,
    "newCommandTimeout": 300,
    "systemPort": 8200
}
```

### Language-Specific Settings

- **English**: `locale: "en_US", language: "en"`
- **Chinese**: `locale: "zh_CN", language: "zh"`

## Page Objects

### MainPage - Navigation and Permissions
- **Navigation**: Tab switching (Home, Friends, Create, Inbox, Profile)
- **Permissions**: System permission dialog handling
- **App Management**: App activation and initialization

### SearchPage - Search Functionality
- **Search Interface**: Search bar interaction and keyword input
- **Search Execution**: Search button and results navigation
- **Trending**: Trending tab access and content browsing
- **Navigation**: Back button and return to main page

### ProfilePage - Profile Management
- **Profile Display**: Profile page loading and verification
- **User Information**: Username retrieval and display
- **Profile Interaction**: Avatar clicking and settings access
- **Navigation**: Back button and return to main page

### VideoPage - Video Operations and Interactions
- **Video Controls**: Like, comment, share, bookmark buttons
- **Video Navigation**: Swipe gestures for video switching
- **Advanced Features**: Double tap to like, long press options
- **Video Status**: Loading verification and playing status
- **Page Management**: Close and back button operations

## Test Data

### Base Test Data
- App package and activity
- Common element locators
- Wait time configurations
- Common test data

### Language-Specific Data
- **English**: English UI text and keywords
- **Chinese**: Chinese UI text and keywords

## Screenshot Management

The test suite includes comprehensive screenshot management:

- Automatic screenshot capture at key test steps
- Screenshot comparison with baseline images
- Failure screenshot capture
- Screenshot organization by feature and step

## Error Handling

- Comprehensive exception handling in page objects
- Automatic failure artifact capture (screenshots, page source)
- Graceful app termination in test teardown
- Permission dialog handling

## Best Practices

1. **Single Responsibility Principle**: Each page object has a clear, focused responsibility
2. **Page Object Model**: All UI interactions are encapsulated in appropriate page objects
3. **Data-Driven Testing**: Test data is separated from test logic
4. **Language Support**: Multi-language support for international testing
5. **Screenshot Management**: Automatic screenshot capture and comparison
6. **Error Handling**: Comprehensive error handling and recovery
7. **Test Isolation**: Each test is independent and cleans up after itself
8. **Logging**: Detailed logging for debugging and monitoring

## Architecture Benefits

### After Refactoring
- **Clear Separation of Concerns**: Each page object has a single, well-defined responsibility
- **No Code Duplication**: Video operations are centralized in VideoPage
- **Easier Maintenance**: Changes to video functionality only require updates to VideoPage
- **Better Test Organization**: Tests use the appropriate page object for each operation
- **Improved Readability**: Test code clearly shows which page object is responsible for each action

### Before Refactoring
- **Code Duplication**: Video interaction methods existed in both MainPage and VideoPage
- **Unclear Responsibilities**: Both classes handled video operations
- **Maintenance Overhead**: Changes required updates in multiple places
- **Confusion**: Tests could use either class for the same functionality

## Troubleshooting

### Common Issues

1. **Element Not Found**: Check if element IDs have changed in app updates
2. **Permission Dialogs**: Ensure `autoGrantPermissions` is set to `true`
3. **Video Loading**: Increase wait times for slow network conditions
4. **Language Issues**: Verify language-specific locators match current app version

### Debug Mode

```bash
# Run with debug logging
pytest tests/com.ss.android.ugc.trill/ -v --log-cli-level=DEBUG
```

## Maintenance

### Updating Element Locators

When the app is updated, element locators may change. Update the following files:

1. `datas/test_data.py` - Update element IDs and text selectors
2. `pages/*.py` - Update page object methods if needed
3. `configs/config_manager.py` - Update app package/activity if needed

### Adding New Tests

1. Add new test methods to `TestTikTokFeatures` class
2. Create new page objects if needed
3. Update test data with new locators
4. Add appropriate screenshots and assertions

### Adding New Video Features

1. Add new methods to `VideoPage` class
2. Update test data with new element locators
3. Create corresponding test methods
4. Update documentation

## Contributing

When contributing to this test suite:

1. Follow the existing code structure and naming conventions
2. Maintain single responsibility principle for page objects
3. Add comprehensive error handling
4. Include appropriate screenshots and logging
5. Update documentation for new features
6. Ensure tests are language-agnostic or include language support
7. Use the appropriate page object for each operation type

