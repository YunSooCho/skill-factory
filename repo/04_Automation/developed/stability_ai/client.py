"""
Stability AI API Client - Image Generation and Editing
"""

import requests
import time
import base64
from typing import Optional, Dict, Any, List, Union, BinaryIO


class StabilityAIError(Exception):
    """Base exception for Stability AI errors"""
    pass


class StabilityAIRateLimitError(StabilityAIError):
    """Rate limit exceeded"""
    pass


class StabilityAIAuthenticationError(StabilityAIError):
    """Authentication failed"""
    pass


class StabilityAIClient:
    """Client for Stability AI Image Generation API"""

    BASE_URL = "https://api.stability.ai/v2beta"

    def __init__(self, api_key: str, timeout: int = 60):
        """
        Initialize Stability AI client

        Args:
            api_key: Stability AI API key
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
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
            raise StabilityAIRateLimitError("Rate limit exceeded")

        if response.status_code == 401:
            raise StabilityAIAuthenticationError("Authentication failed")

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get('message', or error_data.get('error', ''))
            except:
                error_msg = response.text or response.reason or "Unknown error"
            raise StabilityAIError(f"API error ({response.status_code}): {error_msg}")

        return response.json()

    def _encode_image(self, image_source: Union[str, bytes, BinaryIO]) -> str:
        """Encode image to base64 string"""
        if isinstance(image_source, str):
            # Assume it's a file path or URL
            try:
                with open(image_source, 'rb') as f:
                    return base64.b64encode(f.read()).decode('utf-8')
            except:
                # Assume it's a URL or already base64
                return image_source
        elif isinstance(image_source, bytes):
            return base64.b64encode(image_source).decode('utf-8')
        else:
            # BinaryIO object
            return base64.b64encode(image_source.read()).decode('utf-8')

    def outpaint_image(self, image: Union[str, bytes, BinaryIO],
                       prompt: str,
                       left: int = 0,
                       right: int = 0,
                       top: int = 0,
                       bottom: int = 0,
                       num_images: int = 1) -> Dict[str, Any]:
        """
        Extend an image outward (outpainting)

        Args:
            image: Source image (file path, bytes, or file-like object)
            prompt: Text prompt for generation
            left: Left extension in pixels
            right: Right extension in pixels
            top: Top extension in pixels
            bottom: Bottom extension in pixels
            num_images: Number of images to generate

        Returns:
            Dictionary containing generated images

        Raises:
            StabilityAIError: If generation fails
        """
        self._enforce_rate_limit()

        image_b64 = self._encode_image(image)

        payload = {
            "image": f"data:image/png;base64,{image_b64}",
            "@type": "outpaint",
            "prompt": prompt,
            "outpaint_left": left,
            "outpaint_right": right,
            "outpaint_top": top,
            "outpaint_bottom": bottom
        }

        try:
            response = self.session.post(
                f"{self.BASE_URL}/stable-image/generate",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise StabilityAIError(f"Request failed: {str(e)}")

    def generate_image_core(self, prompt: str,
                            negative_prompt: Optional[str] = None,
                            width: int = 1024,
                            height: int = 1024,
                            seed: Optional[int] = None,
                            steps: int = 30,
                            cfg_scale: float = 7.0) -> Dict[str, Any]:
        """
        Generate image using Stable Image Core

        Args:
            prompt: Text prompt for image generation
            negative_prompt: Negative prompt for things to avoid
            width: Image width
            height: Image height
            seed: Random seed for reproducibility
            steps: Number of diffusion steps
            cfg_scale: Guidance scale

        Returns:
            Dictionary containing generated image

        Raises:
            StabilityAIError: If generation fails
        """
        self._enforce_rate_limit()

        payload = {
            "prompt": prompt,
            "width": width,
            "height": height,
            "steps": steps,
            "cfg_scale": cfg_scale
        }

        if negative_prompt:
            payload["negative_prompt"] = negative_prompt

        if seed is not None:
            payload["seed"] = seed

        try:
            response = self.session.post(
                f"{self.BASE_URL}/stable-image/generate/core",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise StabilityAIError(f"Request failed: {str(e)}")

    def generate_image_ultra(self, prompt: str,
                             negative_prompt: Optional[str] = None,
                             seed: Optional[int] = None) -> Dict[str, Any]:
        """
        Generate high-quality image using Stable Image Ultra

        Args:
            prompt: Text prompt for image generation
            negative_prompt: Negative prompt
            seed: Random seed

        Returns:
            Dictionary containing generated image

        Raises:
            StabilityAIError: If generation fails
        """
        self._enforce_rate_limit()

        payload = {"prompt": prompt}

        if negative_prompt:
            payload["negative_prompt"] = negative_prompt

        if seed is not None:
            payload["seed"] = seed

        try:
            response = self.session.post(
                f"{self.BASE_URL}/stable-image/generate/ultra",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise StabilityAIError(f"Request failed: {str(e)}")

    def remove_object(self, image: Union[str, bytes, BinaryIO],
                      mask: Optional[Union[str, bytes, BinaryIO]] = None,
                      prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Remove unwanted objects from image

        Args:
            image: Source image
            mask: Optional mask for objects to remove
            prompt: Optional text prompt describing objects to remove

        Returns:
            Dictionary containing edited image

        Raises:
            StabilityAIError: If operation fails
        """
        self._enforce_rate_limit()

        image_b64 = self._encode_image(image)

        payload = {
            "image": f"data:image/png;base64,{image_b64}",
        }

        if mask:
            mask_b64 = self._encode_image(mask)
            payload["mask"] = f"data:image/png;base64,{mask_b64}"

        if prompt:
            payload["prompt"] = prompt

        try:
            response = self.session.post(
                f"{self.BASE_URL}/stable-image/edit/remove-object",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise StabilityAIError(f"Request failed: {str(e)}")

    def remove_background(self, image: Union[str, bytes, BinaryIO],
                          output_format: str = "png") -> Dict[str, Any]:
        """
        Remove background from image

        Args:
            image: Source image
            output_format: Output format (png/webp)

        Returns:
            Dictionary containing image without background

        Raises:
            StabilityAIError: If operation fails
        """
        self._enforce_rate_limit()

        image_b64 = self._encode_image(image)

        payload = {
            "image": f"data:image/png;base64,{image_b64}",
            "output_format": output_format
        }

        try:
            response = self.session.post(
                f"{self.BASE_URL}/stable-image/edit/remove-background",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise StabilityAIError(f"Request failed: {str(e)}")

    def generate_from_structure(self, structure: Union[str, bytes, BinaryIO],
                                 prompt: str,
                                 negative_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate image using structure control

        Args:
            structure: Structure/image to use as reference
            prompt: Text prompt
            negative_prompt: Negative prompt

        Returns:
            Dictionary containing generated image

        Raises:
            StabilityAIError: If generation fails
        """
        self._enforce_rate_limit()

        structure_b64 = self._encode_image(structure)

        payload = {
            "image": f"data:image/png;base64,{structure_b64}",
            "prompt": prompt
        }

        if negative_prompt:
            payload["negative_prompt"] = negative_prompt

        try:
            response = self.session.post(
                f"{self.BASE_URL}/stable-image/control/structure",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise StabilityAIError(f"Request failed: {str(e)}")

    def inpaint_image(self, image: Union[str, bytes, BinaryIO],
                      mask: Union[str, bytes, BinaryIO],
                      prompt: str) -> Dict[str, Any]:
        """
        Inpaint image using mask

        Args:
            image: Source image
            mask: Mask for area to inpaint
            prompt: Text prompt for inpainting

        Returns:
            Dictionary containing inpainted image

        Raises:
            StabilityAIError: If operation fails
        """
        self._enforce_rate_limit()

        image_b64 = self._encode_image(image)
        mask_b64 = self._encode_image(mask)

        payload = {
            "image": f"data:image/png;base64,{image_b64}",
            "mask": f"data:image/png;base64,{mask_b64}",
            "prompt": prompt
        }

        try:
            response = self.session.post(
                f"{self.BASE_URL}/stable-image/edit/inpaint",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise StabilityAIError(f"Request failed: {str(e)}")

    def generate_from_reference_ultra(self, reference: Union[str, bytes, BinaryIO],
                                       prompt: str,
                                       strength: float = 0.5) -> Dict[str, Any]:
        """
        Generate image using reference with Ultra quality

        Args:
            reference: Reference image
            prompt: Text prompt
            strength: How much to follow the reference (0-1)

        Returns:
            Dictionary containing generated image

        Raises:
            StabilityAIError: If generation fails
        """
        self._enforce_rate_limit()

        ref_b64 = self._encode_image(reference)

        payload = {
            "image": f"data:image/png;base64,{ref_b64}",
            "prompt": prompt,
            "strength": strength
        }

        try:
            response = self.session.post(
                f"{self.BASE_URL}/stable-image/generate/ultra/image-to-image",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise StabilityAIError(f"Request failed: {str(e)}")

    def generate_from_sketch(self, sketch: Union[str, bytes, BinaryIO],
                              prompt: str,
                              negative_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate image from sketch

        Args:
            sketch: Sketch/drawing
            prompt: Text prompt
            negative_prompt: Negative prompt

        Returns:
            Dictionary containing generated image

        Raises:
            StabilityAIError: If generation fails
        """
        self._enforce_rate_limit()

        sketch_b64 = self._encode_image(sketch)

        payload = {
            "image": f"data:image/png;base64,{sketch_b64}",
            "prompt": prompt
        }

        if negative_prompt:
            payload["negative_prompt"] = negative_prompt

        try:
            response = self.session.post(
                f"{self.BASE_URL}/stable-image/control/sketch",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise StabilityAIError(f"Request failed: {str(e)}")