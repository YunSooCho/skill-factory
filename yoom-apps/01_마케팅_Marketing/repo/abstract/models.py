"""
Abstract API Data Models
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class ExchangeRate:
    """Exchange Rate Model"""
    base: str
    target: str
    rate: float
    last_updated: str

@dataclass
class PhoneNumberValidation:
    """Phone Number Validation Model"""
    phone_number: str
    country_code: str
    national_format: str
    international_format: str
    country_name: str
    country_prefix: str
    line_type: Optional[str] = None
    line_type_intelligence: Optional[Dict[str, Any]] = None
    location: Optional[str] = None
    is_valid: bool = False
    carrier: Optional[str] = None

@dataclass
class TimeInfo:
    """Time Information Model"""
    datetime: str
    timezone: str
    timezone_name: str
    utc_offset: float
    week_number: int
    day_of_year: int
    day_of_week: int

@dataclass
class GeolocationInfo:
    """IP Geolocation Information Model"""
    ip_address: str
    city: Optional[str] = None
    region: Optional[str] = None
    region_iso_code: Optional[str] = None
    country: Optional[str] = None
    country_code: Optional[str] = None
    country_iso_code: Optional[str] = None
    continent: Optional[str] = None
    continent_code: Optional[str] = None
    postal_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    timezone: Optional[Dict[str, str]] = None
    flag: Optional[Dict[str, str]] = None
    connection: Optional[Dict[str, Any]] = None
    security: Optional[Dict[str, Any]] = None

@dataclass
class EmailValidation:
    """Email Validation Model"""
    email: str
    is_valid: bool
    is_deliverable: bool
    is_free_email: bool
    is_mx_found: bool
    is_smtp_valid: bool
    quality_score: float
    is_catchall: Optional[bool] = None
    is_role_email: Optional[bool] = None
    is_disposable: Optional[bool] = None
    is_system_email: Optional[bool] = None
    mx_records: Optional[List[str]] = None
    smtp_provider: Optional[str] = None

@dataclass
class Holiday:
    """Holiday Model"""
    name: str
    name_local: Optional[str] = None
    date_iso: Optional[str] = None
    date_year: Optional[int] = None
    date_month: Optional[int] = None
    date_day: Optional[int] = None
    type: Optional[str] = None
    observed_on: Optional[str] = None
    week_day: Optional[str] = None
    description: Optional[str] = None

@dataclass
class CountryHolidays:
    """Country Holidays Model"""
    country: str
    country_code: str
    year: int
    holidays: List[Holiday] = field(default_factory=list)