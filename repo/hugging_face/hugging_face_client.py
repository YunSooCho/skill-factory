"""
AI model hosting API Client
General
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any, List
import time


class RateLimiter:
    """Simple rate limiter for API requests"""

    def __init__(self, max_requests: int = 120, per_seconds: int = 60):
        self.max_requests = max_requests
        self.per_seconds = per_seconds
        self.requests = []
        self.lock = asyncio.Lock()

    async def acquire(self):
        async with self.lock:
            now = time.time()
            self.requests = [req_time for req_time in self.requests
                            if now - req_time < self.per_seconds]

            if len(self.requests) >= self.max_requests:
                sleep_time = self.per_seconds - (now - self.requests[0])
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)
                    self.requests = []

            self.requests.append(now)


class HuggingFaceClient:
    """
    AI model hosting API client.
    """

    BASE_URL = "https://api-inference.huggingface.co"

    def __init__(self, api_key: str):
        """
        Initialize HuggingFaceClient API client.

        Args:
            api_key: Your API key
        """
        self.api_key = api_key
        self.session = None
        self.rate_limiter = RateLimiter(max_requests=120, per_seconds=60)

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with API key"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make API request with error handling and rate limiting.

        Args:
            method: HTTP method
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON body data

        Returns:
            Response data

        Raises:
            Exception: If request fails
        """
        await self.rate_limiter.acquire()

        url = f"{self.BASE_URL}{endpoint}"

        try:
            async with self.session.request(
                method,
                url,
                headers=self._get_headers(),
                params=params,
                json=json_data
            ) as response:
                try:
                    data = await response.json()
                except:
                    text = await response.text()
                    data = {"raw_response": text}

                if response.status >= 400:
                    error_msg = data.get("error", data.get("message", "Unknown error"))
                    raise Exception(f"HuggingFaceClient API error ({response.status}): {error_msg}")

                return data

        except aiohttp.ClientError as e:
            raise Exception(f"Network error during request to {url}: {str(e)}")
        except Exception as e:
            raise Exception(f"Error during HuggingFaceClient API request: {str(e)}")


    # ==================== API Methods ====================

    async def summarize_text(
        self,
        text: str,
        model: str = "facebook/bart-large-cnn",
        max_length: int = 130,
        min_length: int = 30
    ) -> Dict[str, Any]:
        """
        Summarize text (テキストを要約).

        Args:
            text: Input text to summarize
            model: Model ID (default: facebook/bart-large-cnn)
            max_length: Maximum length of summary
            min_length: Minimum length of summary

        Returns:
            Summarized text

        Raises:
            Exception: If request fails
        """
        data = {
            "inputs": text,
            "parameters": {
                "max_length": max_length,
                "min_length": min_length
            }
        }

        return await self._request("POST", f"/models/{model}", json_data=data)

    async def classify_text(
        self,
        text: str,
        model: str = "distilbert-base-uncased-finetuned-sst-2-english",
        labels: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Classify text (テキストを分類).

        Args:
            text: Input text to classify
            model: Model ID (default: distilbert-base-uncased-finetuned-sst-2-english)
            labels: Optional labels for zero-shot classification

        Returns:
            Classification results with labels and scores

        Raises:
            Exception: If request fails
        """
        if labels:
            # Zero-shot classification
            data = {
                "inputs": text,
                "parameters": {
                    "candidate_labels": labels
                }
            }
            endpoint = f"/models/facebook/bart-large-mnli"
        else:
            # Standard classification
            data = {
                "inputs": text
            }
            endpoint = f"/models/{model}"

        return await self._request("POST", endpoint, json_data=data)

    async def answer_question(
        self,
        question: str,
        context: str,
        model: str = "deepset/roberta-base-squad2"
    ) -> Dict[str, Any]:
        """
        Answer question (質問へ回答).

        Args:
            question: Question to answer
            context: Context containing the answer
            model: Model ID (default: deepset/roberta-base-squad2)

        Returns:
            Answer with confidence score

        Raises:
            Exception: If request fails
        """
        data = {
            "inputs": {
                "question": question,
                "context": context
            }
        }

        return await self._request("POST", f"/models/{model}", json_data=data)

    async def compare_text_similarity(
        self,
        text1: str,
        text2: str,
        model: str = "sentence-transformers/all-MiniLM-L6-v2"
    ) -> Dict[str, Any]:
        """
        Determine text similarity (文章の類似性を判別).

        Args:
            text1: First text
            text2: Second text
            model: Model ID (default: sentence-transformers/all-MiniLM-L6-v2)

        Returns:
            Similarity score (0-1)

        Raises:
            Exception: If request fails
        """
        data = {
            "inputs": {
                "source_sentence": text1,
                "sentences": [text2]
            }
        }

        return await self._request("POST", f"/models/{model}", json_data=data)