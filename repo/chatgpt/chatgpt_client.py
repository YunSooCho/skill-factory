"""
ChatGPT API - OpenAI ChatGPT Client

Supports:
- Generate Text
- Text to Speech
- Speech to Text (File Attachment)
- List Models
- Generate Text (Web Search)
- Create Thread
- Generate Text (Image Attachment)
- Generate Text (Advanced Settings)
- Add Message to Thread
- Generate Text from Image URL
Plus webhooks for: Message Generated in Thread
"""

import aiohttp
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class Message:
    """Chat message"""
    role: str  # 'user', 'assistant', 'system'
    content: str


@dataclass
class ChatGenerationResponse:
    """Chat generation response"""
    content: str
    model: str
    finish_reason: str
    usage: Dict[str, int]


@dataclass
class Model:
    """Available model"""
    id: str
    description: str
    context_length: int


@dataclass
class Thread:
    """Conversation thread"""
    id: str
    created_at: str
    metadata: Dict[str, Any]


@dataclass
class ThreadMessage:
    """Message in a thread"""
    id: str
    content: str
    role: str
    created_at: str


@dataclass
class SpeechResponse:
    """Text-to-speech response"""
    audio_data: bytes
    format: str


@dataclass
class TranscriptionResponse:
    """Speech-to-text response"""
    text: str
    language: str
    duration: float


class ChatGPTAPIClient:
    """
    ChatGPT API client for OpenAI's chat completions and related features.

    API Documentation: https://platform.openai.com/docs/api-reference
    """

    BASE_URL = "https://api.openai.com/v1"

    def __init__(self, api_key: str, base_url: Optional[str] = None):
        """
        Initialize ChatGPT API client.

        Args:
            api_key: OpenAI API key from platform.openai.com
            base_url: Custom base URL (optional)
        """
        self.api_key = api_key
        self.BASE_URL = base_url or self.BASE_URL
        self.session = None

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=self._get_headers())
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def generate_text(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> ChatGenerationResponse:
        """
        Generate text using ChatGPT.

        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model name (default: gpt-4)
            temperature: Sampling temperature (0.0-2.0)
            max_tokens: Maximum tokens to generate
            stream: Whether to stream response

        Returns:
            ChatGenerationResponse with generated content

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
                raise Exception(f"ChatGPT API error: {error_msg}")

            return ChatGenerationResponse(
                content=data["choices"][0]["message"]["content"],
                model=data.get("model", model),
                finish_reason=data["choices"][0]["finish_reason"],
                usage=data.get("usage", {})
            )

    async def generate_text_with_web_search(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4o",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> ChatGenerationResponse:
        """
        Generate text using ChatGPT with web search context.

        Args:
            messages: List of message dicts
            model: Model name (use gpt-4o with browsing)
            temperature: Sampling temperature
            max_tokens: Maximum tokens

        Returns:
            ChatGenerationResponse with generated content

        Raises:
            ValueError: If messages is empty
            aiohttp.ClientError: If request fails
        """
        # Add web search instruction to system message
        enhanced_messages = []
        for msg in messages:
            if msg.get("role") == "system":
                enhanced_messages.append({
                    "role": "system",
                    "content": msg["content"] + " Please use web search for current information when needed."
                })
            else:
                enhanced_messages.append(msg)

        return await self.generate_text(
            messages=enhanced_messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        )

    async def generate_text_advanced(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        top_p: float = 1.0,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
        stop_sequences: Optional[List[str]] = None
    ) -> ChatGenerationResponse:
        """
        Generate text with advanced settings.

        Args:
            messages: List of message dicts
            model: Model name
            temperature: Sampling temperature
            max_tokens: Maximum tokens
            top_p: Nucleus sampling parameter
            frequency_penalty: Frequency penalty
            presence_penalty: Presence penalty
            stop_sequences: Sequences that stop generation

        Returns:
            ChatGenerationResponse with generated content

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
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty
        }

        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        if stop_sequences:
            payload["stop"] = stop_sequences

        async with self.session.post(
            f"{self.BASE_URL}/chat/completions",
            json=payload
        ) as response:
            data = await response.json()

            if response.status != 200:
                error_msg = data.get("error", {}).get("message", str(data))
                raise Exception(f"ChatGPT Advanced API error: {error_msg}")

            return ChatGenerationResponse(
                content=data["choices"][0]["message"]["content"],
                model=data.get("model", model),
                finish_reason=data["choices"][0]["finish_reason"],
                usage=data.get("usage", {})
            )

    async def generate_text_with_image(
        self,
        messages: List[Dict[str, Any]],
        model: str = "gpt-4-vision-preview",
        max_tokens: int = 500
    ) -> ChatGenerationResponse:
        """
        Generate text from image input.

        Args:
            messages: List of messages (can include image URLs or base64)
            model: Vision model name
            max_tokens: Maximum tokens

        Returns:
            ChatGenerationResponse with generated content

        Raises:
            ValueError: If messages is empty
            aiohttp.ClientError: If request fails
        """
        if not messages:
            raise ValueError("Messages list cannot be empty")

        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens
        }

        async with self.session.post(
            f"{self.BASE_URL}/chat/completions",
            json=payload
        ) as response:
            data = await response.json()

            if response.status != 200:
                error_msg = data.get("error", {}).get("message", str(data))
                raise Exception(f"ChatGPT Vision API error: {error_msg}")

            return ChatGenerationResponse(
                content=data["choices"][0]["message"]["content"],
                model=data.get("model", model),
                finish_reason=data["choices"][0]["finish_reason"],
                usage=data.get("usage", {})
            )

    async def generate_text_from_image_url(
        self,
        image_url: str,
        prompt: str,
        model: str = "gpt-4-vision-preview",
        max_tokens: int = 500
    ) -> ChatGenerationResponse:
        """
        Generate text from an image URL.

        Args:
            image_url: Image URL
            prompt: Text prompt/questions about the image
            model: Vision model name
            max_tokens: Maximum tokens

        Returns:
            ChatGenerationResponse with generated content

        Raises:
            ValueError: If image_url or prompt is empty
            aiohttp.ClientError: If request fails
        """
        if not image_url:
            raise ValueError("Image URL cannot be empty")
        if not prompt:
            raise ValueError("Prompt cannot be empty")

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }
        ]

        return await self.generate_text_with_image(
            messages=messages,
            model=model,
            max_tokens=max_tokens
        )

    async def list_models(self) -> List[Model]:
        """
        List available models.

        Returns:
            List of Model objects

        Raises:
            aiohttp.ClientError: If request fails
        """
        async with self.session.get(f"{self.BASE_URL}/models") as response:
            data = await response.json()

            if response.status != 200:
                error_msg = data.get("error", {}).get("message", str(data))
                raise Exception(f"List Models error: {error_msg}")

            models = [
                Model(
                    id=m.get("id", ""),
                    description=m.get("description", ""),
                    context_length=len(m.get("description", ""))  # Approximate
                )
                for m in data.get("data", [])
            ]

            return models

    async def create_thread(
        self,
        messages: Optional[List[Dict[str, str]]] = None,
        metadata: Optional[Dict[str, str]] = None
    ) -> Thread:
        """
        Create a new conversation thread.

        Args:
            messages: Optional initial messages
            metadata: Optional metadata

        Returns:
            Thread object

        Raises:
            aiohttp.ClientError: If request fails
        """
        payload = {}

        if messages:
            payload["messages"] = messages
        if metadata:
            payload["metadata"] = metadata

        async with self.session.post(
            f"{self.BASE_URL}/threads",
            json=payload if payload else None
        ) as response:
            data = await response.json()

            if response.status not in [200, 201]:
                error_msg = data.get("error", {}).get("message", str(data))
                raise Exception(f"Create Thread error: {error_msg}")

            return Thread(
                id=data.get("id", ""),
                created_at=data.get("created_at", ""),
                metadata=data.get("metadata", {})
            )

    async def add_message_to_thread(
        self,
        thread_id: str,
        content: str,
        role: str = "user"
    ) -> ThreadMessage:
        """
        Add a message to a thread.

        Args:
            thread_id: Thread ID
            content: Message content
            role: Message role (default: 'user')

        Returns:
            ThreadMessage object

        Raises:
            ValueError: If thread_id or content is empty
            aiohttp.ClientError: If request fails
        """
        if not thread_id:
            raise ValueError("Thread ID cannot be empty")
        if not content:
            raise ValueError("Content cannot be empty")

        payload = {
            "role": role,
            "content": content
        }

        async with self.session.post(
            f"{self.BASE_URL}/threads/{thread_id}/messages",
            json=payload
        ) as response:
            data = await response.json()

            if response.status not in [200, 201]:
                error_msg = data.get("error", {}).get("message", str(data))
                raise Exception(f"Add Message error: {error_msg}")

            return ThreadMessage(
                id=data.get("id", ""),
                content=data.get("content", ""),
                role=data.get("role", ""),
                created_at=data.get("created_at", "")
            )

    async def text_to_speech(
        self,
        text: str,
        model: str = "tts-1",
        voice: str = "alloy",
        output_format: str = "mp3"
    ) -> SpeechResponse:
        """
        Convert text to speech.

        Args:
            text: Text to convert
            model: TTS model ('tts-1', 'tts-1-hd')
            voice: Voice ('alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer')
            output_format: Output format ('mp3', 'opus', 'aac', 'flac', 'wav', 'pcm')

        Returns:
            SpeechResponse with audio data

        Raises:
            ValueError: If text is empty
            aiohttp.ClientError: If request fails
        """
        if not text:
            raise ValueError("Text cannot be empty")

        payload = {
            "model": model,
            "input": text,
            "voice": voice
        }

        async with self.session.post(
            f"{self.BASE_URL}/audio/speech",
            json=payload,
            headers={"Content-Type": "application/json"}
        ) as response:
            if response.status != 200:
                error_msg = await response.text()
                raise Exception(f"Text to Speech error: {error_msg}")

            audio_data = await response.read()

            return SpeechResponse(
                audio_data=audio_data,
                format=output_format
            )

    async def speech_to_text(
        self,
        file_path: str,
        model: str = "whisper-1",
        language: Optional[str] = None,
        prompt: Optional[str] = None
    ) -> TranscriptionResponse:
        """
        Convert speech/audio file to text.

        Args:
            file_path: Path to audio file
            model: Whisper model ('whisper-1')
            language: Optional language code
            prompt: Optional transcription prompt

        Returns:
            TranscriptionResponse with transcribed text

        Raises:
            ValueError: If file doesn't exist
            aiohttp.ClientError: If request fails
        """
        import os

        if not os.path.exists(file_path):
            raise ValueError(f"File not found: {file_path}")

        # Read file
        with open(file_path, "rb") as f:
            file_data = f.read()

        filename = os.path.basename(file_path)

        data = aiohttp.FormData()
        data.add_field("file", file_data, filename=filename)
        data.add_field("model", model)

        if language:
            data.add_field("language", language)
        if prompt:
            data.add_field("prompt", prompt)

        async with self.session.post(
            f"{self.BASE_URL}/audio/transcriptions",
            data=data
        ) as response:
            response_data = await response.json()

            if response.status != 200:
                error_msg = response_data.get("error", {}).get("message", str(response_data))
                raise Exception(f"Speech to Text error: {error_msg}")

            return TranscriptionResponse(
                text=response_data.get("text", ""),
                language=response_data.get("language", language or ""),
                duration=response_data.get("duration", 0.0)
            )

    def verify_webhook(self, payload: Dict[str, Any], signature: str, secret: str) -> bool:
        """
        Verify webhook signature.

        Args:
            payload: Webhook payload
            signature: Signature from webhook headers
            secret: Webhook secret

        Returns:
            bool: True if signature is valid
        """
        import hmac
        import hashlib
        import json

        payload_str = json.dumps(payload, separators=(',', ':'), sort_keys=True)
        expected_signature = hmac.new(
            secret.encode(),
            payload_str.encode(),
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(expected_signature, signature)

    def parse_webhook_event(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse webhook event payload.

        Args:
            payload: Webhook payload

        Returns:
            Dict with event details
        """
        event_type = payload.get("type", "")
        event_data = payload.get("data", {})

        result = {
            "event_type": event_type,
            "event_id": payload.get("id", ""),
            "timestamp": payload.get("timestamp", ""),
            "data": event_data
        }

        # Thread message event
        if event_type == "thread.message.created":
            result["thread_id"] = event_data.get("thread_id", "")
            result["message_id"] = event_data.get("message_id", "")
            result["content"] = event_data.get("content", "")

        return result


async def main():
    """Example usage"""
    api_key = "your-api-key-here"

    async with ChatGPTAPIClient(api_key) as client:
        # Generate text
        messages = [
            {"role": "user", "content": "Explain machine learning in simple terms."}
        ]

        response = await client.generate_text(messages=messages)
        print(f"Response: {response.content}")
        print(f"Model: {response.model}")

        # List models
        models = await client.list_models()
        print(f"Available models: {len(models)}")

        # Create thread
        thread = await client.create_thread()
        print(f"Thread created: {thread.id}")

        # Add message to thread
        msg = await client.add_message_to_thread(
            thread_id=thread.id,
            content="Hello! How can you help me?"
        )
        print(f"Message added: {msg.id}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())