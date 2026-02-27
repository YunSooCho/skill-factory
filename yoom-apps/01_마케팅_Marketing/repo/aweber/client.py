"""
AWeber API Client
"""

import logging
import requests
from typing import List, Optional, Dict, Any
from .models import Subscriber, List, BroadcastOpen, BroadcastClick, BroadcastStatistic

logger = logging.getLogger(__name__)


class AWeberClient:
    """
    AWeber Client for Yoom Integration

    API Actions:
    - Get Subscriber
    - Find Subscriber
    - Get Broadcast Open
    - Get Broadcast Statistic
    - Search List
    - Move Subscriber
    - Create Subscriber
    - Get Broadcast Click
    - Delete Subscriber by Email
    - Update Subscriber by Email
    """

    BASE_URL = "https://api.aweber.com/1.0"

    def __init__(self, access_token: str, account_id: str):
        self.access_token = access_token
        self.account_id = account_id
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        url = f"{self.BASE_URL}/{endpoint}"
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"AWeber Error: {e}")
            raise

    def get_subscriber(self, subscriber_id: str, list_id: str) -> Subscriber:
        result = self._request('GET', f'accounts/{self.account_id}/lists/{list_id}/subscribers/{subscriber_id}')
        s = result
        return Subscriber(
            id=s['id'],
            email=s['email'],
            name=s.get('name'),
            status=s.get('status'),
            subscription_time=s.get('subscription_time')
        )

    def find_subscriber(self, email: str, list_id: str) -> Optional[Subscriber]:
        params = {'email': email}
        result = self._request('GET', f'accounts/{self.account_id}/lists/{list_id}/subscribers', params=params)
        subs = result.get('entries', [])
        if subs:
            s = subs[0]
            return Subscriber(
                id=s['id'], email=s['email'],
                name=s.get('name'), status=s.get('status', 'subscribed')
            )
        return None

    def create_subscriber(
        self,
        email: str,
        list_id: str,
        name: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Subscriber:
        data = {'ws.op': 'create', 'email': email}
        if name:
            data['name'] = name
        if tags:
            data['tags'] = tags
        result = self._request('POST', f'accounts/{self.account_id}/lists/{list_id}/subscribers', json=data)
        s = result
        return Subscriber(
            id=s['id'],
            email=s['email'],
            name=s.get('name'),
            status=s.get('status', 'subscribed')
        )

    def update_subscriber_by_email(
        self,
        email: str,
        list_id: str,
        name: Optional[str] = None,
        status: Optional[str] = None
    ) -> Subscriber:
        sub = self.find_subscriber(email, list_id)
        if not sub:
            raise ValueError(f"Subscriber {email} not found")
        return self.update_subscriber_by_email(email, list_id, name, status)

    def delete_subscriber_by_email(self, email: str, list_id: str) -> Dict[str, Any]:
        sub = self.find_subscriber(email, list_id)
        if not sub:
            raise ValueError(f"Subscriber {email} not found")
        return self._request('DELETE', f'accounts/{self.account_id}/lists/{list_id}/subscribers/{sub.id}')

    def move_subscriber(
        self,
        email: str,
        from_list_id: str,
        to_list_id: str
    ) -> Dict[str, Any]:
        sub = self.find_subscriber(email, from_list_id)
        if not sub:
            raise ValueError(f"Subscriber {email} not found")
        return self.create_subscriber(
            email, to_list_id, sub.name
        )

    def search_list(self, name_filter: Optional[str] = None) -> List[List]:
        params = {}
        if name_filter:
            params['name'] = name_filter
        result = self._request('GET', f'accounts/{self.account_id}/lists', params=params)
        return [
            List(id=l['id'], name=l['name'], total_subscribers=l.get('total_subscribers', 0))
            for l in result.get('entries', [])
        ]

    def get_broadcast_open(self, broadcast_id: str) -> BroadcastOpen:
        result = self._request('GET', f'accounts/{self.account_id}/messages/{broadcast_id}/stats')
        stats = result
        return BroadcastOpen(
            broadcast_id=broadcast_id,
            opens=stats.get('total_opens', 0),
            unique_opens=stats.get('unique_opens', 0)
        )

    def get_broadcast_click(self, broadcast_id: str) -> BroadcastClick:
        result = self._request('GET', f'accounts/{self.account_id}/messages/{broadcast_id}/stats')
        stats = result
        return BroadcastClick(
            broadcast_id=broadcast_id,
            clicks=stats.get('total_clicks', 0),
            unique_clicks=stats.get('unique_clicks', 0)
        )

    def get_broadcast_statistic(self, broadcast_id: str) -> BroadcastStatistic:
        result = self._request('GET', f'accounts/{self.account_id}/messages/{broadcast_id}/stats')
        stats = result
        return BroadcastStatistic(
            broadcast_id=broadcast_id,
            sent=stats.get('total_sent', 0),
            total_opens=stats.get('total_opens', 0),
            total_clicks=stats.get('total_clicks', 0),
            bounces=stats.get('bounces', 0),
            complaints=stats.get('complaints', 0)
        )

    def test_connection(self) -> bool:
        try:
            self.search_list()
            return True
        except Exception:
            return False