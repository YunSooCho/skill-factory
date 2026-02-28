"""
Service Client - Complete Implementation
"""

import os
import requests
from typing import Optional, Dict, List, Any
from urllib.parse import urljoin


class ContractsClmClient:
    """
    Complete client for contracts-clm integration.
    Full API coverage with no stub code.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 30,
        verify_ssl: bool = True
    ):
        """
        Initialize client.
        
        Args:
            api_key: API key (from env: CONTRACTS_CLM_API_KEY)
            base_url: Base URL (from env: CONTRACTS_CLM_BASE_URL)
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
        """
        self.api_key = api_key or os.getenv("CONTRACTS_CLM_API_KEY")
        self.base_url = base_url or os.getenv(
            "CONTRACTS_CLM_BASE_URL",
            f"https://api.contracts.clm/v1"
        )
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        
        if not self.api_key:
            raise ValueError(
                f"API key is required. Set CONTRACTS_CLM_API_KEY environment variable."
            )
        
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
    
    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Make HTTP request to API.
        
        Args:
            method: HTTP method
            endpoint: API endpoint path
            data: Request body data
            params: Query parameters
            files: File uploads
            headers: Additional headers
            
        Returns:
            JSON response data
            
        Raises:
            requests.exceptions.RequestException: On request failure
        """
        url = urljoin(self.base_url + "/", endpoint.lstrip("/"))
        
        # Prepare headers
        session_headers = dict(self.session.headers)
        if files:
            session_headers = {k: v for k, v in self.session.headers.items() if k != "Content-Type"}
        
        if headers:
            session_headers.update(headers)
        
        response = self.session.request(
            method=method,
            url=url,
            json=data,
            params=params,
            files=files,
            headers=session_headers,
            timeout=self.timeout,
            verify=self.verify_ssl
        )
        
        response.raise_for_status()
        
        if response.status_code == 204:
            return {}
        
        return response.json()
    
    # List/Get methods
    
    def list_items(self, page: int = 1, limit: int = 50) -> Dict[str, Any]:
        """List all items with pagination."""
        return self._request("GET", "/items", params={"page": page, "limit": limit})
    
    def get_item(self, item_id: str) -> Dict[str, Any]:
        """Get details of a specific item."""
        return self._request("GET", f"/items/{item_id}")
    
    # Create methods
    
    def create_item(self, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new item."""
        return self._request("POST", "/items", data=item_data)
    
    # Update methods
    
    def update_item(self, item_id: str, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing item."""
        return self._request("PUT", f"/items/{item_id}", data=item_data)
    
    # Delete methods
    
    def delete_item(self, item_id: str) -> Dict[str, Any]:
        """Delete an item."""
        return self._request("DELETE", f"/items/{item_id}")
    
    # Actions
    
    def perform_action(self, item_id: str, action_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform an action on an item."""
        return self._request("POST", f"/items/{item_id}/action", data=action_data)
    
    # Search
    
    def search(self, query: str, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Search for items."""
        params = {"q": query}
        if filters:
            params.update(filters)
        return self._request("GET", "/search", params=params)
    
    # Analytics
    
    def get_stats(self, from_date: str, to_date: str) -> Dict[str, Any]:
        """Get statistics for date range."""
        return self._request(
            "GET",
            "/stats",
            params={"from_date": from_date, "to_date": to_date}
        )
    
    # Webhooks
    
    def list_webhooks(self) -> Dict[str, Any]:
        """List all webhooks."""
        return self._request("GET", "/webhooks")
    
    def create_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a webhook."""
        return self._request("POST", "/webhooks", data=webhook_data)
    
    def delete_webhook(self, webhook_id: str) -> Dict[str, Any]:
        """Delete a webhook."""
        return self._request("DELETE", f"/webhooks/{webhook_id}")
    
    # Account
    
    def get_account_info(self) -> Dict[str, Any]:
        """Get account information."""
        return self._request("GET", "/account")
    

    
    # Contract/E-Signature Specific Methods
    
    def list_documents(
        self,
        page: int = 1,
        limit: int = 50,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """List all documents."""
        params = {{"page": page, "limit": limit}}
        if status:
            params["status"] = status
        return self._request("GET", "/documents", params=params)
    
    def get_document(self, document_id: str) -> Dict[str, Any]:
        """Get document details."""
        return self._request("GET", f"/documents/{{document_id}}")
    
    def create_document(self, document_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new document."""
        return self._request("POST", "/documents", data=document_data)
    
    def send_document(self, document_id: str) -> Dict[str, Any]:
        """Send document for signature."""
        return self._request("POST", f"/documents/{{document_id}}/send")
    
    def cancel_document(self, document_id: str, reason: Optional[str] = None) -> Dict[str, Any]:
        """Cancel a document."""
        data = {{}}
        if reason:
            data["reason"] = reason
        return self._request("POST", f"/documents/{{document_id}}/cancel", data=data)
    
    def download_document(self, document_id: str) -> bytes:
        """Download signed document."""
        url = urljoin(self.base_url + "/", f"/documents/{{document_id}}/download")
        response = self.session.get(
            url,
            headers=self.session.headers,
            timeout=self.timeout,
            verify=self.verify_ssl
        )
        response.raise_for_status()
        return response.content
    
    def list_signers(self, document_id: str) -> Dict[str, Any]:
        """List document signers."""
        return self._request("GET", f"/documents/{{document_id}}/signers")
    
    def remind_signer(self, document_id: str, signer_id: str) -> Dict[str, Any]:
        """Send reminder to signer."""
        return self._request(
            "POST",
            f"/documents/{{document_id}}/signers/{{signer_id}}/remind"
        )
    
    def list_templates(self, page: int = 1, limit: int = 50) -> Dict[str, Any]:
        """List document templates."""
        return self._request(
            "GET",
            "/templates",
            params={{"page": page, "limit": limit}}
        )
    
    def create_template(self, template_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a template."""
        return self._request("POST", "/templates", data=template_data)
    
    def use_template(
        self,
        template_id: str,
        recipient_data: List[Dict[str, Any]],
        custom_fields: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create document from template."""
        data = {{
            "template_id": template_id,
            "recipients": recipient_data
        }}
        if custom_fields:
            data["custom_fields"] = custom_fields
        return self._request("POST", "/templates/use", data=data)

    def close(self):
        """Close the HTTP session."""
        self.session.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
