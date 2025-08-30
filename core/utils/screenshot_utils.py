"""
Screenshot Utilities
截图工具类，提供截图管理、对比等功能
"""

import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Tuple
from PIL import Image, ImageChops

from .logger import Log


class ScreenshotUtils:
    """Screenshot utility class"""
    
    @staticmethod
    def _get_screenshot_dirs(app_package: str) -> tuple:
        """
        Get screenshot directory paths
        
        Args:
            app_package: Application package name
            
        Returns:
            tuple: (base_dir, cur_dir)
        """
        base_dir = f"tests/{app_package}/screenshots/base"
        cur_dir = f"tests/{app_package}/screenshots/cur"
        return base_dir, cur_dir
    
    @staticmethod
    def save_screenshot(driver, app_package: str, name: str = "screenshot", step_num: str = "01") -> str:
        """
        Save screenshot to cur directory
        
        Args:
            driver: Appium driver instance
            app_package: Application package name
            name: Screenshot name
            step_num: Step number
            
        Returns:
            str: Screenshot file path
        """
        try:
            # Get screenshot directory
            _, screenshot_dir = ScreenshotUtils._get_screenshot_dirs(app_package)
            
            os.makedirs(screenshot_dir, exist_ok=True)
            
            now = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"{screenshot_dir}/{now}_{step_num}_{name}.png"
            driver.take_screenshot(screenshot_path)
            
            Log.info(f"Screenshot saved: {screenshot_path}")
            return screenshot_path
            
        except Exception as e:
            Log.error(f"Failed to save screenshot: {str(e)}")
            raise
    
    @staticmethod
    def clear_screenshot_directory(app_package: str) -> bool:
        """
        Clear current screenshot directory
        
        Args:
            app_package: Application package name
            
        Returns:
            bool: Success status
        """
        _, screenshot_dir = ScreenshotUtils._get_screenshot_dirs(app_package)
        
        try:
            if os.path.exists(screenshot_dir):
                shutil.rmtree(screenshot_dir)
                Log.info(f"Cleared screenshot directory: {screenshot_dir}")
            else:
                Log.info(f"Screenshot directory does not exist: {screenshot_dir}")
                # Create directory
                os.makedirs(screenshot_dir, exist_ok=True)
                Log.info(f"Created screenshot directory: {screenshot_dir}")
            return True
        except Exception as e:
            Log.error(f"Failed to clear screenshot directory: {str(e)}")
            return False
    
    @staticmethod
    def compare_screenshots(app_package: str) -> Tuple[bool, List[str], List[str]]:
        """
        Compare screenshots between base and cur directories
        
        Args:
            app_package: Application package name
            
        Returns:
            Tuple[bool, List[str], List[str]]: (all identical, identical files list, different files list)
        """
        base_dir, cur_dir = ScreenshotUtils._get_screenshot_dirs(app_package)
        
        if not os.path.exists(base_dir):
            Log.info(f"Base directory does not exist: {base_dir}")
            return False, [], []
        
        if not os.path.exists(cur_dir):
            Log.info(f"Current directory does not exist: {cur_dir}")
            return False, [], []
        
        base_files = set(os.listdir(base_dir))
        cur_files = set(os.listdir(cur_dir))
        
        # Extract step numbers and names from filenames (remove timestamp)
        def extract_step_info(filename):
            """Extract step number and name from filename"""
            if not filename.endswith('.png'):
                return None
            parts = filename.split('_')
            if len(parts) >= 3:
                # Format: timestamp_step_name.png
                step_num = parts[1]
                name = '_'.join(parts[2:]).replace('.png', '')
                return f"{step_num}_{name}.png"
            return None
        
        # Create mapping of step info to filenames
        base_step_files = {}
        cur_step_files = {}
        
        for filename in base_files:
            step_info = extract_step_info(filename)
            if step_info:
                base_step_files[step_info] = filename
        
        for filename in cur_files:
            step_info = extract_step_info(filename)
            if step_info:
                cur_step_files[step_info] = filename
        
        # Find common step files
        common_steps = set(base_step_files.keys()).intersection(set(cur_step_files.keys()))
        
        if not common_steps:
            Log.info("No common screenshot files found for comparison")
            return False, [], []
        
        Log.info(f"Comparing {len(common_steps)} screenshot files...")
        
        differences = []
        identical = []
        
        for step_info in sorted(common_steps):
            base_filename = base_step_files[step_info]
            cur_filename = cur_step_files[step_info]
            
            base_path = os.path.join(base_dir, base_filename)
            cur_path = os.path.join(cur_dir, cur_filename)
            
            try:
                # Load images
                base_img = Image.open(base_path)
                cur_img = Image.open(cur_path)
                
                # Compare images
                if base_img.size != cur_img.size:
                    differences.append(f"Size mismatch: {step_info}")
                    Log.warning(f"Size mismatch: {step_info}")
                    continue
                
                # Convert to same mode
                if base_img.mode != cur_img.mode:
                    base_img = base_img.convert(cur_img.mode)
                
                # Calculate difference
                diff = ImageChops.difference(base_img, cur_img)
                
                if diff.getbbox() is None:
                    identical.append(step_info)
                    Log.info(f"✅ {step_info} - Identical")
                else:
                    differences.append(step_info)
                    Log.warning(f"❌ {step_info} - Different")
                    
            except Exception as e:
                differences.append(f"Error comparing {step_info}: {str(e)}")
                Log.error(f"Error comparing {step_info}: {str(e)}")
        
        Log.info(f"Comparison Summary: Identical: {len(identical)}, Different: {len(differences)}")
        
        if differences:
            Log.warning("Differences found in screenshots")
            return False, identical, differences
        else:
            Log.info("All screenshots are identical!")
            return True, identical, differences
    
    @staticmethod
    def set_base_screenshots(app_package: str) -> bool:
        """
        Set current screenshots as base screenshots
        
        Args:
            app_package: Application package name
            
        Returns:
            bool: Success status
        """
        base_dir, cur_dir = ScreenshotUtils._get_screenshot_dirs(app_package)
        
        # Check if base directory is empty
        if os.path.exists(base_dir) and os.listdir(base_dir):
            Log.warning(f"Base directory is not empty: {base_dir}")
            Log.warning("Cannot auto-set base screenshots. Please clear base directory first.")
            return False
        
        if not os.path.exists(cur_dir):
            Log.error(f"Current directory does not exist: {cur_dir}")
            return False
        
        cur_files = os.listdir(cur_dir)
        if not cur_files:
            Log.error(f"Current directory is empty: {cur_dir}")
            return False
        
        try:
            # Create base directory
            os.makedirs(base_dir, exist_ok=True)
            
            # Copy all files from cur to base
            for filename in cur_files:
                src = os.path.join(cur_dir, filename)
                dst = os.path.join(base_dir, filename)
                shutil.copy2(src, dst)
            
            Log.info(f"Set {len(cur_files)} screenshots as base screenshots")
            return True
            
        except Exception as e:
            Log.error(f"Failed to set base screenshots: {str(e)}")
            return False
    
    @staticmethod
    def clear_base_screenshots(app_package: str) -> bool:
        """
        Clear base screenshots directory
        
        Args:
            app_package: Application package name
            
        Returns:
            bool: Success status
        """
        base_dir, _ = ScreenshotUtils._get_screenshot_dirs(app_package)
        
        try:
            if os.path.exists(base_dir):
                shutil.rmtree(base_dir)
                Log.info(f"Cleared base screenshots directory: {base_dir}")
            else:
                Log.info(f"Base directory does not exist: {base_dir}")
            return True
        except Exception as e:
            Log.error(f"Failed to clear base directory: {str(e)}")
            return False
    
    @staticmethod
    def auto_set_base_if_successful(app_package: str) -> bool:
        """
        Auto set base screenshots if all tests are successful and base is empty
        
        Args:
            app_package: Application package name
            
        Returns:
            bool: Success status
        """
        base_dir, cur_dir = ScreenshotUtils._get_screenshot_dirs(app_package)
        
        # Check if base directory is empty
        if os.path.exists(base_dir) and os.listdir(base_dir):
            Log.info("Base directory is not empty, skipping auto-set")
            return False
        
        # Check if cur directory has screenshots
        if not os.path.exists(cur_dir) or not os.listdir(cur_dir):
            Log.info("Current directory is empty, skipping auto-set")
            return False
        
        Log.info("Auto-setting base screenshots...")
        return ScreenshotUtils.set_base_screenshots(app_package)
