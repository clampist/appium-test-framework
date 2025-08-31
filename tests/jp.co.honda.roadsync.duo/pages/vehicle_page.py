"""
Vehicle Page Object
Vehicle page object
"""

from appium.webdriver.common.appiumby import AppiumBy
from core.elements.page_object import PageObject
from core.utils.logger import Log


class VehiclePage(PageObject):
    """Vehicle page object"""
    
    def _init_elements(self):
        """Initialize page elements"""
        # Vehicle name
        self.add_element(
            "vehicle_name",
            AppiumBy.ID,
            "com.honda.roadsync.duo:id/vehicle_name",
            "Vehicle Name"
        )
        
        # Vehicle status
        self.add_element(
            "vehicle_status",
            AppiumBy.ID,
            "com.honda.roadsync.duo:id/vehicle_status",
            "Vehicle Status"
        )
        
        # Start trip button
        self.add_element(
            "start_trip_button",
            AppiumBy.ID,
            "com.honda.roadsync.duo:id/start_trip_button",
            "Start Trip Button"
        )
        
        # Vehicle details button
        self.add_element(
            "vehicle_details_button",
            AppiumBy.ID,
            "com.honda.roadsync.duo:id/vehicle_details_button",
            "Vehicle Details Button"
        )
        
        # Back button
        self.add_element(
            "back_button",
            AppiumBy.ID,
            "com.honda.roadsync.duo:id/back_button",
            "Back Button"
        )
        
        # Vehicle image
        self.add_element(
            "vehicle_image",
            AppiumBy.ID,
            "com.honda.roadsync.duo:id/vehicle_image",
            "Vehicle Image"
        )
        
        # Vehicle info list
        self.add_element(
            "vehicle_info_list",
            AppiumBy.ID,
            "com.honda.roadsync.duo:id/vehicle_info_list",
            "Vehicle Info List"
        )
        
        # Edit vehicle button
        self.add_element(
            "edit_vehicle_button",
            AppiumBy.ID,
            "com.honda.roadsync.duo:id/edit_vehicle_button",
            "Edit Vehicle Button"
        )
        
        # Delete vehicle button
        self.add_element(
            "delete_vehicle_button",
            AppiumBy.ID,
            "com.honda.roadsync.duo:id/delete_vehicle_button",
            "Delete Vehicle Button"
        )
    
    def wait_for_page_load(self, timeout=None):
        """Wait for page to load completely"""
        Log.info("Waiting for vehicle page to load...")
        self.wait_for_element("vehicle_name", timeout)
        self.wait_for_element("vehicle_status", timeout)
        self.wait_for_element("start_trip_button", timeout)
    
    def is_page_loaded(self) -> bool:
        """Check if page is loaded completely"""
        try:
            return (self.is_element_displayed("vehicle_name") and
                    self.is_element_displayed("vehicle_status") and
                    self.is_element_displayed("start_trip_button"))
        except Exception:
            return False
    
    def get_vehicle_name(self) -> str:
        """
        Get vehicle name
        
        Returns:
            str: Vehicle name
        """
        try:
            return self.get_element_text("vehicle_name")
        except Exception:
            return ""
    
    def get_vehicle_status(self) -> str:
        """
        Get vehicle status
        
        Returns:
            str: Vehicle status
        """
        try:
            return self.get_element_text("vehicle_status")
        except Exception:
            return ""
    
    def start_trip(self):
        """Start trip"""
        Log.info("Starting trip")
        self.click_element("start_trip_button")
    
    def click_vehicle_details(self):
        """Click vehicle details"""
        Log.info("Clicking vehicle details")
        self.click_element("vehicle_details_button")
    
    def go_back(self):
        """Go back to previous page"""
        Log.info("Going back to previous page")
        self.click_element("back_button")
    
    def click_edit_vehicle(self):
        """Click edit vehicle"""
        Log.info("Clicking edit vehicle")
        self.click_element("edit_vehicle_button")
    
    def delete_vehicle(self):
        """Delete vehicle"""
        Log.info("Deleting vehicle")
        self.click_element("delete_vehicle_button")
    
    def is_vehicle_available(self) -> bool:
        """
        Check if vehicle is available
        
        Returns:
            bool: Whether available
        """
        try:
            status = self.get_vehicle_status().lower()
            return "available" in status or "ready" in status
        except Exception:
            return False
    
    def is_vehicle_in_use(self) -> bool:
        """
        Check if vehicle is in use
        
        Returns:
            bool: Whether in use
        """
        try:
            status = self.get_vehicle_status().lower()
            return "in use" in status or "active" in status
        except Exception:
            return False
    
    def is_vehicle_maintenance(self) -> bool:
        """
        Check if vehicle is under maintenance
        
        Returns:
            bool: Whether under maintenance
        """
        try:
            status = self.get_vehicle_status().lower()
            return "maintenance" in status or "repair" in status
        except Exception:
            return False
    
    def can_start_trip(self) -> bool:
        """
        Check if trip can be started
        
        Returns:
            bool: Whether trip can be started
        """
        try:
            return (self.is_element_enabled("start_trip_button") and 
                    self.is_vehicle_available())
        except Exception:
            return False
    
    def get_vehicle_info(self) -> dict:
        """
        Get vehicle information
        
        Returns:
            dict: Vehicle information
        """
        try:
            vehicle_info = {
                "name": self.get_vehicle_name(),
                "status": self.get_vehicle_status(),
                "available": self.is_vehicle_available(),
                "in_use": self.is_vehicle_in_use(),
                "maintenance": self.is_vehicle_maintenance()
            }
            
            Log.info("Retrieved vehicle info")
            return vehicle_info
            
        except Exception as e:
            Log.error(f"Failed to get vehicle info: {str(e)}")
            return {}
    
    def take_vehicle_screenshot(self, name: str = "vehicle_page"):
        """
        Take screenshot of vehicle page
        
        Args:
            name: Screenshot name
        """
        self.take_screenshot(name)
