"""
Video Page Object for TikTok App
"""

import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from core.elements.page_object import PageObject
from core.utils.logger import Log
from datas.test_data import BaseTikTokTestData


class VideoPage(PageObject):
    """Video page object for TikTok App - handles all video-related operations"""
    
    def __init__(self, driver, test_data=None):
        super().__init__(driver)
        self.test_data = test_data or BaseTikTokTestData()
        self.wait = WebDriverWait(driver, self.test_data.WAIT_TIME)
    
    def swipe_to_next_video(self) -> bool:
        """Swipe up to next video"""
        try:
            screen_size = self.driver.get_window_size()
            start_x = screen_size['width'] * 0.5
            start_y = screen_size['height'] * 0.8
            end_y = screen_size['height'] * 0.2
            
            self.driver.swipe(start_x, start_y, start_x, end_y, 500)
            Log.info("Swiped to next video")
            time.sleep(self.test_data.CommonTestData.VIDEO_WAIT_TIME)
            return True
        except Exception as e:
            Log.error(f"Failed to swipe to next video: {str(e)}")
            return False
    
    def swipe_to_previous_video(self) -> bool:
        """Swipe down to previous video"""
        try:
            screen_size = self.driver.get_window_size()
            start_x = screen_size['width'] * 0.5
            start_y = screen_size['height'] * 0.2
            end_y = screen_size['height'] * 0.8
            
            self.driver.swipe(start_x, start_y, start_x, end_y, 500)
            Log.info("Swiped to previous video")
            time.sleep(self.test_data.CommonTestData.VIDEO_WAIT_TIME)
            return True
        except Exception as e:
            Log.error(f"Failed to swipe to previous video: {str(e)}")
            return False
    
    def wait_for_video_load(self, timeout: int = 10) -> bool:
        """Wait for video to load"""
        try:
            # Wait for video controls to appear
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((AppiumBy.ID, self.test_data.CommonLocators.LIKE_BTN))
            )
            Log.info("Video loaded successfully")
            return True
        except Exception as e:
            Log.error(f"Video failed to load: {str(e)}")
            return False