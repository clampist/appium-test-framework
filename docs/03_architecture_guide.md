# ATF Framework Architecture Guide

## Overview

This guide covers the design principles, system architecture, and implementation details of the ATF Framework. This information helps users understand how the framework works internally and how to extend it effectively.

## Design Principles

### 1. Layered Architecture

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

#### Layer Responsibilities

- **Core Layer (`core/`)**: Universal framework functionality, independent of specific business
- **API Layer (`api/`)**: HTTP client wrapper, supporting different backend systems
- **Test Layer (`tests/`)**: Test case writing, using core and API layer functionality

### 2. Configuration Management

The framework uses a hierarchical configuration management system:

```
config/
├── appium_config.yaml         # Appium configuration
├── device_config.yaml         # Device configuration
├── app_config.yaml           # Application configuration
└── settings.py               # Configuration management class
```

#### Configuration Hierarchy

1. **Environment Configuration**: Defines current environment and settings
2. **Platform Configuration**: Specific configuration for each platform
3. **Application Configuration**: Application-specific settings
4. **Dynamic Override**: Environment variables can override any setting

### 3. Test Classification

The framework separates tests into two categories:

- **Framework Demo Tests**: Demonstrate framework functionality, help developers learn
- **Business Case Tests**: Actual business scenario tests, validate business logic

## System Architecture

### Core Components

#### 1. Configuration Management (`core/config/`)

```python
# core/config/appium_config.py
@dataclass
class AppiumConfig:
    """Appium configuration class"""
    
    # Server configuration
    server_url: str = "http://localhost:4723"
    server_port: int = 4723
    
    # Session configuration
    timeout: int = 30
    implicit_wait: int = 10
    new_command_timeout: int = 3600
    
    # Platform configuration
    platform_name: str = "Android"
    platform_version: str = ""
    device_name: str = ""
    
    # Application configuration
    app_package: str = ""
    app_activity: str = ""
    app_path: str = ""
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Get Appium capabilities"""
        capabilities = {
            "platformName": self.platform_name,
            "appPackage": self.app_package,
            "appActivity": self.app_activity,
            "noReset": self.no_reset,
            "newCommandTimeout": self.new_command_timeout
        }
        return capabilities
```

#### 2. Core Framework (`core/`)

```python
# core/driver/appium_driver.py - Appium driver management
class AppiumDriver:
    """Appium driver management class"""
    
    def __init__(self, config: AppiumConfig):
        self.config = config
        self.driver = None
        self.wait = None
        self._session_id = None
    
    def start_driver(self) -> webdriver.Remote:
        """Start Appium driver"""
        capabilities = self.config.get_capabilities()
        self.driver = webdriver.Remote(
            command_executor=self.config.server_url,
            desired_capabilities=capabilities
        )
        return self.driver
    
    def find_element(self, by: str, value: str, timeout: Optional[int] = None):
        """Find element with explicit wait"""
        wait_time = timeout or self.config.timeout
        wait = WebDriverWait(self.driver, wait_time)
        return wait.until(EC.presence_of_element_located((by, value)))
```

#### 3. Page Object Pattern (`core/elements/`)

```python
# core/elements/page_object.py - Page object base class
class PageObject:
    """Page object base class"""
    
    def __init__(self, driver):
        self.driver = driver
        self.elements = {}
        self._init_elements()
    
    def _init_elements(self):
        """Initialize page elements, subclasses need to override this method"""
        pass
    
    def add_element(self, name: str, by: str, value: str, element_name: str = ""):
        """Add page element"""
        self.elements[name] = BaseElement(
            self.driver, by, value, element_name or name
        )
    
    def click_element(self, element_name: str, timeout: Optional[int] = None):
        """Click element"""
        element = self.get_element(element_name)
        element.click(timeout)
```

#### 4. Utility Classes (`core/utils/`)

```python
# core/utils/logger.py - Unified logging interface
class Log:
    """Static logger utility class"""
    
    _initialized = False
    
    @classmethod
    def info(cls, message: str, *args, **kwargs):
        """Log info message"""
        cls._ensure_initialized()
        logger.info(message, *args, **kwargs)
    
    @classmethod
    def error(cls, message: str, *args, **kwargs):
        """Log error message"""
        cls._ensure_initialized()
        logger.error(message, *args, **kwargs)
```

### API Layer Components

#### 1. API Client (`api/client/`)

```python
# api/client/api_client.py - RESTful API client
class ApiClient:
    """API client class"""
    
    def __init__(self, base_url: str, timeout: int = 30, headers: Optional[Dict[str, str]] = None):
        self.base_url = base_url
        self.timeout = timeout
        self.headers = headers or {}
        self.session = requests.Session()
    
    def get_test_cases(self, project_id: Optional[str] = None, status: Optional[str] = None) -> List[TestCase]:
        """Get test case list"""
        params = {}
        if project_id:
            params['project_id'] = project_id
        if status:
            params['status'] = status
        
        response = self._make_request('GET', '/test-cases', params=params)
        return [TestCase.from_dict(item) for item in response.json()]
```

#### 2. API Server (`api/server/`)

```python
# api/server/api_server.py - Flask-based API service
class ApiServer:
    """API server class"""
    
    def __init__(self, host: str = "0.0.0.0", port: int = 5000, debug: bool = False):
        self.host = host
        self.port = port
        self.debug = debug
        self.app = Flask(__name__)
        self._register_routes()
    
    def _register_routes(self):
        """Register API routes"""
        
        @self.app.route('/health', methods=['GET'])
        def health_check():
            return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})
        
        @self.app.route('/test-cases', methods=['GET'])
        def get_test_cases():
            project_id = request.args.get('project_id')
            status = request.args.get('status')
            test_cases = self._get_mock_test_cases(project_id, status)
            return jsonify([tc.to_dict() for tc in test_cases])
```

## Data Models

### 1. Test Case Model (`api/models/test_case.py`)

```python
# api/models/test_case.py - Test case data model
@dataclass
class TestCase:
    """Test case data model"""
    
    # Basic information
    id: str = ""
    name: str = ""
    description: str = ""
    project_id: str = ""
    
    # Status and priority
    status: str = "active"  # active, inactive, deprecated
    priority: str = "medium"  # low, medium, high, critical
    
    # Category and tags
    category: str = ""
    tags: List[str] = field(default_factory=list)
    
    # Test steps
    steps: List[Dict[str, Any]] = field(default_factory=list)
    
    # Preconditions and postconditions
    preconditions: List[str] = field(default_factory=list)
    postconditions: List[str] = field(default_factory=list)
    
    # Automation related
    is_automated: bool = False
    script_path: str = ""
    framework: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "project_id": self.project_id,
            "status": self.status,
            "priority": self.priority,
            "category": self.category,
            "tags": self.tags,
            "steps": self.steps,
            "preconditions": self.preconditions,
            "postconditions": self.postconditions,
            "is_automated": self.is_automated,
            "script_path": self.script_path,
            "framework": self.framework
        }
```

### 2. Test Result Model (`api/models/test_result.py`)

```python
# api/models/test_result.py - Test result data model
@dataclass
class TestResult:
    """Test result data model"""
    
    # Basic information
    id: str = ""
    test_case_id: str = ""
    test_name: str = ""
    description: str = ""
    
    # Execution result
    status: str = "pending"  # pending, running, passed, failed, skipped, blocked
    execution_time: float = 0.0  # Execution time (seconds)
    
    # Error information
    error_message: str = ""
    error_type: str = ""
    stack_trace: str = ""
    
    # Screenshots and logs
    screenshot_path: str = ""
    log_path: str = ""
    video_path: str = ""
    
    # Environment information
    device_info: Dict[str, Any] = field(default_factory=dict)
    app_info: Dict[str, Any] = field(default_factory=dict)
    platform_info: Dict[str, Any] = field(default_factory=dict)
    
    def is_passed(self) -> bool:
        """Check if passed"""
        return self.status == "passed"
    
    def is_failed(self) -> bool:
        """Check if failed"""
        return self.status == "failed"
```

## Extension Points

### 1. Adding New Configuration Classes

```python
# core/config/custom_config.py
@dataclass
class CustomConfig:
    """Custom configuration class"""
    
    # Configuration fields
    field1: str = ""
    field2: int = 0
    field3: bool = False
    
    def validate(self) -> bool:
        """Validate configuration"""
        if not self.field1:
            return False
        if self.field2 < 0:
            return False
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "field1": self.field1,
            "field2": self.field2,
            "field3": self.field3
        }
```

### 2. Adding New Utility Classes

```python
# core/utils/custom_utils.py
class CustomUtils:
    """Custom utility class"""
    
    @staticmethod
    def custom_function(param1: str, param2: int) -> str:
        """Custom utility function"""
        return f"{param1}_{param2}"
    
    @staticmethod
    def validate_input(data: Dict[str, Any]) -> bool:
        """Validate input data"""
        required_fields = ["field1", "field2"]
        return all(field in data for field in required_fields)
```

### 3. Adding New Page Objects

```python
# tests/business/pages/custom_page.py
from core.elements.page_object import PageObject

class CustomPage(PageObject):
    """Custom page object"""
    
    def _init_elements(self):
        """Initialize page elements"""
        self.add_element("custom_button", "id", "custom_button", "Custom Button")
        self.add_element("custom_input", "id", "custom_input", "Custom Input")
    
    def perform_custom_action(self, text: str):
        """Perform custom action"""
        self.input_text("custom_input", text)
        self.click_element("custom_button")
```

## Best Practices

### 1. Configuration Management

- Use dataclasses for type safety
- Implement validation methods
- Support environment variable override
- Provide default values

### 2. Error Handling

- Use try-catch blocks for critical operations
- Log detailed error information
- Provide meaningful error messages
- Implement graceful degradation

### 3. Resource Management

- Ensure proper cleanup in finally blocks
- Use context managers where appropriate
- Implement proper driver lifecycle management
- Handle session cleanup

### 4. Testing Strategy

- Separate framework tests from business tests
- Use meaningful test names
- Implement proper setup and teardown
- Use test markers for organization

### 5. Documentation

- Document all public APIs
- Provide usage examples
- Keep documentation up to date
- Use consistent formatting

## Performance Considerations

### 1. Driver Management

- Reuse driver instances when possible
- Implement proper session cleanup
- Use connection pooling for API calls
- Optimize element location strategies

### 2. Memory Management

- Release resources promptly
- Avoid memory leaks in long-running tests
- Use generators for large data sets
- Implement proper cleanup in teardown

### 3. Parallel Execution

- Design for parallel execution
- Avoid shared state between tests
- Use thread-safe utilities
- Implement proper resource isolation

## Security Considerations

### 1. Configuration Security

- Never hardcode sensitive information
- Use environment variables for secrets
- Implement proper access controls
- Validate all input data

### 2. API Security

- Use HTTPS for API communications
- Implement proper authentication
- Validate API responses
- Handle sensitive data appropriately

### 3. Test Data Security

- Use test data, not production data
- Implement proper data cleanup
- Avoid logging sensitive information
- Use secure storage for test artifacts

## Future Extensions

### 1. Platform Support

- iOS platform support
- Web platform support
- Cross-platform testing
- Cloud device farm integration

### 2. Advanced Features

- Visual testing capabilities
- Performance testing integration
- API testing integration
- Database testing support

### 3. CI/CD Integration

- Jenkins pipeline support
- GitHub Actions integration
- Azure DevOps integration
- GitLab CI integration

### 4. Reporting Enhancements

- Custom report formats
- Real-time reporting
- Trend analysis
- Integration with external tools
