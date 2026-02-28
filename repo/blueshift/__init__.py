"""
Blueshift - Customer Data Platform & Marketing Automation

API Client for Blueshift customer data platform and marketing automation service.
"""

from .client import BlueshiftClient, Customer, Campaign, Event

__all__ = ["BlueshiftClient", "Customer", "Campaign", "Event"]