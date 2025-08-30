"""
Vehicle Page Object
车辆页面对象
"""

from appium.webdriver.common.appiumby import AppiumBy
from core.elements.page_object import PageObject
from core.utils.logger import Log


class VehiclePage(PageObject):
    """车辆页面对象"""
    
    def _init_elements(self):
        """初始化页面元素"""
        # 车辆名称
        self.add_element(
            "vehicle_name",
            AppiumBy.ID,
            "com.honda.roadsync.duo:id/vehicle_name",
            "Vehicle Name"
        )
        
        # 车辆状态
        self.add_element(
            "vehicle_status",
            AppiumBy.ID,
            "com.honda.roadsync.duo:id/vehicle_status",
            "Vehicle Status"
        )
        
        # 开始行程按钮
        self.add_element(
            "start_trip_button",
            AppiumBy.ID,
            "com.honda.roadsync.duo:id/start_trip_button",
            "Start Trip Button"
        )
        
        # 车辆详情按钮
        self.add_element(
            "vehicle_details_button",
            AppiumBy.ID,
            "com.honda.roadsync.duo:id/vehicle_details_button",
            "Vehicle Details Button"
        )
        
        # 返回按钮
        self.add_element(
            "back_button",
            AppiumBy.ID,
            "com.honda.roadsync.duo:id/back_button",
            "Back Button"
        )
        
        # 车辆图片
        self.add_element(
            "vehicle_image",
            AppiumBy.ID,
            "com.honda.roadsync.duo:id/vehicle_image",
            "Vehicle Image"
        )
        
        # 车辆信息列表
        self.add_element(
            "vehicle_info_list",
            AppiumBy.ID,
            "com.honda.roadsync.duo:id/vehicle_info_list",
            "Vehicle Info List"
        )
        
        # 编辑车辆按钮
        self.add_element(
            "edit_vehicle_button",
            AppiumBy.ID,
            "com.honda.roadsync.duo:id/edit_vehicle_button",
            "Edit Vehicle Button"
        )
        
        # 删除车辆按钮
        self.add_element(
            "delete_vehicle_button",
            AppiumBy.ID,
            "com.honda.roadsync.duo:id/delete_vehicle_button",
            "Delete Vehicle Button"
        )
    
    def wait_for_page_load(self, timeout=None):
        """等待页面加载完成"""
        Log.info("Waiting for vehicle page to load...")
        self.wait_for_element("vehicle_name", timeout)
        self.wait_for_element("vehicle_status", timeout)
        self.wait_for_element("start_trip_button", timeout)
    
    def is_page_loaded(self) -> bool:
        """检查页面是否加载完成"""
        try:
            return (self.is_element_displayed("vehicle_name") and
                    self.is_element_displayed("vehicle_status") and
                    self.is_element_displayed("start_trip_button"))
        except Exception:
            return False
    
    def get_vehicle_name(self) -> str:
        """
        获取车辆名称
        
        Returns:
            str: 车辆名称
        """
        try:
            return self.get_element_text("vehicle_name")
        except Exception:
            return ""
    
    def get_vehicle_status(self) -> str:
        """
        获取车辆状态
        
        Returns:
            str: 车辆状态
        """
        try:
            return self.get_element_text("vehicle_status")
        except Exception:
            return ""
    
    def start_trip(self):
        """开始行程"""
        Log.info("Starting trip")
        self.click_element("start_trip_button")
    
    def click_vehicle_details(self):
        """点击车辆详情"""
        Log.info("Clicking vehicle details")
        self.click_element("vehicle_details_button")
    
    def go_back(self):
        """返回上一页"""
        Log.info("Going back to previous page")
        self.click_element("back_button")
    
    def click_edit_vehicle(self):
        """点击编辑车辆"""
        Log.info("Clicking edit vehicle")
        self.click_element("edit_vehicle_button")
    
    def delete_vehicle(self):
        """删除车辆"""
        Log.info("Deleting vehicle")
        self.click_element("delete_vehicle_button")
    
    def is_vehicle_available(self) -> bool:
        """
        检查车辆是否可用
        
        Returns:
            bool: 是否可用
        """
        try:
            status = self.get_vehicle_status().lower()
            return "available" in status or "ready" in status
        except Exception:
            return False
    
    def is_vehicle_in_use(self) -> bool:
        """
        检查车辆是否正在使用中
        
        Returns:
            bool: 是否正在使用
        """
        try:
            status = self.get_vehicle_status().lower()
            return "in use" in status or "active" in status
        except Exception:
            return False
    
    def is_vehicle_maintenance(self) -> bool:
        """
        检查车辆是否在维护中
        
        Returns:
            bool: 是否在维护
        """
        try:
            status = self.get_vehicle_status().lower()
            return "maintenance" in status or "repair" in status
        except Exception:
            return False
    
    def can_start_trip(self) -> bool:
        """
        检查是否可以开始行程
        
        Returns:
            bool: 是否可以开始行程
        """
        try:
            return (self.is_element_enabled("start_trip_button") and 
                    self.is_vehicle_available())
        except Exception:
            return False
    
    def get_vehicle_info(self) -> dict:
        """
        获取车辆信息
        
        Returns:
            dict: 车辆信息
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
        截取车辆页面截图
        
        Args:
            name: 截图名称
        """
        self.take_screenshot(name)
