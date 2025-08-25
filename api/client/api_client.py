"""
API Client
API客户端，提供与外部系统交互的接口
"""

import json
import requests
from typing import Dict, Any, List, Optional
from datetime import datetime

from core.utils.logger import Log
from core.utils.file_utils import FileUtils
from ..models.test_result import TestResult
from ..models.test_case import TestCase


class ApiClient:
    """API客户端类"""
    
    def __init__(self, base_url: str, timeout: int = 30, headers: Optional[Dict[str, str]] = None):
        """
        初始化API客户端
        
        Args:
            base_url: API基础URL
            timeout: 请求超时时间（秒）
            headers: 请求头
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.headers = headers or {
            'Content-Type': 'application/json',
            'User-Agent': 'ATF-Client/1.0.0'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        Log.info(f"Initialized API client with base URL: {self.base_url}")
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None, 
                     params: Optional[Dict[str, Any]] = None) -> requests.Response:
        """
        发送HTTP请求
        
        Args:
            method: HTTP方法
            endpoint: API端点
            data: 请求数据
            params: 查询参数
            
        Returns:
            requests.Response: 响应对象
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            Log.info(f"Making {method} request to: {url}")
            
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                timeout=self.timeout
            )
            
            Log.info(f"Response status: {response.status_code}")
            
            # 检查响应状态
            response.raise_for_status()
            
            return response
            
        except requests.exceptions.RequestException as e:
            Log.error(f"API request failed: {str(e)}")
            raise
    
    def get_test_cases(self, project_id: Optional[str] = None, 
                      status: Optional[str] = None) -> List[TestCase]:
        """
        获取测试用例列表
        
        Args:
            project_id: 项目ID（可选）
            status: 状态过滤（可选）
            
        Returns:
            List[TestCase]: 测试用例列表
        """
        params = {}
        if project_id:
            params['project_id'] = project_id
        if status:
            params['status'] = status
        
        response = self._make_request('GET', '/test-cases', params=params)
        data = response.json()
        
        test_cases = []
        for item in data.get('test_cases', []):
            test_case = TestCase.from_dict(item)
            test_cases.append(test_case)
        
        Log.info(f"Retrieved {len(test_cases)} test cases")
        return test_cases
    
    def get_test_case(self, test_case_id: str) -> TestCase:
        """
        获取单个测试用例
        
        Args:
            test_case_id: 测试用例ID
            
        Returns:
            TestCase: 测试用例对象
        """
        response = self._make_request('GET', f'/test-cases/{test_case_id}')
        data = response.json()
        
        test_case = TestCase.from_dict(data['test_case'])
        Log.info(f"Retrieved test case: {test_case_id}")
        return test_case
    
    def create_test_case(self, test_case: TestCase) -> TestCase:
        """
        创建测试用例
        
        Args:
            test_case: 测试用例对象
            
        Returns:
            TestCase: 创建的测试用例对象
        """
        data = test_case.to_dict()
        response = self._make_request('POST', '/test-cases', data=data)
        result_data = response.json()
        
        created_test_case = TestCase.from_dict(result_data['test_case'])
        Log.info(f"Created test case: {created_test_case.id}")
        return created_test_case
    
    def update_test_case(self, test_case_id: str, test_case: TestCase) -> TestCase:
        """
        更新测试用例
        
        Args:
            test_case_id: 测试用例ID
            test_case: 测试用例对象
            
        Returns:
            TestCase: 更新后的测试用例对象
        """
        data = test_case.to_dict()
        response = self._make_request('PUT', f'/test-cases/{test_case_id}', data=data)
        result_data = response.json()
        
        updated_test_case = TestCase.from_dict(result_data['test_case'])
        Log.info(f"Updated test case: {test_case_id}")
        return updated_test_case
    
    def delete_test_case(self, test_case_id: str) -> bool:
        """
        删除测试用例
        
        Args:
            test_case_id: 测试用例ID
            
        Returns:
            bool: 是否删除成功
        """
        response = self._make_request('DELETE', f'/test-cases/{test_case_id}')
        Log.info(f"Deleted test case: {test_case_id}")
        return True
    
    def submit_test_result(self, test_result: TestResult) -> TestResult:
        """
        提交测试结果
        
        Args:
            test_result: 测试结果对象
            
        Returns:
            TestResult: 提交的测试结果对象
        """
        data = test_result.to_dict()
        response = self._make_request('POST', '/test-results', data=data)
        result_data = response.json()
        
        submitted_result = TestResult.from_dict(result_data['test_result'])
        Log.info(f"Submitted test result: {submitted_result.id}")
        return submitted_result
    
    def get_test_results(self, test_case_id: Optional[str] = None, 
                        status: Optional[str] = None, 
                        start_date: Optional[datetime] = None,
                        end_date: Optional[datetime] = None) -> List[TestResult]:
        """
        获取测试结果列表
        
        Args:
            test_case_id: 测试用例ID（可选）
            status: 状态过滤（可选）
            start_date: 开始日期（可选）
            end_date: 结束日期（可选）
            
        Returns:
            List[TestResult]: 测试结果列表
        """
        params = {}
        if test_case_id:
            params['test_case_id'] = test_case_id
        if status:
            params['status'] = status
        if start_date:
            params['start_date'] = start_date.isoformat()
        if end_date:
            params['end_date'] = end_date.isoformat()
        
        response = self._make_request('GET', '/test-results', params=params)
        data = response.json()
        
        test_results = []
        for item in data.get('test_results', []):
            test_result = TestResult.from_dict(item)
            test_results.append(test_result)
        
        Log.info(f"Retrieved {len(test_results)} test results")
        return test_results
    
    def get_test_result(self, result_id: str) -> TestResult:
        """
        获取单个测试结果
        
        Args:
            result_id: 测试结果ID
            
        Returns:
            TestResult: 测试结果对象
        """
        response = self._make_request('GET', f'/test-results/{result_id}')
        data = response.json()
        
        test_result = TestResult.from_dict(data['test_result'])
        Log.info(f"Retrieved test result: {result_id}")
        return test_result
    
    def upload_file(self, file_path: str, file_type: str = "screenshot") -> str:
        """
        上传文件
        
        Args:
            file_path: 文件路径
            file_type: 文件类型
            
        Returns:
            str: 文件URL
        """
        if not FileUtils.file_exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        url = f"{self.base_url}/upload"
        
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (file_path, f, 'application/octet-stream')}
                data = {'file_type': file_type}
                
                Log.info(f"Uploading file: {file_path}")
                
                response = self.session.post(
                    url,
                    files=files,
                    data=data,
                    timeout=self.timeout
                )
                
                response.raise_for_status()
                result = response.json()
                
                file_url = result['file_url']
                Log.info(f"File uploaded successfully: {file_url}")
                return file_url
                
        except Exception as e:
            Log.error(f"File upload failed: {str(e)}")
            raise
    
    def get_health_status(self) -> Dict[str, Any]:
        """
        获取API健康状态
        
        Returns:
            Dict[str, Any]: 健康状态信息
        """
        response = self._make_request('GET', '/health')
        return response.json()
    
    def get_api_info(self) -> Dict[str, Any]:
        """
        获取API信息
        
        Returns:
            Dict[str, Any]: API信息
        """
        response = self._make_request('GET', '/info')
        return response.json()
    
    def set_auth_token(self, token: str):
        """
        设置认证令牌
        
        Args:
            token: 认证令牌
        """
        self.session.headers['Authorization'] = f'Bearer {token}'
        Log.info("Authentication token set")
    
    def clear_auth_token(self):
        """清除认证令牌"""
        if 'Authorization' in self.session.headers:
            del self.session.headers['Authorization']
            Log.info("Authentication token cleared")
    
    def close(self):
        """关闭客户端连接"""
        self.session.close()
        Log.info("API client closed")
