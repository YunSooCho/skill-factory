"""
LaunchDarkly API Client
https://apidocs.launchdarkly.com/
"""

import time
import requests
from typing import Optional, Dict, List, Any
from urllib.parse import urljoin

from .models import Flag, Segment, User, Environment, Project
from .exceptions import (
    LaunchDarklyError,
    RateLimitError,
    AuthenticationError,
    ResourceNotFoundError,
    ValidationError,
    ConflictError,
)


class LaunchDarklyClient:
    """LaunchDarkly REST API Client"""

    BASE_URL = "https://app.launchdarkly.com/api/v2/"

    def __init__(
        self,
        access_token: str,
        default_project_key: Optional[str] = None,
        default_env_key: Optional[str] = None,
        timeout: int = 30,
    ):
        """
        Initialize LaunchDarkly client

        Args:
            access_token: LaunchDarkly API access token
            default_project_key: Default project key for operations
            default_env_key: Default environment key for operations
            timeout: Request timeout in seconds
        """
        self.access_token = access_token
        self.default_project_key = default_project_key
        self.default_env_key = default_env_key
        self.timeout = timeout
        self.session = requests.Session()

        # Rate limiting (LaunchDarkly API limits: 60/minute for many endpoints)
        self._min_request_interval = 1.0  # 1 second between requests
        self._last_request_time = 0

    def _wait_for_rate_limit(self):
        """Apply rate limiting to requests"""
        now = time.time()
        time_since_last = now - self._last_request_time

        if time_since_last < self._min_request_interval:
            time.sleep(self._min_request_interval - time_since_last)

        self._last_request_time = time.time()

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
    ) -> Dict:
        """
        Make API request with error handling

        Args:
            method: HTTP method
            endpoint: API endpoint path
            params: URL query parameters
            data: Form data
            json_data: JSON body data

        Returns:
            JSON response data
        """
        self._wait_for_rate_limit()

        url = urljoin(self.BASE_URL, endpoint)
        headers = {
            "Authorization": self.access_token,
            "Content-Type": "application/json",
        }

        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                data=data,
                json=json_data,
                timeout=self.timeout,
            )

            return self._handle_response(response)

        except requests.exceptions.Timeout:
            raise LaunchDarklyError(f"Request timeout after {self.timeout} seconds")
        except requests.exceptions.RequestException as e:
            raise LaunchDarklyError(f"Request failed: {str(e)}")

    def _handle_response(self, response: requests.Response) -> Dict:
        """Handle API response and raise appropriate exceptions"""
        try:
            data = response.json() if response.text else {}
        except ValueError:
            data = {"raw": response.text}

        if response.status_code >= 200 and response.status_code < 300:
            return data
        elif response.status_code == 400:
            raise ValidationError(data.get("message", "Bad request"))
        elif response.status_code == 401:
            raise AuthenticationError("Invalid API key or token")
        elif response.status_code == 403:
            raise AuthenticationError("Insufficient permissions")
        elif response.status_code == 404:
            raise ResourceNotFoundError(data.get("message", "Resource not found"))
        elif response.status_code == 409:
            raise ConflictError(data.get("message", "Resource already exists"))
        elif response.status_code == 422:
            raise ValidationError(data.get("message", "Validation failed"))
        elif response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 60))
            raise RateLimitError("Rate limit exceeded", retry_after=retry_after)
        else:
            raise LaunchDarklyError(f"HTTP {response.status_code}: {data.get('message', '')}")

    def _get_project_key(self, project_key: Optional[str] = None) -> str:
        """Get project key, using default if not provided"""
        return project_key or self.default_project_key

    def _get_env_key(self, env_key: Optional[str] = None) -> str:
        """Get environment key, using default if not provided"""
        return env_key or self.default_env_key

    # ==================== FEATURE FLAGS ====================

    def create_flag(
        self,
        key: str,
        name: str,
        description: str = "",
        kind: str = "boolean",
        variations: Optional[List[Dict[str, Any]]] = None,
        default_variation: Optional[int] = None,
        project_key: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> Flag:
        """
        Create a feature flag

        Args:
            key: Unique key for the flag
            name: Human-readable name
            description: Flag description
            kind: Flag type ('boolean', 'multivariate', 'json')
            variations: List of variation objects
            default_variation: Default variation index
            project_key: Project key
            tags: List of tags

        Returns:
            Created Flag object
        """
        project_key = self._get_project_key(project_key)
        if not project_key:
            raise ValidationError("project_key is required")

        payload = {
            "key": key,
            "name": name,
            "description": description,
            "kind": kind,
            "variations": variations or [{"value": True, "_name": "On"}, {"value": False, "_name": "Off"}],
            "clientSideAvailability": {"usingMobileKey": True, "usingEnvironmentId": True},
        }

        if default_variation is not None:
            payload["defaults"] = {"onVariation": default_variation, "offVariation": default_variation}
        if tags:
            payload["tags"] = tags

        data = self._make_request("POST", f"flags/{project_key}", json_data=payload)
        return Flag.from_api_response(data)

    def get_flag(self, key: str, project_key: Optional[str] = None) -> Flag:
        """
        Get a feature flag

        Args:
            key: Flag key
            project_key: Project key

        Returns:
            Flag object
        """
        project_key = self._get_project_key(project_key)
        if not project_key:
            raise ValidationError("project_key is required")

        data = self._make_request("GET", f"flags/{project_key}/{key}")
        return Flag.from_api_response(data)

    def update_flag(
        self,
        key: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        default_variation: Optional[int] = None,
        on: Optional[bool] = None,
        off_variation: Optional[int] = None,
        project_key: Optional[str] = None,
        env_key: Optional[str] = None,
    ) -> Flag:
        """
        Update a feature flag

        Args:
            key: Flag key
            name: New name
            description: New description
            default_variation: Default variation
            on: Whether flag is on
            off_variation: Off variation index
            project_key: Project key
            env_key: Environment key

        Returns:
            Updated Flag object
        """
        project_key = self._get_project_key(project_key)
        env_key = self._get_env_key(env_key)
        if not project_key:
            raise ValidationError("project_key is required")

        payload = {}
        if name is not None:
            payload["name"] = name
        if description is not None:
            payload["description"] = description

        patch_data = []
        if on is not None:
            patch_data.append({"op": "replace", "path": f"/environments/{env_key}/on", "value": on})
        if default_variation is not None:
            patch_data.append({"op": "replace", "path": f"/environments/{env_key}/onVariation", "value": default_variation})
        if off_variation is not None:
            patch_data.append({"op": "replace", "path": f"/environments/{env_key}/offVariation", "value": off_variation})

        # Update metadata
        if payload:
            self._make_request("PATCH", f"flags/{project_key}/{key}", json_data=payload)

        # Update environment-specific settings
        if patch_data and env_key:
            result = self._make_request(
                "PATCH", f"flags/{project_key}/{key}", json_data=patch_data, params={"env": env_key}
            )
            return Flag.from_api_response(result)

        return self.get_flag(key, project_key)

    def delete_flag(self, key: str, project_key: Optional[str] = None) -> bool:
        """
        Delete a feature flag

        Args:
            key: Flag key
            project_key: Project key

        Returns:
            True if deleted
        """
        project_key = self._get_project_key(project_key)
        if not project_key:
            raise ValidationError("project_key is required")

        self._make_request("DELETE", f"flags/{project_key}/{key}")
        return True

    def list_flags(
        self,
        project_key: Optional[str] = None,
        tag: Optional[str] = None,
        sort: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Flag]:
        """
        List feature flags

        Args:
            project_key: Project key
            tag: Filter by tag
            sort: Sort order ('key', 'name', '-created', '-updated')
            limit: Page size
            offset: Page offset

        Returns:
            List of Flag objects
        """
        project_key = self._get_project_key(project_key)
        if not project_key:
            raise ValidationError("project_key is required")

        params = {"limit": limit, "offset": offset}
        if tag:
            params["tag"] = tag
        if sort:
            params["sort"] = sort

        response = self._make_request("GET", f"flags/{project_key}", params=params)
        items = response.get("items", [])
        return [Flag.from_api_response(item) for item in items]

    # ==================== SEGMENTS ====================

    def create_segment(
        self,
        key: str,
        name: str,
        description: str = "",
        rules: Optional[List[Dict[str, Any]]] = None,
        included: Optional[List[str]] = None,
        excluded: Optional[List[str]] = None,
        project_key: Optional[str] = None,
    ) -> Segment:
        """
        Create a user segment

        Args:
            key: Unique key for the segment
            name: Human-readable name
            description: Segment description
            rules: Segment targeting rules
            included: List of included user keys
            excluded: List of excluded user keys
            project_key: Project key

        Returns:
            Created Segment object
        """
        project_key = self._get_project_key(project_key)
        if not project_key:
            raise ValidationError("project_key is required")

        payload = {
            "key": key,
            "name": name,
            "description": description,
            "unbounded": True,
            "rules": rules or [],
            "included": included or [],
            "excluded": excluded or [],
        }

        data = self._make_request("POST", f"segments/{project_key}", json_data=payload)
        return Segment.from_api_response(data)

    def get_segment(self, key: str, project_key: Optional[str] = None) -> Segment:
        """Get a user segment"""
        project_key = self._get_project_key(project_key)
        if not project_key:
            raise ValidationError("project_key is required")

        data = self._make_request("GET", f"segments/{project_key}/{key}")
        return Segment.from_api_response(data)

    def update_segment(
        self,
        key: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        project_key: Optional[str] = None,
    ) -> Segment:
        """Update a user segment"""
        project_key = self._get_project_key(project_key)
        if not project_key:
            raise ValidationError("project_key is required")

        payload = {}
        if name is not None:
            payload["name"] = name
        if description is not None:
            payload["description"] = description

        data = self._make_request(
            "PATCH", f"segments/{project_key}/{key}", json_data=payload
        )
        return Segment.from_api_response(data)

    def delete_segment(self, key: str, project_key: Optional[str] = None) -> bool:
        """Delete a user segment"""
        project_key = self._get_project_key(project_key)
        if not project_key:
            raise ValidationError("project_key is required")

        self._make_request("DELETE", f"segments/{project_key}/{key}")
        return True

    def list_segments(
        self,
        project_key: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Segment]:
        """List user segments"""
        project_key = self._get_project_key(project_key)
        if not project_key:
            raise ValidationError("project_key is required")

        params = {"limit": limit, "offset": offset}
        response = self._make_request("GET", f"segments/{project_key}", params=params)
        items = response.get("items", [])
        return [Segment.from_api_response(item) for item in items]

    # ==================== PROJECTS ====================

    def list_projects(self) -> List[Project]:
        """List all projects"""
        response = self._make_request("GET", "projects")
        items = response.get("items", [])
        return [Project.from_api_response(item) for item in items]

    def get_project(self, key: str) -> Project:
        """Get a project"""
        data = self._make_request("GET", f"projects/{key}")
        return Project.from_api_response(data)

    # ==================== USERS ====================

    def create_user(
        self,
        key: str,
        email: Optional[str] = None,
        name: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        avatar: Optional[str] = None,
        country: Optional[str] = None,
        custom: Optional[Dict[str, Any]] = None,
    ) -> User:
        """
        Create a user (for user lists/dashboards)

        Args:
            key: User key (unique identifier)
            email: User email
            name: User name
            first_name: First name
            last_name: Last name
            avatar: Avatar URL
            country: Country code
            custom: Custom attributes

        Returns:
            User object
        """
        payload = {"key": key}

        if email:
            payload["email"] = email
        if name:
            payload["name"] = name
        if first_name:
            payload["firstName"] = first_name
        if last_name:
            payload["lastName"] = last_name
        if avatar:
            payload["avatar"] = avatar
        if country:
            payload["country"] = country
        if custom:
            payload["custom"] = custom

        data = self._make_request("POST", "user-search", json_data=payload)
        return User.from_api_response(data)

    def search_users(
        self,
        filter: Optional[str] = None,
        sort: Optional[str] = None,
        limit: int = 20,
    ) -> List[User]:
        """
        Search users

        Args:
            filter: Filter query (e.g., 'email contains "@example.com"')
            sort: Sort field
            limit: Page size

        Returns:
            List of User objects
        """
        params = {"limit": limit}
        if filter:
            params["filter"] = filter
        if sort:
            params["sort"] = sort

        response = self._make_request("GET", "user-search", params=params)
        items = response.get("items", [])
        return [User.from_api_response(item) for item in items]

    # ==================== ENVIRONMENTS ====================

    def list_environments(self, project_key: Optional[str] = None) -> List[Environment]:
        """List project environments"""
        project_key = self._get_project_key(project_key)
        if not project_key:
            raise ValidationError("project_key is required")

        project = self.get_project(project_key)
        return project.environments

    def get_environment(
        self,
        project_key: Optional[str] = None,
        env_key: Optional[str] = None,
    ) -> Environment:
        """Get a specific environment"""
        env_key = self._get_env_key(env_key)
        envs = self.list_environments(project_key)
        for env in envs:
            if env.key == env_key:
                return env
        raise ResourceNotFoundError(f"Environment {env_key} not found")

    # ==================== WEBHOOKS ====================

    def create_webhook(
        self,
        url: str,
        secret: Optional[str] = None,
        sign: Optional[bool] = None,
    ) -> Dict:
        """
        Create a webhook

        Args:
            url: Webhook URL
            secret: Optional secret for signing
            sign: Whether to sign events

        Returns:
            Webhook data
        """
        payload = {"url": url}
        if secret:
            payload["secret"] = secret
        if sign is not None:
            payload["sign"] = sign

        return self._make_request("POST", "webhooks", json_data=payload)

    def list_webhooks(self) -> List[Dict]:
        """List webhooks"""
        response = self._make_request("GET", "webhooks")
        return response.get("items", [])

    def delete_webhook(self, webhook_id: str) -> bool:
        """Delete a webhook"""
        self._make_request("DELETE", f"webhooks/{webhook_id}")
        return True

    # ==================== HELPERS ====================

    def close(self):
        """Close the session"""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()