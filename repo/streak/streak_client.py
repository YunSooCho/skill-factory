"""
Streak API - Gmail CRM Client

Supports 21 API Actions:
- Search Boxes
- Delete a Contact
- Get a Contact
- Update a Task
- Get Threads in a Box
- Create a Contact
- Create a Box
- Get Files in a Box
- Get a Box
- Search Contacts
- Add Files to Box
- Get Tasks in a Box
- Delete a Task
- Create a Comment
- Delete a Box
- Update a Box
- Create a Task
- Create an Organization
- Search Organizations
- Update a Contact
- Update a Stage Name

Triggers:
- New Contact
- Updated Box Stage
- Completed Task
- New Organization
- Updated Organization
- Updated Box
- Updated Contact
- New Comment
- New Box
- New Task
"""

import aiohttp
import asyncio
import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Box:
    """Box entity (pipeline item)"""
    key: str
    name: str
    pipeline_key: str
    stage_key: Optional[str] = None
    notes: Optional[str] = None
    created_at: str = ""
    updated_at: str = ""


@dataclass
class Contact:
    """Contact entity"""
    key: str
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    organization_key: Optional[str] = None
    created_at: str = ""
    updated_at: str = ""


@dataclass
class Organization:
    """Organization entity"""
    key: str
    name: str
    domain: Optional[str] = None
    notes: Optional[str] = None
    created_at: str = ""
    updated_at: str = ""


@dataclass
class Task:
    """Task entity"""
    key: str
    box_key: str
    text: str
    completed: bool = False
    due_date: Optional[str] = None
    created_at: str = ""
    updated_at: str = ""


@dataclass
class Comment:
    """Comment entity"""
    key: str
    box_key: str
    text: str
    author_key: Optional[str] = None
    created_at: str = ""


@dataclass
class File:
    """File entity"""
    key: str
    box_key: str
    name: str
    url: Optional[str] = None
    size: int = 0
    created_at: str = ""


@dataclass
class Thread:
    """Thread entity (email thread)"""
    key: str
    box_key: str
    subject: Optional[str] = None
    last_message_date: Optional[str] = None
    message_count: int = 0


class StreakClientError(Exception):
    """Base exception for Streak client errors"""
    pass


class StreakRateLimitError(StreakClientError):
    """Raised when rate limit is exceeded"""
    pass


class StreakClient:
    """
    Streak API client for Gmail-based CRM.

    API Documentation: https://www.streak.com/api/documentation
    Uses API Key for authentication via Basic Auth.
    """

    BASE_URL = "https://www.streak.com/api/v2"

    def __init__(self, api_key: str, base_url: Optional[str] = None):
        """
        Initialize Streak client.

        Args:
            api_key: API key for authentication
            base_url: Optional custom base URL
        """
        self.api_key = api_key
        self.base_url = (base_url or self.BASE_URL).rstrip("/")
        self.session: Optional[aiohttp.ClientSession] = None
        self._rate_limit_remaining = 100
        self._rate_limit_reset = 0

        logger = logging.getLogger("streak")
        logger.setLevel(logging.DEBUG)
        if not logger.handlers:
            handler = logging.StreamHandler()
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        self._logger = logger

    async def __aenter__(self):
        import base64
        auth_string = base64.b64encode(
            f"{self.api_key}:".encode()
        ).decode()

        headers = {
            "Authorization": f"Basic {auth_string}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        timeout = aiohttp.ClientTimeout(total=30)
        self.session = aiohttp.ClientSession(
            headers=headers,
            timeout=timeout
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request with error handling and rate limiting."""
        await self._check_rate_limit()

        url = f"{self.base_url}{endpoint}"

        retry_count = 0
        max_retries = 3

        while retry_count < max_retries:
            try:
                self._logger.debug(f"Request: {method} {url}")
                if data:
                    self._logger.debug(f"Data: {data}")

                async with self.session.request(
                    method,
                    url,
                    json=data,
                    params=params
                ) as response:
                    await self._update_rate_limit(response)

                    if response.status in [200, 201]:
                        result = await response.json()
                        self._logger.debug(f"Response: {result}")
                        return result

                    elif response.status == 204:
                        return {}

                    elif response.status == 401:
                        raise StreakClientError("Authentication failed")

                    elif response.status == 403:
                        raise StreakClientError("Forbidden - insufficient permissions")

                    elif response.status == 404:
                        raise StreakClientError("Resource not found")

                    elif response.status == 429:
                        await self._handle_rate_limit()
                        retry_count += 1
                        continue

                    else:
                        error_text = await response.text()
                        raise StreakClientError(
                            f"API error {response.status}: {error_text}"
                        )

            except aiohttp.ClientError as e:
                retry_count += 1
                if retry_count >= max_retries:
                    raise StreakClientError(f"Network error: {str(e)}")
                await asyncio.sleep(2 ** retry_count)

    async def _check_rate_limit(self):
        """Check if rate limit allows request"""
        if self._rate_limit_remaining <= 1:
            now = int(datetime.now().timestamp())
            if now < self._rate_limit_reset:
                wait_time = self._rate_limit_reset - now
                self._logger.warning(f"Rate limit reached, waiting {wait_time}s")
                await asyncio.sleep(wait_time)

    async def _update_rate_limit(self, response: aiohttp.ClientResponse):
        """Update rate limit info from response headers"""
        remaining = response.headers.get("X-RateLimit-Remaining")
        reset = response.headers.get("X-RateLimit-Reset")

        if remaining:
            self._rate_limit_remaining = int(remaining)
        if reset:
            self._rate_limit_reset = int(reset)

        self._logger.debug(
            f"Rate limit: {self._rate_limit_remaining} remaining, "
            f"resets at {self._rate_limit_reset}"
        )

    async def _handle_rate_limit(self):
        """Handle rate limit by waiting"""
        now = int(datetime.now().timestamp())
        wait_time = max(0, self._rate_limit_reset - now + 1)
        self._logger.warning(f"Rate limited, waiting {wait_time}s")
        await asyncio.sleep(wait_time)

    async def create_box(
        self,
        pipeline_key: str,
        name: str,
        notes: Optional[str] = None
    ) -> Box:
        """Create a new box (pipeline item)."""
        data = {
            "name": name,
            "pipelineKey": pipeline_key
        }
        if notes:
            data["notes"] = notes

        self._logger.info(f"Creating box '{name}' in pipeline {pipeline_key}")
        result = await self._request("POST", "/pipelines/{pipeline_key}/boxes".format(pipeline_key=pipeline_key), data=data)

        return Box(
            key=result.get("key", ""),
            name=result.get("name", ""),
            pipeline_key=pipeline_key,
            stage_key=result.get("stageKey"),
            notes=result.get("notes"),
            created_at=result.get("creationTimestamp", ""),
            updated_at=result.get("lastUpdatedTimestamp", "")
        )

    async def get_box(self, box_key: str) -> Box:
        """Get a box by key."""
        self._logger.info(f"Getting box {box_key}")
        result = await self._request("GET", f"/boxes/{box_key}")

        return Box(
            key=result.get("key", ""),
            name=result.get("name", ""),
            pipeline_key=result.get("pipelineKey", ""),
            stage_key=result.get("stageKey"),
            notes=result.get("notes"),
            created_at=result.get("creationTimestamp", ""),
            updated_at=result.get("lastUpdatedTimestamp", "")
        )

    async def update_box(
        self,
        box_key: str,
        name: Optional[str] = None,
        notes: Optional[str] = None,
        stage_key: Optional[str] = None
    ) -> Box:
        """Update a box."""
        data = {}
        if name is not None:
            data["name"] = name
        if notes is not None:
            data["notes"] = notes
        if stage_key is not None:
            data["stageKey"] = stage_key

        self._logger.info(f"Updating box {box_key}")
        result = await self._request("PUT", f"/boxes/{box_key}", data=data)

        return Box(
            key=result.get("key", ""),
            name=result.get("name", ""),
            pipeline_key=result.get("pipelineKey", ""),
            stage_key=result.get("stageKey"),
            notes=result.get("notes"),
            created_at=result.get("creationTimestamp", ""),
            updated_at=result.get("lastUpdatedTimestamp", "")
        )

    async def delete_box(self, box_key: str) -> None:
        """Delete a box."""
        self._logger.info(f"Deleting box {box_key}")
        await self._request("DELETE", f"/boxes/{box_key}")

    async def search_boxes(
        self,
        pipeline_key: str,
        query: Optional[str] = None,
        limit: int = 50
    ) -> List[Box]:
        """Search boxes in a pipeline."""
        params = {"limit": limit}
        if query:
            params["q"] = query

        self._logger.info(f"Searching boxes in pipeline {pipeline_key}")
        result = await self._request("GET", f"/pipelines/{pipeline_key}/search".format(pipeline_key=pipeline_key), params=params)

        boxes = []
        for item in result.get("results", []):
            boxes.append(Box(
                key=item.get("key", ""),
                name=item.get("name", ""),
                pipeline_key=pipeline_key,
                stage_key=item.get("stageKey"),
                notes=item.get("notes"),
                created_at=item.get("creationTimestamp", ""),
                updated_at=item.get("lastUpdatedTimestamp", "")
            ))

        return boxes

    async def create_contact(
        self,
        box_key: str,
        name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None
    ) -> Contact:
        """Create a new contact and link to a box."""
        data = {"boxKey": box_key}
        if name:
            data["name"] = name
        if email:
            data["email"] = email
        if phone:
            data["phone"] = phone

        self._logger.info(f"Creating contact for box {box_key}")
        result = await self._request("POST", "/contacts", data=data)

        return Contact(
            key=result.get("key", ""),
            name=result.get("name"),
            email=result.get("email"),
            phone=result.get("phone"),
            created_at=result.get("creationTimestamp", ""),
            updated_at=result.get("lastUpdatedTimestamp", "")
        )

    async def get_contact(self, contact_key: str) -> Contact:
        """Get a contact by key."""
        self._logger.info(f"Getting contact {contact_key}")
        result = await self._request("GET", f"/contacts/{contact_key}")

        return Contact(
            key=result.get("key", ""),
            name=result.get("name"),
            email=result.get("email"),
            phone=result.get("phone"),
            organization_key=result.get("organizationKey"),
            created_at=result.get("creationTimestamp", ""),
            updated_at=result.get("lastUpdatedTimestamp", "")
        )

    async def update_contact(
        self,
        contact_key: str,
        name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None
    ) -> Contact:
        """Update a contact."""
        data = {}
        if name is not None:
            data["name"] = name
        if email is not None:
            data["email"] = email
        if phone is not None:
            data["phone"] = phone

        self._logger.info(f"Updating contact {contact_key}")
        result = await self._request("PUT", f"/contacts/{contact_key}", data=data)

        return Contact(
            key=result.get("key", ""),
            name=result.get("name"),
            email=result.get("email"),
            phone=result.get("phone"),
            organization_key=result.get("organizationKey"),
            created_at=result.get("creationTimestamp", ""),
            updated_at=result.get("lastUpdatedTimestamp", "")
        )

    async def delete_contact(self, contact_key: str) -> None:
        """Delete a contact."""
        self._logger.info(f"Deleting contact {contact_key}")
        await self._request("DELETE", f"/contacts/{contact_key}")

    async def search_contacts(self, query: str, limit: int = 50) -> List[Contact]:
        """Search contacts."""
        params = {"q": query, "limit": limit}

        self._logger.info(f"Searching contacts: {query}")
        result = await self._request("GET", "/contacts/search", params=params)

        contacts = []
        for item in result.get("results", []):
            contacts.append(Contact(
                key=item.get("key", ""),
                name=item.get("name"),
                email=item.get("email"),
                phone=item.get("phone"),
                organization_key=item.get("organizationKey"),
                created_at=item.get("creationTimestamp", ""),
                updated_at=item.get("lastUpdatedTimestamp", "")
            ))

        return contacts

    async def create_organization(
        self,
        name: str,
        domain: Optional[str] = None,
        notes: Optional[str] = None
    ) -> Organization:
        """Create a new organization."""
        data = {"name": name}
        if domain:
            data["domain"] = domain
        if notes:
            data["notes"] = notes

        self._logger.info(f"Creating organization: {name}")
        result = await self._request("POST", "/organizations", data=data)

        return Organization(
            key=result.get("key", ""),
            name=result.get("name", ""),
            domain=result.get("domain"),
            notes=result.get("notes"),
            created_at=result.get("creationTimestamp", ""),
            updated_at=result.get("lastUpdatedTimestamp", "")
        )

    async def search_organizations(self, query: str, limit: int = 50) -> List[Organization]:
        """Search organizations."""
        params = {"q": query, "limit": limit}

        self._logger.info(f"Searching organizations: {query}")
        result = await self._request("GET", "/organizations/search", params=params)

        orgs = []
        for item in result.get("results", []):
            orgs.append(Organization(
                key=item.get("key", ""),
                name=item.get("name", ""),
                domain=item.get("domain"),
                notes=item.get("notes"),
                created_at=item.get("creationTimestamp", ""),
                updated_at=item.get("lastUpdatedTimestamp", "")
            ))

        return orgs

    async def create_task(
        self,
        box_key: str,
        text: str,
        due_date: Optional[str] = None
    ) -> Task:
        """Create a new task for a box."""
        data = {
            "boxKey": box_key,
            "text": text
        }
        if due_date:
            data["dueDate"] = due_date

        self._logger.info(f"Creating task for box {box_key}")
        result = await self._request("POST", "/tasks", data=data)

        return Task(
            key=result.get("key", ""),
            box_key=box_key,
            text=result.get("text", ""),
            completed=result.get("completed", False),
            due_date=result.get("dueDate"),
            created_at=result.get("creationTimestamp", ""),
            updated_at=result.get("lastUpdatedTimestamp", "")
        )

    async def update_task(
        self,
        task_key: str,
        text: Optional[str] = None,
        completed: Optional[bool] = None,
        due_date: Optional[str] = None
    ) -> Task:
        """Update a task."""
        data = {}
        if text is not None:
            data["text"] = text
        if completed is not None:
            data["completed"] = completed
        if due_date is not None:
            data["dueDate"] = due_date

        self._logger.info(f"Updating task {task_key}")
        result = await self._request("PUT", f"/tasks/{task_key}", data=data)

        return Task(
            key=result.get("key", ""),
            box_key=result.get("boxKey", ""),
            text=result.get("text", ""),
            completed=result.get("completed", False),
            due_date=result.get("dueDate"),
            created_at=result.get("creationTimestamp", ""),
            updated_at=result.get("lastUpdatedTimestamp", "")
        )

    async def delete_task(self, task_key: str) -> None:
        """Delete a task."""
        self._logger.info(f"Deleting task {task_key}")
        await self._request("DELETE", f"/tasks/{task_key}")

    async def get_tasks_in_box(self, box_key: str) -> List[Task]:
        """Get all tasks for a box."""
        self._logger.info(f"Getting tasks for box {box_key}")
        result = await self._request("GET", f"/boxes/{box_key}/tasks".format(box_key=box_key))

        tasks = []
        for item in result:
            tasks.append(Task(
                key=item.get("key", ""),
                box_key=box_key,
                text=item.get("text", ""),
                completed=item.get("completed", False),
                due_date=item.get("dueDate"),
                created_at=item.get("creationTimestamp", ""),
                updated_at=item.get("lastUpdatedTimestamp", "")
            ))

        return tasks

    async def create_comment(
        self,
        box_key: str,
        text: str
    ) -> Comment:
        """Create a comment on a box."""
        data = {
            "boxKey": box_key,
            "text": text
        }

        self._logger.info(f"Creating comment on box {box_key}")
        result = await self._request("POST", "/comments", data=data)

        return Comment(
            key=result.get("key", ""),
            box_key=box_key,
            text=result.get("text", ""),
            author_key=result.get("authorKey"),
            created_at=result.get("creationTimestamp", "")
        )

    async def get_files_in_box(self, box_key: str) -> List[File]:
        """Get all files for a box."""
        self._logger.info(f"Getting files for box {box_key}")
        result = await self._request("GET", f"/boxes/{box_key}/files".format(box_key=box_key))

        files = []
        for item in result:
            files.append(File(
                key=item.get("key", ""),
                box_key=box_key,
                name=item.get("name", ""),
                url=item.get("url"),
                size=item.get("size", 0),
                created_at=item.get("creationTimestamp", "")
            ))

        return files

    async def get_threads_in_box(self, box_key: str) -> List[Thread]:
        """Get all email threads for a box."""
        self._logger.info(f"Getting threads for box {box_key}")
        result = await self._request("GET", f"/boxes/{box_key}/threads".format(box_key=box_key))

        threads = []
        for item in result:
            threads.append(Thread(
                key=item.get("key", ""),
                box_key=box_key,
                subject=item.get("subject"),
                last_message_date=item.get("lastMessageDate"),
                message_count=item.get("messageCount", 0)
            ))

        return threads