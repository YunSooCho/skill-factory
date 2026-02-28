"""
Chumonbunjo Cloud API Client

Chumonbunjo Cloud is a Japanese real estate and construction management system.

Supports:
- 注文住宅の契約データを作成 (Create Custom Home Contract Data)
- 注文住宅の契約データを検索 (Search Custom Home Contract Data)
- 注文住宅の契約データを更新 (Update Custom Home Contract Data)
- 注文住宅の契約データを取得 (Get Custom Home Contract Data)
- 分譲住宅の契約データを作成 (Create Housing Development Contract Data)
- 分譲住宅の契約データを検索 (Search Housing Development Contract Data)
- 分譲住宅の契約データを更新 (Update Housing Development Contract Data)
- 分譲住宅の契約データを取得 (Get Housing Development Contract Data)
- 見積書データを検索 (Search Estimate Data)
- 見積書データを取得 (Get Estimate Data)
- 見積書データのCSVを作成 (Create Estimate Data CSV)
- 見積書データのCSVファイルを取得 (Get Estimate Data CSV File)
- 顧客データを作成 (Create Customer Data)
- 顧客データを更新 (Update Customer Data)
- 顧客データを検索 (Search Customer Data)
- 顧客データを取得 (Get Customer Data)
- 仕入先業者を取得 (Get Supplier)
- 仕入先業者を作成 (Create Supplier)
- 仕入先業者を検索 (Search Supplier)
- 仕入先業者を更新 (Update Supplier)
- 協力業者アカウントを検索 (Search Cooperative Partner Account)
- 協力業者アカウントを作成 (Create Cooperative Partner Account)
- 協力業者アカウントを更新 (Update Cooperative Partner Account)
- 協力業者アカウントを取得 (Get Cooperative Partner Account)
- 発注データを取得 (Get Order Data)
- 発注データを検索 (Search Order Data)
- 発注データのCSVを作成 (Create Order Data CSV)
- 発注データのCSVファイルを取得 (Get Order Data CSV File)
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class CustomHomeContract:
    """Custom Home Contract Data (注文住宅の契約データ)"""
    id: str
    contract_number: str
    customer_id: str
    customer_name: str
    property_id: Optional[str]
    contract_date: str
    contract_amount: float
    tax_included: bool
    status: str
    completion_date: Optional[str]
    created_at: str
    updated_at: str


@dataclass
class HousingDevelopmentContract:
    """Housing Development Contract Data (分譲住宅の契約データ)"""
    id: str
    contract_number: str
    customer_id: str
    customer_name: str
    housing_id: str
    housing_number: str
    contract_date: str
    contract_amount: float
    tax_included: bool
    status: str
    handover_date: Optional[str]
    created_at: str
    updated_at: str


@dataclass
class Estimate:
    """Estimate Data (見積書データ)"""
    id: str
    estimate_number: str
    customer_id: str
    customer_name: str
    estimate_date: str
    estimate_amount: float
    tax_included: bool
    validity_period: Optional[str]
    status: str
    created_at: str
    updated_at: str


@dataclass
class Customer:
    """Customer Data (顧客データ)"""
    id: str
    customer_code: str
    name: str
    name_kana: str
    postal_code: str
    address: str
    phone: str
    email: Optional[str]
    customer_type: str
    created_at: str
    updated_at: str


@dataclass
class Supplier:
    """Supplier Data (仕入先業者)"""
    id: str
    supplier_code: str
    name: str
    name_kana: str
    postal_code: str
    address: str
    phone: str
    email: Optional[str]
    supplier_type: str
    created_at: str
    updated_at: str


@dataclass
class CooperativePartnerAccount:
    """Cooperative Partner Account (協力業者アカウント)"""
    id: str
    partner_code: str
    name: str
    name_kana: str
    postal_code: str
    address: str
    phone: str
    email: Optional[str]
    specialization: str
    status: str
    created_at: str
    updated_at: str


@dataclass
class OrderData:
    """Order Data (発注データ)"""
    id: str
    order_number: str
    supplier_id: str
    supplier_name: str
    order_date: str
    delivery_date: Optional[str]
    order_amount: float
    status: str
    created_at: str
    updated_at: str


class ChumonbunjoCloudClient:
    """
    Chumonbunjo Cloud API client for real estate and construction management.

    Authentication: API Key
    Base URL: https://api.chumonbunjo-cloud.jp
    """

    BASE_URL = "https://api.chumonbunjo-cloud.jp/v1"

    def __init__(self, api_key: str, company_code: str):
        """
        Initialize Chumonbunjo Cloud API client.

        Args:
            api_key: Chumonbunjo Cloud API key
            company_code: Company code for the account
        """
        self.api_key = api_key
        self.company_code = company_code
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={
                "X-API-Key": self.api_key,
                "X-Company-Code": self.company_code,
                "Content-Type": "application/json"
            }
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        return_binary: bool = False
    ) -> Any:
        """
        Make HTTP request to Chumonbunjo Cloud API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON body data
            return_binary: If True, return binary data (for CSV downloads)

        Returns:
            Response data as dictionary or binary

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        url = f"{self.BASE_URL}{endpoint}"

        async with self.session.request(
            method,
            url,
            params=params,
            json=json_data
        ) as response:
            if return_binary:
                return await response.read()

            data = await response.json()

            if response.status not in [200, 201, 204]:
                error_msg = data.get("message", "Unknown error") if isinstance(data, dict) else str(data)
                raise Exception(f"Chumonbunjo Cloud API error ({response.status}): {error_msg}")

            return data

    # ==================== Custom Home Contracts ====================

    async def create_custom_home_contract(
        self,
        customer_id: str,
        contract_date: str,
        contract_amount: float,
        property_id: Optional[str] = None,
        tax_included: bool = True,
        completion_date: Optional[str] = None,
        status: str = "new"
    ) -> CustomHomeContract:
        """
        Create a new custom home contract.

        注文住宅の契約データを作成

        Args:
            customer_id: Customer ID
            contract_date: Contract date (YYYY-MM-DD)
            contract_amount: Contract amount
            property_id: Optional property ID
            tax_included: Whether tax is included
            completion_date: Expected completion date (YYYY-MM-DD)
            status: Contract status

        Returns:
            CustomHomeContract object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        json_data = {
            "customer_id": customer_id,
            "contract_date": contract_date,
            "contract_amount": contract_amount,
            "tax_included": tax_included,
            "status": status
        }

        if property_id:
            json_data["property_id"] = property_id
        if completion_date:
            json_data["completion_date"] = completion_date

        data = await self._request("POST", "/contracts/custom-homes", json_data=json_data)

        return self._parse_custom_home_contract(data)

    async def get_custom_home_contract(self, contract_id: str) -> CustomHomeContract:
        """
        Get a custom home contract by ID.

        注文住宅の契約データを取得

        Args:
            contract_id: Contract ID

        Returns:
            CustomHomeContract object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        data = await self._request("GET", f"/contracts/custom-homes/{contract_id}")
        return self._parse_custom_home_contract(data)

    async def search_custom_home_contracts(
        self,
        customer_id: Optional[str] = None,
        status: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        limit: int = 50
    ) -> List[CustomHomeContract]:
        """
        Search for custom home contracts.

        注文住宅の契約データを検索

        Args:
            customer_id: Filter by customer ID
            status: Filter by status
            date_from: Filter by date from (YYYY-MM-DD)
            date_to: Filter by date to (YYYY-MM-DD)
            limit: Maximum number of results

        Returns:
            List of CustomHomeContract objects

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        params = {"limit": limit}

        if customer_id:
            params["customer_id"] = customer_id
        if status:
            params["status"] = status
        if date_from:
            params["date_from"] = date_from
        if date_to:
            params["date_to"] = date_to

        data = await self._request("GET", "/contracts/custom-homes", params=params)

        contracts = data.get("contracts", [])
        return [self._parse_custom_home_contract(c) for c in contracts]

    async def update_custom_home_contract(
        self,
        contract_id: str,
        contract_amount: Optional[float] = None,
        status: Optional[str] = None,
        completion_date: Optional[str] = None
    ) -> CustomHomeContract:
        """
        Update a custom home contract.

        注文住宅の契約データを更新

        Args:
            contract_id: Contract ID
            contract_amount: New contract amount
            status: New status
            completion_date: New completion date (YYYY-MM-DD)

        Returns:
            Updated CustomHomeContract object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        json_data = {}

        if contract_amount is not None:
            json_data["contract_amount"] = contract_amount
        if status:
            json_data["status"] = status
        if completion_date:
            json_data["completion_date"] = completion_date

        data = await self._request("PUT", f"/contracts/custom-homes/{contract_id}", json_data=json_data)

        return self._parse_custom_home_contract(data)

    def _parse_custom_home_contract(self, data: Dict[str, Any]) -> CustomHomeContract:
        """Parse custom home contract data"""
        return CustomHomeContract(
            id=data.get("id", ""),
            contract_number=data.get("contract_number", ""),
            customer_id=data.get("customer_id", ""),
            customer_name=data.get("customer_name", ""),
            property_id=data.get("property_id"),
            contract_date=data.get("contract_date", ""),
            contract_amount=float(data.get("contract_amount", 0)),
            tax_included=data.get("tax_included", True),
            status=data.get("status", ""),
            completion_date=data.get("completion_date"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    # ==================== Housing Development Contracts ====================

    async def create_housing_development_contract(
        self,
        customer_id: str,
        housing_id: str,
        housing_number: str,
        contract_date: str,
        contract_amount: float,
        tax_included: bool = True,
        handover_date: Optional[str] = None,
        status: str = "new"
    ) -> HousingDevelopmentContract:
        """
        Create a new housing development contract.

        分譲住宅の契約データを作成

        Args:
            customer_id: Customer ID
            housing_id: Housing development ID
            housing_number: Housing unit number
            contract_date: Contract date (YYYY-MM-DD)
            contract_amount: Contract amount
            tax_included: Whether tax is included
            handover_date: Expected handover date (YYYY-MM-DD)
            status: Contract status

        Returns:
            HousingDevelopmentContract object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        json_data = {
            "customer_id": customer_id,
            "housing_id": housing_id,
            "housing_number": housing_number,
            "contract_date": contract_date,
            "contract_amount": contract_amount,
            "tax_included": tax_included,
            "status": status
        }

        if handover_date:
            json_data["handover_date"] = handover_date

        data = await self._request("POST", "/contracts/housing-development", json_data=json_data)

        return self._parse_housing_development_contract(data)

    async def get_housing_development_contract(self, contract_id: str) -> HousingDevelopmentContract:
        """
        Get a housing development contract by ID.

        分譲住宅の契約データを取得

        Args:
            contract_id: Contract ID

        Returns:
            HousingDevelopmentContract object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        data = await self._request("GET", f"/contracts/housing-development/{contract_id}")
        return self._parse_housing_development_contract(data)

    async def search_housing_development_contracts(
        self,
        customer_id: Optional[str] = None,
        housing_id: Optional[str] = None,
        status: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        limit: int = 50
    ) -> List[HousingDevelopmentContract]:
        """
        Search for housing development contracts.

        分譲住宅の契約データを検索

        Args:
            customer_id: Filter by customer ID
            housing_id: Filter by housing ID
            status: Filter by status
            date_from: Filter by date from (YYYY-MM-DD)
            date_to: Filter by date to (YYYY-MM-DD)
            limit: Maximum number of results

        Returns:
            List of HousingDevelopmentContract objects

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        params = {"limit": limit}

        if customer_id:
            params["customer_id"] = customer_id
        if housing_id:
            params["housing_id"] = housing_id
        if status:
            params["status"] = status
        if date_from:
            params["date_from"] = date_from
        if date_to:
            params["date_to"] = date_to

        data = await self._request("GET", "/contracts/housing-development", params=params)

        contracts = data.get("contracts", [])
        return [self._parse_housing_development_contract(c) for c in contracts]

    async def update_housing_development_contract(
        self,
        contract_id: str,
        status: Optional[str] = None,
        handover_date: Optional[str] = None
    ) -> HousingDevelopmentContract:
        """
        Update a housing development contract.

        分譲住宅の契約データを更新

        Args:
            contract_id: Contract ID
            status: New status
            handover_date: New handover date (YYYY-MM-DD)

        Returns:
            Updated HousingDevelopmentContract object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        json_data = {}

        if status:
            json_data["status"] = status
        if handover_date:
            json_data["handover_date"] = handover_date

        data = await self._request("PUT", f"/contracts/housing-development/{contract_id}", json_data=json_data)

        return self._parse_housing_development_contract(data)

    def _parse_housing_development_contract(self, data: Dict[str, Any]) -> HousingDevelopmentContract:
        """Parse housing development contract data"""
        return HousingDevelopmentContract(
            id=data.get("id", ""),
            contract_number=data.get("contract_number", ""),
            customer_id=data.get("customer_id", ""),
            customer_name=data.get("customer_name", ""),
            housing_id=data.get("housing_id", ""),
            housing_number=data.get("housing_number", ""),
            contract_date=data.get("contract_date", ""),
            contract_amount=float(data.get("contract_amount", 0)),
            tax_included=data.get("tax_included", True),
            status=data.get("status", ""),
            handover_date=data.get("handover_date"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    # ==================== Estimates ====================

    async def search_estimates(
        self,
        customer_id: Optional[str] = None,
        estimate_number: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50
    ) -> List[Estimate]:
        """
        Search for estimates.

        見積書データを検索

        Args:
            customer_id: Filter by customer ID
            estimate_number: Filter by estimate number
            date_from: Filter by date from (YYYY-MM-DD)
            date_to: Filter by date to (YYYY-MM-DD)
            status: Filter by status
            limit: Maximum number of results

        Returns:
            List of Estimate objects

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        params = {"limit": limit}

        if customer_id:
            params["customer_id"] = customer_id
        if estimate_number:
            params["estimate_number"] = estimate_number
        if date_from:
            params["date_from"] = date_from
        if date_to:
            params["date_to"] = date_to
        if status:
            params["status"] = status

        data = await self._request("GET", "/estimates", params=params)

        estimates = data.get("estimates", [])
        return [self._parse_estimate(e) for e in estimates]

    async def get_estimate(self, estimate_id: str) -> Estimate:
        """
        Get an estimate by ID.

        見積書データを取得

        Args:
            estimate_id: Estimate ID

        Returns:
            Estimate object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        data = await self._request("GET", f"/estimates/{estimate_id}")
        return self._parse_estimate(data)

    async def create_estimate_csv(
        self,
        estimate_ids: List[str],
        format_type: str = "utf8"
    ) -> str:
        """
        Create CSV file for estimates.

        見積書データのCSVを作成

        Args:
            estimate_ids: List of estimate IDs
            format_type: Format type (utf8, sjis)

        Returns:
            CSV file download URL

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        json_data = {
            "estimate_ids": estimate_ids,
            "format": format_type
        }

        data = await self._request("POST", "/estimates/csv/create", json_data=json_data)

        return data.get("download_url", "")

    async def get_estimate_csv_file(self, estimate_id: str) -> bytes:
        """
        Download estimate CSV file.

        見積書データのCSVファイルを取得

        Args:
            estimate_id: Estimate ID

        Returns:
            CSV file content as bytes

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        return await self._request("GET", f"/estimates/{estimate_id}/csv", return_binary=True)

    def _parse_estimate(self, data: Dict[str, Any]) -> Estimate:
        """Parse estimate data"""
        return Estimate(
            id=data.get("id", ""),
            estimate_number=data.get("estimate_number", ""),
            customer_id=data.get("customer_id", ""),
            customer_name=data.get("customer_name", ""),
            estimate_date=data.get("estimate_date", ""),
            estimate_amount=float(data.get("estimate_amount", 0)),
            tax_included=data.get("tax_included", True),
            validity_period=data.get("validity_period"),
            status=data.get("status", ""),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    # ==================== Customers ====================

    async def create_customer(
        self,
        name: str,
        name_kana: str,
        postal_code: str,
        address: str,
        phone: str,
        email: Optional[str] = None,
        customer_type: str = "individual"
    ) -> Customer:
        """
        Create a new customer.

        顧客データを作成

        Args:
            name: Customer name
            name_kana: Customer name in Kana
            postal_code: Postal code
            address: Address
            phone: Phone number
            email: Email address
            customer_type: Customer type (individual, corporate)

        Returns:
            Customer object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        json_data = {
            "name": name,
            "name_kana": name_kana,
            "postal_code": postal_code,
            "address": address,
            "phone": phone,
            "customer_type": customer_type
        }

        if email:
            json_data["email"] = email

        data = await self._request("POST", "/customers", json_data=json_data)

        return self._parse_customer(data)

    async def get_customer(self, customer_id: str) -> Customer:
        """
        Get a customer by ID.

        顧客データを取得

        Args:
            customer_id: Customer ID

        Returns:
            Customer object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        data = await self._request("GET", f"/customers/{customer_id}")
        return self._parse_customer(data)

    async def search_customers(
        self,
        name: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        customer_type: Optional[str] = None,
        limit: int = 50
    ) -> List[Customer]:
        """
        Search for customers.

        顧客データを検索

        Args:
            name: Filter by name
            phone: Filter by phone
            email: Filter by email
            customer_type: Filter by customer type
            limit: Maximum number of results

        Returns:
            List of Customer objects

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        params = {"limit": limit}

        if name:
            params["name"] = name
        if phone:
            params["phone"] = phone
        if email:
            params["email"] = email
        if customer_type:
            params["customer_type"] = customer_type

        data = await self._request("GET", "/customers", params=params)

        customers = data.get("customers", [])
        return [self._parse_customer(c) for c in customers]

    async def update_customer(
        self,
        customer_id: str,
        name: Optional[str] = None,
        name_kana: Optional[str] = None,
        postal_code: Optional[str] = None,
        address: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None
    ) -> Customer:
        """
        Update a customer.

        顧客データを更新

        Args:
            customer_id: Customer ID
            name: New name
            name_kana: New name in Kana
            postal_code: New postal code
            address: New address
            phone: New phone number
            email: New email

        Returns:
            Updated Customer object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        json_data = {}

        if name:
            json_data["name"] = name
        if name_kana:
            json_data["name_kana"] = name_kana
        if postal_code:
            json_data["postal_code"] = postal_code
        if address:
            json_data["address"] = address
        if phone:
            json_data["phone"] = phone
        if email:
            json_data["email"] = email

        data = await self._request("PUT", f"/customers/{customer_id}", json_data=json_data)

        return self._parse_customer(data)

    def _parse_customer(self, data: Dict[str, Any]) -> Customer:
        """Parse customer data"""
        return Customer(
            id=data.get("id", ""),
            customer_code=data.get("customer_code", ""),
            name=data.get("name", ""),
            name_kana=data.get("name_kana", ""),
            postal_code=data.get("postal_code", ""),
            address=data.get("address", ""),
            phone=data.get("phone", ""),
            email=data.get("email"),
            customer_type=data.get("customer_type", ""),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    # ==================== Suppliers ====================

    async def get_supplier(self, supplier_id: str) -> Supplier:
        """
        Get a supplier by ID.

        仕入先業者を取得

        Args:
            supplier_id: Supplier ID

        Returns:
            Supplier object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        data = await self._request("GET", f"/suppliers/{supplier_id}")
        return self._parse_supplier(data)

    async def create_supplier(
        self,
        name: str,
        name_kana: str,
        postal_code: str,
        address: str,
        phone: str,
        email: Optional[str] = None,
        supplier_type: str = "material"
    ) -> Supplier:
        """
        Create a new supplier.

        仕入先業者を作成

        Args:
            name: Supplier name
            name_kana: Supplier name in Kana
            postal_code: Postal code
            address: Address
            phone: Phone number
            email: Email address
            supplier_type: Supplier type (material, construction, etc.)

        Returns:
            Supplier object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        json_data = {
            "name": name,
            "name_kana": name_kana,
            "postal_code": postal_code,
            "address": address,
            "phone": phone,
            "supplier_type": supplier_type
        }

        if email:
            json_data["email"] = email

        data = await self._request("POST", "/suppliers", json_data=json_data)

        return self._parse_supplier(data)

    async def search_suppliers(
        self,
        name: Optional[str] = None,
        supplier_type: Optional[str] = None,
        limit: int = 50
    ) -> List[Supplier]:
        """
        Search for suppliers.

        仕入先業者を検索

        Args:
            name: Filter by name
            supplier_type: Filter by supplier type
            limit: Maximum number of results

        Returns:
            List of Supplier objects

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        params = {"limit": limit}

        if name:
            params["name"] = name
        if supplier_type:
            params["supplier_type"] = supplier_type

        data = await self._request("GET", "/suppliers", params=params)

        suppliers = data.get("suppliers", [])
        return [self._parse_supplier(s) for s in suppliers]

    async def update_supplier(
        self,
        supplier_id: str,
        name: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None
    ) -> Supplier:
        """
        Update a supplier.

        仕入先業者を更新

        Args:
            supplier_id: Supplier ID
            name: New name
            phone: New phone number
            email: New email

        Returns:
            Updated Supplier object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        json_data = {}

        if name:
            json_data["name"] = name
        if phone:
            json_data["phone"] = phone
        if email:
            json_data["email"] = email

        data = await self._request("PUT", f"/suppliers/{supplier_id}", json_data=json_data)

        return self._parse_supplier(data)

    def _parse_supplier(self, data: Dict[str, Any]) -> Supplier:
        """Parse supplier data"""
        return Supplier(
            id=data.get("id", ""),
            supplier_code=data.get("supplier_code", ""),
            name=data.get("name", ""),
            name_kana=data.get("name_kana", ""),
            postal_code=data.get("postal_code", ""),
            address=data.get("address", ""),
            phone=data.get("phone", ""),
            email=data.get("email"),
            supplier_type=data.get("supplier_type", ""),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    # ==================== Cooperative Partners ====================

    async def search_cooperative_partners(
        self,
        name: Optional[str] = None,
        specialization: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50
    ) -> List[CooperativePartnerAccount]:
        """
        Search for cooperative partners.

        協力業者アカウントを検索

        Args:
            name: Filter by name
            specialization: Filter by specialization
            status: Filter by status
            limit: Maximum number of results

        Returns:
            List of CooperativePartnerAccount objects

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        params = {"limit": limit}

        if name:
            params["name"] = name
        if specialization:
            params["specialization"] = specialization
        if status:
            params["status"] = status

        data = await self._request("GET", "/cooperative-partners", params=params)

        partners = data.get("partners", [])
        return [self._parse_cooperative_partner(p) for p in partners]

    async def create_cooperative_partner(
        self,
        name: str,
        name_kana: str,
        postal_code: str,
        address: str,
        phone: str,
        specialization: str,
        email: Optional[str] = None,
        status: str = "active"
    ) -> CooperativePartnerAccount:
        """
        Create a new cooperative partner.

        協力業者アカウントを作成

        Args:
            name: Partner name
            name_kana: Partner name in Kana
            postal_code: Postal code
            address: Address
            phone: Phone number
            specialization: Specialization
            email: Email address
            status: Status (active, inactive)

        Returns:
            CooperativePartnerAccount object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        json_data = {
            "name": name,
            "name_kana": name_kana,
            "postal_code": postal_code,
            "address": address,
            "phone": phone,
            "specialization": specialization,
            "status": status
        }

        if email:
            json_data["email"] = email

        data = await self._request("POST", "/cooperative-partners", json_data=json_data)

        return self._parse_cooperative_partner(data)

    async def update_cooperative_partner(
        self,
        partner_id: str,
        name: Optional[str] = None,
        status: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None
    ) -> CooperativePartnerAccount:
        """
        Update a cooperative partner.

        協力業者アカウントを更新

        Args:
            partner_id: Partner ID
            name: New name
            status: New status
            phone: New phone number
            email: New email

        Returns:
            Updated CooperativePartnerAccount object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        json_data = {}

        if name:
            json_data["name"] = name
        if status:
            json_data["status"] = status
        if phone:
            json_data["phone"] = phone
        if email:
            json_data["email"] = email

        data = await self._request("PUT", f"/cooperative-partners/{partner_id}", json_data=json_data)

        return self._parse_cooperative_partner(data)

    async def get_cooperative_partner(self, partner_id: str) -> CooperativePartnerAccount:
        """
        Get a cooperative partner by ID.

        協力業者アカウントを取得

        Args:
            partner_id: Partner ID

        Returns:
            CooperativePartnerAccount object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        data = await self._request("GET", f"/cooperative-partners/{partner_id}")
        return self._parse_cooperative_partner(data)

    def _parse_cooperative_partner(self, data: Dict[str, Any]) -> CooperativePartnerAccount:
        """Parse cooperative partner data"""
        return CooperativePartnerAccount(
            id=data.get("id", ""),
            partner_code=data.get("partner_code", ""),
            name=data.get("name", ""),
            name_kana=data.get("name_kana", ""),
            postal_code=data.get("postal_code", ""),
            address=data.get("address", ""),
            phone=data.get("phone", ""),
            email=data.get("email"),
            specialization=data.get("specialization", ""),
            status=data.get("status", ""),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    # ==================== Orders ====================

    async def get_order(self, order_id: str) -> OrderData:
        """
        Get order data by ID.

        発注データを取得

        Args:
            order_id: Order ID

        Returns:
            OrderData object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        data = await self._request("GET", f"/orders/{order_id}")
        return self._parse_order(data)

    async def search_orders(
        self,
        supplier_id: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50
    ) -> List[OrderData]:
        """
        Search for order data.

        発注データを検索

        Args:
            supplier_id: Filter by supplier ID
            date_from: Filter by date from (YYYY-MM-DD)
            date_to: Filter by date to (YYYY-MM-DD)
            status: Filter by status
            limit: Maximum number of results

        Returns:
            List of OrderData objects

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        params = {"limit": limit}

        if supplier_id:
            params["supplier_id"] = supplier_id
        if date_from:
            params["date_from"] = date_from
        if date_to:
            params["date_to"] = date_to
        if status:
            params["status"] = status

        data = await self._request("GET", "/orders", params=params)

        orders = data.get("orders", [])
        return [self._parse_order(o) for o in orders]

    async def create_order_csv(
        self,
        order_ids: List[str],
        format_type: str = "utf8"
    ) -> str:
        """
        Create CSV file for orders.

        発注データのCSVを作成

        Args:
            order_ids: List of order IDs
            format_type: Format type (utf8, sjis)

        Returns:
            CSV file download URL

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        json_data = {
            "order_ids": order_ids,
            "format": format_type
        }

        data = await self._request("POST", "/orders/csv/create", json_data=json_data)

        return data.get("download_url", "")

    async def get_order_csv_file(self, order_id: str) -> bytes:
        """
        Download order CSV file.

        発注データのCSVファイルを取得

        Args:
            order_id: Order ID

        Returns:
            CSV file content as bytes

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        return await self._request("GET", f"/orders/{order_id}/csv", return_binary=True)

    def _parse_order(self, data: Dict[str, Any]) -> OrderData:
        """Parse order data"""
        return OrderData(
            id=data.get("id", ""),
            order_number=data.get("order_number", ""),
            supplier_id=data.get("supplier_id", ""),
            supplier_name=data.get("supplier_name", ""),
            order_date=data.get("order_date", ""),
            delivery_date=data.get("delivery_date"),
            order_amount=float(data.get("order_amount", 0)),
            status=data.get("status", ""),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )


# ==================== Example Usage ====================

async def main():
    """Example usage of Chumonbunjo Cloud API client"""

    api_key = "your_chumonbunjo_api_key"
    company_code = "your_company_code"

    async with ChumonbunjoCloudClient(api_key, company_code) as client:
        # Create a customer
        customer = await client.create_customer(
            name="田中太郎",
            name_kana="タナカタロウ",
            postal_code="100-0001",
            address="東京都千代田区1-2-3",
            phone="03-1234-5678",
            email="tanaka@example.com"
        )
        print(f"Created customer: {customer.id}")

        # Create a custom home contract
        contract = await client.create_custom_home_contract(
            customer_id=customer.id,
            contract_date="2024-01-15",
            contract_amount=15000000.0,
            tax_included=True,
            status="new"
        )
        print(f"Created custom home contract: {contract.id}")

        # Search customers
        customers = await client.search_customers(name="田中", limit=10)
        print(f"Found {len(customers)} customers")

        # Search estimates
        estimates = await client.search_estimates(customer_id=customer.id)
        print(f"Found {len(estimates)} estimates")

        # Create a supplier
        supplier = await client.create_supplier(
            name="ABC建材株式会社",
            name_kana="エービーシーケンザイ",
            postal_code="101-0001",
            address="東京都港区1-2-3",
            phone="03-9876-5432",
            supplier_type="material"
        )
        print(f"Created supplier: {supplier.id}")


if __name__ == "__main__":
    asyncio.run(main())