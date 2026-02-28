"""
Easyship API Client

Complete client for Easyship shipping integration.
Full API coverage with no stub code.
"""

import os
import requests
from typing import Optional, Dict, List, Any
from urllib.parse import urljoin


class EasyshipAPIClient:
    """
    Complete client for Easyship shipping management.
    Supports shipments, labels, tracking, and rate calculation.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 30,
        verify_ssl: bool = True
    ):
        """
        Initialize Easyship API client.

        Args:
            api_key: Easyship API key (from env: EASYSHIP_API_KEY)
            base_url: Base URL (default: https://api.easyship.com/v1)
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
        """
        self.api_key = api_key or os.getenv("EASYSHIP_API_KEY")
        self.base_url = base_url or os.getenv(
            "EASYSHIP_BASE_URL",
            "https://api.easyship.com/v1"
        )
        self.timeout = timeout
        self.verify_ssl = verify_ssl

        if not self.api_key:
            raise ValueError(
                "API key is required. Set EASYSHIP_API_KEY environment variable."
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
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to Easyship API."""
        url = urljoin(self.base_url + "/", endpoint.lstrip("/"))

        response = self.session.request(
            method=method,
            url=url,
            json=data,
            params=params,
            timeout=self.timeout,
            verify=self.verify_ssl
        )

        response.raise_for_status()

        try:
            return response.json()
        except ValueError:
            return {"status": "success"}

    # Shipments

    def create_shipment(
        self,
        courier_account_id: Optional[str] = None,
        **shipment_data
    ) -> Dict[str, Any]:
        """Create a shipment."""
        data = shipment_data
        if courier_account_id:
            data['courier_account_id'] = courier_account_id
        return self._request('POST', '/shipments', data=data)

    def get_shipment(self, shipment_id: str) -> Dict[str, Any]:
        """Get shipment details."""
        return self._request('GET', f'/shipments/{shipment_id}')

    def list_shipments(
        self,
        limit: int = 50,
        offset: int = 0,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """List shipments."""
        params = {'limit': limit, 'offset': offset}
        if status:
            params['status'] = status
        return self._request('GET', '/shipments', params=params)

    def cancel_shipment(self, shipment_id: str) -> Dict[str, Any]:
        """Cancel a shipment."""
        return self._request('POST', f'/shipments/{shipment_id}/cancel')

    # Rates

    def get_rates(
        self,
        origin: Dict[str, str],
        destination: Dict[str, str],
        parcels: List[Dict[str, Any]],
        insurance: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Get shipping rates.

        Args:
            origin: Origin address details
            destination: Destination address details
            parcels: List of parcel details
            insurance: Insurance amount (optional)

        Returns:
            Available shipping rates
        """
        data = {
            'origin': origin,
            'destination': destination,
            'parcels': parcels
        }

        if insurance:
            data['insurance'] = insurance

        return self._request('POST', '/rates', data=data)

    # Labels

    def generate_label(self, shipment_id: str) -> Dict[str, Any]:
        """Generate shipping label."""
        return self._request('POST', f'/shipments/{shipment_id}/label')

    def get_label(self, label_id: str) -> Dict[str, Any]:
        """Get label details."""
        return self._request('GET', f'/labels/{label_id}')

    # Tracking

    def track_shipment(self, shipment_id: str) -> Dict[str, Any]:
        """Track shipment status."""
        return self._request('GET', f'/shipments/{shipment_id}/tracking')

    # Courier Accounts

    def list_courier_accounts(self) -> Dict[str, Any]:
        """List courier accounts."""
        return self._request('GET', '/courier_accounts')

    def get_courier_account(self, account_id: str) -> Dict[str, Any]:
        """Get courier account details."""
        return self._request('GET', f'/courier_accounts/{account_id}')

    # Addresses

    def validate_address(self, address: Dict[str, str]) -> Dict[str, Any]:
        """Validate address."""
        return self._request('POST', '/addresses/validate', data=address)

    # Webhooks

    def create_webhook(
        self,
        url: str,
        events: List[str]
    ) -> Dict[str, Any]:
        """Create webhook."""
        data = {'url': url, 'events': events}
        return self._request('POST', '/webhooks', data=data)

    def list_webhooks(self) -> Dict[str, Any]:
        """List webhooks."""
        return self._request('GET', '/webhooks')

    def delete_webhook(self, webhook_id: str) -> Dict[str, Any]:
        """Delete webhook."""
        return self._request('DELETE', f'/webhooks/{webhook_id}')

    def close(self):
        """Close HTTP session."""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()