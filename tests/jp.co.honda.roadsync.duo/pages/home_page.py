"""
Home Page Object
主页对象
"""

from appium.webdriver.common.appiumby import AppiumBy
from core.elements.page_object import PageObject
from core.utils.logger import Log


class HomePage(PageObject):
    """主页对象"""
    
    def _init_elements(self):
        """初始化页面元素"""
        # 欢迎消息
        self.add_element(
            "welcome_message",
            AppiumBy.ID,
            "com.honda.roadsync.duo:id/welcome_message",
            "Welcome Message"
        )
        
        # 车辆列表
        self.add_element(
            "vehicle_list",
            AppiumBy.ID,
            "com.honda.roadsync.duo:id/vehicle_list",
            "Vehicle List"
        )
        
        # 添加车辆按钮
        self.add_element(
            "add_vehicle_button",
            AppiumBy.ID,
            "com.honda.roadsync.duo:id/add_vehicle_button",
            "Add Vehicle Button"
        )
        
        # 设置按钮
        self.add_element(
            "settings_button",
            AppiumBy.ID,
            "com.honda.roadsync.duo:id/settings_button",
            "Settings Button"
        )
        
        # 用户头像
        self.add_element(
            "user_avatar",
            AppiumBy.ID,
            "com.honda.roadsync.duo:id/user_avatar",
            "User Avatar"
        )
        
        # 登出按钮
        self.add_element(
            "logout_button",
            AppiumBy.ID,
            "com.honda.roadsync.duo:id/logout_button",
            "Logout Button"
        )
        
        # 最近行程
        self.add_element(
            "recent_trips",
            AppiumBy.ID,
            "com.honda.roadsync.duo:id/recent_trips",
            "Recent Trips"
        )
        
        # 通知按钮
        self.add_element(
            "notifications_button",
            AppiumBy.ID,
            "com.honda.roadsync.duo:id/notifications_button",
            "Notifications Button"
        )
    
    def wait_for_page_load(self, timeout=None):
        """等待页面加载完成"""
        Log.info("Waiting for home page to load...")
        self.wait_for_element("welcome_message", timeout)
        self.wait_for_element("vehicle_list", timeout)
    
    def is_page_loaded(self) -> bool:
        """检查页面是否加载完成"""
        try:
            return (self.is_element_displayed("welcome_message") and
                    self.is_element_displayed("vehicle_list"))
        except Exception:
            return False
    
    def get_welcome_message(self) -> str:
        """
        获取欢迎消息
        
        Returns:
            str: 欢迎消息
        """
        try:
            return self.get_element_text("welcome_message")
        except Exception:
            return ""
    
    def click_add_vehicle(self):
        """点击添加车辆按钮"""
        Log.info("Clicking add vehicle button")
        self.click_element("add_vehicle_button")
    
    def click_settings(self):
        """点击设置按钮"""
        Log.info("Clicking settings button")
        self.click_element("settings_button")
    
    def click_user_avatar(self):
        """点击用户头像"""
        Log.info("Clicking user avatar")
        self.click_element("user_avatar")
    
    def logout(self):
        """执行登出操作"""
        Log.info("Performing logout")
        
        # 点击用户头像
        self.click_user_avatar()
        
        # 点击登出按钮
        self.click_element("logout_button")
        
        Log.info("Logout completed")
    
    def click_notifications(self):
        """点击通知按钮"""
        Log.info("Clicking notifications button")
        self.click_element("notifications_button")
    
    def get_vehicle_count(self) -> int:
        """
        获取车辆数量
        
        Returns:
            int: 车辆数量
        """
        try:
            vehicle_elements = self.find_elements(
                AppiumBy.XPATH,
                "//android.widget.ListView[@resource-id='com.honda.roadsync.duo:id/vehicle_list']/android.widget.ListItem"
            )
            return len(vehicle_elements)
        except Exception:
            return 0
    
    def select_vehicle(self, vehicle_index: int = 0):
        """
        选择车辆
        
        Args:
            vehicle_index: 车辆索引（默认为0，选择第一辆车）
        """
        Log.info(f"Selecting vehicle at index: {vehicle_index}")
        
        try:
            vehicle_elements = self.find_elements(
                AppiumBy.XPATH,
                "//android.widget.ListView[@resource-id='com.honda.roadsync.duo:id/vehicle_list']/android.widget.ListItem"
            )
            
            if vehicle_index < len(vehicle_elements):
                vehicle_elements[vehicle_index].click()
                Log.info(f"Selected vehicle at index {vehicle_index}")
            else:
                Log.warning(f"Vehicle index {vehicle_index} out of range")
                
        except Exception as e:
            Log.error(f"Failed to select vehicle: {str(e)}")
            raise
    
    def get_recent_trips_count(self) -> int:
        """
        获取最近行程数量
        
        Returns:
            int: 行程数量
        """
        try:
            trip_elements = self.find_elements(
                AppiumBy.XPATH,
                "//android.widget.ListView[@resource-id='com.honda.roadsync.duo:id/recent_trips']/android.widget.ListItem"
            )
            return len(trip_elements)
        except Exception:
            return 0
    
    def select_recent_trip(self, trip_index: int = 0):
        """
        选择最近行程
        
        Args:
            trip_index: 行程索引（默认为0，选择第一个行程）
        """
        Log.info(f"Selecting recent trip at index: {trip_index}")
        
        try:
            trip_elements = self.find_elements(
                AppiumBy.XPATH,
                "//android.widget.ListView[@resource-id='com.honda.roadsync.duo:id/recent_trips']/android.widget.ListItem"
            )
            
            if trip_index < len(trip_elements):
                trip_elements[trip_index].click()
                Log.info(f"Selected recent trip at index {trip_index}")
            else:
                Log.warning(f"Trip index {trip_index} out of range")
                
        except Exception as e:
            Log.error(f"Failed to select recent trip: {str(e)}")
            raise
    
    def is_vehicle_list_empty(self) -> bool:
        """
        检查车辆列表是否为空
        
        Returns:
            bool: 是否为空
        """
        return self.get_vehicle_count() == 0
    
    def is_recent_trips_empty(self) -> bool:
        """
        检查最近行程是否为空
        
        Returns:
            bool: 是否为空
        """
        return self.get_recent_trips_count() == 0
    
    def get_user_info(self) -> dict:
        """
        获取用户信息
        
        Returns:
            dict: 用户信息
        """
        try:
            # 点击用户头像获取用户信息
            self.click_user_avatar()
            
            # 这里应该获取用户信息页面的数据
            # 目前返回模拟数据
            user_info = {
                "username": "testuser@honda.com",
                "full_name": "Test User",
                "role": "Driver"
            }
            
            Log.info("Retrieved user info")
            return user_info
            
        except Exception as e:
            Log.error(f"Failed to get user info: {str(e)}")
            return {}
    
    def take_home_screenshot(self, name: str = "home_page"):
        """
        截取主页截图
        
        Args:
            name: 截图名称
        """
        self.take_screenshot(name)
