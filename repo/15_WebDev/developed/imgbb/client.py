"""
ImgBB REST API Client

This module provides a Python client for interacting with the ImgBB API.
ImgBB is a free image hosting and sharing service.

Base URL: https://api.imgbb.com/1
"""

import requests
from typing import Optional, Dict, Any
import os


class ImgBBClient:
    """
    Client for interacting with the ImgBB API.
    """

    API_URL = "https://api.imgbb.com/1"

    def __init__(self, api_key: str):
        """
        Initialize the ImgBB client.

        Args:
            api_key: Your ImgBB API key
        """
        self.api_key = api_key
        self.session = requests.Session()

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make a request to the ImgBB API.

        Args:
            method: HTTP method
            endpoint: API endpoint path
            **kwargs: Additional arguments for requests.request

        Returns:
            JSON response data

        Raises:
            requests.exceptions.RequestException: On API errors
        """
        url = f"{self.API_URL}{endpoint}?key={self.api_key}"
        response = self.session.request(method, url, **kwargs)

        if response.status_code >= 400:
            error_msg = f"API Error {response.status_code}"
            try:
                error_data = response.json()
                if 'error' in error_data:
                    error_msg += f": {error_data['error'].get('message', response.text)}"
                else:
                    error_msg += f": {response.text}"
            except:
                error_msg += f": {response.text}"
            raise requests.exceptions.RequestException(error_msg)

        return response.json()

    def upload_image(self, image_path: str,
                    name: Optional[str] = None,
                    expiration: Optional[int] = None,
                    resize_width: Optional[int] = None,
                    resize_height: Optional[int] = None) -> Dict[str, Any]:
        """
        Upload an image to ImgBB.

        Args:
            image_path: Path to the image file
            name: Optional custom name for the image
            expiration: Optional expiration time in seconds (default: never)
            resize_width: Optional width to resize image
            resize_height: Optional height to resize image

        Returns:
            Upload response with image URL and metadata
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")

        with open(image_path, 'rb') as image_file:
            files = {'image': image_file}
            data = {}

            if name:
                data['name'] = name

            options = []
            if expiration:
                options.append(f"expiration={expiration}")
            if resize_width:
                options.append(f"resize_width={resize_width}")
            if resize_height:
                options.append(f"resize_height={resize_height}")

            if options:
                data['options'] = '_'.join(options)

            return self._make_request('POST', '/upload', files=files, data=data)

    def upload_image_from_url(self, image_url: str,
                             name: Optional[str] = None,
                             expiration: Optional[int] = None,
                             resize_width: Optional[int] = None,
                             resize_height: Optional[int] = None) -> Dict[str, Any]:
        """
        Upload an image to ImgBB from a URL.

        Args:
            image_url: URL of the image to upload
            name: Optional custom name for the image
            expiration: Optional expiration time in seconds (default: never)
            resize_width: Optional width to resize image
            resize_height: Optional height to resize image

        Returns:
            Upload response with image URL and metadata
        """
        import base64

        # Get the image from URL first
        response = self.session.get(image_url)
        response.raise_for_status()
        image_data = base64.b64encode(response.content).decode('utf-8')

        data = {
            'image': image_data
        }

        if name:
            data['name'] = name

        options = []
        if expiration:
            options.append(f"expiration={expiration}")
        if resize_width:
            options.append(f"resize_width={resize_width}")
        if resize_height:
            options.append(f"resize_height={resize_height}")

        if options:
            data['options'] = '_'.join(options)

        return self._make_request('POST', '/upload', data=data)

    def upload_image_from_base64(self, base64_string: str,
                                 name: Optional[str] = None,
                                 expiration: Optional[int] = None,
                                 resize_width: Optional[int] = None,
                                 resize_height: Optional[int] = None) -> Dict[str, Any]:
        """
        Upload an image to ImgBB from a base64 string.

        Args:
            base64_string: Base64 encoded image string
            name: Optional custom name for the image
            expiration: Optional expiration time in seconds (default: never)
            resize_width: Optional width to resize image
            resize_height: Optional height to resize image

        Returns:
            Upload response with image URL and metadata
        """
        data = {
            'image': base64_string
        }

        if name:
            data['name'] = name

        options = []
        if expiration:
            options.append(f"expiration={expiration}")
        if resize_width:
            options.append(f"resize_width={resize_width}")
        if resize_height:
            options.append(f"resize_height={resize_height}")

        if options:
            data['options'] = '_'.join(options)

        return self._make_request('POST', '/upload', data=data)

    def close(self):
        """
        Close the session.
        """
        self.session.close()