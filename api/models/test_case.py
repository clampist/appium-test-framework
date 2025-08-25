"""
Test Case Model
测试用例数据模型
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

from core.utils.logger import Log


@dataclass
class TestCase:
    """测试用例数据模型"""
    
    # 基本信息
    id: str = ""
    name: str = ""
    description: str = ""
    project_id: str = ""
    
    # 状态和优先级
    status: str = "active"  # active, inactive, deprecated
    priority: str = "medium"  # low, medium, high, critical
    
    # 分类和标签
    category: str = ""
    tags: List[str] = field(default_factory=list)
    
    # 测试步骤
    steps: List[Dict[str, Any]] = field(default_factory=list)
    expected_results: List[str] = field(default_factory=list)
    
    # 前置和后置条件
    preconditions: List[str] = field(default_factory=list)
    postconditions: List[str] = field(default_factory=list)
    
    # 自动化相关
    is_automated: bool = False
    automation_script: str = ""
    automation_framework: str = ""
    
    # 时间信息
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: str = ""
    updated_by: str = ""
    
    # 其他信息
    additional_data: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """初始化后处理"""
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典
        
        Returns:
            Dict[str, Any]: 字典表示
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
        从字典创建对象
        
        Args:
            data: 字典数据
            
        Returns:
            TestCase: 测试用例对象
        """
        # 处理时间字段
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
        添加测试步骤
        
        Args:
            step_description: 步骤描述
            expected_result: 预期结果
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
        添加标签
        
        Args:
            tag: 标签名称
        """
        if tag not in self.tags:
            self.tags.append(tag)
            Log.info(f"Added tag '{tag}' to test case {self.id}")
    
    def remove_tag(self, tag: str):
        """
        移除标签
        
        Args:
            tag: 标签名称
        """
        if tag in self.tags:
            self.tags.remove(tag)
            Log.info(f"Removed tag '{tag}' from test case {self.id}")
    
    def has_tag(self, tag: str) -> bool:
        """
        检查是否有指定标签
        
        Args:
            tag: 标签名称
            
        Returns:
            bool: 是否有标签
        """
        return tag in self.tags
    
    def update_status(self, status: str):
        """
        更新状态
        
        Args:
            status: 新状态
        """
        valid_statuses = ['active', 'inactive', 'deprecated']
        if status not in valid_statuses:
            raise ValueError(f"Invalid status: {status}. Valid statuses: {valid_statuses}")
        
        self.status = status
        self.updated_at = datetime.now()
        Log.info(f"Updated test case {self.id} status to: {status}")
    
    def update_priority(self, priority: str):
        """
        更新优先级
        
        Args:
            priority: 新优先级
        """
        valid_priorities = ['low', 'medium', 'high', 'critical']
        if priority not in valid_priorities:
            raise ValueError(f"Invalid priority: {priority}. Valid priorities: {valid_priorities}")
        
        self.priority = priority
        self.updated_at = datetime.now()
        Log.info(f"Updated test case {self.id} priority to: {priority}")
    
    def mark_as_automated(self, script_path: str = "", framework: str = ""):
        """
        标记为自动化测试
        
        Args:
            script_path: 脚本路径
            framework: 框架名称
        """
        self.is_automated = True
        if script_path:
            self.automation_script = script_path
        if framework:
            self.automation_framework = framework
        
        self.updated_at = datetime.now()
        Log.info(f"Marked test case {self.id} as automated")
    
    def mark_as_manual(self):
        """标记为手动测试"""
        self.is_automated = False
        self.automation_script = ""
        self.automation_framework = ""
        
        self.updated_at = datetime.now()
        Log.info(f"Marked test case {self.id} as manual")
    
    def get_summary(self) -> str:
        """
        获取测试用例摘要
        
        Returns:
            str: 摘要信息
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
        验证测试用例数据
        
        Returns:
            bool: 是否有效
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
