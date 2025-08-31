"""
Home Page Object
Home page object
"""

from appium.webdriver.common.appiumby import AppiumBy
from core.elements.page_object import PageObject
from core.utils.logger import Log


class HomePage(PageObject):
    """Home page object"""
    
    def _init_elements(self):
        """Initialize page elements"""
        # Welcome message
        self.add_element(
            "welcome_message",
            AppiumBy.ID,
            "com.honda.roadsync.duo:id/welcome_message",
            "Welcome Message"
        )
        
        # Vehicle list
        self.add_element(
            "vehicle_list",
            AppiumBy.ID,
            "com.honda.roadsync.duo:id/vehicle_list",
            "Vehicle List"
        )
        
        # Add vehicle button
        self.add_element(
            "add_vehicle_button",
            AppiumBy.ID,
            "com.honda.roadsync.duo:id/add_vehicle_button",
            "Add Vehicle Button"
        )
        
        # Settings button
        self.add_element(
            "settings_button",
            AppiumBy.ID,
            "com.honda.roadsync.duo:id/settings_button",
            "Settings Button"
        )
        
        # User avatar
        self.add_element(
            "user_avatar",
            AppiumBy.ID,
            "com.honda.roadsync.duo:id/user_avatar",
            "User Avatar"
        )
        
        # Logout button
        self.add_element(
            "logout_button",
            AppiumBy.ID,
            "com.honda.roadsync.duo:id/logout_button",
            "Logout Button"
        )
        
        # Recent trips
        self.add_element(
            "recent_trips",
            AppiumBy.ID,
            "com.honda.roadsync.duo:id/recent_trips",
            "Recent Trips"
        )
        
        # Notifications button
        self.add_element(
            "notifications_button",
            AppiumBy.ID,
            "com.honda.roadsync.duo:id/notifications_button",
            "Notifications Button"
        )
    
    def wait_for_page_load(self, timeout=None):
        """Wait for page to load completely"""
        Log.info("Waiting for home page to load...")
        self.wait_for_element("welcome_message", timeout)
        self.wait_for_element("vehicle_list", timeout)
    
    def is_page_loaded(self) -> bool:
        """Check if page is loaded completely"""
        try:
            return (self.is_element_displayed("welcome_message") and
                    self.is_element_displayed("vehicle_list"))
        except Exception:
            return False
    
    def get_welcome_message(self) -> str:
        """
        Get welcome message
        
        Returns:
            str: Welcome message
        """
        try:
            return self.get_element_text("welcome_message")
        except Exception:
            return ""
    
    def click_add_vehicle(self):
        """Click add vehicle button"""
        Log.info("Clicking add vehicle button")
        self.click_element("add_vehicle_button")
    
    def click_settings(self):
        """Click settings button"""
        Log.info("Clicking settings button")
        self.click_element("settings_button")
    
    def click_user_avatar(self):
        """Click user avatar"""
        Log.info("Clicking user avatar")
        self.click_element("user_avatar")
    
    def logout(self):
        """Perform logout operation"""
        Log.info("Performing logout")
        
        # Click user avatar
        self.click_user_avatar()
        
        # Click logout button
        self.click_element("logout_button")
        
        Log.info("Logout completed")
    
    def click_notifications(self):
        """Click notifications button"""
        Log.info("Clicking notifications button")
        self.click_element("notifications_button")
    
    def get_vehicle_count(self) -> int:
        """
        Get vehicle count
        
        Returns:
            int: Vehicle count
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
        Select vehicle
        
        Args:
            vehicle_index: Vehicle index (default 0, select first vehicle)
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
        Get recent trips count
        
        Returns:
            int: Trip count
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
        Select recent trip
        
        Args:
            trip_index: Trip index (default 0, select first trip)
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
        Check if vehicle list is empty
        
        Returns:
            bool: Whether empty
        """
        return self.get_vehicle_count() == 0
    
    def is_recent_trips_empty(self) -> bool:
        """
        Check if recent trips is empty
        
        Returns:
            bool: Whether empty
        """
        return self.get_recent_trips_count() == 0
    
    def get_user_info(self) -> dict:
        """
        Get user information
        
        Returns:
            dict: User information
        """
        try:
            # Click user avatar to get user info
            self.click_user_avatar()
            
            # Should get user info page data here
            # Currently return mock data
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
        Take home page screenshot
        
        Args:
            name: Screenshot name
        """
        self.take_screenshot(name)
