"""
Templated API Client - Template Rendering Service
"""

import requests
import time
import base64
from typing import Optional, Dict, Any, List, Union, BinaryIO


class TemplatedError(Exception):
    """Base exception for Templated errors"""
    pass


class TemplatedRateLimitError(TemplatedError):
    """Rate limit exceeded"""
    pass


class TemplatedAuthenticationError(TemplatedError):
    """Authentication failed"""
    pass


class TemplatedClient:
    """Client for Templated Template Rendering API"""

    BASE_URL = "https://api.templated.io/v1"

    def __init__(self, api_key: str, timeout: int = 60):
        """
        Initialize Templated client

        Args:
            api_key: Templated API key
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })
        self.min_delay = 0.1
        self.last_request_time = 0

    def _enforce_rate_limit(self):
        """Enforce rate limiting between requests"""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time

        if time_since_last_request < self.min_delay:
            time.sleep(self.min_delay - time_since_last_request)

        self.last_request_time = time.time()

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle API response and errors"""
        if response.status_code == 429:
            raise TemplatedRateLimitError("Rate limit exceeded")

        if response.status_code == 401:
            raise TemplatedAuthenticationError("Authentication failed")

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get('message', or error_data.get('error', ''))
            except:
                error_msg = response.text or response.reason or "Unknown error"
            raise TemplatedError(f"API error ({response.status_code}): {error_msg}")

        return response.json()

    def _encode_image(self, image_source: Union[str, bytes, BinaryIO]) -> str:
        """Encode image to base64 string"""
        if isinstance(image_source, str):
            try:
                with open(image_source, 'rb') as f:
                    return base64.b64encode(f.read()).decode('utf-8')
            except:
                return image_source
        elif isinstance(image_source, bytes):
            return base64.b64encode(image_source).decode('utf-8')
        else:
            return base64.b64encode(image_source.read()).decode('utf-8')

    def merge_renders(self, render_ids: List[str],
                      output_format: str = "pdf",
                      **kwargs) -> Dict[str, Any]:
        """
        Merge multiple renders into a single document

        Args:
            render_ids: List of render IDs to merge
            output_format: Output format (pdf/png/jpeg)
            **kwargs: Additional parameters

        Returns:
            Dictionary containing merged render result

        Raises:
            TemplatedError: If merge fails
        """
        self._enforce_rate_limit()

        payload = {
            "render_ids": render_ids,
            "output_format": output_format
        }
        payload.update(kwargs)

        try:
            response = self.session.post(
                f"{self.BASE_URL}/renders/merge",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise TemplatedError(f"Request failed: {str(e)}")

    def search_templates(self, query: str = "",
                         category: Optional[str] = None,
                         limit: int = 20,
                         offset: int = 0) -> Dict[str, Any]:
        """
        Search for templates

        Args:
            query: Search query string
            category: Filter by category
            limit: Number of results
            offset: Pagination offset

        Returns:
            Dictionary containing template search results

        Raises:
            TemplatedError: If search fails
        """
        self._enforce_rate_limit()

        params = {"limit": limit, "offset": offset}

        if query:
            params["query"] = query

        if category:
            params["category"] = category

        try:
            response = self.session.get(
                f"{self.BASE_URL}/templates",
                params=params,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise TemplatedError(f"Request failed: {str(e)}")

    def create_render(self, template_id: str,
                      data: Dict[str, Any],
                      format: str = "pdf",
                      **kwargs) -> Dict[str, Any]:
        """
        Create a render from a template

        Args:
            template_id: Template ID to use
            data: Data to populate the template
            format: Output format (pdf/png/jpeg/html)
            **kwargs: Additional render parameters

        Returns:
            Dictionary containing render result with render ID

        Raises:
            TemplatedError: If render creation fails
        """
        self._enforce_rate_limit()

        payload = {
            "template_id": template_id,
            "data": data,
            "format": format
        }
        payload.update(kwargs)

        try:
            response = self.session.post(
                f"{self.BASE_URL}/renders",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise TemplatedError(f"Request failed: {str(e)}")

    def upload_image(self, image: Union[str, bytes, BinaryIO],
                     name: Optional[str] = None) -> Dict[str, Any]:
        """
        Upload an image for use in templates

        Args:
            image: Image to upload (file path, bytes, or file object)
            name: Optional name for the image

        Returns:
            Dictionary containing upload result with image URL

        Raises:
            TemplatedError: If upload fails
        """
        self._enforce_rate_limit()

        image_b64 = self._encode_image(image)

        payload = {"image": f"data:image/png;base64,{image_b64}"}

        if name:
            payload["name"] = name

        try:
            response = self.session.post(
                f"{self.BASE_URL}/images",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise TemplatedError(f"Request failed: {str(e)}")

    def download_render(self, render_id: str,
                        output_path: Optional[str] = None) -> Union[bytes, str]:
        """
        Download a rendered document

        Args:
            render_id: Render ID to download
            output_path: Optional local path to save the file

        Returns:
            File content as bytes, or path if output_path provided

        Raises:
            TemplatedError: If download fails
        """
        self._enforce_rate_limit()

        try:
            response = self.session.get(
                f"{self.BASE_URL}/renders/{render_id}/download",
                timeout=self.timeout,
                stream=True
            )

            if response.status_code == 404:
                raise TemplatedError("Render not found")

            if response.status_code >= 400:
                raise TemplatedError(
                    f"Download failed with status {response.status_code}"
                )

            content = response.content

            if output_path:
                with open(output_path, 'wb') as f:
                    f.write(content)
                return output_path

            return content

        except requests.exceptions.RequestException as e:
            raise TemplatedError(f"Download failed: {str(e)}")

    def get_render_status(self, render_id: str) -> Dict[str, Any]:
        """
        Get render status

        Args:
            render_id: Render ID

        Returns:
            Dictionary containing render status

        Raises:
            TemplatedError: If request fails
        """
        self._enforce_rate_limit()

        try:
            response = self.session.get(
                f"{self.BASE_URL}/renders/{render_id}",
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise TemplatedError(f"Request failed: {str(e)}")