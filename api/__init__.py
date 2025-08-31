"""
ATF API Package
External and internal interaction layer interface layer, providing API interfaces and data models
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
