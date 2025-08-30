"""
Test Data for Monoxer App
Monoxer应用测试数据
"""


class MonoxerTestData:
    """Monoxer应用测试数据类"""
    
    # 应用基本信息
    APP_PACKAGE = "com.monoxer"
    APP_ACTIVITY = "com.monoxer.view.main.MainActivity"
    WAIT_TIME = 15
    
    # 元素定位器
    class Locators:
        """元素定位器"""
        
        # 底部导航栏
        HOME_TAB = "com.monoxer:id/bottom_navigation_home_for_individuals"
        SEARCH_TAB = "com.monoxer:id/bottom_navigation_search"
        LIBRARY_TAB = "com.monoxer:id/bottom_navigation_library"
        
        # 侧边栏
        HEADER_SELECTOR = "com.monoxer:id/iOS_like_header_org_selector"
        INVITATION_CODE_BTN = 'new UiSelector().text("Enter invitation code")'
        SYNC_BTN = 'new UiSelector().text("Sync")'
        LINEAR_LAYOUT = "com.monoxer:id/linear_layout"
        
        # 搜索功能
        SEARCH_INPUT = "com.monoxer:id/search_src_text"
        SEARCH_VIEW = "com.monoxer:id/search_view"
        SEARCH_BAR = "com.monoxer:id/search_bar"
        CARD_VIEW = "com.monoxer:id/card_view"
        CONTENTS_BTN = "com.monoxer:id/contents"
        
        # Library功能
        MY_BOOKS_TAB = "My Books"
        AUTO_TEST_TITLE = '//android.widget.TextView[@resource-id="com.monoxer:id/word_books_book_title" and @text="auto_test"]'
        OPEN_DECK_BTN = "com.monoxer:id/open_deck"
        START_TEST_BTN = "com.monoxer:id/start_test"
        
        # STUDY功能
        CHOICE1_TEXT = "com.monoxer:id/choice1_text"
        DONE_BTN = 'new UiSelector().text("Done")'
        DONE_BTN_XPATH = '//android.widget.TextView[@resource-id="com.monoxer:id/label" and @text="Done"]'
        
        # 通用按钮
        NAVIGATE_UP = "Navigate up"
    
    # 测试数据
    class TestData:
        """测试数据"""
        
        # 搜索关键词
        SEARCH_KEYWORD = "日本の祝日"
        
        # 等待时间
        POPUP_TIMEOUT = 5
        PAGE_LOAD_TIMEOUT = 10
        STUDY_WAIT_TIME = 5
