"""
Data models for Facebook Ads API integration.
"""
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime


@dataclass
class FacebookObject:
    """Base Facebook object with id and name."""

    id: Optional[str] = None
    name: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FacebookObject":
        """Create FacebookObject from API response."""
        return cls(id=data.get("id"), name=data.get("name"))


@dataclass
class AdAccount(FacebookObject):
    """Facebook Ad Account data model."""

    account_status: Optional[int] = None
    currency: Optional[str] = None
    timezone_name: Optional[str] = None
    timezone_offset_hours_utc: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AdAccount":
        """Create AdAccount from API response."""
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            account_status=data.get("account_status"),
            currency=data.get("currency"),
            timezone_name=data.get("timezone_name"),
            timezone_offset_hours_utc=data.get("timezone_offset_hours_utc"),
        )


@dataclass
class Campaign(FacebookObject):
    """Facebook Campaign data model."""

    status: Optional[str] = None
    objective: Optional[str] = None
    daily_budget: Optional[int] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Campaign":
        """Create Campaign from API response."""
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            status=data.get("status"),
            objective=data.get("objective"),
            daily_budget=data.get("daily_budget"),
            start_time=data.get("start_time"),
            end_time=data.get("end_time"),
        )


@dataclass
class AdSet(FacebookObject):
    """Facebook Ad Set data model."""

    status: Optional[str] = None
    campaign_id: Optional[str] = None
    daily_budget: Optional[int] = None
    lifetime_budget: Optional[int] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AdSet":
        """Create AdSet from API response."""
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            status=data.get("status"),
            campaign_id=data.get("campaign_id"),
            daily_budget=data.get("daily_budget"),
            lifetime_budget=data.get("lifetime_budget"),
            start_time=data.get("start_time"),
            end_time=data.get("end_time"),
        )


@dataclass
class Ad(FacebookObject):
    """Facebook Ad data model."""

    status: Optional[str] = None
    adset_id: Optional[str] = None
    campaign_id: Optional[str] = None
    creative_id: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Ad":
        """Create Ad from API response."""
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            status=data.get("status"),
            adset_id=data.get("adset_id"),
            campaign_id=data.get("campaign_id"),
            creative_id=data.get("creative_id"),
        )


@dataclass
class AdInsight:
    """Facebook Ads Insight/Report data model."""

    id: Optional[str] = None
    campaign_id: Optional[str] = None
    campaign_name: Optional[str] = None
    adset_id: Optional[str] = None
    adset_name: Optional[str] = None
    ad_id: Optional[str] = None
    ad_name: Optional[str] = None
    account_id: Optional[str] = None

    # Metrics
    impressions: Optional[int] = None
    clicks: Optional[int] = None
    spend: Optional[float] = None
    cpc: Optional[float] = None
    ctr: Optional[float] = None
    cpm: Optional[float] = None
    reach: Optional[int] = None
    conversions: Optional[int] = None
    cost_per_conversion: Optional[float] = None
    date_start: Optional[str] = None
    date_stop: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AdInsight":
        """Create AdInsight from API response."""
        return cls(
            id=data.get("id"),
            campaign_id=data.get("campaign_id"),
            campaign_name=data.get("campaign_name"),
            adset_id=data.get("adset_id"),
            adset_name=data.get("adset_name"),
            ad_id=data.get("ad_id"),
            ad_name=data.get("ad_name"),
            account_id=data.get("account_id"),
            impressions=data.get("impressions"),
            clicks=data.get("clicks"),
            spend=data.get("spend"),
            cpc=data.get("cpc"),
            ctr=data.get("ctr"),
            cpm=data.get("cpm"),
            reach=data.get("reach"),
            conversions=data.get("conversions"),
            cost_per_conversion=data.get("cost_per_conversion"),
            date_start=data.get("date_start"),
            date_stop=data.get("date_stop"),
        )


@dataclass
class Lead:
    """Facebook Lead data model for webhooks."""

    leadgen_id: Optional[str] = None
    ad_id: Optional[str] = None
    adgroup_id: Optional[str] = None
    campaign_id: Optional[str] = None
    form_id: Optional[str] = None
    created_time: Optional[str] = None
    field_data: List[Dict[str, str]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Lead":
        """Create Lead from API response or webhook."""
        field_data = []
        if "field_data" in data:
            for field in data["field_data"]:
                field_data.append(
                    {
                        "name": field.get("name"),
                        "values": field.get("values", []),
                    }
                )

        return cls(
            leadgen_id=data.get("leadgen_id"),
            ad_id=data.get("ad_id"),
            adgroup_id=data.get("adgroup_id"),
            campaign_id=data.get("campaign_id"),
            form_id=data.get("form_id"),
            created_time=data.get("created_time"),
            field_data=field_data,
        )