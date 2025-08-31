"""
API Client
API client, providing interfaces for interaction with external systems
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
    """API client class"""
    
    def __init__(self, base_url: str, timeout: int = 30, headers: Optional[Dict[str, str]] = None):
        """
        Initialize API client
        
        Args:
            base_url: API base URL
            timeout: Request timeout (seconds)
            headers: Request headers
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
        Send HTTP request
        
        Args:
            method: HTTP method
            endpoint: API endpoint
            data: Request data
            params: Query parameters
            
        Returns:
            requests.Response: Response object
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
            
            # Check response status
            response.raise_for_status()
            
            return response
            
        except requests.exceptions.RequestException as e:
            Log.error(f"API request failed: {str(e)}")
            raise
    
    def get_test_cases(self, project_id: Optional[str] = None, 
                      status: Optional[str] = None) -> List[TestCase]:
        """
        Get test case list
        
        Args:
            project_id: Project ID (optional)
            status: Status filter (optional)
            
        Returns:
            List[TestCase]: Test case list
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
        Get single test case
        
        Args:
            test_case_id: Test case ID
            
        Returns:
            TestCase: Test case object
        """
        response = self._make_request('GET', f'/test-cases/{test_case_id}')
        data = response.json()
        
        test_case = TestCase.from_dict(data['test_case'])
        Log.info(f"Retrieved test case: {test_case_id}")
        return test_case
    
    def create_test_case(self, test_case: TestCase) -> TestCase:
        """
        Create test case
        
        Args:
            test_case: Test case object
            
        Returns:
            TestCase: Created test case object
        """
        data = test_case.to_dict()
        response = self._make_request('POST', '/test-cases', data=data)
        result_data = response.json()
        
        created_test_case = TestCase.from_dict(result_data['test_case'])
        Log.info(f"Created test case: {created_test_case.id}")
        return created_test_case
    
    def update_test_case(self, test_case_id: str, test_case: TestCase) -> TestCase:
        """
        Update test case
        
        Args:
            test_case_id: Test case ID
            test_case: Test case object
            
        Returns:
            TestCase: Updated test case object
        """
        data = test_case.to_dict()
        response = self._make_request('PUT', f'/test-cases/{test_case_id}', data=data)
        result_data = response.json()
        
        updated_test_case = TestCase.from_dict(result_data['test_case'])
        Log.info(f"Updated test case: {test_case_id}")
        return updated_test_case
    
    def delete_test_case(self, test_case_id: str) -> bool:
        """
        Delete test case
        
        Args:
            test_case_id: Test case ID
            
        Returns:
            bool: Whether deletion was successful
        """
        response = self._make_request('DELETE', f'/test-cases/{test_case_id}')
        Log.info(f"Deleted test case: {test_case_id}")
        return True
    
    def submit_test_result(self, test_result: TestResult) -> TestResult:
        """
        Submit test result
        
        Args:
            test_result: Test result object
            
        Returns:
            TestResult: Submitted test result object
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
        Get test result list
        
        Args:
            test_case_id: Test case ID (optional)
            status: Status filter (optional)
            start_date: Start date (optional)
            end_date: End date (optional)
            
        Returns:
            List[TestResult]: Test result list
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
        Get single test result
        
        Args:
            result_id: Test result ID
            
        Returns:
            TestResult: Test result object
        """
        response = self._make_request('GET', f'/test-results/{result_id}')
        data = response.json()
        
        test_result = TestResult.from_dict(data['test_result'])
        Log.info(f"Retrieved test result: {result_id}")
        return test_result
    
    def upload_file(self, file_path: str, file_type: str = "screenshot") -> str:
        """
        Upload file
        
        Args:
            file_path: File path
            file_type: File type
            
        Returns:
            str: File URL
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
        Get API health status
        
        Returns:
            Dict[str, Any]: Health status information
        """
        response = self._make_request('GET', '/health')
        return response.json()
    
    def get_api_info(self) -> Dict[str, Any]:
        """
        Get API information
        
        Returns:
            Dict[str, Any]: API information
        """
        response = self._make_request('GET', '/info')
        return response.json()
    
    def set_auth_token(self, token: str):
        """
        Set authentication token
        
        Args:
            token: Authentication token
        """
        self.session.headers['Authorization'] = f'Bearer {token}'
        Log.info("Authentication token set")
    
    def clear_auth_token(self):
        """Clear authentication token"""
        if 'Authorization' in self.session.headers:
            del self.session.headers['Authorization']
            Log.info("Authentication token cleared")
    
    def close(self):
        """Close client connection"""
        self.session.close()
        Log.info("API client closed")
