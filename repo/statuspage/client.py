import requests
from typing import Dict, Optional


class StatuspageClient:
    """Client for Statuspage API - Status Page Platform"""

    def __init__(self, api_key: str, page_id: str):
        self.api_key = api_key
        self.page_id = page_id
        self.base_url = "https://api.statuspage.io"
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'OAuth {api_key}',
            'Content-Type': 'application/json'
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json() if response.content else {}

    def create_scheduled_maintenance(self, maintenance_data: Dict) -> Dict:
        return self._request('POST', f'/v1/pages/{self.page_id}/scheduled-maintenances', json={
            'scheduled_maintenance': maintenance_data
        })

    def create_incident(self, incident_data: Dict) -> Dict:
        return self._request('POST', f'/v1/pages/{self.page_id}/incidents', json={
            'incident': incident_data
        })

    def update_incident(self, incident_id: str, data: Dict) -> Dict:
        return self._request('PATCH', f'/v1/pages/{self.page_id}/incidents/{incident_id}', json={
            'incident': data
        })

    def search_subscribers(self, query: str) -> Dict:
        return self._request('GET', f'/v1/pages/{self.page_id}/subscribers/search', params={'query': query})

    def search_incidents(self, query: str) -> Dict:
        return self._request('GET', f'/v1/pages/{self.page_id}/incidents/search', params={'query': query})