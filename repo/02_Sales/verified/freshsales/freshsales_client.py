"""
Freshsales API Client
API Documentation: https://developers.freshworks.com/crm/api/
"""

import requests
from typing import Optional, Dict, List, Any
from datetime import datetime


class FreshsalesAPIError(Exception):
    """Custom exception for Freshsales API errors."""
    pass


class FreshsalesClient:
    """Client for Freshsales CRM API."""

    def __init__(self, api_key: str, domain: str, base_url: Optional[str] = None):
        """
        Initialize Freshsales API client.

        Args:
            api_key: Your Freshsales API key
            domain: Your Freshsales domain (e.g., mycompany)
            base_url: API base URL (default: https://{domain}.freshsales.io)
        """
        self.api_key = api_key
        self.domain = domain
        self.base_url = base_url or f"https://{domain}.freshsales.io"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Token token={api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make API request with error handling.

        Args:
            method: HTTP method
            endpoint: API endpoint
            **kwargs: Additional request arguments

        Returns:
            Response data
        """
        url = f"{self.base_url}{endpoint}"

        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()

            data = response.json()
            return {
                "status": "success",
                "data": data,
                "status_code": response.status_code
            }

        except requests.exceptions.HTTPError as e:
            error_data = self._parse_error(response)
            raise FreshsalesAPIError(
                f"HTTP {response.status_code}: {error_data.get('message', str(e))}"
            )
        except requests.exceptions.RequestException as e:
            raise FreshsalesAPIError(f"Request failed: {str(e)}")

    def _parse_error(self, response: requests.Response) -> Dict[str, Any]:
        """Parse error response."""
        try:
            return response.json() if response.content else {"message": response.text}
        except Exception:
            return {"message": response.text}

    def create_view_contact(
        self,
        first_name: str,
        last_name: str,
        email: str,
        phone: Optional[str] = None,
        mobile: Optional[str] = None,
        title: Optional[str] = None,
        twitter: Optional[str] = None,
        linkedin: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a view/contact (連絡先の作成).

        API Reference: Contacts endpoint

        Args:
            first_name: First name
            last_name: Last name
            email: Email address
            phone: Phone number
            mobile: Mobile phone number
            title: Job title
            twitter: Twitter handle
            linkedin: LinkedIn profile URL

        Returns:
            Created contact information with ID
        """
        endpoint = "/api/contacts"

        data = {
            "contact": {
                "first_name": first_name,
                "last_name": last_name,
                "email": email
            }
        }

        if phone:
            data["contact"]["phone"] = phone
        if mobile:
            data["contact"]["mobile_number"] = mobile
        if title:
            data["contact"]["job_title"] = title
        if twitter:
            data["contact"]["twitter"] = twitter
        if linkedin:
            data["contact"]["linkedin"] = linkedin

        return self._make_request("POST", endpoint, json=data)

    def update_view_contact(
        self,
        contact_id: int,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        mobile: Optional[str] = None,
        title: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update view/contact information (連絡先情報の更新).

        API Reference: Contacts PUT endpoint

        Args:
            contact_id: Contact ID
            first_name: First name
            last_name: Last name
            email: Email address
            phone: Phone number
            mobile: Mobile phone number
            title: Job title

        Returns:
            Updated contact information
        """
        endpoint = f"/api/contacts/{contact_id}"

        data = {"contact": {}}

        if first_name:
            data["contact"]["first_name"] = first_name
        if last_name:
            data["contact"]["last_name"] = last_name
        if email:
            data["contact"]["email"] = email
        if phone:
            data["contact"]["phone"] = phone
        if mobile:
            data["contact"]["mobile_number"] = mobile
        if title:
            data["contact"]["job_title"] = title

        return self._make_request("PUT", endpoint, json=data)

    def get_view_contact(self, contact_id: int) -> Dict[str, Any]:
        """
        Get view/contact details (連絡先の詳細を取得).

        API Reference: Contacts GET endpoint

        Args:
            contact_id: Contact ID

        Returns:
            Contact details
        """
        endpoint = f"/api/contacts/{contact_id}"
        return self._make_request("GET", endpoint)

    def delete_view_contact(self, contact_id: int) -> Dict[str, Any]:
        """
        Delete view/contact (連絡先を削除).

        API Reference: Contacts DELETE endpoint

        Args:
            contact_id: Contact ID

        Returns:
            Deletion confirmation
        """
        endpoint = f"/api/contacts/{contact_id}"
        return self._make_request("DELETE", endpoint)

    def create_account(
        self,
        name: str,
        website: Optional[str] = None,
        phone: Optional[str] = None,
        address: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        zipcode: Optional[str] = None,
        country: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create an account (アカウントの作成).

        API Reference: Accounts endpoint

        Args:
            name: Account name
            website: Website URL
            phone: Phone number
            address: Street address
            city: City
            state: State or province
            zipcode: Postal code
            country: Country

        Returns:
            Created account information with ID
        """
        endpoint = "/api/sales_accounts"

        data = {
            "sales_account": {
                "name": name
            }
        }

        if website:
            data["sales_account"]["website"] = website
        if phone:
            data["sales_account"]["phone"] = phone
        if address:
            data["sales_account"]["address"] = address
        if city:
            data["sales_account"]["city"] = city
        if state:
            data["sales_account"]["state"] = state
        if zipcode:
            data["sales_account"]["zipcode"] = zipcode
        if country:
            data["sales_account"]["country"] = country

        return self._make_request("POST", endpoint, json=data)

    def update_account(
        self,
        account_id: int,
        name: Optional[str] = None,
        website: Optional[str] = None,
        phone: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update account information (アカウント情報の更新).

        API Reference: Accounts PUT endpoint

        Args:
            account_id: Account ID
            name: Account name
            website: Website URL
            phone: Phone number

        Returns:
            Updated account information
        """
        endpoint = f"/api/sales_accounts/{account_id}"

        data = {"sales_account": {}}

        if name:
            data["sales_account"]["name"] = name
        if website:
            data["sales_account"]["website"] = website
        if phone:
            data["sales_account"]["phone"] = phone

        return self._make_request("PUT", endpoint, json=data)

    def get_account(self, account_id: int) -> Dict[str, Any]:
        """
        Get account details (アカウントの詳細を取得).

        API Reference: Accounts GET endpoint

        Args:
            account_id: Account ID

        Returns:
            Account details
        """
        endpoint = f"/api/sales_accounts/{account_id}"
        return self._make_request("GET", endpoint)

    def create_deal(
        self,
        deal_name: str,
        contact_id: Optional[int] = None,
        account_id: Optional[int] = None,
        deal_value: Optional[float] = None,
        currency: str = "USD",
        deal_stage_id: Optional[int] = None,
        closing_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a deal (取引の作成).

        API Reference: Deals endpoint

        Args:
            deal_name: Deal name
            contact_id: Associated contact ID
            account_id: Associated account ID
            deal_value: Deal value
            currency: Currency code (default: USD)
            deal_stage_id: Deal stage ID
            closing_date: Expected closing date (YYYY-MM-DD)

        Returns:
            Created deal information with ID
        """
        endpoint = "/api/deals"

        data = {
            "deal": {
                "name": deal_name,
                "amount": deal_value,
                "currency_code": currency
            }
        }

        if contact_id:
            data["deal"]["contact_ids"] = [contact_id]
        if account_id:
            data["deal"]["sales_account_id"] = account_id
        if deal_stage_id:
            data["deal"]["deal_stage_id"] = deal_stage_id
        if closing_date:
            data["deal"]["expected_close_date"] = closing_date

        return self._make_request("POST", endpoint, json=data)

    def update_deal(
        self,
        deal_id: int,
        deal_name: Optional[str] = None,
        deal_value: Optional[float] = None,
        deal_stage_id: Optional[int] = None,
        closing_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update deal information (取引情報の更新).

        API Reference: Deals PUT endpoint

        Args:
            deal_id: Deal ID
            deal_name: Deal name
            deal_value: Deal value
            deal_stage_id: Deal stage ID
            closing_date: Expected closing date (YYYY-MM-DD)

        Returns:
            Updated deal information
        """
        endpoint = f"/api/deals/{deal_id}"

        data = {"deal": {}}

        if deal_name:
            data["deal"]["name"] = deal_name
        if deal_value is not None:
            data["deal"]["amount"] = deal_value
        if deal_stage_id:
            data["deal"]["deal_stage_id"] = deal_stage_id
        if closing_date:
            data["deal"]["expected_close_date"] = closing_date

        return self._make_request("PUT", endpoint, json=data)

    def get_deal(self, deal_id: int) -> Dict[str, Any]:
        """
        Get deal details (取引の詳細を取得).

        API Reference: Deals GET endpoint

        Args:
            deal_id: Deal ID

        Returns:
            Deal details
        """
        endpoint = f"/api/deals/{deal_id}"
        return self._make_request("GET", endpoint)

    def delete_deal(self, deal_id: int) -> Dict[str, Any]:
        """
        Delete a deal (取引を削除).

        API Reference: Deals DELETE endpoint

        Args:
            deal_id: Deal ID

        Returns:
            Deletion confirmation
        """
        endpoint = f"/api/deals/{deal_id}"
        return self._make_request("DELETE", endpoint)

    def create_task(
        self,
        title: str,
        due_date: str,
        owner_id: int,
        targetable_id: Optional[int] = None,
        targetable_type: Optional[str] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a task (タスクの作成).

        API Reference: Tasks endpoint

        Args:
            title: Task title
            due_date: Due date and time (ISO 8601 format)
            owner_id: Owner user ID
            targetable_id: Related entity ID (contact, deal, etc.)
            targetable_type: Related entity type (Contact, Deal, etc.)
            description: Task description

        Returns:
            Created task information with ID
        """
        endpoint = "/api/tasks"

        data = {
            "task": {
                "title": title,
                "due_date": due_date,
                "owner_id": owner_id
            }
        }

        if targetable_id and targetable_type:
            data["task"]["targetable_id"] = targetable_id
            data["task"]["targetable_type"] = targetable_type
        if description:
            data["task"]["description"] = description

        return self._make_request("POST", endpoint, json=data)

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        due_date: Optional[str] = None,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update task information (タスク情報の更新).

        API Reference: Tasks PUT endpoint

        Args:
            task_id: Task ID
            title: Task title
            due_date: Due date and time (ISO 8601 format)
            status: Task status (open, in_progress, completed)

        Returns:
            Updated task information
        """
        endpoint = f"/api/tasks/{task_id}"

        data = {"task": {}}

        if title:
            data["task"]["title"] = title
        if due_date:
            data["task"]["due_date"] = due_date
        if status:
            data["task"]["status"] = status

        return self._make_request("PUT", endpoint, json=data)

    def get_task(self, task_id: int) -> Dict[str, Any]:
        """
        Get task details (タスクの詳細を取得).

        API Reference: Tasks GET endpoint

        Args:
            task_id: Task ID

        Returns:
            Task details
        """
        endpoint = f"/api/tasks/{task_id}"
        return self._make_request("GET", endpoint)

    def delete_task(self, task_id: int) -> Dict[str, Any]:
        """
        Delete a task (タスクを削除).

        API Reference: Tasks DELETE endpoint

        Args:
            task_id: Task ID

        Returns:
            Deletion confirmation
        """
        endpoint = f"/api/tasks/{task_id}"
        return self._make_request("DELETE", endpoint)

    def create_note(
        self,
        description: str,
        targetable_id: int,
        targetable_type: str = "Contact",
        noteable_id: Optional[int] = None,
        noteable_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a note (ノートの新規作成).

        API Reference: Notes endpoint

        Args:
            description: Note content
            targetable_id: Target entity ID
            targetable_type: Target entity type (Contact, Deal, etc.)
            noteable_id: Related entity ID (optional for some note types)
            noteable_type: Related entity type (optional)

        Returns:
            Created note information with ID
        """
        endpoint = "/api/notes"

        data = {
            "note": {
                "description": description,
                "targetable_id": str(targetable_id),
                "targetable_type": targetable_type
            }
        }

        if noteable_id and noteable_type:
            data["note"]["noteable_id"] = str(noteable_id)
            data["note"]["noteable_type"] = noteable_type

        return self._make_request("POST", endpoint, json=data)

    def upload_file(
        self,
        file_path: str,
        targetable_id: int,
        targetable_type: str = "Contact"
    ) -> Dict[str, Any]:
        """
        Upload a file (ファイルのアップロード).

        API Reference: Files endpoint

        Args:
            file_path: Path to file to upload
            targetable_id: Target entity ID
            targetable_type: Target entity type (Contact, Deal, etc.)

        Returns:
            Uploaded file information
        """
        endpoint = "/api/files"

        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {
                'targetable_id': str(targetable_id),
                'targetable_type': targetable_type
            }

            return self._make_request("POST", endpoint, files=files, data=data)

    def search(
        self,
        query: str,
        entity_type: str = "all",
        filter: Optional[Dict[str, Any]] = None,
        page: int = 1,
        per_page: int = 30
    ) -> Dict[str, Any]:
        """
        Search for users, leads, contacts, accounts, or deals
        (ユーザー/リード/コンタクト/アカウント/取引を検索).

        API Reference: Search endpoint

        Args:
            query: Search query
            entity_type: Entity type to search (all, contact, lead, deal, account, user)
            filter: Additional filters (e.g., "status": "open")
            page: Page number (default: 1)
            per_page: Results per page (default: 30)

        Returns:
            Search results
        """
        endpoint = f"/api/{entity_type.lower()}s/search"

        params = {
            "q": query,
            "page": str(page),
            "per_page": str(per_page)
        }

        return self._make_request("GET", endpoint, params=params)