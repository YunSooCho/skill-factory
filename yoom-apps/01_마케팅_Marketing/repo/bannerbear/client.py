"""
Bannerbear API Client
"""

import logging
import requests
from typing import List, Optional, Dict, Any
from .models import ImageDetail, VideoDetail, MovieDetail, ScreenshotDetail, Collection, FileData

logger = logging.getLogger(__name__)


class BannerbearClient:
    """
    Bannerbear Client for Yoom Integration

    API Actions:
    - Create Collection
    - Get Video Detail
    - Create Image
    - Create Video
    - Create Movie
    - Get Screenshot Detail
    - Get File Data
    - Create Screenshot
    - Get Movie Detail
    - Get Collection Detail
    - Get Image Detail
    """

    BASE_URL = "https://api.bannerbear.com/v2"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        url = f"{self.BASE_URL}/{endpoint}"
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Bannerbear Error: {e}")
            raise

    def create_image(
        self,
        template: str,
        modifications: List[Dict[str, Any]]
    ) -> ImageDetail:
        data = {'template': template, 'modifications': modifications}
        result = self._request('POST', 'images', json=data)
        return ImageDetail(
            uid=result['uid'],
            status=result['status'],
            image_url=result.get('image_url')
        )

    def create_video(
        self,
        template: str,
        modifications: List[Dict[str, Any]],
        frames: int = 30
    ) -> VideoDetail:
        data = {'template': template, 'modifications': modifications, 'frames': frames}
        result = self._request('POST', 'videos', json=data)
        return VideoDetail(
            uid=result['uid'],
            status=result['status'],
            video_url=result.get('video_url')
        )

    def create_movie(
        self,
        video_templates: List[Dict[str, Any]]
    ) -> MovieDetail:
        data = {'video_templates': video_templates}
        result = self._request('POST', 'movies', json=data)
        return MovieDetail(
            uid=result['uid'],
            status=result['status'],
            movie_mp4_url=result.get('movie_mp4_url')
        )

    def create_screenshot(
        self,
        url: str,
        width: Optional[int] = None,
        height: Optional[int] = None
    ) -> ScreenshotDetail:
        data = {'url': url}
        if width:
            data['width'] = width
        if height:
            data['height'] = height
        result = self._request('POST', 'screenshots', json=data)
        return ScreenshotDetail(
            uid=result['uid'],
            status=result['status'],
            image_url=result.get('image_url')
        )

    def create_collection(
        self,
        name: str,
        images: List[str]
    ) -> Collection:
        data = {'name': name, 'images': images}
        result = self._request('POST', 'collections', json=data)
        return Collection(
            uid=result['uid'],
            name=result['name'],
            status=result['status']
        )

    def get_image_detail(self, uid: str) -> ImageDetail:
        result = self._request('GET', f'images/{uid}')
        return ImageDetail(
            uid=result['uid'],
            status=result['status'],
            image_url=result.get('image_url')
        )

    def get_video_detail(self, uid: str) -> VideoDetail:
        result = self._request('GET', f'videos/{uid}')
        return VideoDetail(
            uid=result['uid'],
            status=result['status'],
            video_url=result.get('video_url')
        )

    def get_movie_detail(self, uid: str) -> MovieDetail:
        result = self._request('GET', f'movies/{uid}')
        return MovieDetail(
            uid=result['uid'],
            status=result['status'],
            movie_mp4_url=result.get('movie_mp4_url')
        )

    def get_screenshot_detail(self, uid: str) -> ScreenshotDetail:
        result = self._request('GET', f'screenshots/{uid}')
        return ScreenshotDetail(
            uid=result['uid'],
            status=result['status'],
            image_url=result.get('image_url')
        )

    def get_collection_detail(self, uid: str) -> Collection:
        result = self._request('GET', f'collections/{uid}')
        return Collection(
            uid=result['uid'],
            name=result['name'],
            status=result['status']
        )

    def get_file_data(self, uid: str) -> FileData:
        result = self._request('GET', f'images/{uid}')
        return FileData(
            uid=result['uid'],
            filename=result.get('image_png_filename', ''),
            url=result.get('image_url', ''),
            mime_type='image/png',
            size=0
        )

    def test_connection(self) -> bool:
        try:
            self._request('GET', 'account')
            return True
        except Exception:
            return False