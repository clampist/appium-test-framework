"""
Time Utilities
Time utility class, providing time-related functionality
"""

import time
from datetime import datetime, timedelta
from typing import Optional, Union
from dateutil import parser

from .logger import Log


class TimeUtils:
    """Time utility class"""
    
    @staticmethod
    def get_current_timestamp() -> float:
        """
        Get current timestamp
        
        Returns:
            float: Current timestamp
        """
        return time.time()
    
    @staticmethod
    def get_current_datetime() -> datetime:
        """
        Get current datetime
        
        Returns:
            datetime: Current datetime
        """
        return datetime.now()
    
    @staticmethod
    def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
        """
        Format datetime
        
        Args:
            dt: Datetime object
            format_str: Format string
            
        Returns:
            str: Formatted string
        """
        return dt.strftime(format_str)
    
    @staticmethod
    def parse_datetime(date_str: str) -> datetime:
        """
        Parse datetime string
        
        Args:
            date_str: Datetime string
            
        Returns:
            datetime: Datetime object
        """
        try:
            return parser.parse(date_str)
        except Exception as e:
            Log.error(f"Failed to parse datetime string '{date_str}': {str(e)}")
            raise
    
    @staticmethod
    def sleep(seconds: Union[int, float]):
        """
        Sleep for specified time
        
        Args:
            seconds: Sleep seconds
        """
        time.sleep(seconds)
    
    @staticmethod
    def wait_for_condition(condition_func, timeout: int = 30, interval: float = 0.5, 
                          condition_name: str = "condition"):
        """
        Wait for condition to be met
        
        Args:
            condition_func: Condition function, returns True when condition is met
            timeout: Timeout (seconds)
            interval: Check interval (seconds)
            condition_name: Condition name (for logging)
            
        Returns:
            bool: Whether condition is met
        """
        start_time = TimeUtils.get_current_timestamp()
        end_time = start_time + timeout
        
        Log.info(f"Waiting for {condition_name} (timeout: {timeout}s)")
        
        while TimeUtils.get_current_timestamp() < end_time:
            try:
                if condition_func():
                    Log.info(f"Condition '{condition_name}' met")
                    return True
            except Exception as e:
                Log.warning(f"Error checking condition '{condition_name}': {str(e)}")
            
            TimeUtils.sleep(interval)
        
        Log.error(f"Condition '{condition_name}' not met within {timeout}s")
        return False
    
    @staticmethod
    def get_time_difference(start_time: Union[datetime, float], 
                           end_time: Optional[Union[datetime, float]] = None) -> float:
        """
        Calculate time difference
        
        Args:
            start_time: Start time
            end_time: End time (optional, defaults to current time)
            
        Returns:
            float: Time difference (seconds)
        """
        if end_time is None:
            end_time = TimeUtils.get_current_timestamp()
        
        if isinstance(start_time, datetime):
            start_time = start_time.timestamp()
        
        if isinstance(end_time, datetime):
            end_time = end_time.timestamp()
        
        return end_time - start_time
    
    @staticmethod
    def format_duration(seconds: float) -> str:
        """
        Format duration
        
        Args:
            seconds: Seconds
            
        Returns:
            str: Formatted duration
        """
        if seconds < 60:
            return f"{seconds:.2f}s"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f}m"
        else:
            hours = seconds / 3600
            return f"{hours:.1f}h"
    
    @staticmethod
    def add_time(dt: datetime, **kwargs) -> datetime:
        """
        Add time to datetime
        
        Args:
            dt: Original datetime
            **kwargs: Time parameters to add (days, hours, minutes, seconds, etc.)
            
        Returns:
            datetime: New datetime
        """
        return dt + timedelta(**kwargs)
    
    @staticmethod
    def subtract_time(dt: datetime, **kwargs) -> datetime:
        """
        Subtract time from datetime
        
        Args:
            dt: Original datetime
            **kwargs: Time parameters to subtract (days, hours, minutes, seconds, etc.)
            
        Returns:
            datetime: New datetime
        """
        return dt - timedelta(**kwargs)
    
    @staticmethod
    def is_weekend(dt: datetime) -> bool:
        """
        Check if it's weekend
        
        Args:
            dt: Datetime
            
        Returns:
            bool: Whether it's weekend
        """
        return dt.weekday() >= 5
    
    @staticmethod
    def is_workday(dt: datetime) -> bool:
        """
        Check if it's workday
        
        Args:
            dt: Datetime
            
        Returns:
            bool: Whether it's workday
        """
        return dt.weekday() < 5
    
    @staticmethod
    def get_start_of_day(dt: datetime) -> datetime:
        """
        Get start of day (00:00:00)
        
        Args:
            dt: Datetime
            
        Returns:
            datetime: Start of day
        """
        return dt.replace(hour=0, minute=0, second=0, microsecond=0)
    
    @staticmethod
    def get_end_of_day(dt: datetime) -> datetime:
        """
        Get end of day (23:59:59)
        
        Args:
            dt: Datetime
            
        Returns:
            datetime: End of day
        """
        return dt.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    @staticmethod
    def get_start_of_week(dt: datetime) -> datetime:
        """
        Get start of week (Monday 00:00:00)
        
        Args:
            dt: Datetime
            
        Returns:
            datetime: Start of week
        """
        days_since_monday = dt.weekday()
        return TimeUtils.get_start_of_day(dt - timedelta(days=days_since_monday))
    
    @staticmethod
    def get_end_of_week(dt: datetime) -> datetime:
        """
        Get end of week (Sunday 23:59:59)
        
        Args:
            dt: Datetime
            
        Returns:
            datetime: End of week
        """
        days_until_sunday = 6 - dt.weekday()
        return TimeUtils.get_end_of_day(dt + timedelta(days=days_until_sunday))
    
    @staticmethod
    def get_start_of_month(dt: datetime) -> datetime:
        """
        Get start of month
        
        Args:
            dt: Datetime
            
        Returns:
            datetime: Start of month
        """
        return dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    @staticmethod
    def get_end_of_month(dt: datetime) -> datetime:
        """
        Get end of month
        
        Args:
            dt: Datetime
            
        Returns:
            datetime: End of month
        """
        # Get first day of next month, then subtract 1 day
        if dt.month == 12:
            next_month = dt.replace(year=dt.year + 1, month=1, day=1)
        else:
            next_month = dt.replace(month=dt.month + 1, day=1)
        
        return TimeUtils.get_end_of_day(next_month - timedelta(days=1))
    
    @staticmethod
    def is_same_day(dt1: datetime, dt2: datetime) -> bool:
        """
        Check if two dates are the same day
        
        Args:
            dt1: First datetime
            dt2: Second datetime
            
        Returns:
            bool: Whether same day
        """
        return dt1.date() == dt2.date()
    
    @staticmethod
    def is_same_week(dt1: datetime, dt2: datetime) -> bool:
        """
        Check if two dates are the same week
        
        Args:
            dt1: First datetime
            dt2: Second datetime
            
        Returns:
            bool: Whether same week
        """
        start1 = TimeUtils.get_start_of_week(dt1)
        start2 = TimeUtils.get_start_of_week(dt2)
        return start1.date() == start2.date()
    
    @staticmethod
    def is_same_month(dt1: datetime, dt2: datetime) -> bool:
        """
        Check if two dates are the same month
        
        Args:
            dt1: First datetime
            dt2: Second datetime
            
        Returns:
            bool: Whether same month
        """
        return dt1.year == dt2.year and dt1.month == dt2.month
