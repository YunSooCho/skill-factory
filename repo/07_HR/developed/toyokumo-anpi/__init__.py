"""
Toyokumo Anpi Safety Confirmation System Integration

Toyokumo Anpi is a Japanese safety confirmation system used to check
employee safety during disasters or emergencies.
"""

from .client import ToyokumoAnpiClient

__all__ = ['ToyokumoAnpiClient']
__version__ = '1.0.0'