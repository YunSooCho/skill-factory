"""
CRM for small businesses API Client
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


class ZohoBiginClient:
    """
    CRM for small businesses API client.
    """

    BASE_URL = "https://www.zohoapis.com/bigin/v1"

    def __init__(self, api_key: str):
        """
        Initialize ZohoBiginClient API client.

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
                    raise Exception(f"ZohoBiginClient API error ({response.status}): {error_msg}")

                return data

        except aiohttp.ClientError as e:
            raise Exception(f"Network error during request to {url}: {str(e)}")
        except Exception as e:
            raise Exception(f"Error during ZohoBiginClient API request: {str(e)}")


    # ==================== API Methods ====================

    # ==================== Contact Methods (連絡先) ====================

    async def create_contact(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        title: Optional[str] = None,
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
            **kwargs: Additional fields

        Returns:
            Created contact data

        Raises:
            Exception: If request fails
        """
        data = {
            "data": [{
                "First_Name": first_name,
                "Last_Name": last_name,
                "Email": email,
                "Phone": phone,
                "Title": title,
                **{"key": value for key, value in kwargs.items() if value is not None}
            }]
        }

        return await self._request("POST", "/Contacts", json_data=data)

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
        return await self._request("DELETE", f"/Contacts/{contact_id}")

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
        return await self._request("GET", f"/Contacts/{contact_id}")

    async def update_contact(
        self,
        contact_id: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        title: Optional[str] = None,
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
            **kwargs: Additional fields

        Returns:
            Updated contact data

        Raises:
            Exception: If request fails
        """
        data = {
            "data": [{
                "First_Name": first_name,
                "Last_Name": last_name,
                "Email": email,
                "Phone": phone,
                "Title": title,
                **{"key": value for key, value in kwargs.items() if value is not None}
            }]
        }

        return await self._request("PUT", f"/Contacts/{contact_id}", json_data=data)

    async def search_contacts(
        self,
        criteria: Optional[str] = None,
        page: int = 1,
        per_page: int = 200
    ) -> Dict[str, Any]:
        """
        Search contacts (連絡先を検索).

        Args:
            criteria: Search criteria (CVL format)
            page: Page number (default: 1)
            per_page: Results per page (default: 200)

        Returns:
            List of matching contacts

        Raises:
            Exception: If request fails
        """
        params = {
            "page": page,
            "per_page": per_page
        }
        if criteria:
            params["criteria"] = criteria

        return await self._request("GET", "/Contacts/search", params=params)

    # ==================== Company Methods (会社) ====================

    async def create_company(
        self,
        company_name: Optional[str] = None,
        website: Optional[str] = None,
        phone: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create company (会社を作成).

        Args:
            company_name: Company name
            website: Company website
            phone: Company phone
            **kwargs: Additional fields

        Returns:
            Created company data

        Raises:
            Exception: If request fails
        """
        data = {
            "data": [{
                "Account_Name": company_name,
                "Website": website,
                "Phone": phone,
                **{"key": value for key, value in kwargs.items() if value is not None}
            }]
        }

        return await self._request("POST", "/Accounts", json_data=data)

    async def delete_company(self, company_id: str) -> Dict[str, Any]:
        """
        Delete company (会社を削除).

        Args:
            company_id: Company ID to delete

        Returns:
            Deletion confirmation

        Raises:
            Exception: If request fails
        """
        return await self._request("DELETE", f"/Accounts/{company_id}")

    async def get_company(self, company_id: str) -> Dict[str, Any]:
        """
        Get company (会社を取得).

        Args:
            company_id: Company ID

        Returns:
            Company data

        Raises:
            Exception: If request fails
        """
        return await self._request("GET", f"/Accounts/{company_id}")

    async def update_company(
        self,
        company_id: str,
        company_name: Optional[str] = None,
        website: Optional[str] = None,
        phone: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Update company (会社を更新).

        Args:
            company_id: Company ID to update
            company_name: Company name
            website: Company website
            phone: Company phone
            **kwargs: Additional fields

        Returns:
            Updated company data

        Raises:
            Exception: If request fails
        """
        data = {
            "data": [{
                "Account_Name": company_name,
                "Website": website,
                "Phone": phone,
                **{"key": value for key, value in kwargs.items() if value is not None}
            }]
        }

        return await self._request("PUT", f"/Accounts/{company_id}", json_data=data)

    async def search_companies(
        self,
        criteria: Optional[str] = None,
        page: int = 1,
        per_page: int = 200
    ) -> Dict[str, Any]:
        """
        Search companies (会社を検索).

        Args:
            criteria: Search criteria (CVL format)
            page: Page number (default: 1)
            per_page: Results per page (default: 200)

        Returns:
            List of matching companies

        Raises:
            Exception: If request fails
        """
        params = {
            "page": page,
            "per_page": per_page
        }
        if criteria:
            params["criteria"] = criteria

        return await self._request("GET", "/Accounts/search", params=params)

    # ==================== Deal Methods (商談) ====================

    async def create_deal(
        self,
        deal_name: Optional[str] = None,
        stage: Optional[str] = None,
        amount: Optional[float] = None,
        closing_date: Optional[str] = None,
        contact_id: Optional[str] = None,
        account_id: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create deal (商談を作成).

        Args:
            deal_name: Deal name
            stage: Deal stage
            amount: Deal amount
            closing_date: Closing date (ISO format)
            contact_id: Associated contact ID
            account_id: Associated account ID
            **kwargs: Additional fields

        Returns:
            Created deal data

        Raises:
            Exception: If request fails
        """
        data = {
            "data": [{
                "Deal_Name": deal_name,
                "Stage": stage,
                "Amount": amount,
                "Closing_Date": closing_date,
                "Contact_Name": {"id": contact_id} if contact_id else None,
                "Account_Name": {"id": account_id} if account_id else None,
                **{"key": value for key, value in kwargs.items() if value is not None}
            }]
        }

        return await self._request("POST", "/Pipelines", json_data=data)

    async def delete_deal(self, deal_id: str) -> Dict[str, Any]:
        """
        Delete deal (商談を削除).

        Args:
            deal_id: Deal ID to delete

        Returns:
            Deletion confirmation

        Raises:
            Exception: If request fails
        """
        return await self._request("DELETE", f"/Pipelines/{deal_id}")

    async def get_deal(self, deal_id: str) -> Dict[str, Any]:
        """
        Get deal (商談を取得).

        Args:
            deal_id: Deal ID

        Returns:
            Deal data

        Raises:
            Exception: If request fails
        """
        return await self._request("GET", f"/Pipelines/{deal_id}")

    async def update_deal(
        self,
        deal_id: str,
        deal_name: Optional[str] = None,
        stage: Optional[str] = None,
        amount: Optional[float] = None,
        closing_date: Optional[str] = None,
        contact_id: Optional[str] = None,
        account_id: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Update deal (商談を更新).

        Args:
            deal_id: Deal ID to update
            deal_name: Deal name
            stage: Deal stage
            amount: Deal amount
            closing_date: Closing date (ISO format)
            contact_id: Associated contact ID
            account_id: Associated account ID
            **kwargs: Additional fields

        Returns:
            Updated deal data

        Raises:
            Exception: If request fails
        """
        data = {
            "data": [{
                "Deal_Name": deal_name,
                "Stage": stage,
                "Amount": amount,
                "Closing_Date": closing_date,
                "Contact_Name": {"id": contact_id} if contact_id else None,
                "Account_Name": {"id": account_id} if account_id else None,
                **{"key": value for key, value in kwargs.items() if value is not None}
            }]
        }

        return await self._request("PUT", f"/Pipelines/{deal_id}", json_data=data)

    async def search_deals(
        self,
        criteria: Optional[str] = None,
        page: int = 1,
        per_page: int = 200
    ) -> Dict[str, Any]:
        """
        Search deals (商談を検索).

        Args:
            criteria: Search criteria (CVL format)
            page: Page number (default: 1)
            per_page: Results per page (default: 200)

        Returns:
            List of matching deals

        Raises:
            Exception: If request fails
        """
        params = {
            "page": page,
            "per_page": per_page
        }
        if criteria:
            params["criteria"] = criteria

        return await self._request("GET", "/Pipelines/search", params=params)

    # ==================== Event Methods (イベント) ====================

    async def create_event(
        self,
        event_title: Optional[str] = None,
        start_datetime: Optional[str] = None,
        end_datetime: Optional[str] = None,
        location: Optional[str] = None,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create event (イベントを作成).

        Args:
            event_title: Event title
            start_datetime: Start datetime (ISO format)
            end_datetime: End datetime (ISO format)
            location: Event location
            description: Event description
            **kwargs: Additional fields

        Returns:
            Created event data

        Raises:
            Exception: If request fails
        """
        data = {
            "data": [{
                "Event_Title": event_title,
                "Start_DateTime": start_datetime,
                "End_DateTime": end_datetime,
                "Venue": location,
                "Description": description,
                **{"key": value for key, value in kwargs.items() if value is not None}
            }]
        }

        return await self._request("POST", "/Events", json_data=data)

    async def delete_event(self, event_id: str) -> Dict[str, Any]:
        """
        Delete event (イベントを削除).

        Args:
            event_id: Event ID to delete

        Returns:
            Deletion confirmation

        Raises:
            Exception: If request fails
        """
        return await self._request("DELETE", f"/Events/{event_id}")

    async def get_event(self, event_id: str) -> Dict[str, Any]:
        """
        Get event (イベントを取得).

        Args:
            event_id: Event ID

        Returns:
            Event data

        Raises:
            Exception: If request fails
        """
        return await self._request("GET", f"/Events/{event_id}")

    async def update_event(
        self,
        event_id: str,
        event_title: Optional[str] = None,
        start_datetime: Optional[str] = None,
        end_datetime: Optional[str] = None,
        location: Optional[str] = None,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Update event (イベントを更新).

        Args:
            event_id: Event ID to update
            event_title: Event title
            start_datetime: Start datetime (ISO format)
            end_datetime: End datetime (ISO format)
            location: Event location
            description: Event description
            **kwargs: Additional fields

        Returns:
            Updated event data

        Raises:
            Exception: If request fails
        """
        data = {
            "data": [{
                "Event_Title": event_title,
                "Start_DateTime": start_datetime,
                "End_DateTime": end_datetime,
                "Venue": location,
                "Description": description,
                **{"key": value for key, value in kwargs.items() if value is not None}
            }]
        }

        return await self._request("PUT", f"/Events/{event_id}", json_data=data)

    async def search_events(
        self,
        criteria: Optional[str] = None,
        page: int = 1,
        per_page: int = 200
    ) -> Dict[str, Any]:
        """
        Search events (イベントを検索).

        Args:
            criteria: Search criteria (CVL format)
            page: Page number (default: 1)
            per_page: Results per page (default: 200)

        Returns:
            List of matching events

        Raises:
            Exception: If request fails
        """
        params = {
            "page": page,
            "per_page": per_page
        }
        if criteria:
            params["criteria"] = criteria

        return await self._request("GET", "/Events/search", params=params)

    # ==================== Task Methods (タスク) ====================

    async def create_task(
        self,
        subject: Optional[str] = None,
        due_date: Optional[str] = None,
        priority: str = "Medium",
        status: str = "Not Started",
        description: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create task (タスクを作成).

        Args:
            subject: Task subject
            due_date: Due date (ISO format)
            priority: Priority (High, Medium, Low)
            status: Status (Not Started, In Progress, Completed, Deferred, Cancelled)
            description: Task description
            **kwargs: Additional fields

        Returns:
            Created task data

        Raises:
            Exception: If request fails
        """
        data = {
            "data": [{
                "Subject": subject,
                "Due_Date": due_date,
                "Priority": priority,
                "Status": status,
                "Description": description,
                **{"key": value for key, value in kwargs.items() if value is not None}
            }]
        }

        return await self._request("POST", "/Tasks", json_data=data)

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
        return await self._request("DELETE", f"/Tasks/{task_id}")

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
        return await self._request("GET", f"/Tasks/{task_id}")

    async def update_task(
        self,
        task_id: str,
        subject: Optional[str] = None,
        due_date: Optional[str] = None,
        priority: Optional[str] = None,
        status: Optional[str] = None,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Update task (タスクを更新).

        Args:
            task_id: Task ID to update
            subject: Task subject
            due_date: Due date (ISO format)
            priority: Priority (High, Medium, Low)
            status: Status (Not Started, In Progress, Completed, Deferred, Cancelled)
            description: Task description
            **kwargs: Additional fields

        Returns:
            Updated task data

        Raises:
            Exception: If request fails
        """
        data = {
            "data": [{
                "Subject": subject,
                "Due_Date": due_date,
                "Priority": priority,
                "Status": status,
                "Description": description,
                **{"key": value for key, value in kwargs.items() if value is not None}
            }]
        }

        return await self._request("PUT", f"/Tasks/{task_id}", json_data=data)

    async def search_tasks(
        self,
        criteria: Optional[str] = None,
        page: int = 1,
        per_page: int = 200
    ) -> Dict[str, Any]:
        """
        Search tasks (タスクを検索).

        Args:
            criteria: Search criteria (CVL format)
            page: Page number (default: 1)
            per_page: Results per page (default: 200)

        Returns:
            List of matching tasks

        Raises:
            Exception: If request fails
        """
        params = {
            "page": page,
            "per_page": per_page
        }
        if criteria:
            params["criteria"] = criteria

        return await self._request("GET", "/Tasks/search", params=params)

    # ==================== Note Methods (メモ) ====================

    async def create_note(
        self,
        note_title: Optional[str] = None,
        note_content: Optional[str] = None,
        parent_id: Optional[str] = None,
        parent_type: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create note (メモを作成).

        Args:
            note_title: Note title
            note_content: Note content
            parent_id: Parent record ID
            parent_type: Parent record type (Contacts, Accounts, Deals, etc.)
            **kwargs: Additional fields

        Returns:
            Created note data

        Raises:
            Exception: If request fails
        """
        data = {
            "data": [{
                "Note_Title": note_title,
                "Note_Content": note_content,
                "Parent_Id": {"id": parent_id} if parent_id else None,
                **{"key": value for key, value in kwargs.items() if value is not None}
            }]
        }

        return await self._request("POST", "/Notes", json_data=data)

    # ==================== Product Methods (商品) ====================

    async def create_product(
        self,
        product_name: Optional[str] = None,
        product_code: Optional[str] = None,
        description: Optional[str] = None,
        unit_price: Optional[float] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create product (商品を作成).

        Args:
            product_name: Product name
            product_code: Product code/SKU
            description: Product description
            unit_price: Unit price
            **kwargs: Additional fields

        Returns:
            Created product data

        Raises:
            Exception: If request fails
        """
        data = {
            "data": [{
                "Product_Name": product_name,
                "Product_Code": product_code,
                "Description": description,
                "Unit_Price": unit_price,
                **{"key": value for key, value in kwargs.items() if value is not None}
            }]
        }

        return await self._request("POST", "/Products", json_data=data)

    async def delete_product(self, product_id: str) -> Dict[str, Any]:
        """
        Delete product (商品を削除).

        Args:
            product_id: Product ID to delete

        Returns:
            Deletion confirmation

        Raises:
            Exception: If request fails
        """
        return await self._request("DELETE", f"/Products/{product_id}")

    async def get_product(self, product_id: str) -> Dict[str, Any]:
        """
        Get product (商品を取得).

        Args:
            product_id: Product ID

        Returns:
            Product data

        Raises:
            Exception: If request fails
        """
        return await self._request("GET", f"/Products/{product_id}")

    async def update_product(
        self,
        product_id: str,
        product_name: Optional[str] = None,
        product_code: Optional[str] = None,
        description: Optional[str] = None,
        unit_price: Optional[float] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Update product (商品を更新).

        Args:
            product_id: Product ID to update
            product_name: Product name
            product_code: Product code/SKU
            description: Product description
            unit_price: Unit price
            **kwargs: Additional fields

        Returns:
            Updated product data

        Raises:
            Exception: If request fails
        """
        data = {
            "data": [{
                "Product_Name": product_name,
                "Product_Code": product_code,
                "Description": description,
                "Unit_Price": unit_price,
                **{"key": value for key, value in kwargs.items() if value is not None}
            }]
        }

        return await self._request("PUT", f"/Products/{product_id}", json_data=data)

    async def search_products(
        self,
        criteria: Optional[str] = None,
        page: int = 1,
        per_page: int = 200
    ) -> Dict[str, Any]:
        """
        Search products (商品を検索).

        Args:
            criteria: Search criteria (CVL format)
            page: Page number (default: 1)
            per_page: Results per page (default: 200)

        Returns:
            List of matching products

        Raises:
            Exception: If request fails
        """
        params = {
            "page": page,
            "per_page": per_page
        }
        if criteria:
            params["criteria"] = criteria

        return await self._request("GET", "/Products/search", params=params)