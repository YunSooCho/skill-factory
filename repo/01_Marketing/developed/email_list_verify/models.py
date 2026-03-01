"""
 Email List Verify API Models
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any
from enum import Enum


class EmailStatus(str, Enum):
    """Email verification status"""

    DELIVERABLE = "deliverable"
    UNDELIVERABLE = "undeliverable"
    RISKY = "risky"
    BOUNCING = "bouncing"
    INVALID = "invalid"
    UNKNOWN = "unknown"


class DisposableStatus(str, Enum):
    """Disposable email status"""

    NOT_DISPOSABLE = "not_disposable"
    DISPOSABLE = "disposable"
    FREE = "free"
    ROLE_BASED = "role_based"
    UNKNOWN = "unknown"


@dataclass
class VerificationResult:
    """Email verification result"""

    email: str
    status: EmailStatus
    is_valid: bool
    is_deliverable: bool
    score: float
    reasons: Optional[list[str]]
    mx_record: Optional[str]
    smtp_response: Optional[str]
    details: Optional[Dict[str, Any]]
    verified_at: Optional[str]

    @classmethod
    def from_api_response(cls, data: dict) -> "VerificationResult":
        """Create VerificationResult from API response"""
        # Normalize status strings
        status_str = data.get("status", data.get("result", "")).lower()
        if "deliverable" in status_str:
            status = EmailStatus.DELIVERABLE
        elif "undeliverable" in status_str:
            status = EmailStatus.UNDELIVERABLE
        elif "risky" in status_str:
            status = EmailStatus.RISKY
        elif "bounce" in status_str:
            status = EmailStatus.BOUNCING
        elif "invalid" in status_str:
            status = EmailStatus.INVALID
        else:
            status = EmailStatus.UNKNOWN

        return cls(
            email=data.get("email", ""),
            status=status,
            is_valid=data.get("is_valid", data.get("isValid", status != EmailStatus.INVALID)),
            is_deliverable=data.get(
                "is_deliverable",
                data.get("isDeliverable", status in [EmailStatus.DELIVERABLE]),
            ),
            score=float(data.get("score", data.get("quality_score", 0.0))),
            reasons=data.get("reasons", []) or [],
            mx_record=data.get("mx_record", data.get("mxRecord")),
            smtp_response=data.get("smtp_response", data.get("smtpResponse")),
            details=data.get("details", data.get("extra_results", {})) or {},
            verified_at=data.get("verified_at", data.get("timestamp")),
        )


@dataclass
class DeliverabilityResult:
    """Email deliverability evaluation result"""

    email: str
    is_deliverable: bool
    confidence_score: float
    inbox_rate: Optional[float]
    bounce_rate: Optional[float]
    risk_score: float
    risk_level: str
    provider: Optional[str]
    provider_type: Optional[str]
    details: Optional[Dict[str, Any]]
    evaluated_at: Optional[str]

    @classmethod
    def from_api_response(cls, data: dict) -> "DeliverabilityResult":
        """Create DeliverabilityResult from API response"""
        return cls(
            email=data.get("email", ""),
            is_deliverable=data.get(
                "is_deliverable",
                data.get("deliverable", data.get("canDeliver", False)),
            ),
            confidence_score=float(data.get("confidence_score", data.get("confidence", 0.0))),
            inbox_rate=float(data.get("inbox_rate", data.get("inboxRate", 0.0)) or 0.0),
            bounce_rate=float(data.get("bounce_rate", data.get("bounceRate", 0.0)) or 0.0),
            risk_score=float(data.get("risk_score", data.get("riskScore", 0.0))),
            risk_level=data.get("risk_level", data.get("riskLevel", "unknown")),
            provider=data.get("provider", data.get("emailProvider")),
            provider_type=data.get("provider_type", data.get("providerType")),
            details=data.get("details", data.get("extra", {})) or {},
            evaluated_at=data.get("evaluated_at", data.get("timestamp")),
        )


@dataclass
class BusinessEmailResult:
    """Business email search result"""

    domain: str
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    full_name: Optional[str]
    confidence: float
    source: Optional[str]
    company_name: Optional[str]
    alternative_emails: Optional[list[str]]
    found: bool = False

    @classmethod
    def from_api_response(cls, data: dict) -> "BusinessEmailResult":
        """Create BusinessEmailResult from API response"""
        return cls(
            domain=data.get("domain", ""),
            email=data.get("email"),
            first_name=data.get("first_name", data.get("firstName")),
            last_name=data.get("last_name", data.get("lastName")),
            full_name=data.get("full_name", data.get("fullName", data.get("name"))),
            confidence=float(data.get("confidence", data.get("score", 0.0))),
            source=data.get("source", data.get("type")),
            company_name=data.get("company_name", data.get("company")),
            alternative_emails=data.get("alternative_emails", []) or [],
            found=data.get("found", data.get("exists", bool(data.get("email")))),
        )


@dataclass
class DisposableEmailCheck:
    """Disposable email check result"""

    email: str
    is_disposable: bool
    status: DisposableStatus
    domain_type: Optional[str]
    provider: Optional[str]
    details: Optional[Dict[str, Any]]
    checked_at: Optional[str]

    @classmethod
    def from_api_response(cls, data: dict) -> "DisposableEmailCheck":
        """Create DisposableEmailCheck from API response"""
        is_disposable = data.get(
            "is_disposable", data.get("disposable", data.get("isDisposable", False))
        )

        # Determine status
        status_str = data.get("status", "").lower()
        if not status_str:
            if is_disposable:
                status = DisposableStatus.DISPOSABLE
            else:
                status = DisposableStatus.NOT_DISPOSABLE
        elif "disposable" in status_str:
            status = DisposableStatus.DISPOSABLE
        elif "free" in status_str:
            status = DisposableStatus.FREE
        elif "role" in status_str:
            status = DisposableStatus.ROLE_BASED
        else:
            status = DisposableStatus.NOT_DISPOSABLE

        return cls(
            email=data.get("email", ""),
            is_disposable=is_disposable,
            status=status,
            domain_type=data.get(
                "domain_type", data.get("domainType", "standard")
            ),
            provider=data.get("provider", data.get("domain")),
            details=data.get("details", {}) or {},
            checked_at=data.get("checked_at", data.get("timestamp")),
        )