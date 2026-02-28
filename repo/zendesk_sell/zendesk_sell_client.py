"""
Sales CRM by Zendesk API Client
Sales
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any, List
import time


class RateLimiter:
    """Simple rate limiter for API requests"""

    def __init__(self, max_requests: int = 120, per_seconds: int = 60):
        self.max_requests = max_requests
        self.per_seconds = per_seconds
        self.requests = []
        self.lock = asyncio.Lock()

    async def acquire(self):
        async with self.lock:
            now = time.time()
            self.requests = [req_time for req_time in self.requests
                            if now - req_time < self.per_seconds]

            if len(self.requests) >= self.max_requests:
                sleep_time = self.per_seconds - (now - self.requests[0])
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)
                    self.requests = []

            self.requests.append(now)


class ZendeskSellClient:
    """
    Sales CRM by Zendesk API client.
    """

    BASE_URL = "https://api.sell.zendesk.com/v1"

    def __init__(self, api_key: str):
        """
        Initialize ZendeskSellClient API client.

        Args:
            api_key: Your API key
        """
        self.api_key = api_key
        self.session = None
        self.rate_limiter = RateLimiter(max_requests=120, per_seconds=60)

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with API key"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make API request with error handling and rate limiting.

        Args:
            method: HTTP method
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON body data

        Returns:
            Response data

        Raises:
            Exception: If request fails
        """
        await self.rate_limiter.acquire()

        url = f"{self.BASE_URL}{endpoint}"

        try:
            async with self.session.request(
                method,
                url,
                headers=self._get_headers(),
                params=params,
                json=json_data
            ) as response:
                try:
                    data = await response.json()
                except:
                    text = await response.text()
                    data = {"raw_response": text}

                if response.status >= 400:
                    error_msg = data.get("error", data.get("message", "Unknown error"))
                    raise Exception(f"ZendeskSellClient API error ({response.status}): {error_msg}")

                return data

        except aiohttp.ClientError as e:
            raise Exception(f"Network error during request to {url}: {str(e)}")
        except Exception as e:
            raise Exception(f"Error during ZendeskSellClient API request: {str(e)}")


    # ==================== API Methods ====================

    # ==================== Contact Methods (連絡先) ====================

    async def create_contact(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        title: Optional[str] = None,
        company: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create contact (連絡先を作成).

        Args:
            first_name: First name
            last_name: Last name
            email: Email address
            phone: Phone number
            title: Job title
            company: Company name
            **kwargs: Additional fields

        Returns:
            Created contact data

        Raises:
            Exception: If request fails
        """
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "title": title,
            "company": company,
            **kwargs
        }
        data = {k: v for k, v in data.items() if v is not None}

        return await self._request("POST", "/contacts", json_data=data)

    async def delete_contact(self, contact_id: str) -> Dict[str, Any]:
        """
        Delete contact (連絡先を削除).

        Args:
            contact_id: Contact ID to delete

        Returns:
            Deletion confirmation

        Raises:
            Exception: If request fails
        """
        return await self._request("DELETE", f"/contacts/{contact_id}")

    async def get_contact(self, contact_id: str) -> Dict[str, Any]:
        """
        Get contact (連絡先を取得).

        Args:
            contact_id: Contact ID

        Returns:
            Contact data

        Raises:
            Exception: If request fails
        """
        return await self._request("GET", f"/contacts/{contact_id}")

    async def update_contact(
        self,
        contact_id: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        title: Optional[str] = None,
        company: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Update contact (連絡先を更新).

        Args:
            contact_id: Contact ID to update
            first_name: First name
            last_name: Last name
            email: Email address
            phone: Phone number
            title: Job title
            company: Company name
            **kwargs: Additional fields

        Returns:
            Updated contact data

        Raises:
            Exception: If request fails
        """
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "title": title,
            "company": company,
            **kwargs
        }
        data = {k: v for k, v in data.items() if v is not None}

        return await self._request("PUT", f"/contacts/{contact_id}", json_data=data)

    async def search_contacts(
        self,
        query: Optional[str] = None,
        email: Optional[str] = None,
        name: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Search contacts (連絡先を検索).

        Args:
            query: General search query
            email: Search by email
            name: Search by name
            limit: Maximum results (default: 100)
            offset: Pagination offset (default: 0)

        Returns:
            List of matching contacts

        Raises:
            Exception: If request fails
        """
        params = {
            "limit": limit,
            "offset": offset
        }
        if query:
            params["q"] = query
        if email:
            params["email"] = email
        if name:
            params["name"] = name

        return await self._request("GET", "/contacts/search", params=params)

    # ==================== Lead Methods (リード) ====================

    async def create_lead(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        title: Optional[str] = None,
        company: Optional[str] = None,
        source: Optional[str] = None,
        status: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create lead (リードを作成).

        Args:
            first_name: First name
            last_name: Last name
            email: Email address
            phone: Phone number
            title: Job title
            company: Company name
            source: Lead source
            status: Lead status
            **kwargs: Additional fields

        Returns:
            Created lead data

        Raises:
            Exception: If request fails
        """
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "title": title,
            "company": company,
            "source": source,
            "status": status,
            **kwargs
        }
        data = {k: v for k, v in data.items() if v is not None}

        return await self._request("POST", "/leads", json_data=data)

    async def update_lead(
        self,
        lead_id: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        title: Optional[str] = None,
        company: Optional[str] = None,
        source: Optional[str] = None,
        status: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Update lead (リードを更新).

        Args:
            lead_id: Lead ID to update
            first_name: First name
            last_name: Last name
            email: Email address
            phone: Phone number
            title: Job title
            company: Company name
            source: Lead source
            status: Lead status
            **kwargs: Additional fields

        Returns:
            Updated lead data

        Raises:
            Exception: If request fails
        """
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "title": title,
            "company": company,
            "source": source,
            "status": status,
            **kwargs
        }
        data = {k: v for k, v in data.items() if v is not None}

        return await self._request("PUT", f"/leads/{lead_id}", json_data=data)

    async def delete_lead(self, lead_id: str) -> Dict[str, Any]:
        """
        Delete lead (リードを削除).

        Args:
            lead_id: Lead ID to delete

        Returns:
            Deletion confirmation

        Raises:
            Exception: If request fails
        """
        return await self._request("DELETE", f"/leads/{lead_id}")

    async def search_leads(
        self,
        query: Optional[str] = None,
        email: Optional[str] = None,
        name: Optional[str] = None,
        status: Optional[str] = None,
        source: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Search leads (リードを検索).

        Args:
            query: General search query
            email: Search by email
            name: Search by name
            status: Filter by status
            source: Filter by source
            limit: Maximum results (default: 100)
            offset: Pagination offset (default: 0)

        Returns:
            List of matching leads

        Raises:
            Exception: If request fails
        """
        params = {
            "limit": limit,
            "offset": offset
        }
        if query:
            params["q"] = query
        if email:
            params["email"] = email
        if name:
            params["name"] = name
        if status:
            params["status"] = status
        if source:
            params["source"] = source

        return await self._request("GET", "/leads/search", params=params)

    async def get_lead_details(self, lead_id: str) -> Dict[str, Any]:
        """
        Get lead details (リードの詳細を取得).

        Args:
            lead_id: Lead ID

        Returns:
            Lead details

        Raises:
            Exception: If request fails
        """
        return await self._request("GET", f"/leads/{lead_id}/details")

    # ==================== Deal Methods (取引) ====================

    async def create_deal(
        self,
        name: str,
        contact_id: Optional[str] = None,
        value: Optional[float] = None,
        currency: str = "USD",
        stage: Optional[str] = None,
        probability: Optional[int] = None,
        expected_close_date: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create deal (取引を作成).

        Args:
            name: Deal name
            contact_id: Associated contact ID
            value: Deal value
            currency: Currency code (default: USD)
            stage: Deal stage
            probability: Win probability (0-100)
            expected_close_date: Expected close date (ISO format)
            **kwargs: Additional fields

        Returns:
            Created deal data

        Raises:
            Exception: If request fails
        """
        data = {
            "name": name,
            "contact_id": contact_id,
            "value": value,
            "currency": currency,
            "stage": stage,
            "probability": probability,
            "expected_close_date": expected_close_date,
            **kwargs
        }
        data = {k: v for k, v in data.items() if v is not None}

        return await self._request("POST", "/deals", json_data=data)

    async def update_deal(
        self,
        deal_id: str,
        name: Optional[str] = None,
        contact_id: Optional[str] = None,
        value: Optional[float] = None,
        currency: Optional[str] = None,
        stage: Optional[str] = None,
        probability: Optional[int] = None,
        expected_close_date: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Update deal (取引を更新).

        Args:
            deal_id: Deal ID to update
            name: Deal name
            contact_id: Associated contact ID
            value: Deal value
            currency: Currency code
            stage: Deal stage
            probability: Win probability (0-100)
            expected_close_date: Expected close date (ISO format)
            **kwargs: Additional fields

        Returns:
            Updated deal data

        Raises:
            Exception: If request fails
        """
        data = {
            "name": name,
            "contact_id": contact_id,
            "value": value,
            "currency": currency,
            "stage": stage,
            "probability": probability,
            "expected_close_date": expected_close_date,
            **kwargs
        }
        data = {k: v for k, v in data.items() if v is not None}

        return await self._request("PUT", f"/deals/{deal_id}", json_data=data)

    async def delete_deal(self, deal_id: str) -> Dict[str, Any]:
        """
        Delete deal (取引を削除).

        Args:
            deal_id: Deal ID to delete

        Returns:
            Deletion confirmation

        Raises:
            Exception: If request fails
        """
        return await self._request("DELETE", f"/deals/{deal_id}")

    async def get_deal(self, deal_id: str) -> Dict[str, Any]:
        """
        Get deal (取引を取得).

        Args:
            deal_id: Deal ID

        Returns:
            Deal data

        Raises:
            Exception: If request fails
        """
        return await self._request("GET", f"/deals/{deal_id}")

    async def search_deals(
        self,
        query: Optional[str] = None,
        stage: Optional[str] = None,
        status: Optional[str] = None,
        contact_id: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Search deals (取引を検索).

        Args:
            query: General search query
            stage: Filter by stage
            status: Filter by status
            contact_id: Filter by contact ID
            limit: Maximum results (default: 100)
            offset: Pagination offset (default: 0)

        Returns:
            List of matching deals

        Raises:
            Exception: If request fails
        """
        params = {
            "limit": limit,
            "offset": offset
        }
        if query:
            params["q"] = query
        if stage:
            params["stage"] = stage
        if status:
            params["status"] = status
        if contact_id:
            params["contact_id"] = contact_id

        return await self._request("GET", "/deals/search", params=params)

    async def search_deal_sources(
        self,
        limit: int = 100,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Search deal sources (取引ソースを検索).

        Args:
            limit: Maximum results (default: 100)
            offset: Pagination offset (default: 0)

        Returns:
            List of deal sources

        Raises:
            Exception: If request fails
        """
        params = {
            "limit": limit,
            "offset": offset
        }

        return await self._request("GET", "/deal-sources", params=params)

    async def search_deal_stages(
        self,
        limit: int = 100,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Search deal stages (取引ステージを検索).

        Args:
            limit: Maximum results (default: 100)
            offset: Pagination offset (default: 0)

        Returns:
            List of deal stages

        Raises:
            Exception: If request fails
        """
        params = {
            "limit": limit,
            "offset": offset
        }

        return await self._request("GET", "/deal-stages", params=params)

    # ==================== Task Methods (タスク) ====================

    async def create_task(
        self,
        title: str,
        description: Optional[str] = None,
        due_date: Optional[str] = None,
        priority: str = "normal",
        contact_id: Optional[str] = None,
        deal_id: Optional[str] = None,
        status: str = "open",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create task (タスクを作成).

        Args:
            title: Task title
            description: Task description
            due_date: Due date (ISO format)
            priority: Priority (low, normal, high)
            contact_id: Associated contact ID
            deal_id: Associated deal ID
            status: Task status (open, completed)
            **kwargs: Additional fields

        Returns:
            Created task data

        Raises:
            Exception: If request fails
        """
        data = {
            "title": title,
            "description": description,
            "due_date": due_date,
            "priority": priority,
            "contact_id": contact_id,
            "deal_id": deal_id,
            "status": status,
            **kwargs
        }
        data = {k: v for k, v in data.items() if v is not None}

        return await self._request("POST", "/tasks", json_data=data)

    async def update_task(
        self,
        task_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        due_date: Optional[str] = None,
        priority: Optional[str] = None,
        contact_id: Optional[str] = None,
        deal_id: Optional[str] = None,
        status: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Update task (タスクを更新).

        Args:
            task_id: Task ID to update
            title: Task title
            description: Task description
            due_date: Due date (ISO format)
            priority: Priority (low, normal, high)
            contact_id: Associated contact ID
            deal_id: Associated deal ID
            status: Task status (open, completed)
            **kwargs: Additional fields

        Returns:
            Updated task data

        Raises:
            Exception: If request fails
        """
        data = {
            "title": title,
            "description": description,
            "due_date": due_date,
            "priority": priority,
            "contact_id": contact_id,
            "deal_id": deal_id,
            "status": status,
            **kwargs
        }
        data = {k: v for k, v in data.items() if v is not None}

        return await self._request("PUT", f"/tasks/{task_id}", json_data=data)

    async def delete_task(self, task_id: str) -> Dict[str, Any]:
        """
        Delete task (タスクを削除).

        Args:
            task_id: Task ID to delete

        Returns:
            Deletion confirmation

        Raises:
            Exception: If request fails
        """
        return await self._request("DELETE", f"/tasks/{task_id}")

    async def get_task(self, task_id: str) -> Dict[str, Any]:
        """
        Get task (タスクを取得).

        Args:
            task_id: Task ID

        Returns:
            Task data

        Raises:
            Exception: If request fails
        """
        return await self._request("GET", f"/tasks/{task_id}")

    async def search_tasks(
        self,
        query: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        contact_id: Optional[str] = None,
        deal_id: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Search tasks (タスクを検索).

        Args:
            query: General search query
            status: Filter by status
            priority: Filter by priority
            contact_id: Filter by contact ID
            deal_id: Filter by deal ID
            limit: Maximum results (default: 100)
            offset: Pagination offset (default: 0)

        Returns:
            List of matching tasks

        Raises:
            Exception: If request fails
        """
        params = {
            "limit": limit,
            "offset": offset
        }
        if query:
            params["q"] = query
        if status:
            params["status"] = status
        if priority:
            params["priority"] = priority
        if contact_id:
            params["contact_id"] = contact_id
        if deal_id:
            params["deal_id"] = deal_id

        return await self._request("GET", "/tasks/search", params=params)

    # ==================== Note Methods (ノート) ====================

    async def create_note(
        self,
        content: str,
        contact_id: Optional[str] = None,
        deal_id: Optional[str] = None,
        lead_id: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create note (ノートを作成).

        Args:
            content: Note content
            contact_id: Associated contact ID
            deal_id: Associated deal ID
            lead_id: Associated lead ID
            **kwargs: Additional fields

        Returns:
            Created note data

        Raises:
            Exception: If request fails
        """
        data = {
            "content": content,
            "contact_id": contact_id,
            "deal_id": deal_id,
            "lead_id": lead_id,
            **kwargs
        }
        data = {k: v for k, v in data.items() if v is not None}

        return await self._request("POST", "/notes", json_data=data)

    async def update_note(
        self,
        note_id: str,
        content: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Update note (ノートを更新).

        Args:
            note_id: Note ID to update
            content: Note content
            **kwargs: Additional fields

        Returns:
            Updated note data

        Raises:
            Exception: If request fails
        """
        data = {
            "content": content,
            **kwargs
        }
        data = {k: v for k, v in data.items() if v is not None}

        return await self._request("PUT", f"/notes/{note_id}", json_data=data)

    async def delete_note(self, note_id: str) -> Dict[str, Any]:
        """
        Delete note (ノートを削除).

        Args:
            note_id: Note ID to delete

        Returns:
            Deletion confirmation

        Raises:
            Exception: If request fails
        """
        return await self._request("DELETE", f"/notes/{note_id}")

    async def get_note(self, note_id: str) -> Dict[str, Any]:
        """
        Get note (ノートを取得).

        Args:
            note_id: Note ID

        Returns:
            Note data

        Raises:
            Exception: If request fails
        """
        return await self._request("GET", f"/notes/{note_id}")

    async def search_notes(
        self,
        query: Optional[str] = None,
        contact_id: Optional[str] = None,
        deal_id: Optional[str] = None,
        lead_id: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Search notes (ノートを検索).

        Args:
            query: General search query
            contact_id: Filter by contact ID
            deal_id: Filter by deal ID
            lead_id: Filter by lead ID
            limit: Maximum results (default: 100)
            offset: Pagination offset (default: 0)

        Returns:
            List of matching notes

        Raises:
            Exception: If request fails
        """
        params = {
            "limit": limit,
            "offset": offset
        }
        if query:
            params["q"] = query
        if contact_id:
            params["contact_id"] = contact_id
        if deal_id:
            params["deal_id"] = deal_id
        if lead_id:
            params["lead_id"] = lead_id

        return await self._request("GET", "/notes/search", params=params)

    # ==================== User Methods (ユーザー) ====================

    async def get_user(self, user_id: str) -> Dict[str, Any]:
        """
        Get user (ユーザーを取得).

        Args:
            user_id: User ID

        Returns:
            User data

        Raises:
            Exception: If request fails
        """
        return await self._request("GET", f"/users/{user_id}")

    async def search_users(
        self,
        query: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Search users (ユーザーを検索).

        Args:
            query: General search query
            limit: Maximum results (default: 100)
            offset: Pagination offset (default: 0)

        Returns:
            List of matching users

        Raises:
            Exception: If request fails
        """
        params = {
            "limit": limit,
            "offset": offset
        }
        if query:
            params["q"] = query

        return await self._request("GET", "/users/search", params=params)

    async def search_lead_sources(
        self,
        limit: int = 100,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Search lead sources (リードソースを検索).

        Args:
            limit: Maximum results (default: 100)
            offset: Pagination offset (default: 0)

        Returns:
            List of lead sources

        Raises:
            Exception: If request fails
        """
        params = {
            "limit": limit,
            "offset": offset
        }

        return await self._request("GET", "/lead-sources", params=params)

