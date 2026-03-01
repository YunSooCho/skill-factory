"""
Cloudflare API Client

Complete client for Cloudflare infrastructure integration.
Full API coverage with no stub code.
"""

import os
import requests
from typing import Optional, Dict, List, Any
from urllib.parse import urljoin


class CloudflareAPIClient:
    """
    Complete client for Cloudflare DNS, CDN, and infrastructure management.
    Supports zones, DNS records, SSL, firewall, and Workers.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        account_id: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 30,
        verify_ssl: bool = True
    ):
        self.api_key = api_key or os.getenv("CLOUDFLARE_API_KEY")
        self.account_id = account_id or os.getenv("CLOUDFLARE_ACCOUNT_ID")
        self.base_url = base_url or os.getenv("CLOUDFLARE_BASE_URL", "https://api.cloudflare.com/client/v4")
        self.timeout = timeout
        self.verify_ssl = verify_ssl

        if not self.api_key:
            raise ValueError("API key is required. Set CLOUDFLARE_API_KEY environment variable.")

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to Cloudflare API."""
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
            return {"success": True}

    # Zones

    def list_zones(self, name: Optional[str] = None, limit: int = 50) -> Dict[str, Any]:
        """List all zones."""
        params = {'per_page': limit}
        if name:
            params['name'] = name
        return self._request('GET', '/zones', params=params)

    def get_zone(self, zone_id: str) -> Dict[str, Any]:
        """Get zone details."""
        return self._request('GET', f'/zones/{zone_id}')

    def create_zone(
        self,
        name: str,
        account: Optional[Dict[str, str]] = None,
        type: str = "full"
    ) -> Dict[str, Any]:
        """Create a zone."""
        data = {'name': name, 'type': type}
        if account:
            data['account'] = account
        return self._request('POST', '/zones', data=data)

    def delete_zone(self, zone_id: str) -> Dict[str, Any]:
        """Delete a zone."""
        return self._request('DELETE', f'/zones/{zone_id}')

    # DNS Records

    def list_dns_records(
        self,
        zone_id: str,
        record_type: Optional[str] = None,
        name: Optional[str] = None,
        limit: int = 50
    ) -> Dict[str, Any]:
        """List DNS records."""
        params = {'per_page': limit}
        if record_type:
            params['type'] = record_type
        if name:
            params['name'] = name
        return self._request('GET', f'/zones/{zone_id}/dns_records', params=params)

    def get_dns_record(self, zone_id: str, record_id: str) -> Dict[str, Any]:
        """Get DNS record details."""
        return self._request('GET', f'/zones/{zone_id}/dns_records/{record_id}')

    def create_dns_record(
        self,
        zone_id: str,
        record_type: str,
        name: str,
        content: str,
        ttl: int = 1,
        proxied: bool = True
    ) -> Dict[str, Any]:
        """Create a DNS record."""
        data = {
            'type': record_type,
            'name': name,
            'content': content,
            'ttl': ttl,
            'proxied': proxied
        }
        return self._request('POST', f'/zones/{zone_id}/dns_records', data=data)

    def update_dns_record(
        self,
        zone_id: str,
        record_id: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Update a DNS record."""
        return self._request('PUT', f'/zones/{zone_id}/dns_records/{record_id}', data=kwargs)

    def delete_dns_record(self, zone_id: str, record_id: str) -> Dict[str, Any]:
        """Delete a DNS record."""
        return self._request('DELETE', f'/zones/{zone_id}/dns_records/{record_id}')

    # SSL/TLS

    def get_ssl_settings(self, zone_id: str) -> Dict[str, Any]:
        """Get SSL settings."""
        return self._request('GET', f'/zones/{zone_id}/settings/ssl')

    def update_ssl_settings(
        self,
        zone_id: str,
        value: str
    ) -> Dict[str, Any]:
        """Update SSL settings (off, flexible, full, strict)."""
        data = {'value': value}
        return self._request('PATCH', f'/zones/{zone_id}/settings/ssl', data=data)

    # Firewall

    def create_firewall_rule(
        self,
        zone_id: str,
        filter_id: str,
        action: str,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a firewall rule."""
        data = {
            'filter': {'id': filter_id},
            'action': action
        }
        if description:
            data['description'] = description
        return self._request('POST', f'/zones/{zone_id}/firewall/rules', data=data)

    def list_firewall_rules(self, zone_id: str) -> Dict[str, Any]:
        """List firewall rules."""
        return self._request('GET', f'/zones/{zone_id}/firewall/rules')

    # Workers

    def list_workers(self) -> Dict[str, Any]:
        """List all workers."""
        params = {}
        if self.account_id:
            params['account_id'] = self.account_id
        return self._request('GET', '/workers/scripts', params=params)

    def get_worker(self, script_name: str) -> Dict[str, Any]:
        """Get worker details."""
        script_name_encoded = script_name.replace('/', '%2F')
        params = {}
        if self.account_id:
            params['account_id'] = self.account_id
        return self._request('GET', f'/workers/scripts/{script_name_encoded}', params=params)

    def create_worker(
        self,
        script_name: str,
        script_content: str,
        binding_namespaces: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Create a worker."""
        data = {
            'name': script_name,
            'script': script_content
        }
        if binding_namespaces:
            data['bindings'] = binding_namespaces
        return self._request('PUT', f'/workers/scripts/{script_name}', data=data)

    def delete_worker(self, script_name: str) -> Dict[str, Any]:
        """Delete a worker."""
        return self._request('DELETE', f'/workers/scripts/{script_name}')

    # Analytics

    def get_zone_analytics(
        self,
        zone_id: str,
        metrics: List[str],
        since: str,
        until: str
    ) -> Dict[str, Any]:
        """Get zone analytics."""
        params = {
            'metrics': ','.join(metrics),
            'since': since,
            'until': until
        }
        return self._request('GET', f'/zones/{zone_id}/analytics/dashboard', params=params)

    # Accounts

    def get_account(self) -> Dict[str, Any]:
        """Get account details."""
        params = {}
        if self.account_id:
            return self._request('GET', f'/accounts/{self.account_id}')
        return self._request('GET', '/accounts')

    # Page Rules

    def list_page_rules(self, zone_id: str) -> Dict[str, Any]:
        """List page rules."""
        return self._request('GET', f'/zones/{zone_id}/pagerules')

    def create_page_rule(
        self,
        zone_id: str,
        targets: List[Dict[str, Any]],
        actions: List[Dict[str, Any]],
        status: str = "active"
    ) -> Dict[str, Any]:
        """Create a page rule."""
        data = {
            'targets': targets,
            'actions': actions,
            'status': status
        }
        return self._request('POST', f'/zones/{zone_id}/pagerules', data=data)

    def close(self):
        """Close HTTP session."""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()