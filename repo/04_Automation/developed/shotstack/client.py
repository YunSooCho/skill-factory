"""
Shotstack API Client - Video Generation and Asset Management
"""

import requests
import time
from typing import Optional, Dict, Any, List, BinaryIO


class ShotstackError(Exception):
    """Base exception for Shotstack errors"""
    pass


class ShotstackRateLimitError(ShotstackError):
    """Rate limit exceeded"""
    pass


class ShotstackAuthenticationError(ShotstackError):
    """Authentication failed"""
    pass


class ShotstackClient:
    """Client for Shotstack Video Generation API"""

    BASE_URL = "https://api.shotstack.io/stage"

    def __init__(self, api_key: str, timeout: int = 60):
        """
        Initialize Shotstack client

        Args:
            api_key: Shotstack API key
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'x-api-key': api_key,
            'Content-Type': 'application/json'
        })
        # Rate limiting
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
            raise ShotstackRateLimitError(
                "Rate limit exceeded. Please try again later."
            )

        if response.status_code == 401:
            raise ShotstackAuthenticationError(
                "Authentication failed. Please check your API key."
            )

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get('message', or error_data.get('error', ''))
            except:
                error_msg = response.text or response.reason or "Unknown error"
            raise ShotstackError(
                f"API request failed with status {response.status_code}: {error_msg}"
            )

        return response.json()

    def get_asset_information(self, asset_id: str) -> Dict[str, Any]:
        """
        Get information about an asset

        Args:
            asset_id: Asset ID to retrieve information

        Returns:
            Dictionary containing asset information

        Raises:
            ShotstackError: If request fails
        """
        self._enforce_rate_limit()

        try:
            response = self.session.get(
                f'{self.BASE_URL}/assets/{asset_id}',
                timeout=self.timeout
            )
            return self._handle_response(response)

        except requests.exceptions.Timeout:
            raise ShotstackError("Request timed out")
        except requests.exceptions.RequestException as e:
            raise ShotstackError(f"Request failed: {str(e)}")

    def download_asset_data(self, asset_id: str, output_path: str) -> str:
        """
        Download asset data to a file

        Args:
            asset_id: Asset ID to download
            output_path: Local file path to save the asset

        Returns:
            Path to downloaded file

        Raises:
            ShotstackError: If download fails
        """
        self._enforce_rate_limit()

        try:
            response = self.session.get(
                f'{self.BASE_URL}/assets/{asset_id}/download',
                timeout=self.timeout,
                stream=True
            )

            if response.status_code == 404:
                raise ShotstackError("Asset not found")

            if response.status_code >= 400:
                error_msg = response.text or response.reason
                raise ShotstackError(
                    f"Download failed with status {response.status_code}: {error_msg}"
                )

            # Stream download to file
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            return output_path

        except requests.exceptions.Timeout:
            raise ShotstackError("Download timed out")
        except requests.exceptions.RequestException as e:
            raise ShotstackError(f"Download failed: {str(e)}")

    def generate_text_to_speech(self, text: str, voice: str = "samantha",
                                speed: float = 1.0, pitch: float = 1.0,
                                output_format: str = "mp3") -> Dict[str, Any]:
        """
        Generate audio from text using text-to-speech

        Args:
            text: Text to convert to speech
            voice: Voice to use (default: "samantha")
            speed: Speech speed multiplier (default: 1.0)
            pitch: Pitch multiplier (default: 1.0)
            output_format: Audio format, "mp3" or "wav" (default: "mp3")

        Returns:
            Dictionary containing generation result with asset ID

        Raises:
            ShotstackError: If generation fails
        """
        self._enforce_rate_limit()

        payload = {
            "type": "tts",
            "text": text,
            "voice": voice,
            "speed": speed,
            "pitch": pitch,
            "outputFormat": output_format
        }

        try:
            response = self.session.post(
                f'{self.BASE_URL}/generate',
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)

        except requests.exceptions.Timeout:
            raise ShotstackError("Request timed out")
        except requests.exceptions.RequestException as e:
            raise ShotstackError(f"Request failed: {str(e)}")

    def start_workflow_job(self, workflow_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Start a workflow job for video generation

        Args:
            workflow_config: Workflow configuration dictionary containing timeline, tracks, etc.

        Returns:
            Dictionary containing job ID and status

        Raises:
            ShotstackError: If job creation fails
        """
        self._enforce_rate_limit()

        try:
            response = self.session.post(
                f'{self.BASE_URL}/render',
                json=workflow_config,
                timeout=self.timeout
            )
            return self._handle_response(response)

        except requests.exceptions.Timeout:
            raise ShotstackError("Request timed out")
        except requests.exceptions.RequestException as e:
            raise ShotstackError(f"Request failed: {str(e)}")

    def generate_text_to_image(self, prompt: str, width: int = 1024,
                               height: int = 1024, num_images: int = 1,
                               style: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate images from text prompt

        Args:
            prompt: Text prompt for image generation
            width: Image width (default: 1024)
            height: Image height (default: 1024)
            num_images: Number of images to generate (default: 1)
            style: Optional style parameter

        Returns:
            Dictionary containing generation result with asset IDs

        Raises:
            ShotstackError: If generation fails
        """
        self._enforce_rate_limit()

        payload = {
            "type": "tti",  # Text to Image
            "prompt": prompt,
            "width": width,
            "height": height,
            "numImages": num_images
        }

        if style:
            payload["style"] = style

        try:
            response = self.session.post(
                f'{self.BASE_URL}/generate',
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)

        except requests.exceptions.Timeout:
            raise ShotstackError("Request timed out")
        except requests.exceptions.RequestException as e:
            raise ShotstackError(f"Request failed: {str(e)}")

    def list_files(self, limit: int = 100, offset: int = 0,
                   file_type: Optional[str] = None) -> Dict[str, Any]:
        """
        List uploaded files and assets

        Args:
            limit: Number of results to return (default: 100)
            offset: Number of results to skip (default: 0)
            file_type: Filter by file type (optional)

        Returns:
            Dictionary containing list of files

        Raises:
            ShotstackError: If listing fails
        """
        self._enforce_rate_limit()

        params = {
            "limit": limit,
            "offset": offset
        }

        if file_type:
            params["type"] = file_type

        try:
            response = self.session.get(
                f'{self.BASE_URL}/assets',
                params=params,
                timeout=self.timeout
            )
            return self._handle_response(response)

        except requests.exceptions.Timeout:
            raise ShotstackError("Request timed out")
        except requests.exceptions.RequestException as e:
            raise ShotstackError(f"Request failed: {str(e)}")

    def upload_file(self, file_path: str, file_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Upload a file to Shotstack

        Args:
            file_path: Local file path to upload
            file_type: Optional file type

        Returns:
            Dictionary containing upload result with asset ID

        Raises:
            ShotstackError: If upload fails
        """
        self._enforce_rate_limit()

        try:
            with open(file_path, 'rb') as f:
                files = {
                    'file': f
                }

                data = {}
                if file_type:
                    data['type'] = file_type

                response = self.session.post(
                    f'{self.BASE_URL}/assets/upload',
                    files=files,
                    data=data,
                    timeout=self.timeout
                )

            return self._handle_response(response)

        except FileNotFoundError:
            raise ShotstackError(f"File not found: {file_path}")
        except requests.exceptions.Timeout:
            raise ShotstackError("Upload timed out")
        except requests.exceptions.RequestException as e:
            raise ShotstackError(f"Upload failed: {str(e)}")

    def generate_image_to_video(self, image_asset_id: str, duration: float = 5.0,
                                 motion: Optional[str] = None,
                                 audio_asset_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate video from image

        Args:
            image_asset_id: Asset ID of the source image
            duration: Video duration in seconds (default: 5.0)
            motion: Optional motion effect (e.g., "zoom", "pan")
            audio_asset_id: Optional asset ID for background audio

        Returns:
            Dictionary containing generation result with asset ID

        Raises:
            ShotstackError: If generation fails
        """
        self._enforce_rate_limit()

        payload = {
            "type": "itv",  # Image to Video
            "imageAssetId": image_asset_id,
            "duration": duration
        }

        if motion:
            payload["motion"] = motion

        if audio_asset_id:
            payload["audioAssetId"] = audio_asset_id

        try:
            response = self.session.post(
                f'{self.BASE_URL}/generate',
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)

        except requests.exceptions.Timeout:
            raise ShotstackError("Request timed out")
        except requests.exceptions.RequestException as e:
            raise ShotstackError(f"Request failed: {str(e)}")

    def get_render_status(self, render_id: str) -> Dict[str, Any]:
        """
        Get the status of a render job

        Args:
            render_id: Render job ID

        Returns:
            Dictionary containing render status

        Raises:
            ShotstackError: If request fails
        """
        self._enforce_rate_limit()

        try:
            response = self.session.get(
                f'{self.BASE_URL}/render/{render_id}',
                timeout=self.timeout
            )
            return self._handle_response(response)

        except requests.exceptions.Timeout:
            raise ShotstackError("Request timed out")
        except requests.exceptions.RequestException as e:
            raise ShotstackError(f"Request failed: {str(e)}")