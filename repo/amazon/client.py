"""
Amazon MWS / SP-API Client
Amazon Marketplace Web Services and Selling Partner API client.
Integration for products, orders, inventory, and more.
Documentation: https://developer.amazon.com/
"""

import os
import requests
import hashlib
import hmac
import urllib.parse
from datetime import datetime
from typing import Optional, Dict, List, Any


class AmazonClient:
    """
    Complete client for Amazon MWS/SP-API operations.
    Supports Marketplace Web Services and Selling Partner API.
    """
    
    def __init__(
        self,
        seller_id: Optional[str] = None,
        access_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        marketplace_id: Optional[str] = None,
        sp_api_token: Optional[str] = None,
        region: str = "US",
        timeout: int = 30,
        verify_ssl: bool = True
    ):
        """
        Initialize Amazon client.
        
        Args:
            seller_id: Merchant/Seller ID (from env: AMAZON_SELLER_ID)
            access_key: AWS Access Key (from env: AMAZON_ACCESS_KEY)
            secret_key: AWS Secret Key (from env: AMAZON_SECRET_KEY)
            marketplace_id: Marketplace ID (from env: AMAZON_MARKETPLACE_ID)
            sp_api_token: SP-API LWA access token (from env: AMAZON_SP_API_TOKEN)
            region: AWS region (US, EU, etc.)
            timeout: Request timeout
            verify_ssl: SSL verification
            
        Environment variables:
            AMAZON_SELLER_ID: Your merchant/seller ID
            AMAZON_ACCESS_KEY: AWS access key ID
            AMAZON_SECRET_KEY: AWS secret access key
            AMAZON_MARKETPLACE_ID: Marketplace ID (e.g., ATVPDKIKX0DER for US)
            AMAZON_SP_API_TOKEN: Selling Partner API token
        """
        self.seller_id = seller_id or os.getenv("AMAZON_SELLER_ID")
        self.access_key = access_key or os.getenv("AMAZON_ACCESS_KEY")
        self.secret_key = secret_key or os.getenv("AMAZON_SECRET_KEY")
        self.marketplace_id = marketplace_id or os.getenv("AMAZON_MARKETPLACE_ID")
        self.sp_api_token = sp_api_token or os.getenv("AMAZON_SP_API_TOKEN")
        self.region = region
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        
        self.session = requests.Session()
        
        # Region endpoints
        self.endpoints = {
            "US": ("https://mws.amazonservices.com", "https://sellingpartnerapi-na.amazon.com"),
            "EU": ("https://mws-eu.amazonservices.com", "https://sellingpartnerapi-eu.amazon.com"),
            "FE": ("https://mws-fe.amazonservices.com", "https://sellingpartnerapi-fe.amazon.com")
        }
    
    def _sign_mws_request(
        self,
        endpoint: str,
        action: str,
        params: Dict[str, str],
        method: str = "POST"
    ) -> str:
        """
        Sign MWS request with AWS signature.
        """
        # Add standard params
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        params.update({
            "AWSAccessKeyId": self.access_key,
            "Action": action,
            "SellerId": self.seller_id,
            "SignatureVersion": "2",
            "SignatureMethod": "HmacSHA256",
            "Timestamp": timestamp,
            "Version": "2013-09-01"
        })
        
        if self.marketplace_id:
            params["MarketplaceId"] = self.marketplace_id
        
        # Sort parameters
        sorted_params = sorted(params.items())
        query_string = "&".join([f"{k}={urllib.parse.quote(str(v), safe='')}" for k, v in sorted_params])
        
        # Create canonical string
        canonical = f"{method}\n{urllib.parse.urlparse(endpoint).netloc}\n/\n{query_string}"
        
        # Sign
        signature = hmac.new(
            self.secret_key.encode(),
            canonical.encode(),
            hashlib.sha256
        ).digest()
        
        encoded_signature = urllib.parse.quote(signature, safe='')
        
        return f"{endpoint}?{query_string}&Signature={encoded_signature}"
    
    def _mws_request(
        self,
        action: str,
        params: Dict[str, str],
        method: str = "POST"
    ) -> Dict[str, Any]:
        """
        Make MWS request.
        """
        mws_endpoint, _ = self.endpoints.get(self.region, self.endpoints["US"])
        
        signed_url = self._sign_mws_request(mws_endpoint, action, params, method)
        
        response = self.session.get(
            signed_url,
            timeout=self.timeout,
            verify=self.verify_ssl
        )
        response.raise_for_status()
        
        return response.text if response.text else {}
    
    # ============================================================================
    # Orders (MWS)
    # ============================================================================
    
    def list_orders(
        self,
        created_after: Optional[str] = None,
        created_before: Optional[str] = None,
        last_updated_after: Optional[str] = None,
        last_updated_before: Optional[str] = None,
        order_statuses: Optional[List[str]] = None,
        marketplace_ids: Optional[List[str]] = None,
        max_results_per_page: int = 100
    ) -> Dict[str, Any]:
        """
        List orders from Amazon MWS.
        
        Args:
            created_after: Orders created after this date (ISO 8601)
            created_before: Orders created before this date
            last_updated_after: Orders updated after this date
            last_updated_before: Orders updated before this date
            order_statuses: List of order statuses
            marketplace_ids: List of marketplace IDs
            max_results_per_page: Max results (1-100)
            
        Returns:
            Orders data
        """
        params = {"MaxResultsPerPage": str(max_results_per_page)}
        
        if created_after:
            params["CreatedAfter"] = created_after
        if created_before:
            params["CreatedBefore"] = created_before
        if last_updated_after:
            params["LastUpdatedAfter"] = last_updated_after
        if last_updated_before:
            params["LastUpdatedBefore"] = last_updated_before
        if order_statuses:
            params["OrderStatus.Status.1"] = order_statuses[0]
        if marketplace_ids:
            params["MarketplaceId.Id.1"] = marketplace_ids[0]
        
        return self._mws_request("ListOrders", params)
    
    def get_order(self, amazon_order_id: str) -> Dict[str, Any]:
        """
        Get details of a specific order.
        """
        params = {"AmazonOrderId": amazon_order_id}
        return self._mws_request("GetOrder", params)
    
    def list_order_items(self, amazon_order_id: str) -> Dict[str, Any]:
        """
        List items in an order.
        """
        params = {"AmazonOrderId": amazon_order_id}
        return self._mws_request("ListOrderItems", params)
    
    # ============================================================================
    # Inventory (MWS)
    # ============================================================================
    
    def list_inventory_supply(
        self,
        marketplace_id: Optional[str] = None,
        response_group: str = "Basic",
        merchant_skus: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get inventory supply for SKUs.
        
        Args:
            marketplace_id: Marketplace ID
            response_group: Response group (Basic, Detail)
            merchant_skus: List of merchant SKUs
            
        Returns:
            Inventory data
        """
        params = {"ResponseGroup": response_group}
        
        if marketplace_id:
            params["MarketplaceId"] = marketplace_id
        
        if merchant_skus:
            for i, sku in enumerate(merchant_skus, 1):
                params[f"MerchantSKU.SKU.{i}"] = sku
        
        return self._mws_request("ListInventorySupply", params)
    
    # ============================================================================
    # Products (MWS)
    # ============================================================================
    
    def get_matching_product_for_id(
        self,
        marketplace_id: str,
        id_type: str,
        id_list: List[str]
    ) -> Dict[str, Any]:
        """
        Get product information for ASIN, SellerSKU, UPC, etc.
        
        Args:
            marketplace_id: Marketplace ID
            id_type: ID type (ASIN, SellerSKU, UPC, EAN, ISBN)
            id_list: List of IDs
            
        Returns:
            Product data
        """
        params = {
            "MarketplaceId": marketplace_id,
            "IdType": id_type
        }
        
        for i, id_val in enumerate(id_list, 1):
            params[f"IdList.Id.{i}"] = id_val
        
        return self._mws_request("GetMatchingProductForId", params)
    
    def get_product_categories_for_sku(
        self,
        marketplace_id: str,
        seller_sku: str
    ) -> Dict[str, Any]:
        """
        Get category information for a SKU.
        """
        params = {
            "MarketplaceId": marketplace_id,
            "SellerSKU": seller_sku
        }
        return self._mws_request("GetProductCategoriesForSKU", params)
    
    # ============================================================================
    # Reports (MWS)
    # ============================================================================
    
    def request_report(
        self,
        report_type: str,
        marketplace_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Request a report.
        
        Args:
            report_type: Report type (see MWS docs)
            marketplace_id: Marketplace ID
            start_date: Start date (ISO 8601)
            end_date: End date (ISO 8601)
            
        Returns:
            Report request result
        """
        params = {"ReportType": report_type}
        
        if marketplace_id:
            params["MarketplaceIdList.Id.1"] = marketplace_id
        if start_date:
            params["StartDate"] = start_date
        if end_date:
            params["EndDate"] = end_date
        
        return self._mws_request("RequestReport", params)
    
    def get_report_list(
        self,
        report_types: Optional[List[str]] = None,
        max_count: int = 100
    ) -> Dict[str, Any]:
        """
        Get list of available reports.
        """
        params = {"MaxCount": str(max_count)}
        
        if report_types:
            for i, rt in enumerate(report_types, 1):
                params[f"ReportTypeList.Type.{i}"] = rt
        
        return self._mws_request("GetReportList", params)
    
    def get_report(self, report_id: str) -> str:
        """
        Get report content.
        """
        params = {"ReportId": report_id}
        return self._mws_request("GetReport", params)
    
    # ============================================================================
    # Feeds (MWS)
    # ============================================================================
    
    def submit_feed(
        self,
        feed_type: str,
        feed_content: str,
        marketplace_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Submit a feed (for bulk operations).
        
        Args:
            feed_type: Feed type
            feed_content: Feed content (XML)
            marketplace_id: Marketplace ID
            
        Returns:
            Feed submission result
        """
        params = {
            "FeedType": feed_type,
            "FeedContent": feed_content
        }
        
        if marketplace_id:
            params["MarketplaceIdList.Id.1"] = marketplace_id
        
        return self._mws_request("SubmitFeed", params, method="POST")
    
    def get_feed_submission_list(
        self,
        feed_ids: Optional[List[str]] = None,
        max_count: int = 100
    ) -> Dict[str, Any]:
        """
        Get list of feed submissions.
        """
        params = {"MaxCount": str(max_count)}
        
        if feed_ids:
            for i, fid in enumerate(feed_ids, 1):
                params[f"FeedSubmissionIdList.Id.{i}"] = fid
        
        return self._mws_request("GetFeedSubmissionList", params)
    
    # ============================================================================
    # Financials (MWS)
    # ============================================================================
    
    def list_financial_events(
        self,
        posted_after: Optional[str] = None,
        posted_before: Optional[str] = None,
        max_results: int = 100
    ) -> Dict[str, Any]:
        """
        List financial events.
        """
        params = {"MaxResultsPerPage": str(max_results)}
        
        if posted_after:
            params["FinancialEventGroupStartedAfter"] = posted_after
        if posted_before:
            params["FinancialEventGroupStartedBefore"] = posted_before
        
        return self._mws_request("ListFinancialEventGroups", params)
    
    # ============================================================================
    # SP-API (Selling Partner API) Basic Support
    # ============================================================================
    
    def _sp_request(
        self,
        endpoint: str,
        method: str = "GET",
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make SP-API request.
        """
        _, sp_endpoint = self.endpoints.get(self.region, self.endpoints["US"])
        url = f"{sp_endpoint}{endpoint}"
        
        headers = {
            "Authorization": f"Bearer {self.sp_api_token}",
            "x-amz-date": datetime.utcnow().strftime("%Y%m%dT%H%M%SZ"),
            "Content-Type": "application/json"
        }
        
        response = self.session.request(
            method=method,
            url=url,
            json=data,
            headers=headers,
            timeout=self.timeout,
            verify=self.verify_ssl
        )
        response.raise_for_status()
        
        return response.json()
    
    def get_orders_sp(
        self,
        created_after: str,
        marketplace_ids: List[str],
        order_statuses: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get orders via Selling Partner API.
        """
        params = {
            "createdAfter": created_after,
            "marketplaceIds": marketplace_ids
        }
        
        if order_statuses:
            params["orderStatuses"] = order_statuses
        
        return self._sp_request("/orders/v0/orders", params=urllib.parse.urlencode(params))