"""
Page objects package for TikTok App
"""

from .main_page import MainPage
from .search_page import SearchPage
from .profile_page import ProfilePage
from .video_page import VideoPage

__all__ = [
    'MainPage',      # Navigation and permissions
    'SearchPage',    # Search functionality
    'ProfilePage',   # Profile management
    'VideoPage'      # Video operations and interactions
]

