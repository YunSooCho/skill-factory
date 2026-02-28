"""
OpenAI API Client

Provides async client for OpenAI API including:
- Text generation (Chat Completions)
- Completion API (legacy)
- Embeddings
- Image generation
- Models list
"""

import aiohttp
import asyncio
import json
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any, List, AsyncGenerator
from dataclasses import dataclass, field


@dataclass
class ChatMessage:
    """Chat message for completion"""
    role: str
    content: str


@dataclass
class ChatCompletionResponse:
    """Chat completion response"""
    id: str
    object: str
    created: int
    model: str
    choices: List[Dict[str, Any]]
    usage: Dict[str, int]
    finish_reason: Optional[str] = None
    content: Optional[str] = field(init=False)

    def __post_init__(self):
        """Extract content from first choice"""
        if self.choices and len(self.choices) > 0:
            message = self.choices[0].get('message', {})
            self.content = message.get('content')
            self.finish_reason = self.choices[0].get('finish_reason')


@dataclass
class EmbeddingResponse:
    """Embedding response"""
    object: str
    embedding: List[float]
    index: int
    model: str
    usage: Dict[str, int]


@dataclass
class ImageGenerationResponse:
    """Image generation response"""
    created: int
    data: List[Dict[str, Any]]

    def get_urls(self) -> List[str]:
        """Get all image URLs"""
        return [item.get('url', '') for item in self.data if item.get('url')]


@dataclass
class ModelInfo:
    """
    Model information
    """
    id: str
    object: str
    created: int
    owned_by: str


class RateLimiter:
    """Rate limiter for API calls"""

    def __init__(self, max_requests: int = 3000, per_seconds: int = 60):
        self.max_requests = max_requests
        self.per_seconds = per_seconds
        self.requests: List[datetime] = []
        self.lock = asyncio.Lock()

    async def acquire(self) -> None:
        """Wait until a request can be made"""
        async with self.lock:
            now = datetime.now(timezone.utc)

            # Remove old requests outside the time window
            cutoff = now - timedelta(seconds=self.per_seconds)
            self.requests = [req for req in self.requests if req > cutoff]

            # Check if need to wait
            if len(self.requests) >= self.max_requests:
                oldest_request = sorted(self.requests)[0]
                sleep_time = (oldest_request + timedelta(seconds=self.per_seconds) - now).total_seconds()
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)

            self.requests.append(now)


class OpenAIClient:
    """
    Async OpenAI API client with rate limiting and error handling.

    API Documentation: https://platform.openai.com/docs/api-reference

    Requires API key from https://platform.openai.com/api-keys
    """

    BASE_URL = "https://api.openai.com/v1"

    def __init__(
        self,
        api_key: str,
        organization: Optional[str] = None,
        max_requests_per_minute: int = 3000
    ):
        """
        Initialize OpenAI client.

        Args:
            api_key: OpenAI API key
            organization: Optional organization ID
            max_requests_per_minute: Rate limit for requests (default: 3000)
        """
        self.api_key = api_key
        self.organization = organization
        self.session = None
        self.rate_limiter = RateLimiter(max_requests=max_requests_per_minute, per_seconds=60)

        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        if organization:
            self.headers["OpenAI-Organization"] = organization

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=self.headers)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Make API request with rate limiting and error handling.

        Args:
            method: HTTP method
            endpoint: API endpoint
            data: Request body data
            params: Query parameters

        Returns:
            Response data as dict

        Raises:
            aiohttp.ClientError: If request fails
            ValueError: If API returns error
        """
        await self.rate_limiter.acquire()

        url = f"{self.BASE_URL}/{endpoint.lstrip('/')}"

        try:
            async with self.session.request(
                method=method,
                url=url,
                json=data,
                params=params
            ) as response:
                response_data = await response.json()

                if response.status not in (200, 201):
                    error_msg = response_data.get('error', {}).get('message', 'Unknown error')
                    raise ValueError(f"OpenAI API error ({response.status}): {error_msg}")

                return response_data

        except aiohttp.ClientError as e:
            raise aiohttp.ClientError(f"HTTP request failed: {e}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON response: {response_data}")

    # ==================== Chat Completions ====================

    async def chat_completion(
        self,
        messages: List[ChatMessage] | List[Dict[str, str]],
        model: str = "gpt-4-turbo-preview",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        top_p: float = 1.0,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
        stream: bool = False,
        n: int = 1,
        stop: Optional[str | List[str]] = None
    ) -> ChatCompletionResponse | AsyncGenerator[str, None]:
        """
        Create chat completion.

        Args:
            messages: List of chat messages
            model: Model to use (default: gpt-4-turbo-preview)
            temperature: Sampling temperature (0-2, default: 0.7)
            max_tokens: Maximum tokens to generate
            top_p: Nucleus sampling parameter (default: 1.0)
            frequency_penalty: Frequency penalty (default: 0.0)
            presence_penalty: Presence penalty (default: 0.0)
            stream: Whether to stream responses
            n: Number of completions to generate (default: 1)
            stop: Stop sequences

        Returns:
            ChatCompletionResponse or AsyncGenerator if stream=True

        Raises:
            ValueError: If API returns error
            aiohttp.ClientError: If request fails
        """
        # Convert dict messages to ChatMessage if needed
        if messages and isinstance(messages[0], dict):
            messages = [ChatMessage(**msg) for msg in messages]

        data = {
            "model": model,
            "messages": [{"role": msg.role, "content": msg.content} for msg in messages],
            "temperature": temperature,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
            "stream": stream,
            "n": n
        }

        if max_tokens is not None:
            data["max_tokens"] = max_tokens
        if stop is not None:
            data["stop"] = stop

        if stream:
            return self._stream_chat_completion(data)
        else:
            response_data = await self._request("POST", "/chat/completions", data=data)
            return ChatCompletionResponse(**response_data)

    async def _stream_chat_completion(
        self,
        data: Dict[str, Any]
    ) -> AsyncGenerator[str, None]:
        """Stream chat completion"""
        async with self.session.post(
            f"{self.BASE_URL}/chat/completions",
            json=data
        ) as response:
            if response.status != 200:
                error_data = await response.json()
                error_msg = error_data.get('error', {}).get('message', 'Unknown error')
                raise ValueError(f"OpenAI API error ({response.status}): {error_msg}")

            async for line in response.content:
                line = line.decode('utf-8').strip()
                if line.startswith('data: '):
                    data_str = line[6:]
                    if data_str == '[DONE]':
                        break
                    try:
                        chunk = json.loads(data_str)
                        delta = chunk.get('choices', [{}])[0].get('delta', {})
                        content = delta.get('content', '')
                        if content:
                            yield content
                    except json.JSONDecodeError:
                        continue

    # ==================== Models ====================

    async def list_models(self) -> List[ModelInfo]:
        """
        List available models.

        Returns:
            List of ModelInfo objects

        Raises:
            ValueError: If API returns error
            aiohttp.ClientError: If request fails
        """
        response_data = await self._request("GET", "/models")
        models = response_data.get('data', [])
        return [ModelInfo(**model) for model in models]

    # ==================== Embeddings ====================

    async def create_embedding(
        self,
        text: str,
        model: str = "text-embedding-3-small"
    ) -> EmbeddingResponse:
        """
        Create embedding for text.

        Args:
            text: Text to embed
            model: Embedding model to use

        Returns:
            EmbeddingResponse with embedding vector

        Raises:
            ValueError: If API returns error
            aiohttp.ClientError: If request fails
        """
        data = {
            "model": model,
            "input": text
        }

        response_data = await self._request("POST", "/embeddings", data=data)
        embedding_data = response_data['data'][0]

        return EmbeddingResponse(
            object=embedding_data['object'],
            embedding=embedding_data['embedding'],
            index=embedding_data['index'],
            model=response_data['model'],
            usage=response_data.get('usage', {})
        )

    # ==================== Image Generation ====================

    async def create_image(
        self,
        prompt: str,
        model: str = "dall-e-3",
        size: str = "1024x1024",
        quality: str = "standard",
        n: int = 1
    ) -> ImageGenerationResponse:
        """
        Generate image from text prompt.

        Args:
            prompt: Text prompt for image generation
            model: Image model (dall-e-3 or dall-e-2)
            size: Image size (dall-e-3: 1024x1024, 1024x1792, 1792x1024; dall-e-2: 256x256, 512x512, 1024x1024)
            quality: Image quality (standard or hd, dall-e-3 only)
            n: Number of images to generate (dall-e-3: 1, dall-e-2: 1-10)

        Returns:
            ImageGenerationResponse with image URLs

        Raises:
            ValueError: If API returns error
            aiohttp.ClientError: If request fails
        """
        data = {
            "model": model,
            "prompt": prompt,
            "size": size,
            "n": n
        }

        if model == "dall-e-3":
            data["quality"] = quality

        response_data = await self._request("POST", "/images/generations", data=data)
        return ImageGenerationResponse(**response_data)


# ==================== Example Usage ====================

async def main():
    """Example usage of OpenAI client"""

    # Replace with your actual API key
    api_key = "your-openai-api-key-here"

    async with OpenAIClient(api_key=api_key) as client:
        try:
            # Chat completion
            messages = [
                ChatMessage(role="user", content="What is the capital of France?")
            ]
            response = await client.chat_completion(messages, model="gpt-4-turbo-preview")
            print(f"Chat response: {response.content}")

            # List models
            models = await client.list_models()
            print(f"Available models: {[model.id for model in models[:5]]}")

            # Create embedding
            embedding = await client.create_embedding("Hello world")
            print(f"Embedding dimension: {len(embedding.embedding)}")

            # Generate image
            image_response = await client.create_image(
                prompt="A beautiful sunset over mountains",
                size="1024x1024"
            )
            print(f"Generated images: {image_response.get_urls()}")

        except ValueError as e:
            print(f"API Error: {e}")
        except aiohttp.ClientError as e:
            print(f"Connection error: {e}")


if __name__ == "__main__":
    asyncio.run(main())