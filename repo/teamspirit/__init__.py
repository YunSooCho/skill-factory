"""
TeamSpirit HR System Integration

TeamSpirit is a comprehensive Japanese HR management system that provides
functions for attendance management, leave requests, and employee data management.
"""

from .client import TeamSpiritClient

__all__ = ['TeamSpiritClient']
__version__ = '1.0.0'