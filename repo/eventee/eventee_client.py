import requests
import time
from typing import Dict

class EventeeAPIError(Exception):
    pass

class EventeeClient:
    def __init__(self, api_key: str, base_url: str = "https://api.eventee.cz/v1", timeout: int = 30, max_retries: int = 3):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout, self.max_retries = timeout, max_retries
        self._last_request = 0
        self._min_interval = 0.1

    def _make_request(self, method: str, endpoint: str, json_data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict:
        url = f"{self.base_url}{endpoint}"
        headers = {'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'}
        for attempt in range(self.max_retries):
            try:
                time.sleep(max(0, self._min_interval - (time.time() - self._last_request)))
                response = requests.request(method, url, json=json_data, params=params, headers=headers, timeout=self.timeout)
                self._last_request = time.time()
                if response.status_code == 429:
                    if attempt < self.max_retries - 1:
                        time.sleep(1); continue
                if not response.ok:
                    raise EventeeAPIError(f"API error {response.status_code}: {response.text}")
                return response.json()
            except requests.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise EventeeAPIError(f"Request failed: {str(e)}")
                time.sleep(1)
        raise EventeeAPIError("Max retries exceeded")

    def create_speaker(self, name: str, bio: Optional[str] = None, photo_url: Optional[str] = None) -> Dict:
        data = {'name': name}
        if bio: data['bio'] = bio
        if photo_url: data['photo_url'] = photo_url
        return self._make_request('POST', '/speakers', json_data=data)

    def update_speaker(self, speaker_id: str, data: Dict) -> Dict:
        return self._make_request('PUT', f'/speakers/{speaker_id}', json_data=data)

    def delete_speaker(self, speaker_id: str) -> Dict:
        return self._make_request('DELETE', f'/speakers/{speaker_id}')

    def create_hall(self, name: str, description: Optional[str] = None, capacity: Optional[int] = None) -> Dict:
        data = {'name': name}
        if description: data['description'] = description
        if capacity: data['capacity'] = capacity
        return self._make_request('POST', '/halls', json_data=data)

    def update_hall(self, hall_id: str, data: Dict) -> Dict:
        return self._make_request('PUT', f'/halls/{hall_id}', json_data=data)

    def delete_hall(self, hall_id: str) -> Dict:
        return self._make_request('DELETE', f'/halls/{hall_id}')

    def create_track(self, name: str, color: Optional[str] = None) -> Dict:
        data = {'name': name}
        if color: data['color'] = color
        return self._make_request('POST', '/tracks', json_data=data)

    def update_track(self, track_id: str, data: Dict) -> Dict:
        return self._make_request('PUT', f'/tracks/{track_id}', json_data=data)

    def delete_track(self, track_id: str) -> Dict:
        return self._make_request('DELETE', f'/tracks/{track_id}')

    def create_lecture(self, title: str, start_time: str, end_time: str, speaker_id: str, hall_id: str, track_id: Optional[str] = None) -> Dict:
        data = {'title': title, 'start_time': start_time, 'end_time': end_time, 'speaker_id': speaker_id, 'hall_id': hall_id}
        if track_id: data['track_id'] = track_id
        return self._make_request('POST', '/lectures', json_data=data)

    def update_lecture(self, lecture_id: str, data: Dict) -> Dict:
        return self._make_request('PUT', f'/lectures/{lecture_id}', json_data=data)

    def delete_lecture(self, lecture_id: str) -> Dict:
        return self._make_request('DELETE', f'/lectures/{lecture_id}')

    def get_all_content(self, limit: int = 100, offset: int = 0) -> Dict:
        return self._make_request('GET', '/content', params={'limit': limit, 'offset': offset})

    def invite_attendee(self, email: str, first_name: str, last_name: str) -> Dict:
        return self._make_request('POST', '/attendees', json_data={'email': email, 'first_name': first_name, 'last_name': last_name})

    def remove_attendee(self, attendee_id: str) -> Dict:
        return self._make_request('DELETE', f'/attendees/{attendee_id}')

    def close(self):
        self.session = None