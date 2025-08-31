"""
Test Result Model
Test result data model
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

from core.utils.logger import Log


@dataclass
class TestResult:
    """Test result data model"""
    
    # Basic information
    id: str = ""
    test_case_id: str = ""
    test_run_id: str = ""
    
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
    
    # Execution environment
    executed_by: str = ""
    executed_on: str = ""
    environment: str = ""
    
    # Time information
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    
    # Other information
    additional_data: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Post-initialization processing"""
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary
        
        Returns:
            Dict[str, Any]: Dictionary representation
        """
        return {
            'id': self.id,
            'test_case_id': self.test_case_id,
            'test_run_id': self.test_run_id,
            'status': self.status,
            'execution_time': self.execution_time,
            'error_message': self.error_message,
            'error_type': self.error_type,
            'stack_trace': self.stack_trace,
            'screenshot_path': self.screenshot_path,
            'log_path': self.log_path,
            'video_path': self.video_path,
            'device_info': self.device_info,
            'app_info': self.app_info,
            'platform_info': self.platform_info,
            'executed_by': self.executed_by,
            'executed_on': self.executed_on,
            'environment': self.environment,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'finished_at': self.finished_at.isoformat() if self.finished_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'additional_data': self.additional_data,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TestResult':
        """
        Create object from dictionary
        
        Args:
            data: Dictionary data
            
        Returns:
            TestResult: Test result object
        """
        # Handle time fields
        started_at = None
        if data.get('started_at'):
            try:
                started_at = datetime.fromisoformat(data['started_at'])
            except ValueError:
                Log.warning(f"Invalid started_at format: {data['started_at']}")
        
        finished_at = None
        if data.get('finished_at'):
            try:
                finished_at = datetime.fromisoformat(data['finished_at'])
            except ValueError:
                Log.warning(f"Invalid finished_at format: {data['finished_at']}")
        
        created_at = None
        if data.get('created_at'):
            try:
                created_at = datetime.fromisoformat(data['created_at'])
            except ValueError:
                Log.warning(f"Invalid created_at format: {data['created_at']}")
        
        return cls(
            id=data.get('id', ''),
            test_case_id=data.get('test_case_id', ''),
            test_run_id=data.get('test_run_id', ''),
            status=data.get('status', 'pending'),
            execution_time=data.get('execution_time', 0.0),
            error_message=data.get('error_message', ''),
            error_type=data.get('error_type', ''),
            stack_trace=data.get('stack_trace', ''),
            screenshot_path=data.get('screenshot_path', ''),
            log_path=data.get('log_path', ''),
            video_path=data.get('video_path', ''),
            device_info=data.get('device_info', {}),
            app_info=data.get('app_info', {}),
            platform_info=data.get('platform_info', {}),
            executed_by=data.get('executed_by', ''),
            executed_on=data.get('executed_on', ''),
            environment=data.get('environment', ''),
            started_at=started_at,
            finished_at=finished_at,
            created_at=created_at,
            additional_data=data.get('additional_data', {}),
        )
    
    def start_execution(self):
        """Start test execution"""
        self.status = "running"
        self.started_at = datetime.now()
        Log.info(f"Started execution of test result: {self.id}")
    
    def finish_execution(self, status: str, execution_time: float = None):
        """
        Finish test execution
        
        Args:
            status: Execution status
            execution_time: Execution time (seconds)
        """
        valid_statuses = ['passed', 'failed', 'skipped', 'blocked']
        if status not in valid_statuses:
            raise ValueError(f"Invalid status: {status}. Valid statuses: {valid_statuses}")
        
        self.status = status
        self.finished_at = datetime.now()
        
        if execution_time is not None:
            self.execution_time = execution_time
        elif self.started_at and self.finished_at:
            self.execution_time = (self.finished_at - self.started_at).total_seconds()
        
        Log.info(f"Finished execution of test result {self.id} with status: {status}")
    
    def set_error(self, error_message: str, error_type: str = "", stack_trace: str = ""):
        """
        Set error information
        
        Args:
            error_message: Error message
            error_type: Error type
            stack_trace: Stack trace
        """
        self.error_message = error_message
        self.error_type = error_type
        self.stack_trace = stack_trace
        
        Log.info(f"Set error for test result {self.id}: {error_message}")
    
    def add_screenshot(self, screenshot_path: str):
        """
        Add screenshot path
        
        Args:
            screenshot_path: Screenshot file path
        """
        self.screenshot_path = screenshot_path
        Log.info(f"Added screenshot for test result {self.id}: {screenshot_path}")
    
    def add_log(self, log_path: str):
        """
        Add log path
        
        Args:
            log_path: Log file path
        """
        self.log_path = log_path
        Log.info(f"Added log for test result {self.id}: {log_path}")
    
    def add_video(self, video_path: str):
        """
        Add video path
        
        Args:
            video_path: Video file path
        """
        self.video_path = video_path
        Log.info(f"Added video for test result {self.id}: {video_path}")
    
    def set_device_info(self, device_info: Dict[str, Any]):
        """
        Set device information
        
        Args:
            device_info: Device information dictionary
        """
        self.device_info = device_info
        Log.info(f"Set device info for test result {self.id}")
    
    def set_app_info(self, app_info: Dict[str, Any]):
        """
        Set application information
        
        Args:
            app_info: Application information dictionary
        """
        self.app_info = app_info
        Log.info(f"Set app info for test result {self.id}")
    
    def set_platform_info(self, platform_info: Dict[str, Any]):
        """
        Set platform information
        
        Args:
            platform_info: Platform information dictionary
        """
        self.platform_info = platform_info
        Log.info(f"Set platform info for test result {self.id}")
    
    def is_passed(self) -> bool:
        """
        Check if passed
        
        Returns:
            bool: Whether passed
        """
        return self.status == "passed"
    
    def is_failed(self) -> bool:
        """
        Check if failed
        
        Returns:
            bool: Whether failed
        """
        return self.status == "failed"
    
    def is_skipped(self) -> bool:
        """
        Check if skipped
        
        Returns:
            bool: Whether skipped
        """
        return self.status == "skipped"
    
    def is_blocked(self) -> bool:
        """
        Check if blocked
        
        Returns:
            bool: Whether blocked
        """
        return self.status == "blocked"
    
    def is_running(self) -> bool:
        """
        Check if running
        
        Returns:
            bool: Whether running
        """
        return self.status == "running"
    
    def get_execution_duration(self) -> float:
        """
        Get execution duration
        
        Returns:
            float: Execution time (seconds)
        """
        if self.started_at and self.finished_at:
            return (self.finished_at - self.started_at).total_seconds()
        return self.execution_time
    
    def get_summary(self) -> str:
        """
        Get test result summary
        
        Returns:
            str: Summary information
        """
        parts = [f"Test {self.test_case_id}"]
        
        if self.status:
            parts.append(f"[{self.status.upper()}]")
        
        if self.execution_time > 0:
            parts.append(f"({self.execution_time:.2f}s)")
        
        if self.error_message:
            parts.append(f"- {self.error_message[:50]}...")
        
        return " ".join(parts)
    
    def validate(self) -> bool:
        """
        Validate test result data
        
        Returns:
            bool: Whether valid
        """
        errors = []
        
        if not self.test_case_id:
            errors.append("Test case ID is required")
        
        valid_statuses = ['pending', 'running', 'passed', 'failed', 'skipped', 'blocked']
        if self.status not in valid_statuses:
            errors.append(f"Invalid status: {self.status}")
        
        if self.execution_time < 0:
            errors.append("Execution time cannot be negative")
        
        if errors:
            for error in errors:
                Log.error(f"Test result validation error: {error}")
            return False
        
        return True
