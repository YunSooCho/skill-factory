"""
Firebase Database Integration

Firebase provides real-time database and Firestore NoSQL database
services with offline capabilities and automatic scaling.
"""

from .client import FirebaseClient

__all__ = ['FirebaseClient']
__version__ = '1.0.0'