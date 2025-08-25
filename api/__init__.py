"""
ATF API Package
对外对内交互层接口层，提供API接口和数据模型
"""

__version__ = "1.0.0"
__author__ = "ATF Team"

from .client.api_client import ApiClient
from .server.api_server import ApiServer
from .models.test_result import TestResult
from .models.test_case import TestCase

__all__ = [
    "ApiClient",
    "ApiServer", 
    "TestResult",
    "TestCase"
]
