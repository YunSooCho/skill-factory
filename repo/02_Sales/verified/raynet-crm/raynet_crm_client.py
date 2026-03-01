"""
Raynet CRM API Client
API Documentation: https://raynet.info/api/
"""

import requests
from typing import Optional, Dict, List, Any


class RaynetCrmAPIError(Exception):
    """Custom exception for Raynet CRM API errors."""
    pass


class RaynetCrmClient:
    """Client for Raynet CRM API."""

    def __init__(self, api_key: str, base_url: str = "https://app.raynet.cz/api/v2"):
        """
        Initialize Raynet CRM API client.

        Args:
            api_key: Your Raynet CRM API key
            base_url: API base URL (default: https://app.raynet.cz/api/v2)
        """
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "X-Instance-Name": api_key,
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
            raise RaynetCrmAPIError(
                f"HTTP {response.status_code}: {error_data.get('message', str(e))}"
            )
        except requests.exceptions.RequestException as e:
            raise RaynetCrmAPIError(f"Request failed: {str(e)}")

    def _parse_error(self, response: requests.Response) -> Dict[str, Any]:
        """Parse error response."""
        try:
            return response.json() if response.content else {"message": response.text}
        except Exception:
            return {"message": response.text}

    def create_account(
        self,
        name: str,
        identification_number: Optional[str] = None,
        vat_number: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        website: Optional[str] = None,
        address: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Create a new account (Create Account).

        API Reference: Accounts endpoint

        Args:
            name: Company name
            identification_number: Company registration number
            vat_number: VAT number
            phone: Phone number
            email: Email address
            website: Website URL
            address: Address dict with keys: street, city, zip, country

        Returns:
            Created account information with ID
        """
        endpoint = "/companies"

        data = {"primaryName": name}

        if identification_number:
            data["identificationNumber"] = identification_number
        if vat_number:
            data["vatNumber"] = vat_number
        if phone:
            data["phone"] = phone
        if email:
            data["email"] = email
        if website:
            data["website"] = website
        if address:
            data["address"] = address

        return self._make_request("POST", endpoint, json=data)

    def get_account(self, account_id: int) -> Dict[str, Any]:
        """
        Get account details (Get Account).

        API Reference: Accounts GET endpoint

        Args:
            account_id: Account ID

        Returns:
            Account details
        """
        endpoint = f"/companies/{account_id}"
        return self._make_request("GET", endpoint)

    def search_accounts(
        self,
        query: Optional[str] = None,
        limit: int = 20
    ) -> Dict[str, Any]:
        """
        Search accounts (Search Account).

        API Reference: Accounts search endpoint

        Args:
            query: Search query (name, email, phone)
            limit: Maximum results

        Returns:
            List of accounts
        """
        endpoint = "/companies/"

        params = {}
        if query:
            params["query"] = query
        params["limit"] = limit

        return self._make_request("GET", endpoint, params=params)

    def update_account(
        self,
        account_id: int,
        name: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update an account (Update Account).

        API Reference: Accounts PUT endpoint

        Args:
            account_id: Account ID
            name: Company name
            phone: Phone number
            email: Email address

        Returns:
            Updated account information
        """
        endpoint = f"/companies/{account_id}"

        data = {}
        if name:
            data["primaryName"] = name
        if phone:
            data["phone"] = phone
        if email:
            data["email"] = email

        return self._make_request("PUT", endpoint, json=data)

    def delete_account(self, account_id: int) -> Dict[str, Any]:
        """
        Delete an account (Delete Account).

        API Reference: Accounts DELETE endpoint

        Args:
            account_id: Account ID

        Returns:
            Deletion confirmation
        """
        endpoint = f"/companies/{account_id}"
        return self._make_request("DELETE", endpoint)

    def create_contact(
        self,
        first_name: str,
        last_name: str,
        company_id: Optional[int] = None,
        position: Optional[str] = None,
        phone: Optional[str] = None,
        mobile: Optional[str] = None,
        email: Optional[str] = None,
        address: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Create a new contact (Create Contact).

        API Reference: Contacts endpoint

        Args:
            first_name: First name
            last_name: Last name
            company_id: Associated company ID
            position: Job position/title
            phone: Phone number
            mobile: Mobile phone number
            email: Email address
            address: Address dict

        Returns:
            Created contact information with ID
        """
        endpoint = "/people"

        data = {
            "primaryName": first_name,
            "lastName": last_name
        }

        if company_id:
            data["companyId"] = company_id
        if position:
            data["position"] = position
        if phone:
            data["phone"] = phone
        if mobile:
            data["mobile"] = mobile
        if email:
            data["email"] = email
        if address:
            data["address"] = address

        return self._make_request("POST", endpoint, json=data)

    def get_contact(self, contact_id: int) -> Dict[str, Any]:
        """
        Get contact details (Get Contact).

        API Reference: Contacts GET endpoint

        Args:
            contact_id: Contact ID

        Returns:
            Contact details
        """
        endpoint = f"/people/{contact_id}"
        return self._make_request("GET", endpoint)

    def search_contacts(
        self,
        query: Optional[str] = None,
        company_id: Optional[int] = None,
        limit: int = 20
    ) -> Dict[str, Any]:
        """
        Search contacts (Search Contact).

        API Reference: Contacts search endpoint

        Args:
            query: Search query
            company_id: Filter by company ID
            limit: Maximum results

        Returns:
            List of contacts
        """
        endpoint = "/people/"

        params = {}
        if query:
            params["query"] = query
        if company_id:
            params["companyId"] = company_id
        params["limit"] = limit

        return self._make_request("GET", endpoint, params=params)

    def update_contact(
        self,
        contact_id: int,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        position: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update a contact (Update Contact).

        API Reference: Contacts PUT endpoint

        Args:
            contact_id: Contact ID
            first_name: First name
            last_name: Last name
            position: Job position
            phone: Phone number
            email: Email address

        Returns:
            Updated contact information
        """
        endpoint = f"/people/{contact_id}"

        data = {}
        if first_name:
            data["primaryName"] = first_name
        if last_name:
            data["lastName"] = last_name
        if position:
            data["position"] = position
        if phone:
            data["phone"] = phone
        if email:
            data["email"] = email

        return self._make_request("PUT", endpoint, json=data)

    def delete_contact(self, contact_id: int) -> Dict[str, Any]:
        """
        Delete a contact (Delete Contact).

        API Reference: Contacts DELETE endpoint

        Args:
            contact_id: Contact ID

        Returns:
            Deletion confirmation
        """
        endpoint = f"/people/{contact_id}"
        return self._make_request("DELETE", endpoint)

    def create_product(
        self,
        name: str,
        code: str,
        price: Optional[float] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new product (Create Product).

        API Reference: Products endpoint

        Args:
            name: Product name
            code: Product code
            price: Unit price
            description: Product description

        Returns:
            Created product information with ID
        """
        endpoint = "/products"

        data = {
            "primaryName": name,
            "code": code
        }

        if price is not None:
            data["price"] = price
        if description:
            data["description"] = description

        return self._make_request("POST", endpoint, json=data)

    def get_product(self, product_id: int) -> Dict[str, Any]:
        """
        Get product details (Get Product).

        API Reference: Products GET endpoint

        Args:
            product_id: Product ID

        Returns:
            Product details
        """
        endpoint = f"/products/{product_id}"
        return self._make_request("GET", endpoint)

    def search_products(
        self,
        query: Optional[str] = None,
        limit: int = 20
    ) -> Dict[str, Any]:
        """
        Search products (Search Product).

        API Reference: Products search endpoint

        Args:
            query: Search query
            limit: Maximum results

        Returns:
            List of products
        """
        endpoint = "/products/"

        params = {}
        if query:
            params["query"] = query
        params["limit"] = limit

        return self._make_request("GET", endpoint, params=params)

    def update_product(
        self,
        product_id: int,
        name: Optional[str] = None,
        price: Optional[float] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update a product (Update Product).

        API Reference: Products PUT endpoint

        Args:
            product_id: Product ID
            name: Product name
            price: Unit price
            description: Product description

        Returns:
            Updated product information
        """
        endpoint = f"/products/{product_id}"

        data = {}
        if name:
            data["primaryName"] = name
        if price is not None:
            data["price"] = price
        if description:
            data["description"] = description

        return self._make_request("PUT", endpoint, json=data)

    def delete_product(self, product_id: int) -> Dict[str, Any]:
        """
        Delete a product (Delete Product).

        API Reference: Products DELETE endpoint

        Args:
            product_id: Product ID

        Returns:
            Deletion confirmation
        """
        endpoint = f"/products/{product_id}"
        return self._make_request("DELETE", endpoint)

    def create_lead(
        self,
        first_name: str,
        last_name: str,
        company_name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new lead (Create Lead).

        API Reference: Leads endpoint

        Args:
            first_name: First name
            last_name: Last name
            company_name: Company name
            email: Email address
            phone: Phone number
            status: Lead status

        Returns:
            Created lead information with ID
        """
        endpoint = "/leads"

        data = {
            "primaryName": first_name,
            "lastName": last_name
        }

        if company_name:
            data["primaryCompany"] = company_name
        if email:
            data["email"] = email
        if phone:
            data["phone"] = phone
        if status:
            data["status"] = status

        return self._make_request("POST", endpoint, json=data)

    def get_lead(self, lead_id: int) -> Dict[str, Any]:
        """
        Get lead details (Get Lead).

        API Reference: Leads GET endpoint

        Args:
            lead_id: Lead ID

        Returns:
            Lead details
        """
        endpoint = f"/leads/{lead_id}"
        return self._make_request("GET", endpoint)

    def search_leads(
        self,
        query: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 20
    ) -> Dict[str, Any]:
        """
        Search leads (Search Lead).

        API Reference: Leads search endpoint

        Args:
            query: Search query
            status: Filter by status
            limit: Maximum results

        Returns:
            List of leads
        """
        endpoint = "/leads/"

        params = {}
        if query:
            params["query"] = query
        if status:
            params["status"] = status
        params["limit"] = limit

        return self._make_request("GET", endpoint, params=params)

    def update_lead(
        self,
        lead_id: int,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update a lead (Update Lead).

        API Reference: Leads PUT endpoint

        Args:
            lead_id: Lead ID
            first_name: First name
            last_name: Last name
            status: Lead status

        Returns:
            Updated lead information
        """
        endpoint = f"/leads/{lead_id}"

        data = {}
        if first_name:
            data["primaryName"] = first_name
        if last_name:
            data["lastName"] = last_name
        if status:
            data["status"] = status

        return self._make_request("PUT", endpoint, json=data)

    def delete_lead(self, lead_id: int) -> Dict[str, Any]:
        """
        Delete a lead (Delete Lead).

        API Reference: Leads DELETE endpoint

        Args:
            lead_id: Lead ID

        Returns:
            Deletion confirmation
        """
        endpoint = f"/leads/{lead_id}"
        return self._make_request("DELETE", endpoint)