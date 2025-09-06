"""
Test data definitions for TikTok App
Test data definitions for TikTok App
"""

import os
from typing import Dict, Any


class BaseTikTokTestData:
    """Base test data class for TikTok App"""
    
    # Application basic information
    APP_PACKAGE = "com.ss.android.ugc.trill"
    APP_ACTIVITY = "com.ss.android.ugc.aweme.splash.SplashActivity"
    WAIT_TIME = 5  # Reduced wait time from 15s to 5s
    
    # Common element locators (language independent)
    class CommonLocators:
        """Common element locators (language independent)"""
        
        # Bottom navigation bar
        HOME_TAB = "com.ss.android.ugc.trill:id/lay"
        FRIENDS_TAB = "com.ss.android.ugc.trill:id/lax"
        CREATE_TAB = "com.ss.android.ugc.trill:id/lav"
        INBOX_TAB = "com.ss.android.ugc.trill:id/laz"
        PROFILE_TAB = "com.ss.android.ugc.trill:id/lb0"
        
        # Common buttons
        BACK_BTN = "com.ss.android.ugc.trill:id/b2t"
        CREATE_CLOSE_BTN = "com.ss.android.ugc.trill:id/neq"
        CLOSE_ICON_BTN = 'new UiSelector().description("Close")'
        
        # Video player controls
        LIKE_BTN = "com.ss.android.ugc.trill:id/elf"
        COMMENT_BTN = "com.ss.android.ugc.trill:id/dc8"
        SHARE_BTN = "com.ss.android.ugc.trill:id/rdf"
        BOOKMARK_BTN = "com.ss.android.ugc.trill:id/g3o"
        
        # Search functionality
        SEARCH_BAR = "com.ss.android.ugc.trill:id/hv0"
        SEARCH_INPUT = "com.ss.android.ugc.trill:id/fu_"
        SEARCH_BTN = "com.ss.android.ugc.trill:id/vt3"
        
        # Profile elements
        PROFILE_AVATAR = "com.ss.android.ugc.trill:id/az_"
        USERNAME_TEXT = "com.ss.android.ugc.trill:id/osw"
        
        # Permission dialogs
        PERMISSION_ALLOW_BTN = "com.android.packageinstaller:id/permission_allow_button"
        PERMISSION_DENY_BTN = "com.android.packageinstaller:id/permission_deny_button"
    
    # Common test data (language independent)
    class CommonTestData:
        """Common test data (language independent)"""
        VIDEO_WAIT_TIME = 3
        ANIMATION_WAIT_TIME = 1  # Reduced animation wait time from 2s to 1s
        LOADING_WAIT_TIME = 3    # Reduced loading wait time from 5s to 3s


class EnglishTikTokTestData(BaseTikTokTestData):
    """English version TikTok App test data"""
    
    # English version language-related locators
    class Locators(BaseTikTokTestData.CommonLocators):
        """English version language-related locators"""
        
        # Onboarding (English)
        GET_STARTED_BTN = 'new UiSelector().text("Get Started")'
        LOGIN_BTN = 'new UiSelector().text("Log in")'
        SIGN_UP_BTN = 'new UiSelector().text("Sign up")'
        
        # Navigation (English)
        HOME_TEXT = 'new UiSelector().text("Home")'
        FRIENDS_TEXT = 'new UiSelector().text("Friends")'
        CREATE_TEXT = 'new UiSelector().text("Create")'
        INBOX_TEXT = 'new UiSelector().text("Inbox")'
        PROFILE_TEXT = 'new UiSelector().text("Profile")'
        
        # Search (English)
        SEARCH_PLACEHOLDER = 'new UiSelector().text("Search")'
        TRENDING_TEXT = 'new UiSelector().text("Trending")'
        
        # Profile (English)
        EDIT_PROFILE_BTN = 'new UiSelector().text("Edit profile")'
        SETTINGS_BTN = 'new UiSelector().text("Settings")'
        
        # Permission dialogs (English)
        ALLOW_TEXT = 'new UiSelector().text("Allow")'
        DENY_TEXT = 'new UiSelector().text("Deny")'
    
    # English version test data
    class TestData(BaseTikTokTestData.CommonTestData):
        """English version test data"""
        SEARCH_KEYWORD = "funny"
        TRENDING_HASHTAG = "#fyp"


class ChineseTikTokTestData(BaseTikTokTestData):
    """Chinese version TikTok App test data"""
    
    # Chinese version language-related locators
    class Locators(BaseTikTokTestData.CommonLocators):
        """Chinese version language-related locators"""
        
        # Onboarding (Chinese)
        GET_STARTED_BTN = 'new UiSelector().text("开始使用")'
        LOGIN_BTN = 'new UiSelector().text("登录")'
        SIGN_UP_BTN = 'new UiSelector().text("注册")'
        
        # Navigation (Chinese)
        HOME_TEXT = 'new UiSelector().text("首页")'
        FRIENDS_TEXT = 'new UiSelector().text("朋友")'
        CREATE_TEXT = 'new UiSelector().text("创建")'
        INBOX_TEXT = 'new UiSelector().text("消息")'
        PROFILE_TEXT = 'new UiSelector().text("我")'
        
        # Search (Chinese)
        SEARCH_PLACEHOLDER = 'new UiSelector().text("搜索")'
        TRENDING_TEXT = 'new UiSelector().text("热门")'
        
        # Profile (Chinese)
        EDIT_PROFILE_BTN = 'new UiSelector().text("编辑资料")'
        SETTINGS_BTN = 'new UiSelector().text("设置")'
        
        # Permission dialogs (Chinese)
        ALLOW_TEXT = 'new UiSelector().text("允许")'
        DENY_TEXT = 'new UiSelector().text("拒绝")'
    
    # Chinese version test data
    class TestData(BaseTikTokTestData.CommonTestData):
        """Chinese version test data"""
        SEARCH_KEYWORD = "搞笑"
        TRENDING_HASHTAG = "#热门"


def get_test_data(language: str = "en"):
    """
    Get test data based on language
    
    Args:
        language: Language code (en/zh)
        
    Returns:
        Test data class instance
    """
    if language == "zh":
        return ChineseTikTokTestData()
    else:
        return EnglishTikTokTestData()

