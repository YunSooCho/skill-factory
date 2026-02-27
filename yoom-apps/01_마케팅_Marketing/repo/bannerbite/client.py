"""
BannerBite API Client
"""

import logging
import requests
from typing import List, Optional, Dict, Any
from .models import Project, Bite, Media

logger = logging.getLogger(__name__)


class BannerBiteClient:
    """
    BannerBite Client for Yoom Integration

    API Actions:
    - Get Bite
    - Render Media
    - Get Project
    - Search Bites by Project ID
    - List Projects
    """

    BASE_URL = "https://api.bannerbite.com/v1"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-Key': api_key,
            'Content-Type': 'application/json'
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        url = f"{self.BASE_URL}/{endpoint}"
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"BannerBite Error: {e}")
            raise

    def list_projects(self, limit: int = 50, offset: int = 0) -> List[Project]:
        params = {'limit': limit, 'offset': offset}
        result = self._request('GET', 'projects', params=params)
        return [
            Project(
                id=p['id'], name=p['name'],
                status=p['status'], created_at=p['created_at'],
                updated_at=p['updated_at']
            ) for p in result.get('projects', [])
        ]

    def get_project(self, project_id: str) -> Project:
        result = self._request('GET', f'projects/{project_id}')
        p = result['project']
        return Project(
            id=p['id'], name=p['name'],
            status=p['status'], created_at=p['created_at'],
            updated_at=p['updated_at']
        )

    def search_bites_by_project(
        self,
        project_id: str,
        media_type: Optional[str] = None
    ) -> List[Bite]:
        params = {}
        if media_type:
            params['media_type'] = media_type
        result = self._request('GET', f'projects/{project_id}/bites', params=params)
        return [
            Bite(
                id=b['id'], project_id=b['project_id'], name=b['name'],
                media_type=b['media_type'], status=b['status'],
                url=b.get('url')
            ) for b in result.get('bites', [])
        ]

    def get_bite(self, bite_id: str) -> Bite:
        result = self._request('GET', f'bites/{bite_id}')
        b = result['bite']
        return Bite(
            id=b['id'], project_id=b['project_id'], name=b['name'],
            media_type=b['media_type'], status=b['status'],
            url=b.get('url')
        )

    def render_media(
        self,
        template_id: str,
        data: Dict[str, Any],
        format: str = 'mp4'
    ) -> Media:
        payload = {'template_id': template_id, 'data': data, 'format': format}
        result = self._request('POST', 'render', json=payload)
        m = result['media']
        return Media(
            id=m['id'], type=m['type'], url=m['url'],
            thumbnail_url=m.get('thumbnail_url')
        )

    def test_connection(self) -> bool:
        try:
            self.list_projects(limit=1)
            return True
        except Exception:
            return False