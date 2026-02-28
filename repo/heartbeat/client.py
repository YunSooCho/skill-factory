import requests
from typing import Dict, List, Optional


class HeartbeatClient:
    """Client for Heartbeat API - Community Platform"""

    def __init__(self, api_key: str, base_url: str = "https://api.heartbeat.chat"):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
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

    def get_user(self, user_id: str) -> Dict:
        return self._request('GET', f'/v1/users/{user_id}')

    def create_event(self, event_data: Dict) -> Dict:
        return self._request('POST', '/v1/events', json=event_data)

    def invite_users(self, user_ids: List[str]) -> Dict:
        return self._request('POST', '/v1/invitations', json={'user_ids': user_ids})

    def create_channel(self, name: str, **kwargs) -> Dict:
        data = {'name': name, **kwargs}
        return self._request('POST', '/v1/channels', json=data)

    def create_group(self, name: str, **kwargs) -> Dict:
        data = {'name': name, **kwargs}
        return self._request('POST', '/v1/groups', json=data)

    def delete_user(self, user_id: str) -> Dict:
        return self._request('DELETE', f'/v1/users/{user_id}')

    def get_channel_threads(self, channel_id: str) -> List[Dict]:
        result = self._request('GET', f'/v1/channels/{channel_id}/threads')
        return result.get('threads', [])

    def add_to_group(self, group_id: str, user_ids: List[str]) -> Dict:
        return self._request('POST', f'/v1/groups/{group_id}/members', json={'user_ids': user_ids})

    def create_comment(self, thread_id: str, content: str) -> Dict:
        return self._request('POST', f'/v1/threads/{thread_id}/comments', json={'content': content})

    def delete_from_group(self, group_id: str, user_ids: List[str]) -> Dict:
        return self._request('DELETE', f'/v1/groups/{group_id}/members', json={'user_ids': user_ids})

    def create_thread(self, channel_id: str, title: str, content: str) -> Dict:
        return self._request('POST', f'/v1/channels/{channel_id}/threads', json={
            'title': title,
            'content': content
        })

    def send_direct_message(self, recipient_id: str, content: str) -> Dict:
        return self._request('POST', '/v1/messages', json={
            'recipient_id': recipient_id,
            'content': content
        })