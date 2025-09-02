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
    
    def click_like_button(self) -> bool:
        """Click like button on video"""
        try:
            like_btn = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ID, self.test_data.CommonLocators.LIKE_BTN)
            ))
            like_btn.click()
            Log.info("Clicked like button on video")
            time.sleep(1)
            return True
        except Exception as e:
            Log.error(f"Failed to click like button: {str(e)}")
            return False
    
    def click_comment_button(self) -> bool:
        """Click comment button on video"""
        try:
            comment_btn = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ID, self.test_data.CommonLocators.COMMENT_BTN)
            ))
            comment_btn.click()
            Log.info("Clicked comment button on video")
            time.sleep(self.test_data.CommonTestData.ANIMATION_WAIT_TIME)
            return True
        except Exception as e:
            Log.error(f"Failed to click comment button: {str(e)}")
            return False
    
    def click_share_button(self) -> bool:
        """Click share button on video"""
        try:
            share_btn = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ID, self.test_data.CommonLocators.SHARE_BTN)
            ))
            share_btn.click()
            Log.info("Clicked share button on video")
            time.sleep(self.test_data.CommonTestData.ANIMATION_WAIT_TIME)
            return True
        except Exception as e:
            Log.error(f"Failed to click share button: {str(e)}")
            return False
    
    def click_bookmark_button(self) -> bool:
        """Click bookmark button on video"""
        try:
            bookmark_btn = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ID, self.test_data.CommonLocators.BOOKMARK_BTN)
            ))
            bookmark_btn.click()
            Log.info("Clicked bookmark button on video")
            time.sleep(1)
            return True
        except Exception as e:
            Log.error(f"Failed to click bookmark button: {str(e)}")
            return False
    
    def click_close_button(self) -> bool:
        """Click close button to exit video"""
        try:
            close_btn = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ID, self.test_data.CommonLocators.CLOSE_BTN)
            ))
            close_btn.click()
            Log.info("Clicked close button")
            time.sleep(self.test_data.CommonTestData.ANIMATION_WAIT_TIME)
            return True
        except Exception as e:
            Log.error(f"Failed to click close button: {str(e)}")
            return False
    
    def click_back_button(self) -> bool:
        """Click back button to return from video"""
        try:
            back_btn = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.ID, self.test_data.CommonLocators.BACK_BTN)
            ))
            back_btn.click()
            Log.info("Clicked back button")
            time.sleep(self.test_data.CommonTestData.ANIMATION_WAIT_TIME)
            return True
        except Exception as e:
            Log.error(f"Failed to click back button: {str(e)}")
            return False
    
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
    
    def is_video_playing(self) -> bool:
        """Check if video is playing"""
        try:
            # Wait for video player elements to be present
            self.wait.until(EC.presence_of_element_located(
                (AppiumBy.ID, self.test_data.CommonLocators.LIKE_BTN)
            ))
            Log.info("Video is playing")
            return True
        except Exception as e:
            Log.error(f"Video not playing: {str(e)}")
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
    
    def double_tap_to_like(self) -> bool:
        """Double tap on video to like (alternative to like button)"""
        try:
            screen_size = self.driver.get_window_size()
            center_x = screen_size['width'] * 0.5
            center_y = screen_size['height'] * 0.5
            
            # Perform double tap
            self.driver.tap([(center_x, center_y)], 2)
            Log.info("Double tapped video to like")
            time.sleep(1)
            return True
        except Exception as e:
            Log.error(f"Failed to double tap video: {str(e)}")
            return False
    
    def long_press_video(self, duration: int = 2000) -> bool:
        """Long press on video (for additional options)"""
        try:
            screen_size = self.driver.get_window_size()
            center_x = screen_size['width'] * 0.5
            center_y = screen_size['height'] * 0.5
            
            # Perform long press
            self.driver.long_press(center_x, center_y, duration)
            Log.info(f"Long pressed video for {duration}ms")
            time.sleep(1)
            return True
        except Exception as e:
            Log.error(f"Failed to long press video: {str(e)}")
            return False
    
    def get_video_duration(self) -> str:
        """Get video duration text if available"""
        try:
            # Try to find duration element (this would need to be added to test_data)
            duration_element = self.wait.until(EC.presence_of_element_located(
                (AppiumBy.CLASS_NAME, "android.widget.TextView")
            ))
            duration = duration_element.text
            Log.info(f"Video duration: {duration}")
            return duration
        except Exception as e:
            Log.warning(f"Could not get video duration: {str(e)}")
            return ""
    
    def is_video_muted(self) -> bool:
        """Check if video is muted"""
        try:
            # This would need a mute indicator element in test_data
            # For now, return False as placeholder
            Log.info("Video mute status check not implemented yet")
            return False
        except Exception as e:
            Log.warning(f"Could not check video mute status: {str(e)}")
            return False

