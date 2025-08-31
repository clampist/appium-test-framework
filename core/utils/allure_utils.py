"""
Allure Report Utilities
Tools for integrating screenshots and other attachments with Allure reports
"""

import os
import allure
from datetime import datetime
from typing import Optional
from pathlib import Path

from core.utils.screenshot_utils import ScreenshotUtils
from core.utils.logger import Log


class AllureUtils:
    """Allure report utility class"""
    
    @staticmethod
    def attach_screenshot(driver, name: str = "Screenshot", description: str = None) -> None:
        """
        Attach screenshot to Allure report
        
        Args:
            driver: Appium driver instance
            name: Screenshot name
            description: Screenshot description
        """
        try:
            # Take screenshot
            screenshot_path = ScreenshotUtils.save_screenshot(
                driver, 
                "com.monoxer", 
                name.lower().replace(" ", "_"), 
                datetime.now().strftime("%H%M%S")
            )
            
            # Attach to Allure report
            with open(screenshot_path, "rb") as f:
                allure.attach(
                    f.read(),
                    name=name,
                    attachment_type=allure.attachment_type.PNG
                )
            
            Log.info(f"Screenshot attached to Allure report: {name}")
            
        except Exception as e:
            Log.error(f"Failed to attach screenshot to Allure report: {str(e)}")
    
    @staticmethod
    def attach_page_source(driver, name: str = "Page Source", description: str = None) -> None:
        """
        Attach page source to Allure report
        
        Args:
            driver: Appium driver instance
            name: Attachment name
            description: Attachment description
        """
        try:
            page_source = driver.page_source
            
            allure.attach(
                page_source,
                name=name,
                attachment_type=allure.attachment_type.XML
            )
            
            Log.info(f"Page source attached to Allure report: {name}")
            
        except Exception as e:
            Log.error(f"Failed to attach page source to Allure report: {str(e)}")
    
    @staticmethod
    def attach_logs(log_content: str, name: str = "Test Logs", description: str = None) -> None:
        """
        Attach logs to Allure report
        
        Args:
            log_content: Log content to attach
            name: Attachment name
            description: Attachment description
        """
        try:
            allure.attach(
                log_content,
                name=name,
                attachment_type=allure.attachment_type.TEXT
            )
            
            Log.info(f"Logs attached to Allure report: {name}")
            
        except Exception as e:
            Log.error(f"Failed to attach logs to Allure report: {str(e)}")
    
    @staticmethod
    def attach_config(config_data: dict, name: str = "Test Configuration", description: str = None) -> None:
        """
        Attach configuration to Allure report
        
        Args:
            config_data: Configuration data to attach
            name: Attachment name
            description: Attachment description
        """
        try:
            import json
            
            config_json = json.dumps(config_data, indent=2, ensure_ascii=False)
            
            allure.attach(
                config_json,
                name=name,
                attachment_type=allure.attachment_type.JSON
            )
            
            Log.info(f"Configuration attached to Allure report: {name}")
            
        except Exception as e:
            Log.error(f"Failed to attach configuration to Allure report: {str(e)}")
    
    @staticmethod
    def add_step(step_name: str, step_description: str = None):
        """
        Add step to Allure report
        
        Args:
            step_name: Step name
            step_description: Step description
        """
        return allure.step(step_name, description=step_description)
    
    @staticmethod
    def add_severity(severity: str):
        """
        Add severity to Allure report
        
        Args:
            severity: Severity level (blocker, critical, normal, minor, trivial)
        """
        return allure.severity(severity)
    
    @staticmethod
    def add_feature(feature_name: str):
        """
        Add feature to Allure report
        
        Args:
            feature_name: Feature name
        """
        return allure.feature(feature_name)
    
    @staticmethod
    def add_story(story_name: str):
        """
        Add story to Allure report
        
        Args:
            story_name: Story name
        """
        return allure.story(story_name)
    
    @staticmethod
    def add_epic(epic_name: str):
        """
        Add epic to Allure report
        
        Args:
            epic_name: Epic name
        """
        return allure.epic(epic_name)
    
    @staticmethod
    def add_description(description: str, description_type: str = "text"):
        """
        Add description to Allure report
        
        Args:
            description: Description content
            description_type: Description type ("text", "html", "markdown")
        """
        return allure.description(description, description_type=description_type)
    
    @staticmethod
    def add_link(url: str, name: str = None, link_type: str = "link"):
        """
        Add link to Allure report
        
        Args:
            url: Link URL
            name: Link name
            link_type: Link type ("link", "issue", "test_case")
        """
        return allure.link(url, name, link_type)
    
    @staticmethod
    def add_parameter(name: str, value: str):
        """
        Add parameter to Allure report
        
        Args:
            name: Parameter name
            value: Parameter value
        """
        # Use dynamic parameter instead
        return allure.dynamic.parameter(name, value)
    
    @staticmethod
    def add_tag(tag: str):
        """
        Add tag to Allure report
        
        Args:
            tag: Tag name
        """
        return allure.tag(tag)


def attach_screenshot_on_failure(driver, test_name: str = "Test Failure"):
    """
    Convenience function to attach screenshot on test failure
    
    Args:
        driver: Appium driver instance
        test_name: Test name for screenshot
    """
    AllureUtils.attach_screenshot(
        driver, 
        f"{test_name} - Failure Screenshot",
        f"Screenshot taken when test '{test_name}' failed"
    )


def attach_page_source_on_failure(driver, test_name: str = "Test Failure"):
    """
    Convenience function to attach page source on test failure
    
    Args:
        driver: Appium driver instance
        test_name: Test name for attachment
    """
    AllureUtils.attach_page_source(
        driver,
        f"{test_name} - Page Source",
        f"Page source when test '{test_name}' failed"
    )
