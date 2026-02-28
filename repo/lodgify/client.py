"""Lodgify Reservation Management API Client"""
import requests
from typing import Dict, List, Optional, Any

class LodgifyClient:
    def __init__(self, api_key: str, base_url: str = "https://api.lodgify.com/v1", timeout: int = 30):
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

    def get_reservations(self, property_id: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        params = {'limit': limit}
        if property_id:
            params['propertyId'] = property_id
        result = self._request('GET', '/reservations', params=params)
        return result.get('reservations', [])

    def get_reservation(self, reservation_id: str) -> Dict[str, Any]:
        return self._request('GET', f'/reservations/{reservation_id}')

    def create_reservation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request('POST', '/reservations', data=data)

    def update_reservation(self, reservation_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request('PUT', f'/reservations/{reservation_id}', data=data)

    def get_properties(self) -> List[Dict[str, Any]]:
        result = self._request('GET', '/properties')
        return result.get('properties', [])

    def get_property(self, property_id: str) -> Dict[str, Any]:
        return self._request('GET', f'/properties/{property_id}')

    def get_guests(self, limit: int = 100) -> List[Dict[str, Any]]:
        result = self._request('GET', '/guests', params={'limit': limit})
        return result.get('guests', [])

    def get_guest(self, guest_id: str) -> Dict[str, Any]:
        return self._request('GET', f'/guests/{guest_id}')

    def get_availability(self, property_id: str, start_date: str, end_date: str) -> Dict[str, Any]:
        return self._request('GET', f'/properties/{property_id}/availability', params={
            'start': start_date, 'end': end_date
        })