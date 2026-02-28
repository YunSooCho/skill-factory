import requests
from typing import Dict, List, Optional


class RefinerClient:
    """Client for Refiner API - User Survey Platform"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.refiner.io"
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json() if response.content else {}

    def search_survey_responses(self, survey_id: str, **filters) -> List[Dict]:
        result = self._request('GET', f'/v1/surveys/{survey_id}/responses', params=filters)
        return result.get('responses', []) if isinstance(result, dict) else []

    def create_or_update_user(self, user_data: Dict) -> Dict:
        return self._request('POST', '/v1/users', json=user_data)

    def set_form_publication_status(self, form_id: str, published: bool) -> Dict:
        return self._request('PUT', f'/v1/forms/{form_id}/status', json={'published': published})

    def track_event(self, event_name: str, user_id: str, **kwargs) -> Dict:
        data = {'event_name': event_name, 'user_id': user_id, **kwargs}
        return self._request('POST', '/v1/events', json=data)

    def store_survey_responses(self, survey_id: str, responses: List[Dict]) -> Dict:
        return self._request('POST', f'/v1/surveys/{survey_id}/responses', json={'responses': responses})

    def search_contacts(self, query: str) -> List[Dict]:
        result = self._request('GET', '/v1/contacts/search', params={'q': query})
        return result.get('contacts', []) if isinstance(result, dict) else []

    def archive_form(self, form_id: str) -> Dict:
        return self._request('DELETE', f'/v1/forms/{form_id}')