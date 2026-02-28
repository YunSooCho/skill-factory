"""LaunchDarkly API Models"""
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Any
from datetime import datetime


@dataclass
class Flag:
    """Feature flag model"""

    key: str
    name: str
    description: str = ""
    kind: str = "boolean"  # boolean, multivariate, json
    variations: List[Dict[str, Any]] = field(default_factory=list)
    default_variation: Optional[int] = None
    temporary: bool = False
    tags: List[str] = field(default_factory=list)
    variation_type: Optional[str] = None
    client_side_availability: Dict[str, bool] = field(default_factory=dict)
    creation_date: Optional[int] = None
    maintainers: List[Dict[str, str]] = field(default_factory=list)

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> "Flag":
        return cls(
            key=data.get("_key", data.get("key", "")),
            name=data.get("name", data.get("_key", "")),
            description=data.get("description", ""),
            kind=data.get("kind", "boolean"),
            variations=data.get("variations", []),
            default_variation=data.get("defaults", {}).get("onVariation"),
            temporary=data.get("temporary", False),
            tags=data.get("tags", []),
            variation_type=data.get("_variationType"),
            client_side_availability=data.get("clientSideAvailability", {}),
            creation_date=data.get("_creationDate"),
            maintainers=data.get("_maintainers", []),
        )

    def to_api_dict(self) -> Dict[str, Any]:
        return {
            "key": self.key,
            "name": self.name,
            "description": self.description,
            "kind": self.kind,
            "variations": self.variations,
            "temporary": self.temporary,
            "tags": self.tags,
            "clientSideAvailability": self.client_side_availability,
        }


@dataclass
class Rule:
    """Flag targeting rule"""

    id: str
    variation: int
    clauses: List[Dict[str, Any]] = field(default_factory=list)
    track_events: bool = False
    rollout_weights: List[int] = field(default_factory=list)


@dataclass
class Segment:
    """User segment"""

    key: str
    name: str
    description: str = ""
    unbounded: bool = False
    creation_date: Optional[int] = None
    rules: List[Dict[str, Any]] = field(default_factory=list)
    included: List[str] = field(default_factory=list)
    excluded: List[str] = field(default_factory=list)

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> "Segment":
        return cls(
            key=data.get("key", ""),
            name=data.get("name", ""),
            description=data.get("description", ""),
            unbounded=data.get("unbounded", False),
            creation_date=data.get("_creationDate"),
            rules=data.get("rules", []),
            included=data.get("included", []),
            excluded=data.get("excluded", []),
        )

    def to_api_dict(self) -> Dict[str, Any]:
        return {
            "key": self.key,
            "name": self.name,
            "description": self.description,
            "unbounded": self.unbounded,
            "rules": self.rules,
            "included": self.included,
            "excluded": self.excluded,
        }


@dataclass
class User:
    """LaunchDarkly user"""

    key: str
    name: Optional[str] = None
    email: Optional[str] = None
    avatar: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    ip: Optional[str] = None
    country: Optional[str] = None
    custom: Dict[str, Any] = field(default_factory=dict)
    anonymous: bool = False
    private_attributes: List[str] = field(default_factory=list)

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> "User":
        return cls(
            key=data.get("key", ""),
            name=data.get("name"),
            email=data.get("email"),
            avatar=data.get("avatar"),
            first_name=data.get("firstName"),
            last_name=data.get("lastName"),
            ip=data.get("ip"),
            country=data.get("country"),
            custom=data.get("custom", {}),
            anonymous=data.get("anonymous", False),
            private_attributes=data.get("privateAttributeNames", []),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "key": self.key,
            "name": self.name,
            "email": self.email,
            "avatar": self.avatar,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "ip": self.ip,
            "country": self.country,
            "custom": self.custom,
            "anonymous": self.anonymous,
            "privateAttributeNames": self.private_attributes,
        }


@dataclass
class Environment:
    """LaunchDarkly environment"""

    key: str
    name: str
    api_key: str = ""
    mobile_key: str = ""
    client_side_id: str = ""
    default_ttl: Optional[int] = None
    secure_mode: bool = False

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> "Environment":
        return cls(
            key=data.get("key", ""),
            name=data.get("name", ""),
            api_key=data.get("apiKey", ""),
            mobile_key=data.get("mobileKey", ""),
            client_side_id=data.get("clientSideId", ""),
            default_ttl=data.get("defaultTtl"),
            secure_mode=data.get("secureMode", False),
        )


@dataclass
class Project:
    """LaunchDarkly project"""

    key: str
    name: str
    environments: List[Environment] = field(default_factory=list)
    production: Optional[Dict[str, str]] = None
    default_environment: Optional[str] = None

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> "Project":
        return cls(
            key=data.get("key", ""),
            name=data.get("name", ""),
            environments=[Environment.from_api_response(env) for env in data.get("environments", [])],
            production=data.get("production"),
            default_environment=data.get("defaultEnvironment"),
        )