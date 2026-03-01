"""
DeepSeek API - LLM API Client

Supports:
- Generate Text
"""

import aiohttp
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class Message:
    """Chat message"""
    role: str  # 'system', 'user', 'assistant'
    content: str


@dataclass
class TextGenerationResponse:
    """Text generation response"""
    content: str
    model: str
    finish_reason: str
    usage: Dict[str, int]
    created: int


class DeepSeekAPIClient:
    """
    DeepSeek API client for text generation.

    API Documentation: https://platform.deepseek.com/api-docs/
    """

    BASE_URL = "https://api.deepseek.com/v1"

    def __init__(self, api_key: str):
        """
        Initialize DeepSeek API client.

        Args:
            api_key: DeepSeek API key from platform.deepseek.com
        """
        self.api_key = api_key
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def generate_text(
        self,
        messages: List[Dict[str, str]],
        model: str = "deepseek-chat",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> TextGenerationResponse:
        """
        Generate text using DeepSeek's LLM.

        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model name (default: deepseek-chat)
            temperature: Sampling temperature (0.0-2.0)
            max_tokens: Maximum tokens to generate
            stream: Whether to stream the response

        Returns:
            TextGenerationResponse with generated content

        Raises:
            ValueError: If messages is empty
            aiohttp.ClientError: If request fails
        """
        if not messages:
            raise ValueError("Messages list cannot be empty")

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "stream": stream
        }

        if max_tokens is not None:
            payload["max_tokens"] = max_tokens

        async with self.session.post(
            f"{self.BASE_URL}/chat/completions",
            json=payload
        ) as response:
            data = await response.json()

            if response.status != 200:
                error_msg = data.get("error", {}).get("message", str(data))
                raise Exception(f"DeepSeek API error: {error_msg}")

            return TextGenerationResponse(
                content=data["choices"][0]["message"]["content"],
                model=data["model"],
                finish_reason=data["choices"][0]["finish_reason"],
                usage=data.get("usage", {}),
                created=data.get("created", 0)
            )


async def main():
    """Example usage"""
    api_key = "your-api-key-here"

    async with DeepSeekAPIClient(api_key) as client:
        messages = [
            {"role": "user", "content": "Hello! How are you?"}
        ]

        response = await client.generate_text(messages)
        print(f"Generated text: {response.content}")
        print(f"Model: {response.model}")
        print(f"Tokens used: {response.usage}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())