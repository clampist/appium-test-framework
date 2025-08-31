"""
Test Case Model
Test case data model
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

from core.utils.logger import Log


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
    expected_results: List[str] = field(default_factory=list)
    
    # Preconditions and postconditions
    preconditions: List[str] = field(default_factory=list)
    postconditions: List[str] = field(default_factory=list)
    
    # Automation related
    is_automated: bool = False
    automation_script: str = ""
    automation_framework: str = ""
    
    # Time information
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: str = ""
    updated_by: str = ""
    
    # Other information
    additional_data: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Post-initialization processing"""
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary
        
        Returns:
            Dict[str, Any]: Dictionary representation
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'project_id': self.project_id,
            'status': self.status,
            'priority': self.priority,
            'category': self.category,
            'tags': self.tags,
            'steps': self.steps,
            'expected_results': self.expected_results,
            'preconditions': self.preconditions,
            'postconditions': self.postconditions,
            'is_automated': self.is_automated,
            'automation_script': self.automation_script,
            'automation_framework': self.automation_framework,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'created_by': self.created_by,
            'updated_by': self.updated_by,
            'additional_data': self.additional_data,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TestCase':
        """
        Create object from dictionary
        
        Args:
            data: Dictionary data
            
        Returns:
            TestCase: Test case object
        """
        # Handle time fields
        created_at = None
        if data.get('created_at'):
            try:
                created_at = datetime.fromisoformat(data['created_at'])
            except ValueError:
                Log.warning(f"Invalid created_at format: {data['created_at']}")
        
        updated_at = None
        if data.get('updated_at'):
            try:
                updated_at = datetime.fromisoformat(data['updated_at'])
            except ValueError:
                Log.warning(f"Invalid updated_at format: {data['updated_at']}")
        
        return cls(
            id=data.get('id', ''),
            name=data.get('name', ''),
            description=data.get('description', ''),
            project_id=data.get('project_id', ''),
            status=data.get('status', 'active'),
            priority=data.get('priority', 'medium'),
            category=data.get('category', ''),
            tags=data.get('tags', []),
            steps=data.get('steps', []),
            expected_results=data.get('expected_results', []),
            preconditions=data.get('preconditions', []),
            postconditions=data.get('postconditions', []),
            is_automated=data.get('is_automated', False),
            automation_script=data.get('automation_script', ''),
            automation_framework=data.get('automation_framework', ''),
            created_at=created_at,
            updated_at=updated_at,
            created_by=data.get('created_by', ''),
            updated_by=data.get('updated_by', ''),
            additional_data=data.get('additional_data', {}),
        )
    
    def add_step(self, step_description: str, expected_result: str = ""):
        """
        Add test step
        
        Args:
            step_description: Step description
            expected_result: Expected result
        """
        step = {
            'step_number': len(self.steps) + 1,
            'description': step_description,
            'expected_result': expected_result,
        }
        self.steps.append(step)
        
        if expected_result:
            self.expected_results.append(expected_result)
        
        Log.info(f"Added step {step['step_number']} to test case {self.id}")
    
    def add_tag(self, tag: str):
        """
        Add tag
        
        Args:
            tag: Tag name
        """
        if tag not in self.tags:
            self.tags.append(tag)
            Log.info(f"Added tag '{tag}' to test case {self.id}")
    
    def remove_tag(self, tag: str):
        """
        Remove tag
        
        Args:
            tag: Tag name
        """
        if tag in self.tags:
            self.tags.remove(tag)
            Log.info(f"Removed tag '{tag}' from test case {self.id}")
    
    def has_tag(self, tag: str) -> bool:
        """
        Check if has specified tag
        
        Args:
            tag: Tag name
            
        Returns:
            bool: Whether has tag
        """
        return tag in self.tags
    
    def update_status(self, status: str):
        """
        Update status
        
        Args:
            status: New status
        """
        valid_statuses = ['active', 'inactive', 'deprecated']
        if status not in valid_statuses:
            raise ValueError(f"Invalid status: {status}. Valid statuses: {valid_statuses}")
        
        self.status = status
        self.updated_at = datetime.now()
        Log.info(f"Updated test case {self.id} status to: {status}")
    
    def update_priority(self, priority: str):
        """
        Update priority
        
        Args:
            priority: New priority
        """
        valid_priorities = ['low', 'medium', 'high', 'critical']
        if priority not in valid_priorities:
            raise ValueError(f"Invalid priority: {priority}. Valid priorities: {valid_priorities}")
        
        self.priority = priority
        self.updated_at = datetime.now()
        Log.info(f"Updated test case {self.id} priority to: {priority}")
    
    def mark_as_automated(self, script_path: str = "", framework: str = ""):
        """
        Mark as automated test
        
        Args:
            script_path: Script path
            framework: Framework name
        """
        self.is_automated = True
        if script_path:
            self.automation_script = script_path
        if framework:
            self.automation_framework = framework
        
        self.updated_at = datetime.now()
        Log.info(f"Marked test case {self.id} as automated")
    
    def mark_as_manual(self):
        """Mark as manual test"""
        self.is_automated = False
        self.automation_script = ""
        self.automation_framework = ""
        
        self.updated_at = datetime.now()
        Log.info(f"Marked test case {self.id} as manual")
    
    def get_summary(self) -> str:
        """
        Get test case summary
        
        Returns:
            str: Summary information
        """
        parts = [self.name]
        
        if self.priority:
            parts.append(f"[{self.priority.upper()}]")
        
        if self.status:
            parts.append(f"({self.status})")
        
        if self.is_automated:
            parts.append("[AUTO]")
        
        return " ".join(parts)
    
    def validate(self) -> bool:
        """
        Validate test case data
        
        Returns:
            bool: Whether valid
        """
        errors = []
        
        if not self.name:
            errors.append("Test case name is required")
        
        if not self.project_id:
            errors.append("Project ID is required")
        
        valid_statuses = ['active', 'inactive', 'deprecated']
        if self.status not in valid_statuses:
            errors.append(f"Invalid status: {self.status}")
        
        valid_priorities = ['low', 'medium', 'high', 'critical']
        if self.priority not in valid_priorities:
            errors.append(f"Invalid priority: {self.priority}")
        
        if errors:
            for error in errors:
                Log.error(f"Test case validation error: {error}")
            return False
        
        return True
