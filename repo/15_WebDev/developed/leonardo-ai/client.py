"""
Leonardo.ai REST API Client

This module provides a Python client for interacting with the Leonardo.ai API.
Leonardo.ai is an AI-powered image generation and editing platform.

Base URL: https://cloud.leonardo.ai/api/rest/v1
"""

import requests
from typing import Optional, Dict, Any, List
import time


class LeonardoAIClient:
    """
    Client for interacting with the Leonardo.ai API.
    """

    BASE_URL = "https://cloud.leonardo.ai/api/rest/v1"

    def __init__(self, api_key: str):
        """
        Initialize the Leonardo.ai client.

        Args:
            api_key: Your Leonardo.ai API key (Bearer token)
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make a request to the Leonardo.ai API.

        Args:
            method: HTTP method
            endpoint: API endpoint path
            **kwargs: Additional arguments for requests.request

        Returns:
            JSON response data

        Raises:
            requests.exceptions.RequestException: On API errors
        """
        url = f"{self.BASE_URL}{endpoint}"
        response = self.session.request(method, url, **kwargs)

        if response.status_code >= 400:
            error_msg = f"API Error {response.status_code}"
            try:
                error_data = response.json()
                error_msg += f": {error_data.get('error', {}).get('message', response.text)}"
            except:
                error_msg += f": {response.text}"
            raise requests.exceptions.RequestException(error_msg)

        return response.json()

    # Generation Operations

    def create_generation(self, prompt: str,
                         model_id: Optional[str] = None,
                         width: int = 512,
                         height: int = 512,
                         num_images: int = 1,
                         negative_prompt: Optional[str] = None,
                         seed: Optional[int] = None,
                         num_inference_steps: int = 30,
                         guidance_scale: float = 7.0) -> Dict[str, Any]:
        """
        Create an image generation request.

        Args:
            prompt: Text prompt for image generation
            model_id: Optional model ID (default: Leonardo's default model)
            width: Image width in pixels
            height: Image height in pixels
            num_images: Number of images to generate
            negative_prompt: Optional negative prompt
            seed: Optional random seed for reproducibility
            num_inference_steps: Number of denoising steps
            guidance_scale: Guidance scale for generation

        Returns:
            Generation request data with generation ID
        """
        data = {
            "prompt": prompt,
            "width": width,
            "height": height,
            "num_images": num_images,
            "num_inference_steps": num_inference_steps,
            "guidance_scale": guidance_scale
        }

        if model_id:
            data["modelId"] = model_id
        if negative_prompt:
            data["negative_prompt"] = negative_prompt
        if seed is not None:
            data["seed"] = seed

        return self._make_request('POST', '/generations', json=data)

    def get_generation_by_id(self, generation_id: str) -> Dict[str, Any]:
        """
        Get generation details by ID.

        Args:
            generation_id: The ID of the generation

        Returns:
            Generation data
        """
        return self._make_request('GET', f'/generations/{generation_id}')

    def wait_for_generation(self, generation_id: str,
                           timeout: int = 300,
                           poll_interval: int = 2) -> Dict[str, Any]:
        """
        Wait for a generation to complete.

        Args:
            generation_id: The ID of the generation
            timeout: Maximum wait time in seconds
            poll_interval: Polling interval in seconds

        Returns:
            Completed generation data

        Raises:
            TimeoutError: If generation doesn't complete within timeout
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            result = self.get_generation_by_id(generation_id)

            # Check if generation is complete
            if result.get('generations_by_pk', {}).get('status') == 'COMPLETE':
                return result
            elif result.get('generations_by_pk', {}).get('status') == 'FAILED':
                raise requests.exceptions.RequestException(
                    f"Generation failed: {result.get('generations_by_pk', {}).get('error')}"
                )

            time.sleep(poll_interval)

        raise TimeoutError(f"Generation did not complete within {timeout} seconds")

    def get_generations_by_user(self, user_id: Optional[str] = None,
                                offset: int = 0,
                                limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get generations by user.

        Args:
            user_id: Optional user ID (defaults to authenticated user)
            offset: Pagination offset
            limit: Number of results to return

        Returns:
            List of generation data
        """
        params = {'offset': offset, 'limit': limit}
        if user_id:
            params['elementId'] = user_id

        return self._make_request('GET', '/generations', params=params)

    # Model Operations

    def get_models(self, offset: int = 0, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get available models.

        Args:
            offset: Pagination offset
            limit: Number of results to return

        Returns:
            List of model data
        """
        params = {'offset': offset, 'limit': limit}
        return self._make_request('GET', '/models', params=params)

    def get_model_platform(self) -> Dict[str, Any]:
        """
        Get model platform data.

        Returns:
            Model platform information
        """
        return self._make_request('GET', '/models/platform')

    # Texture Generation

    def generate_texture(self, prompt: str,
                        width: int = 512,
                        height: int = 512,
                        num_images: int = 1) -> Dict[str, Any]:
        """
        Generate texture images.

        Args:
            prompt: Text prompt for texture generation
            width: Image width in pixels
            height: Image height in pixels
            num_images: Number of textures to generate

        Returns:
            Texture generation data
        """
        data = {
            "prompt": prompt,
            "width": width,
            "height": height,
            "numImages": num_images
        }
        return self._make_request('POST', '/generations/texture', json=data)

    # Image Operations

    def get_image_details(self, image_id: str) -> Dict[str, Any]:
        """
        Get details of a generated image.

        Args:
            image_id: The ID of the image

        Returns:
            Image data
        """
        return self._make_request('GET', f'/images/{image_id}')

    def delete_image(self, image_id: str) -> None:
        """
        Delete a generated image.

        Args:
            image_id: The ID of the image
        """
        self._make_request('DELETE', f'/images/{image_id}')

    # Realtime Canvas Operations

    def init_realtime_canvas(self) -> Dict[str, Any]:
        """
        Initialize a realtime canvas session.

        Returns:
            Canvas session data
        """
        return self._make_request('POST', '/realtime/init')

    # Dataset Operations

    def get_datasets(self, offset: int = 0, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get user's datasets.

        Args:
            offset: Pagination offset
            limit: Number of results to return

        Returns:
            List of dataset data
        """
        params = {'offset': offset, 'limit': limit}
        return self._make_request('GET', '/datasets', params=params)

    def create_dataset(self, name: str, description: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new dataset.

        Args:
            name: Dataset name
            description: Optional dataset description

        Returns:
            Created dataset data
        """
        data = {"name": name}
        if description:
            data["description"] = description
        return self._make_request('POST', '/datasets', json=data)

    # Custom Model Operations

    def get_custom_models(self, offset: int = 0, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get user's custom models.

        Args:
            offset: Pagination offset
            limit: Number of results to return

        Returns:
            List of custom model data
        """
        params = {'offset': offset, 'limit': limit}
        return self._make_request('GET', '/models/custom', params=params)

    # Fine-tuning Operations

    def get_jobs(self, offset: int = 0, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get fine-tuning and training jobs.

        Args:
            offset: Pagination offset
            limit: Number of results to return

        Returns:
            List of job data
        """
        params = {'offset': offset, 'limit': limit}
        return self._make_request('GET', '/jobs', params=params)

    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """
        Get status of a fine-tuning job.

        Args:
            job_id: The ID of the job

        Returns:
            Job status data
        """
        return self._make_request('GET', f'/jobs/{job_id}')

    def cancel_job(self, job_id: str) -> None:
        """
        Cancel a fine-tuning job.

        Args:
            job_id: The ID of the job
        """
        self._make_request('POST', f'/jobs/{job_id}/cancel')

    # Account Operations

    def get_me(self) -> Dict[str, Any]:
        """
        Get current user information.

        Returns:
            User information
        """
        return self._make_request('GET', '/me')

    def get_user_platform_info(self) -> Dict[str, Any]:
        """
        Get user platform information.

        Returns:
            User platform data including subscription info
        """
        return self._make_request('GET', '/me/platform')

    def close(self):
        """
        Close the session.
        """
        self.session.close()