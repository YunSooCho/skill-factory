"""
Airtable Pocket API Client

This module provides a Python client for interacting with Airtable Pocket,
the mobile companion for quick data capture and offline access.
"""

import requests
from typing import Dict, List, Optional, Any
import json


class PocketClient:
    """
    Client for Airtable Pocket API.

    Pocket provides:
    - Quick data capture from mobile
    - Offline data access
    - QR code scanning
    - Photo capture
    - Voice notes
    """

    def __init__(
        self,
        api_token: str,
        base_url: str = "https://api.airtable.com/v0",
        timeout: int = 30
    ):
        """Initialize the Pocket client."""
        self.api_token = api_token
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json'
        })

    def _request(self, method: str, endpoint: str, params=None, data=None) -> Dict[str, Any]:
        """Make an authenticated request to the API."""
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, params=params, json=data, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def quick_capture(
        self,
        base_id: str,
        table_id: str,
        data: Dict[str, Any],
        source: str = "pocket"
    ) -> Dict[str, Any]:
        """Quick capture a record from Pocket."""
        payload = {
            'fields': data,
            'source': source,
            'sourceMetadata': {
                'platform': 'pocket',
                'timestamp': None
            }
        }
        return self._request('POST', f'/{base_id}/{table_id}', data=payload)

    def add_note(
        self,
        base_id: str,
        table_id: str,
        record_id: str,
        note: str,
        note_type: str = "text"
    ) -> Dict[str, Any]:
        """Add a note to a record."""
        payload = {
            'note': note,
            'type': note_type
        }
        return self._request('POST', f'/{base_id}/{table_id}/{record_id}/notes', data=payload)

    def add_photo(
        self,
        base_id: str,
        table_id: str,
        record_id: str,
        photo_url: str,
        caption: Optional[str] = None
    ) -> Dict[str, Any]:
        """Add a photo to a record."""
        payload = {
            'url': photo_url,
            'caption': caption
        }
        return self._request('POST', f'/{base_id}/{table_id}/{record_id}/photos', data=payload)

    def add_voice_note(
        self,
        base_id: str,
        table_id: str,
        record_id: str,
        audio_url: str,
        transcription: Optional[str] = None
    ) -> Dict[str, Any]:
        """Add a voice note to a record."""
        payload = {
            'audioUrl': audio_url,
            'transcription': transcription
        }
        return self._request('POST', f'/{base_id}/{table_id}/{record_id}/voiceNotes', data=payload)

    def scan_qr_code(
        self,
        base_id: str,
        table_id: str,
        qr_data: str,
        lookup_field: str
    ) -> Dict[str, Any]:
        """Scan QR code and find matching record."""
        params = {
            'qrData': qr_data,
            'lookupField': lookup_field
        }
        return self._request('GET', f'/{base_id}/{table_id}/qrLookup', params=params)

    def get_offline_records(
        self,
        base_id: str,
        table_id: str,
        last_sync: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get records for offline access."""
        params = {'forOffline': True}
        if last_sync:
            params['lastSync'] = last_sync
        result = self._request('GET', f'/{base_id}/{table_id}', params=params)
        return result.get('records', [])

    def sync_offline_changes(
        self,
        base_id: str,
        table_id: str,
        changes: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Sync offline changes to the server."""
        payload = {
            'changes': changes
        }
        return self._request('POST', f'/{base_id}/{table_id}/sync', data=payload)

    def create_form_submission(
        self,
        base_id: str,
        form_id: str,
        submission_data: Dict[str, Any],
        location: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Submit a form from Pocket."""
        payload = {
            'data': submission_data
        }
        if location:
            payload['location'] = location
        return self._request('POST', f'/{base_id}/forms/{form_id}/submissions', data=payload)

    def get_nearby_records(
        self,
        base_id: str,
        table_id: str,
        location: Dict[str, float],
        radius: float = 1000,
        location_field: str = "Location"
    ) -> List[Dict[str, Any]]:
        """Get records near a location."""
        params = {
            'lat': location['lat'],
            'lng': location['lng'],
            'radius': radius,
            'locationField': location_field
        }
        result = self._request('GET', f'/{base_id}/{table_id}/nearby', params=params)
        return result.get('records', [])

    def get_sync_status(self, base_id: str, table_id: str) -> Dict[str, Any]:
        """Get sync status for offline data."""
        return self._request('GET', f'/{base_id}/{table_id}/syncStatus')

    def set_background_sync(
        self,
        base_id: str,
        table_id: str,
        enabled: bool,
        interval: int = 300
    ) -> Dict[str, Any]:
        """Configure background sync settings."""
        payload = {
            'enabled': enabled,
            'interval': interval
        }
        return self._request('POST', f'/{base_id}/{table_id}/backgroundSync', data=payload)

    def get_pocket_templates(
        self,
        base_id: str,
        table_id: str
    ) -> List[Dict[str, Any]]:
        """Get data capture templates for Pocket."""
        result = self._request('GET', f'/{base_id}/{table_id}/pocketTemplates')
        return result.get('templates', [])

    def create_pocket_template(
        self,
        base_id: str,
        table_id: str,
        name: str,
        fields: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Create a data capture template."""
        payload = {
            'name': name,
            'fields': fields
        }
        return self._request('POST', f'/{base_id}/{table_id}/pocketTemplates', data=payload)

    def get_recent_activity(
        self,
        base_id: str,
        table_id: str,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Get recent Pocket activity."""
        params = {'limit': limit}
        result = self._request('GET', f'/{base_id}/{table_id}/pocketActivity', params=params)
        return result.get('activity', [])