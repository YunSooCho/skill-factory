"""
OpenRouter - AI Model Routing API

Supports:
- Create Chat Completion
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class Message:
    """Chat message"""
    role: str
    content: str


@dataclass
class CompletionResponse:
    """Chat completion response"""
    id: str
    model: str
    choices: List[Dict[str, Any]]
    usage: Dict[str, int]


class OpenRouterClient:
    """
    OpenRouter API client for AI model access.

    API Documentation: https://openrouter.ai/docs
    Requires an API key from OpenRouter.
    """

    BASE_URL = "https://openrouter.ai/api/v1"

    def __init__(self, api_key: str):
        """
        Initialize OpenRouter client.

        Args:
            api_key: OpenRouter API key
        """
        self.api_key = api_key
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def create_chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "mistralai/mistral-7b-instruct",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> CompletionResponse:
        """
        Create a chat completion.

        Args:
            messages: List of message dicts with role and content
            model: Model identifier
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            stream: Whether to stream the response

        Returns:
            CompletionResponse with completion data

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "stream": stream
            }

            if max_tokens:
                payload["max_tokens"] = max_tokens

            async with self.session.post(
                f"{self.BASE_URL}/chat/completions",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"OpenRouter error: {data.get('error', 'Unknown error')}")

                return CompletionResponse(
                    id=data["id"],
                    model=data["model"],
                    choices=data["choices"],
                    usage=data.get("usage", {})
                )

        except Exception as e:
            raise Exception(f"Failed to create chat completion: {str(e)}")