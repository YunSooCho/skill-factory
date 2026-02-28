"""
Smaregi Timecard - Japan-based Time Attendance System
"""

from .client import SmaregiTimecardClient, SmaregiTimecardError

__all__ = ['SmaregiTimecardClient', 'SmaregiTimecardError']