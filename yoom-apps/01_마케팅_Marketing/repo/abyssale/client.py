"""
Abyssale API Client
Documentation: https://docs.abyssale.com/
"""

import logging
import requests
import time
from typing import List, Optional, Dict, Any
from .models import GeneratedContent, File, Format, GenerationRequest

logger = logging.getLogger(__name__)


class AbyssaleClient:
    """
    Abyssale API Client for Yoom Integration

    API Actions:
    - Generate Content
    - Get File
    """

    BASE_URL = "https://api.abyssale.com/v1"

    def __init__(self, api_key: str):
        """
        Initialize Abyssale Client

        Args:
            api_key: Abyssale API key
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make HTTP request to Abyssale API

        Args:
            method: HTTP method
            endpoint: API endpoint
            **kwargs: Additional arguments for requests

        Returns:
            JSON response data

        Raises:
            requests.RequestException: If request fails
        """
        url = f"{self.BASE_URL}/{endpoint}"
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Abyssale API Error: {e}")
            if hasattr(e, 'response') and e.response:
                logger.error(f"Response: {e.response.text}")
            raise

    # ========== CONTENT GENERATION ==========

    def generate_content(
        self,
        template_uuid: str,
        format_uuid: Optional[str] = None,
        elements: Optional[Dict[str, Any]] = None,
        asynchronous: bool = False
    ) -> GeneratedContent:
        """
        Generate Content (images/videos from template)

        Args:
            template_uuid: Template UUID
            format_uuid: Format UUID (optional, generates all formats if not specified)
            elements: Dictionary of element values to replace in template
            asynchronous: If True, return immediately and let generation run in background

        Returns:
            GeneratedContent object

        Example:
            content = client.generate_content(
                template_uuid='tpl_xxx',
                elements={
                    'title': 'Welcome',
                    'image_url': 'https://example.com/image.jpg',
                    'color': '#FF0000'
                }
            )
        """
        request = GenerationRequest(
            template_uuid=template_uuid,
            format_uuid=format_uuid,
            elements=elements,
            asynchronous=asynchronous
        )

        data = request.to_dict()
        result = self._request('POST', '/generations', json=data)

        formats = []
        if 'result' in result:
            for format_data in result.get('result', []):
                formats.append(Format(
                    type=format_data.get('type'),
                    width=format_data.get('width'),
                    height=format_data.get('height'),
                    url=format_data.get('url'),
                    size=format_data.get('size')
                ))

        return GeneratedContent(
            id=result.get('id'),
            format_uuid=result.get('format_uuid'),
            status=result.get('status'),
            url=result.get('url'),
            error_message=result.get('error_message'),
            formats=formats
        )

    def get_generation_status(self, generation_id: str) -> GeneratedContent:
        """
        Get Generation Status

        Args:
            generation_id: Generation ID

        Returns:
            GeneratedContent object with current status
        """
        result = self._request('GET', f'/generations/{generation_id}')

        formats = []
        if 'result' in result:
            for format_data in result.get('result', []):
                formats.append(Format(
                    type=format_data.get('type'),
                    width=format_data.get('width'),
                    height=format_data.get('height'),
                    url=format_data.get('url'),
                    size=format_data.get('size')
                ))

        return GeneratedContent(
            id=result.get('id'),
            format_uuid=result.get('format_uuid'),
            status=result.get('status'),
            url=result.get('url'),
            error_message=result.get('error_message'),
            formats=formats
        )

    def poll_generation(
        self,
        generation_id: str,
        max_wait: int = 60,
        interval: int = 2
    ) -> GeneratedContent:
        """
        Poll Generation until complete or failed

        Args:
            generation_id: Generation ID
            max_wait: Maximum wait time in seconds
            interval: Poll interval in seconds

        Returns:
            GeneratedContent object
        """
        start_time = time.time()

        while time.time() - start_time < max_wait:
            content = self.get_generation_status(generation_id)

            if content.status in ['completed', 'failed']:
                return content

            time.sleep(interval)

        raise TimeoutError(f"Generation {generation_id} did not complete within {max_wait} seconds")

    # ========== FILE OPERATIONS ==========

    def get_file(self, file_id: str) -> File:
        """
        Get File Details

        Args:
            file_id: File ID

        Returns:
            File object
        """
        result = self._request('GET', f'/files/{file_id}')
        return File(
            id=result.get('id'),
            name=result.get('name'),
            url=result.get('url'),
            mime_type=result.get('mime_type'),
            size=result.get('size'),
            created_at=result.get('created_at'),
            thumbnail_url=result.get('thumbnail_url')
        )

    def upload_file(self, file_path: str) -> File:
        """
        Upload File

        Args:
            file_path: Path to file

        Returns:
            File object
        """
        with open(file_path, 'rb') as f:
            files = {'file': f}
            result = self._request('POST', '/files', files=files)

        return File(
            id=result.get('id'),
            name=result.get('name'),
            url=result.get('url'),
            mime_type=result.get('mime_type'),
            size=result.get('size'),
            created_at=result.get('created_at'),
            thumbnail_url=result.get('thumbnail_url')
        )

    # ========== TEMPLATES ==========

    def list_templates(self) -> List[Dict[str, Any]]:
        """
        List Available Templates

        Returns:
            List of template dictionaries
        """
        result = self._request('GET', '/templates')
        return result.get('templates', [])

    def get_template(self, template_id: str) -> Dict[str, Any]:
        """
        Get Template Details

        Args:
            template_id: Template ID

        Returns:
            Template dictionary
        """
        return self._request('GET', f'/templates/{template_id}')

    # ========== UTILITY ==========

    def test_connection(self) -> bool:
        """
        Test API connection

        Returns:
            True if connection successful
        """
        try:
            self.list_templates()
            return True
        except Exception:
            return False