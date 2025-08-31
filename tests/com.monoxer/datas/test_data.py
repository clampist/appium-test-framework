"""
Test data definitions for Monoxer App
Test data definitions for Monoxer App
"""

import os
from typing import Dict, Any


class BaseMonoxerTestData:
    """Base test data class for Monoxer App"""
    
    # Application basic information
    APP_PACKAGE = "com.monoxer"
    APP_ACTIVITY = "com.monoxer.view.main.MainActivity"
    WAIT_TIME = 15
    
    # Common element locators (language independent)
    class CommonLocators:
        """Common element locators (language independent)"""
        
        # Bottom navigation bar
        HOME_TAB = "com.monoxer:id/bottom_navigation_home_for_individuals"
        SEARCH_TAB = "com.monoxer:id/bottom_navigation_search"
        LIBRARY_TAB = "com.monoxer:id/bottom_navigation_library"
        
        # Sidebar
        HEADER_SELECTOR = "com.monoxer:id/iOS_like_header_org_selector"
        LINEAR_LAYOUT = "com.monoxer:id/linear_layout"
        
        # Search functionality
        SEARCH_INPUT = "com.monoxer:id/search_src_text"
        SEARCH_VIEW = "com.monoxer:id/search_view"
        SEARCH_BAR = "com.monoxer:id/search_bar"
        CARD_VIEW = "com.monoxer:id/card_view"
        CONTENTS_BTN = "com.monoxer:id/contents"
        
        # Library functionality
        AUTO_TEST_TITLE = '//android.widget.TextView[@resource-id="com.monoxer:id/word_books_book_title" and @text="auto_test"]'
        OPEN_DECK_BTN = "com.monoxer:id/open_deck"
        START_TEST_BTN = "com.monoxer:id/start_test"
        
        # STUDY functionality
        CHOICE1_TEXT = "com.monoxer:id/choice1_text"
        DONE_BTN_XPATH = '//android.widget.TextView[@resource-id="com.monoxer:id/label" and @text="Done"]'
        
        # Common buttons
        NAVIGATE_UP = "Navigate up"
    
    # Common test data (language independent)
    class CommonTestData:
        """Common test data (language independent)"""
        STUDY_WAIT_TIME = 5


class EnglishMonoxerTestData(BaseMonoxerTestData):
    """English version Monoxer App test data"""
    
    # English version language-related locators
    class Locators(BaseMonoxerTestData.CommonLocators):
        """English version language-related locators"""
        
        # Sidebar (English)
        INVITATION_CODE_BTN = 'new UiSelector().text("Enter invitation code")'
        SYNC_BTN = 'new UiSelector().text("Sync")'
        
        # Library functionality (English)
        MY_BOOKS_TAB = "My Books"
        
        # STUDY functionality (English)
        DONE_BTN = 'new UiSelector().text("Done")'
    
    # English version test data
    class TestData(BaseMonoxerTestData.CommonTestData):
        """English version test data"""
        SEARCH_KEYWORD = "日本の祝日"


class JapaneseMonoxerTestData(BaseMonoxerTestData):
    """Japanese version Monoxer App test data"""
    
    # Japanese version language-related locators
    class Locators(BaseMonoxerTestData.CommonLocators):
        """Japanese version language-related locators"""
        
        # Sidebar (Japanese)
        INVITATION_CODE_BTN = 'new UiSelector().text("招待コードを入力")'
        SYNC_BTN = 'new UiSelector().text("同期")'
        
        # Library functionality (Japanese)
        MY_BOOKS_TAB = "マイBook"
        
        # STUDY functionality (Japanese)
        DONE_BTN = 'new UiSelector().text("確定")'
    
    # Japanese version test data
    class TestData(BaseMonoxerTestData.CommonTestData):
        """Japanese version test data"""
        SEARCH_KEYWORD = "日本の祝日"



# Language configuration mapping
LANGUAGE_CONFIG_MAP = {
    "en": EnglishMonoxerTestData,
    "ja": JapaneseMonoxerTestData,
}

# Default to English version
MonoxerTestData = EnglishMonoxerTestData


def get_test_data(language: str = "en") -> type:
    """
    Get corresponding test data class based on language
    
    Args:
        language: Language code ("en", "ja")
        
    Returns:
        Corresponding test data class
    """
    return LANGUAGE_CONFIG_MAP.get(language, EnglishMonoxerTestData)



