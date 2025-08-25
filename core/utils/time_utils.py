"""
Time Utilities
时间工具类，提供时间相关的功能
"""

import time
from datetime import datetime, timedelta
from typing import Optional, Union
from dateutil import parser

from .logger import Log


class TimeUtils:
    """时间工具类"""
    
    @staticmethod
    def get_current_timestamp() -> float:
        """
        获取当前时间戳
        
        Returns:
            float: 当前时间戳
        """
        return time.time()
    
    @staticmethod
    def get_current_datetime() -> datetime:
        """
        获取当前日期时间
        
        Returns:
            datetime: 当前日期时间
        """
        return datetime.now()
    
    @staticmethod
    def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
        """
        格式化日期时间
        
        Args:
            dt: 日期时间对象
            format_str: 格式化字符串
            
        Returns:
            str: 格式化后的字符串
        """
        return dt.strftime(format_str)
    
    @staticmethod
    def parse_datetime(date_str: str) -> datetime:
        """
        解析日期时间字符串
        
        Args:
            date_str: 日期时间字符串
            
        Returns:
            datetime: 日期时间对象
        """
        try:
            return parser.parse(date_str)
        except Exception as e:
            Log.error(f"Failed to parse datetime string '{date_str}': {str(e)}")
            raise
    
    @staticmethod
    def sleep(seconds: Union[int, float]):
        """
        睡眠指定时间
        
        Args:
            seconds: 睡眠秒数
        """
        time.sleep(seconds)
    
    @staticmethod
    def wait_for_condition(condition_func, timeout: int = 30, interval: float = 0.5, 
                          condition_name: str = "condition"):
        """
        等待条件满足
        
        Args:
            condition_func: 条件函数，返回True表示条件满足
            timeout: 超时时间（秒）
            interval: 检查间隔（秒）
            condition_name: 条件名称（用于日志）
            
        Returns:
            bool: 条件是否满足
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
        计算时间差
        
        Args:
            start_time: 开始时间
            end_time: 结束时间（可选，默认为当前时间）
            
        Returns:
            float: 时间差（秒）
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
        格式化持续时间
        
        Args:
            seconds: 秒数
            
        Returns:
            str: 格式化后的持续时间
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
        给日期时间添加时间
        
        Args:
            dt: 原始日期时间
            **kwargs: 要添加的时间参数（days, hours, minutes, seconds等）
            
        Returns:
            datetime: 新的日期时间
        """
        return dt + timedelta(**kwargs)
    
    @staticmethod
    def subtract_time(dt: datetime, **kwargs) -> datetime:
        """
        从日期时间减去时间
        
        Args:
            dt: 原始日期时间
            **kwargs: 要减去的时间参数（days, hours, minutes, seconds等）
            
        Returns:
            datetime: 新的日期时间
        """
        return dt - timedelta(**kwargs)
    
    @staticmethod
    def is_weekend(dt: datetime) -> bool:
        """
        检查是否为周末
        
        Args:
            dt: 日期时间
            
        Returns:
            bool: 是否为周末
        """
        return dt.weekday() >= 5
    
    @staticmethod
    def is_workday(dt: datetime) -> bool:
        """
        检查是否为工作日
        
        Args:
            dt: 日期时间
            
        Returns:
            bool: 是否为工作日
        """
        return dt.weekday() < 5
    
    @staticmethod
    def get_start_of_day(dt: datetime) -> datetime:
        """
        获取一天的开始时间（00:00:00）
        
        Args:
            dt: 日期时间
            
        Returns:
            datetime: 一天的开始时间
        """
        return dt.replace(hour=0, minute=0, second=0, microsecond=0)
    
    @staticmethod
    def get_end_of_day(dt: datetime) -> datetime:
        """
        获取一天的结束时间（23:59:59）
        
        Args:
            dt: 日期时间
            
        Returns:
            datetime: 一天的结束时间
        """
        return dt.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    @staticmethod
    def get_start_of_week(dt: datetime) -> datetime:
        """
        获取一周的开始时间（周一00:00:00）
        
        Args:
            dt: 日期时间
            
        Returns:
            datetime: 一周的开始时间
        """
        days_since_monday = dt.weekday()
        return TimeUtils.get_start_of_day(dt - timedelta(days=days_since_monday))
    
    @staticmethod
    def get_end_of_week(dt: datetime) -> datetime:
        """
        获取一周的结束时间（周日23:59:59）
        
        Args:
            dt: 日期时间
            
        Returns:
            datetime: 一周的结束时间
        """
        days_until_sunday = 6 - dt.weekday()
        return TimeUtils.get_end_of_day(dt + timedelta(days=days_until_sunday))
    
    @staticmethod
    def get_start_of_month(dt: datetime) -> datetime:
        """
        获取一个月的开始时间
        
        Args:
            dt: 日期时间
            
        Returns:
            datetime: 一个月的开始时间
        """
        return dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    @staticmethod
    def get_end_of_month(dt: datetime) -> datetime:
        """
        获取一个月的结束时间
        
        Args:
            dt: 日期时间
            
        Returns:
            datetime: 一个月的结束时间
        """
        # 获取下个月的第一天，然后减去1天
        if dt.month == 12:
            next_month = dt.replace(year=dt.year + 1, month=1, day=1)
        else:
            next_month = dt.replace(month=dt.month + 1, day=1)
        
        return TimeUtils.get_end_of_day(next_month - timedelta(days=1))
    
    @staticmethod
    def is_same_day(dt1: datetime, dt2: datetime) -> bool:
        """
        检查两个日期是否为同一天
        
        Args:
            dt1: 第一个日期时间
            dt2: 第二个日期时间
            
        Returns:
            bool: 是否为同一天
        """
        return dt1.date() == dt2.date()
    
    @staticmethod
    def is_same_week(dt1: datetime, dt2: datetime) -> bool:
        """
        检查两个日期是否为同一周
        
        Args:
            dt1: 第一个日期时间
            dt2: 第二个日期时间
            
        Returns:
            bool: 是否为同一周
        """
        start1 = TimeUtils.get_start_of_week(dt1)
        start2 = TimeUtils.get_start_of_week(dt2)
        return start1.date() == start2.date()
    
    @staticmethod
    def is_same_month(dt1: datetime, dt2: datetime) -> bool:
        """
        检查两个日期是否为同一月
        
        Args:
            dt1: 第一个日期时间
            dt2: 第二个日期时间
            
        Returns:
            bool: 是否为同一月
        """
        return dt1.year == dt2.year and dt1.month == dt2.month
