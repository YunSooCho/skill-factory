"""
TextCortex AI API Client - AI Text Generation
"""

import requests
import time
from typing import Optional, Dict, Any


class TextCortexError(Exception):
    """Base exception for TextCortex errors"""
    pass


class TextCortexRateLimitError(TextCortexError):
    """Rate limit exceeded"""
    pass


class TextCortexAuthenticationError(TextCortexError):
    """Authentication failed"""
    pass


class TextCortexClient:
    """Client for TextCortex AI Text Generation API"""

    BASE_URL = "https://api.textcortex.com/v1"

    def __init__(self, api_key: str, timeout: int = 30):
        """
        Initialize TextCortex client

        Args:
            api_key: TextCortex API key
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
            raise TextCortexRateLimitError("Rate limit exceeded")

        if response.status_code == 401:
            raise TextCortexAuthenticationError("Authentication failed")

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get('message', or error_data.get('error', ''))
            except:
                error_msg = response.text or response.reason or "Unknown error"
            raise TextCortexError(f"API error ({response.status_code}): {error_msg}")

        return response.json()

    def generate_summary(self, text: str, max_length: Optional[int] = None) -> Dict[str, Any]:
        """Generate text summary"""
        self._enforce_rate_limit()

        payload = {"text": text}
        if max_length:
            payload["max_length"] = max_length

        try:
            response = self.session.post(
                f"{self.BASE_URL}/summarize",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise TextCortexError(f"Request failed: {str(e)}")

    def generate_product_description(self, product_name: str = "",
                                      features: str = "",
                                      tone: str = "professional") -> Dict[str, Any]:
        """Generate product description"""
        self._enforce_rate_limit()

        payload = {
            "product_name": product_name,
            "features": features,
            "tone": tone
        }

        try:
            response = self.session.post(
                f"{self.BASE_URL}/product-description",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise TextCortexError(f"Request failed: {str(e)}")

    def simplify_text(self, text: str, target_level: str = "simple") -> Dict[str, Any]:
        """Simplify text"""
        self._enforce_rate_limit()

        payload = {
            "text": text,
            "target_level": target_level
        }

        try:
            response = self.session.post(
                f"{self.BASE_URL}/simplify",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise TextCortexError(f"Request failed: {str(e)}")

    def translate_text(self, text: str, target_language: str) -> Dict[str, Any]:
        """Translate text"""
        self._enforce_rate_limit()

        payload = {
            "text": text,
            "target_language": target_language
        }

        try:
            response = self.session.post(
                f"{self.BASE_URL}/translate",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise TextCortexError(f"Request failed: {str(e)}")

    def paraphrase_text(self, text: str, tone: str = "neutral") -> Dict[str, Any]:
        """Paraphrase text"""
        self._enforce_rate_limit()

        payload = {
            "text": text,
            "tone": tone
        }

        try:
            response = self.session.post(
                f"{self.BASE_URL}/paraphrase",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise TextCortexError(f"Request failed: {str(e)}")

    def rewrite_text(self, text: str, style: str = "professional") -> Dict[str, Any]:
        """Rewrite text"""
        self._enforce_rate_limit()

        payload = {
            "text": text,
            "style": style
        }

        try:
            response = self.session.post(
                f"{self.BASE_URL}/rewrite",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise TextCortexError(f"Request failed: {str(e)}")

    def generate_social_media_post(self, topic: str, platform: str = "twitter",
                                    tone: str = "engaging") -> Dict[str, Any]:
        """Generate social media posts"""
        self._enforce_rate_limit()

        payload = {
            "topic": topic,
            "platform": platform,
            "tone": tone
        }

        try:
            response = self.session.post(
                f"{self.BASE_URL}/social-media-post",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise TextCortexError(f"Request failed: {str(e)}")

    def generate_text_completion(self, prompt: str, max_tokens: int = 100) -> Dict[str, Any]:
        """Generate text completion"""
        self._enforce_rate_limit()

        payload = {
            "prompt": prompt,
            "max_tokens": max_tokens
        }

        try:
            response = self.session.post(
                f"{self.BASE_URL}/complete",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise TextCortexError(f"Request failed: {str(e)}")

    def generate_code(self, prompt: str, language: str = "python") -> Dict[str, Any]:
        """Generate code"""
        self._enforce_rate_limit()

        payload = {
            "prompt": prompt,
            "language": language
        }

        try:
            response = self.session.post(
                f"{self.BASE_URL}/code",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise TextCortexError(f"Request failed: {str(e)}")

    def generate_email(self, subject: str = "", purpose: str = "",
                        tone: str = "professional") -> Dict[str, Any]:
        """Generate email text"""
        self._enforce_rate_limit()

        payload = {
            "subject": subject,
            "purpose": purpose,
            "tone": tone
        }

        try:
            response = self.session.post(
                f"{self.BASE_URL}/email",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise TextCortexError(f"Request failed: {str(e)}")