"""
All Images AI API Client
"""

import logging
import requests
from typing import List, Optional, Dict, Any
from .models import ImageGeneration, Image

logger = logging.getLogger(__name__)


class AllImagesAIClient:
    """
    All Images AI Client for Yoom Integration

    API Actions:
    - Search Image Generation
    - Get Image
    - Delete Image Generation
    - Get Image Generation
    - Create Image Generation
    """

    BASE_URL = "https://api.allimages.ai/v1"

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
            logger.error(f"AllImagesAI Error: {e}")
            raise

    def create_image_generation(
        self,
        prompt: str,
        style: Optional[str] = None,
        width: int = 1024,
        height: int = 1024,
        num_images: int = 1
    ) -> ImageGeneration:
        data = {'prompt': prompt, 'width': width, 'height': height, 'num_images': num_images}
        if style:
            data['style'] = style
        result = self._request('POST', 'generations', json=data)
        return ImageGeneration(
            id=result['id'],
            prompt=result['prompt'],
            status=result['status'],
            created_at=result['created_at'],
            images=result.get('images', [])
        )

    def get_image_generation(self, generation_id: str) -> ImageGeneration:
        result = self._request('GET', f'generations/{generation_id}')
        return ImageGeneration(
            id=result['id'],
            prompt=result['prompt'],
            status=result['status'],
            created_at=result['created_at'],
            images=result.get('images', []),
            error_message=result.get('error_message')
        )

    def search_image_generations(
        self,
        prompt: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 20
    ) -> List[ImageGeneration]:
        params = {'limit': limit}
        if prompt:
            params['prompt'] = prompt
        if status:
            params['status'] = status
        result = self._request('GET', 'generations', params=params)
        return [
            ImageGeneration(
                id=g['id'], prompt=g['prompt'], status=g['status'],
                created_at=g['created_at'], images=g.get('images', [])
            ) for g in result.get('items', [])
        ]

    def get_image(self, image_id: str) -> Image:
        result = self._request('GET', f'images/{image_id}')
        return Image(
            id=result['id'], url=result['url'],
            width=result['width'], height=result['height'],
            type=result['type'], size=result['size']
        )

    def delete_image_generation(self, generation_id: str) -> Dict[str, Any]:
        return self._request('DELETE', f'generations/{generation_id}')

    def test_connection(self) -> bool:
        try:
            self.search_image_generations(limit=1)
            return True
        except Exception:
            return False