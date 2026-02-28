"""mSpy Monitoring API Client"""
import requests
from typing import Dict, List, Optional, Any

class MspyClient:
    def __init__(self, api_key: str, base_url: str = "https://api.mspy.com/v1", timeout: int = 30):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'})

    def _request(self, method: str, endpoint: str, params=None, data=None) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, params=params, json=data, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def get_devices(self) -> List[Dict[str, Any]]:
        result = self._request('GET', '/devices')
        return result.get('devices', [])

    def get_device(self, device_id: str) -> Dict[str, Any]:
        return self._request('GET', f'/devices/{device_id}')

    def get_activity_logs(self, device_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        result = self._request('GET', f'/devices/{device_id}/activity', params={'limit': limit})
        return result.get('logs', [])

    def get_location(self, device_id: str) -> Dict[str, Any]:
        return self._request('GET', f'/devices/{device_id}/location')

    def get_messages(self, device_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        result = self._request('GET', f'/devices/{device_id}/messages', params={'limit': limit})
        return result.get('messages', [])

    def get_calls(self, device_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        result = self._request('GET', f'/devices/{device_id}/calls', params={'limit': limit})
        return result.get('calls', [])

    def get_app_usage(self, device_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        result = self._request('GET', f'/devices/{device_id}/apps', params={'limit': limit})
        return result.get('apps', [])

    def set_alert(self, device_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request('POST', f'/devices/{device_id}/alerts', data=data)

    def get_alerts(self, device_id: str) -> List[Dict[str, Any]]:
        result = self._request('GET', f'/devices/{device_id}/alerts')
        return result.get('alerts', [])