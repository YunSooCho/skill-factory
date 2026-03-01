"""
Hot Profile API Client
Japanese comprehensive CRM platform with business cards, leads, deals, and reporting

API Documentation: https://hot-profile.jp/api (assumed structure)
"""

import requests
import time
from typing import Dict, List, Optional, Any
from requests.exceptions import RequestException


class HotProfileAPIError(Exception):
    """Custom exception for HotProfile API errors"""
    pass


class HotProfileRateLimitError(HotProfileAPIError):
    """Rate limit exceeded error"""
    pass


class HotProfileClient:
    """
    HotProfile REST API Client
    Supports comprehensive CRM operations including:
    - Business cards (名刺)
    - Leads (リード)
    - Companies (会社)
    - Deals (商談)
    - Products/Items (商品マスター)
    - Reports (報告管理)
    - Tasks (タスク)
    """

    def __init__(self, api_key: str, domain: str, timeout: int = 30):
        """
        Initialize HotProfile API client

        Args:
            api_key: API key for authentication
            domain: HotProfile domain (e.g., 'company.hot-profile.jp')
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.domain = domain
        self.timeout = timeout
        self.base_url = f"https://{domain}/api/v1"
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'X-API-Key': api_key
        })
        self.last_request_time = 0
        self.min_request_interval = 0.2  # 200ms between requests
        self.rate_limit_remaining = None

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None,
                     params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make an authenticated API request with error handling and rate limiting

        Args:
            method: HTTP method
            endpoint: API endpoint
            data: Request body data
            params: Query parameters

        Returns:
            Response data as dictionary
        """
        # Rate limiting
        current_time = time.time()

        if self.rate_limit_remaining is not None and self.rate_limit_remaining <= 0:
            time.sleep(1)

        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)

        url = f"{self.base_url}{endpoint}"

        try:
            if method.upper() == 'GET':
                response = self.session.get(url, params=params, timeout=self.timeout)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data, params=params, timeout=self.timeout)
            elif method.upper() == 'PUT':
                response = self.session.put(url, json=data, params=params, timeout=self.timeout)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url, params=params, timeout=self.timeout)
            else:
                raise HotProfileAPIError(f"Unsupported HTTP method: {method}")

            self.last_request_time = time.time()

            # Update rate limit info
            self.rate_limit_remaining = int(response.headers.get('X-RateLimit-Remaining', '1'))

            # Handle rate limiting (HTTP 429)
            if response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 5))
                time.sleep(retry_after)
                return self._make_request(method, endpoint, data, params)

            # Handle errors
            if response.status_code >= 400:
                try:
                    error_data = response.json()
                except:
                    error_data = {}
                error_msg = error_data.get('error', error_data.get('message', response.text))
                raise HotProfileAPIError(f"API error {response.status_code}: {error_msg}")

            return response.json() if response.content else {}

        except RequestException as e:
            raise HotProfileAPIError(f"Request failed: {str(e)}")

    # ========== BUSINESS CARD METHODS (名刺) ==========

    def create_business_card(self, **kwargs) -> Dict[str, Any]:
        """
        Register business card information

        Args:
            **kwargs: Business card fields (name, company, email, phone, etc.)

        Returns:
            Created business card data
        """
        return self._make_request('POST', '/business_cards', data=kwargs)

    def update_business_card(self, card_id: str, **kwargs) -> Dict[str, Any]:
        """Update business card"""
        return self._make_request('PUT', f'/business_cards/{card_id}', data=kwargs)

    def search_business_cards(self, query: Optional[str] = None, **filter_params) -> List[Dict[str, Any]]:
        """Search business cards"""
        params = {}
        if query:
            params['q'] = query
        params.update(filter_params)
        return self._make_request('GET', '/business_cards', params=params)

    def get_business_card_fields(self) -> Dict[str, Any]:
        """Get business card field information"""
        return self._make_request('GET', '/business_cards/fields')

    def update_business_card_custom_fields(self, card_id: str, **custom_fields) -> Dict[str, Any]:
        """Update business card custom fields"""
        return self._make_request('PUT', f'/business_cards/{card_id}/custom_fields', data=custom_fields)

    # ========== LEAD METHODS (リード) ==========

    def create_lead(self, **kwargs) -> Dict[str, Any]:
        """
        Create a new lead

        Args:
            **kwargs: Lead fields (name, email, phone, status, etc.)

        Returns:
            Created lead data
        """
        return self._make_request('POST', '/leads', data=kwargs)

    def update_lead(self, lead_id: str, **kwargs) -> Dict[str, Any]:
        """Update lead"""
        return self._make_request('PUT', f'/leads/{lead_id}', data=kwargs)

    def get_lead_info(self, lead_id: str) -> Dict[str, Any]:
        """Get lead information"""
        return self._make_request('GET', f'/leads/{lead_id}')

    def search_leads(self, query: Optional[str] = None, **filter_params) -> List[Dict[str, Any]]:
        """Search leads"""
        params = {}
        if query:
            params['q'] = query
        params.update(filter_params)
        return self._make_request('GET', '/leads', params=params)

    def update_lead_custom_fields(self, lead_id: str, **custom_fields) -> Dict[str, Any]:
        """Update lead custom fields"""
        return self._make_request('PUT', f'/leads/{lead_id}/custom_fields', data=custom_fields)

    def get_lead_fields(self) -> Dict[str, Any]:
        """Get lead field information"""
        return self._make_request('GET', '/leads/fields')

    # ========== COMPANY METHODS (会社) ==========

    def create_company(self, **kwargs) -> Dict[str, Any]:
        """
        Create a new company

        Args:
            **kwargs: Company fields (name, website, address, etc.)

        Returns:
            Created company data
        """
        return self._make_request('POST', '/companies', data=kwargs)

    def update_company(self, company_id: str, **kwargs) -> Dict[str, Any]:
        """Update company"""
        return self._make_request('PUT', f'/companies/{company_id}', data=kwargs)

    def get_company_info(self, company_id: str) -> Dict[str, Any]:
        """Get company information"""
        return self._make_request('GET', f'/companies/{company_id}')

    def search_companies(self, query: Optional[str] = None, **filter_params) -> List[Dict[str, Any]]:
        """Search companies"""
        params = {}
        if query:
            params['q'] = query
        params.update(filter_params)
        return self._make_request('GET', '/companies', params=params)

    def update_company_custom_fields(self, company_id: str, **custom_fields) -> Dict[str, Any]:
        """Update company custom fields"""
        return self._make_request('PUT', f'/companies/{company_id}/custom_fields', data=custom_fields)

    def get_company_fields(self) -> Dict[str, Any]:
        """Get company field information"""
        return self._make_request('GET', '/companies/fields')

    # ========== DEAL METHODS (商談) ==========

    def create_deal(self, **kwargs) -> Dict[str, Any]:
        """
        Create a new deal

        Args:
            **kwargs: Deal fields (name, amount, stage, close_date, etc.)

        Returns:
            Created deal data
        """
        return self._make_request('POST', '/deals', data=kwargs)

    def update_deal(self, deal_id: str, **kwargs) -> Dict[str, Any]:
        """Update deal"""
        return self._make_request('PUT', f'/deals/{deal_id}', data=kwargs)

    def search_deals(self, query: Optional[str] = None, **filter_params) -> List[Dict[str, Any]]:
        """Search deals"""
        params = {}
        if query:
            params['q'] = query
        params.update(filter_params)
        return self._make_request('GET', '/deals', params=params)

    def update_deal_custom_fields(self, deal_id: str, **custom_fields) -> Dict[str, Any]:
        """Update deal custom fields"""
        return self._make_request('PUT', f'/deals/{deal_id}/custom_fields', data=custom_fields)

    def get_deal_fields(self) -> Dict[str, Any]:
        """Get deal field information"""
        return self._make_request('GET', '/deals/fields')

    # ========== PRODUCT/ITEM METHODS (商品マスター) ==========

    def create_product(self, **kwargs) -> Dict[str, Any]:
        """Register product master"""
        return self._make_request('POST', '/products', data=kwargs)

    def update_product(self, product_id: str, **kwargs) -> Dict[str, Any]:
        """Update product master"""
        return self._make_request('PUT', f'/products/{product_id}', data=kwargs)

    def search_products(self, query: Optional[str] = None, **filter_params) -> List[Dict[str, Any]]:
        """Search product master"""
        params = {}
        if query:
            params['q'] = query
        params.update(filter_params)
        return self._make_request('GET', '/products', params=params)

    # ========== TASK METHODS (タスク) ==========

    def search_tasks(self, query: Optional[str] = None, **filter_params) -> List[Dict[str, Any]]:
        """Search tasks"""
        params = {}
        if query:
            params['q'] = query
        params.update(filter_params)
        return self._make_request('GET', '/tasks', params=params)

    # ========== REPORT MANAGEMENT METHODS (報告管理) ==========

    def create_report(self, **kwargs) -> Dict[str, Any]:
        """Register report management"""
        return self._make_request('POST', '/reports', data=kwargs)

    def update_report(self, report_id: str, **kwargs) -> Dict[str, Any]:
        """Update report management"""
        return self._make_request('PUT', f'/reports/{report_id}', data=kwargs)

    def search_reports(self, query: Optional[str] = None, **filter_params) -> List[Dict[str, Any]]:
        """Search report management"""
        params = {}
        if query:
            params['q'] = query
        params.update(filter_params)
        return self._make_request('GET', '/reports', params=params)

    def update_report_custom_fields(self, report_id: str, **custom_fields) -> Dict[str, Any]:
        """Update report management custom fields"""
        return self._make_request('PUT', f'/reports/{report_id}/custom_fields', data=custom_fields)

    def get_report_fields(self) -> Dict[str, Any]:
        """Get report management field information"""
        return self._make_request('GET', '/reports/fields')


if __name__ == '__main__':
    import os

    API_KEY = os.getenv('HOT_PROFILE_API_KEY', 'your_api_key')
    DOMAIN = os.getenv('HOT_PROFILE_DOMAIN', 'your-company.hot-profile.jp')

    client = HotProfileClient(api_key=API_KEY, domain=DOMAIN)

    try:
        # Example: Create a lead
        lead = client.create_lead(
            name="山田 太郎",
            company="株式会社サンプル",
            email="yamada@example.com",
            status="新規"
        )
        print(f"Created lead: {lead}")

        # Example: Create a company
        company = client.create_company(
            name="株式会社サンプル",
            website="https://example.com",
            industry="テクノロジー"
        )
        print(f"Created company: {company}")

        # Example: Create a business card
        card = client.create_business_card(
            name="佐藤 花子",
            title="担当者",
            company="株式会社ABC",
            email="satou@abc.com",
            phone="03-1234-5678"
        )
        print(f"Created business card: {card}")

        # Example: Create a deal
        deal = client.create_deal(
            name="大型案件",
            amount=10000000,
            stage="商談中",
            expected_close_date="2025-06-30"
        )
        print(f"Created deal: {deal}")

        # Example: Search leads
        leads = client.search_leads(query="山田")
        print(f"Search results: {leads}")

        # Example: Get field information
        lead_fields = client.get_lead_fields()
        print(f"Lead fields: {lead_fields}")

    except HotProfileAPIError as e:
        print(f"Error: {e}")