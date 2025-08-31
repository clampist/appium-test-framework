"""
API Server
API server, providing RESTful API services
"""

import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename

from core.utils.logger import Log
from core.utils.file_utils import FileUtils
from ..models.test_result import TestResult
from ..models.test_case import TestCase


class ApiServer:
    """API server class"""
    
    def __init__(self, host: str = "0.0.0.0", port: int = 5000, debug: bool = False):
        """
        Initialize API server
        
        Args:
            host: Listen host
            port: Listen port
            debug: Debug mode
        """
        self.host = host
        self.port = port
        self.debug = debug
        
        # Create Flask application
        self.app = Flask(__name__)
        self.app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
        
        # Set upload directory
        self.upload_folder = "uploads"
        FileUtils.ensure_dir(self.upload_folder)
        
        # Register routes
        self._register_routes()
        
        Log.info(f"Initialized API server on {host}:{port}")
    
    def _register_routes(self):
        """Register API routes"""
        
        # Health check
        @self.app.route('/health', methods=['GET'])
        def health_check():
            return jsonify({
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'version': '1.0.0'
            })
        
        # API information
        @self.app.route('/info', methods=['GET'])
        def api_info():
            return jsonify({
                'name': 'ATF API Server',
                'version': '1.0.0',
                'description': 'Appium Test Framework API Server',
                'endpoints': [
                    '/health',
                    '/info',
                    '/test-cases',
                    '/test-results',
                    '/upload'
                ]
            })
        
        # Test case related routes
        @self.app.route('/test-cases', methods=['GET'])
        def get_test_cases():
            try:
                project_id = request.args.get('project_id')
                status = request.args.get('status')
                
                # Should get test cases from database here
                # Currently return mock data
                test_cases = self._get_mock_test_cases(project_id, status)
                
                return jsonify({
                    'test_cases': [tc.to_dict() for tc in test_cases],
                    'total': len(test_cases)
                })
            except Exception as e:
                Log.error(f"Error getting test cases: {str(e)}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/test-cases/<test_case_id>', methods=['GET'])
        def get_test_case(test_case_id):
            try:
                # Should get test case from database here
                test_case = self._get_mock_test_case(test_case_id)
                
                if not test_case:
                    return jsonify({'error': 'Test case not found'}), 404
                
                return jsonify({'test_case': test_case.to_dict()})
            except Exception as e:
                Log.error(f"Error getting test case {test_case_id}: {str(e)}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/test-cases', methods=['POST'])
        def create_test_case():
            try:
                data = request.get_json()
                test_case = TestCase.from_dict(data)
                
                # Should save to database here
                # Currently just return mock data
                test_case.id = f"tc_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                
                Log.info(f"Created test case: {test_case.id}")
                
                return jsonify({'test_case': test_case.to_dict()}), 201
            except Exception as e:
                Log.error(f"Error creating test case: {str(e)}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/test-cases/<test_case_id>', methods=['PUT'])
        def update_test_case(test_case_id):
            try:
                data = request.get_json()
                test_case = TestCase.from_dict(data)
                test_case.id = test_case_id
                
                # Should update database here
                Log.info(f"Updated test case: {test_case_id}")
                
                return jsonify({'test_case': test_case.to_dict()})
            except Exception as e:
                Log.error(f"Error updating test case {test_case_id}: {str(e)}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/test-cases/<test_case_id>', methods=['DELETE'])
        def delete_test_case(test_case_id):
            try:
                # Should delete from database here
                Log.info(f"Deleted test case: {test_case_id}")
                
                return jsonify({'message': 'Test case deleted successfully'})
            except Exception as e:
                Log.error(f"Error deleting test case {test_case_id}: {str(e)}")
                return jsonify({'error': str(e)}), 500
        
        # Test result related routes
        @self.app.route('/test-results', methods=['GET'])
        def get_test_results():
            try:
                test_case_id = request.args.get('test_case_id')
                status = request.args.get('status')
                start_date = request.args.get('start_date')
                end_date = request.args.get('end_date')
                
                # Should get test results from database here
                test_results = self._get_mock_test_results(test_case_id, status, start_date, end_date)
                
                return jsonify({
                    'test_results': [tr.to_dict() for tr in test_results],
                    'total': len(test_results)
                })
            except Exception as e:
                Log.error(f"Error getting test results: {str(e)}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/test-results/<result_id>', methods=['GET'])
        def get_test_result(result_id):
            try:
                # Should get test result from database here
                test_result = self._get_mock_test_result(result_id)
                
                if not test_result:
                    return jsonify({'error': 'Test result not found'}), 404
                
                return jsonify({'test_result': test_result.to_dict()})
            except Exception as e:
                Log.error(f"Error getting test result {result_id}: {str(e)}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/test-results', methods=['POST'])
        def submit_test_result():
            try:
                data = request.get_json()
                test_result = TestResult.from_dict(data)
                
                # Should save to database here
                test_result.id = f"tr_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                test_result.created_at = datetime.now()
                
                Log.info(f"Submitted test result: {test_result.id}")
                
                return jsonify({'test_result': test_result.to_dict()}), 201
            except Exception as e:
                Log.error(f"Error submitting test result: {str(e)}")
                return jsonify({'error': str(e)}), 500
        
        # File upload routes
        @self.app.route('/upload', methods=['POST'])
        def upload_file():
            try:
                if 'file' not in request.files:
                    return jsonify({'error': 'No file provided'}), 400
                
                file = request.files['file']
                file_type = request.form.get('file_type', 'unknown')
                
                if file.filename == '':
                    return jsonify({'error': 'No file selected'}), 400
                
                if file:
                    filename = secure_filename(file.filename)
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f"{timestamp}_{filename}"
                    
                    file_path = os.path.join(self.upload_folder, filename)
                    file.save(file_path)
                    
                    file_url = f"/uploads/{filename}"
                    
                    Log.info(f"File uploaded: {file_path}")
                    
                    return jsonify({
                        'file_url': file_url,
                        'filename': filename,
                        'file_type': file_type
                    })
                
            except Exception as e:
                Log.error(f"Error uploading file: {str(e)}")
                return jsonify({'error': str(e)}), 500
        
        # File download routes
        @self.app.route('/uploads/<filename>', methods=['GET'])
        def download_file(filename):
            try:
                file_path = os.path.join(self.upload_folder, filename)
                
                if not FileUtils.file_exists(file_path):
                    return jsonify({'error': 'File not found'}), 404
                
                return send_file(file_path, as_attachment=True)
                
            except Exception as e:
                Log.error(f"Error downloading file {filename}: {str(e)}")
                return jsonify({'error': str(e)}), 500
    
    def _get_mock_test_cases(self, project_id: Optional[str] = None, 
                            status: Optional[str] = None) -> List[TestCase]:
        """Get mock test case data"""
        test_cases = [
            TestCase(
                id="tc_001",
                name="Login Test",
                description="Test user login functionality",
                project_id="project_001",
                status="active",
                priority="high",
                tags=["login", "authentication"]
            ),
            TestCase(
                id="tc_002", 
                name="Registration Test",
                description="Test user registration functionality",
                project_id="project_001",
                status="active",
                priority="medium",
                tags=["registration", "user"]
            )
        ]
        
        # Filter
        if project_id:
            test_cases = [tc for tc in test_cases if tc.project_id == project_id]
        
        if status:
            test_cases = [tc for tc in test_cases if tc.status == status]
        
        return test_cases
    
    def _get_mock_test_case(self, test_case_id: str) -> Optional[TestCase]:
        """Get mock test case data"""
        test_cases = self._get_mock_test_cases()
        for tc in test_cases:
            if tc.id == test_case_id:
                return tc
        return None
    
    def _get_mock_test_results(self, test_case_id: Optional[str] = None,
                              status: Optional[str] = None,
                              start_date: Optional[str] = None,
                              end_date: Optional[str] = None) -> List[TestResult]:
        """Get mock test result data"""
        test_results = [
            TestResult(
                id="tr_001",
                test_case_id="tc_001",
                status="passed",
                execution_time=30.5,
                screenshot_path="/uploads/screenshot_001.png",
                error_message="",
                created_at=datetime.now()
            ),
            TestResult(
                id="tr_002",
                test_case_id="tc_002", 
                status="failed",
                execution_time=45.2,
                screenshot_path="/uploads/screenshot_002.png",
                error_message="Element not found",
                created_at=datetime.now()
            )
        ]
        
        # Filter
        if test_case_id:
            test_results = [tr for tr in test_results if tr.test_case_id == test_case_id]
        
        if status:
            test_results = [tr for tr in test_results if tr.status == status]
        
        return test_results
    
    def _get_mock_test_result(self, result_id: str) -> Optional[TestResult]:
        """Get mock test result data"""
        test_results = self._get_mock_test_results()
        for tr in test_results:
            if tr.id == result_id:
                return tr
        return None
    
    def start(self):
        """Start API server"""
        try:
            Log.info(f"Starting API server on {self.host}:{self.port}")
            self.app.run(host=self.host, port=self.port, debug=self.debug)
        except Exception as e:
            Log.error(f"Failed to start API server: {str(e)}")
            raise
    
    def stop(self):
        """Stop API server"""
        Log.info("API server stopped")
    
    def get_app(self) -> Flask:
        """Get Flask application instance"""
        return self.app
