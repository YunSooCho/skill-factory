"""
Vectorizer AI API Client - Image to Vector Conversion
"""

import requests
import time
import base64
from typing import Optional, Dict, Any, Union, BinaryIO


class VectorizerAIError(Exception):
    """Base exception for Vectorizer AI errors"""
    pass


class VectorizerAIRateLimitError(VectorizerAIError):
    """Rate limit exceeded"""
    pass


class VectorizerAIAuthenticationError(VectorizerAIError):
    """Authentication failed"""
    pass


class VectorizerAIClient:
    """Client for Vectorizer AI Image to Vector API"""

    BASE_URL = "https://api.vectorizer.ai/v1"

    def __init__(self, api_key: str, timeout: int = 60):
        """
        Initialize Vectorizer AI client

        Args:
            api_key: Vectorizer AI API key
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
            raise VectorizerAIRateLimitError("Rate limit exceeded")

        if response.status_code == 401:
            raise VectorizerAIAuthenticationError("Authentication failed")

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get('message', or error_data.get('error', ''))
            except:
                error_msg = response.text or response.reason or "Unknown error"
            raise VectorizerAIError(f"API error ({response.status_code}): {error_msg}")

        return response.json()

    def vectorize_image(self, image: Union[str, bytes, BinaryIO],
                        output_format: str = "svg",
                        detail_level: str = "high",
                        colors: Optional[str] = None) -> Dict[str, Any]:
        """
        Convert image to vector format

        Args:
            image: Image to vectorize (file path, bytes, or file object)
            output_format: Output format (svg, pdf) (default: "svg")
            detail_level: Detail level (low, medium, high) (default: "high")
            colors: Color mode (color, grayscale) (optional)

        Returns:
            Dictionary containing vectorization result

        Raises:
            VectorizerAIError: If vectorization fails
        """
        self._enforce_rate_limit()

        if isinstance(image, str):
            try:
                with open(image, 'rb') as f:
                    file_b64 = base64.b64encode(f.read()).decode('utf-8')
            except:
                raise VectorizerAIError(f"Failed to read image: {image}")
        elif isinstance(image, bytes):
            file_b64 = base64.b64encode(image).decode('utf-8')
        else:
            file_b64 = base64.b64encode(image.read()).decode('utf-8')

        payload = {
            "image": f"data:image/png;base64,{file_b64}",
            "output_format": output_format,
            "detail_level": detail_level
        }

        if colors:
            payload["colors"] = colors

        try:
            response = self.session.post(
                f"{self.BASE_URL}/vectorize",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise VectorizerAIError(f"Request failed: {str(e)}")

    def get_vectorization_status(self, job_id: str) -> Dict[str, Any]:
        """
        Get vectorization job status

        Args:
            job_id: Vectorization job ID

        Returns:
            Dictionary containing job status

        Raises:
            VectorizerAIError: If request fails
        """
        self._enforce_rate_limit()

        try:
            response = self.session.get(
                f"{self.BASE_URL}/jobs/{job_id}",
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise VectorizerAIError(f"Request failed: {str(e)}")

    def download_vector(self, job_id: str, output_path: Optional[str] = None) -> Union[bytes, str]:
        """
        Download vectorized image

        Args:
            job_id: Vectorization job ID
            output_path: Optional local path to save file

        Returns:
            Vector file content as bytes, or path if output_path provided

        Raises:
            VectorizerAIError: If download fails
        """
        self._enforce_rate_limit()

        try:
            response = self.session.get(
                f"{self.BASE_URL}/jobs/{job_id}/download",
                timeout=self.timeout,
                stream=True
            )

            if response.status_code == 404:
                raise VectorizerAIError("Vector not found or not ready")

            if response.status_code >= 400:
                raise VectorizerAIError(
                    f"Download failed with status {response.status_code}"
                )

            content = response.content

            if output_path:
                with open(output_path, 'wb') as f:
                    f.write(content)
                return output_path

            return content

        except requests.exceptions.RequestException as e:
            raise VectorizerAIError(f"Download failed: {str(e)}")