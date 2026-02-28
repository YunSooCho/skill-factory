"""
Google Gemini API - AI Content Generation Client

Supports:
- Generate Content
- Generate Content with URL Context
- Generate Content with File
- Generate Content with Google Search
- Upload File
"""

import aiohttp
import json
import base64
from typing import Optional, Dict, Any, List, Union
from dataclasses import dataclass


@dataclass
class GenerationResponse:
    """Content generation response"""
    content: str
    model: str
    finish_reason: str
    usage: Optional[Dict[str, int]] = None
    citations: Optional[List[str]] = None


@dataclass
class UploadedFile:
    """Uploaded file object"""
    file_id: str
    name: str
    mime_type: str
    size: int
    uri: str


@dataclass
class SearchResult:
    """Search result object"""
    title: str
    url: str
    snippet: str


class GeminiClient:
    """
    Google Gemini API client for AI-powered content generation.

    Gemini is Google's multimodal AI model capable of understanding
    and generating text, images, and other content types.

    API Documentation: https://lp.yoom.fun/apps/gemini
    Requires:
    - Google Cloud project with Vertex AI API enabled
    - API key or OAuth credentials
    """

    BASE_URL = "https://generativelanguage.googleapis.com/v1beta"

    def __init__(
        self,
        api_key: str,
        model: str = "gemini-pro",
        enable_search: bool = False
    ):
        """
        Initialize Gemini client.

        Args:
            api_key: Google Cloud API key
            model: Model name to use (e.g., gemini-pro, gemini-pro-vision)
            enable_search: Whether to enable Google Search integration
        """
        self.api_key = api_key
        self.model = model
        self.enable_search = enable_search
        self.session = None
        self._rate_limit_delay = 0.2

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make an API request with error handling.

        Args:
            method: HTTP method
            endpoint: API endpoint
            params: Query parameters
            json_data: JSON body data

        Returns:
            Response data as dictionary

        Raises:
            Exception: If request fails or returns error
        """
        url = endpoint

        if params is None:
            params = {}

        params["key"] = self.api_key

        try:
            async with self.session.request(
                method,
                url,
                params=params,
                json=json_data
            ) as response:
                response_data = await response.json()

                if response.status >= 400:
                    error = response_data.get("error", {})
                    error_message = error.get("message", f"HTTP {response.status} error")
                    raise Exception(f"Gemini API error: {error_message}")

                return response_data

        except aiohttp.ClientError as e:
            raise Exception(f"Network error: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON response: {str(e)}")

    # ==================== Generate Content ====================

    async def generate_content(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_output_tokens: int = 1024,
        top_p: float = 0.95,
        top_k: int = 40,
        system_instruction: Optional[str] = None
    ) -> GenerationResponse:
        """
        Generate content using Gemini.

        Args:
            prompt: Text prompt for generation
            temperature: Sampling temperature (0.0-2.0)
            max_output_tokens: Maximum tokens to generate
            top_p: Nucleus sampling parameter
            top_k: Top-k sampling parameter
            system_instruction: Optional system instruction

        Returns:
            GenerationResponse with generated content

        Raises:
            Exception: If generation fails
            ValueError: If parameters are invalid
        """
        if not prompt:
            raise ValueError("prompt is required")

        if temperature < 0 or temperature > 2:
            raise ValueError("temperature must be between 0 and 2")

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_output_tokens,
                "topP": top_p,
                "topK": top_k
            }
        }

        if system_instruction:
            payload["system_instruction"] = {
                "parts": [{"text": system_instruction}]
            }

        response_data = await self._make_request(
            "POST",
            f"{self.BASE_URL}/models/{self.model}:generateContent",
            json_data=payload
        )

        candidates = response_data.get("candidates", [])
        if not candidates:
            raise Exception("No content generated")

        candidate = candidates[0]
        content_parts = candidate.get("content", {}).get("parts", [])
        generated_text = ""

        for part in content_parts:
            if "text" in part:
                generated_text += part["text"]

        return GenerationResponse(
            content=generated_text,
            model=self.model,
            finish_reason=candidate.get("finishReason", "STOP"),
            usage=response_data.get("usageMetadata"),
            citations=candidate.get("citationMetadata", {}).get("citations")
        )

    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_output_tokens: int = 1024
    ) -> GenerationResponse:
        """
        Send a conversation history and get a response.

        Args:
            messages: List of message dicts with 'role' and 'content'
                     (role: 'user' or 'model')
            temperature: Sampling temperature (0.0-2.0)
            max_output_tokens: Maximum tokens to generate

        Returns:
            GenerationResponse with generated content

        Raises:
            Exception: If generation fails
        """
        if not messages:
            raise ValueError("messages is required")

        contents = []
        for msg in messages:
            role = "user" if msg.get("role") == "user" else "model"
            contents.append({
                "role": role,
                "parts": [{"text": msg.get("content", "")}]
            })

        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_output_tokens
            }
        }

        response_data = await self._make_request(
            "POST",
            f"{self.BASE_URL}/models/{self.model}:generateContent",
            json_data=payload
        )

        candidates = response_data.get("candidates", [])
        if not candidates:
            raise Exception("No response generated")

        candidate = candidates[0]
        content_parts = candidate.get("content", {}).get("parts", [])
        generated_text = ""

        for part in content_parts:
            if "text" in part:
                generated_text += part["text"]

        return GenerationResponse(
            content=generated_text,
            model=self.model,
            finish_reason=candidate.get("finishReason", "STOP"),
            usage=response_data.get("usageMetadata")
        )

    # ==================== Generate Content with URL Context ====================

    async def generate_content_with_url(
        self,
        prompt: str,
        urls: List[str],
        temperature: float = 0.7,
        max_output_tokens: int = 1024
    ) -> GenerationResponse:
        """
        Generate content with context from URLs.

        Args:
            prompt: Text prompt for generation
            urls: List of URLs to fetch context from
            temperature: Sampling temperature (0.0-2.0)
            max_output_tokens: Maximum tokens to generate

        Returns:
            GenerationResponse with generated content

        Raises:
            Exception: If generation fails
            ValueError: If parameters are invalid
        """
        if not prompt:
            raise ValueError("prompt is required")
        if not urls:
            raise ValueError("urls is required")

        # Fetch context from URLs
        context_parts = []

        for url in urls:
            try:
                async with self.session.get(url) as response:
                    if response.status == 200:
                        content = await response.text()
                        context_parts.append(f"From {url}:\n{content[:2000]}")
            except Exception as e:
                context_parts.append(f"Error fetching {url}: {str(e)}")

        context = "\n\n".join(context_parts)

        full_prompt = f"""Context from provided URLs:
{context}


Based on the above context, please answer the following:
{prompt}"""

        payload = {
            "contents": [
                {
                    "parts": [{"text": full_prompt}]
                }
            ],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_output_tokens
            }
        }

        response_data = await self._make_request(
            "POST",
            f"{self.BASE_URL}/models/{self.model}:generateContent",
            json_data=payload
        )

        candidates = response_data.get("candidates", [])
        if not candidates:
            raise Exception("No content generated")

        candidate = candidates[0]
        content_parts = candidate.get("content", {}).get("parts", [])
        generated_text = ""

        for part in content_parts:
            if "text" in part:
                generated_text += part["text"]

        return GenerationResponse(
            content=generated_text,
            model=self.model,
            finish_reason=candidate.get("finishReason", "STOP"),
            usage=response_data.get("usageMetadata")
        )

    # ==================== Generate Content with File ====================

    async def generate_content_with_file(
        self,
        prompt: str,
        file_id: str,
        file_mime_type: str,
        file_data: bytes,
        temperature: float = 0.7,
        max_output_tokens: int = 1024
    ) -> GenerationResponse:
        """
        Generate content with context from an uploaded file.

        Args:
            prompt: Text prompt for generation
            file_id: File ID (from upload_file)
            file_mime_type: MIME type of the file
            file_data: File data as bytes
            temperature: Sampling temperature (0.0-2.0)
            max_output_tokens: Maximum tokens to generate

        Returns:
            GenerationResponse with generated content

        Raises:
            Exception: If generation fails
            ValueError: If parameters are invalid
        """
        if not prompt:
            raise ValueError("prompt is required")
        if not file_id:
            raise ValueError("file_id is required")

        # Prepare file part for the request
        if self.model == "gemini-pro-vision":
            # For vision model, send inline data
            encoded_data = base64.b64encode(file_data).decode("utf-8")

            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "inline_data": {
                                    "mime_type": file_mime_type,
                                    "data": encoded_data
                                }
                            },
                            {
                                "text": f"File ID: {file_id}\n\n{prompt}"
                            }
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": temperature,
                    "maxOutputTokens": max_output_tokens
                }
            }
        else:
            # For text-only model, just use the prompt with file reference
            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": f"Referencing uploaded file (ID: {file_id})\n\n{prompt}"
                            }
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": temperature,
                    "maxOutputTokens": max_output_tokens
                }
            }

        response_data = await self._make_request(
            "POST",
            f"{self.BASE_URL}/models/{self.model}:generateContent",
            json_data=payload
        )

        candidates = response_data.get("candidates", [])
        if not candidates:
            raise Exception("No content generated")

        candidate = candidates[0]
        content_parts = candidate.get("content", {}).get("parts", [])
        generated_text = ""

        for part in content_parts:
            if "text" in part:
                generated_text += part["text"]

        return GenerationResponse(
            content=generated_text,
            model=self.model,
            finish_reason=candidate.get("finishReason", "STOP"),
            usage=response_data.get("usageMetadata")
        )

    # ==================== Generate Content with Google Search ====================

    async def generate_content_with_search(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_output_tokens: int = 1024
    ) -> GenerationResponse:
        """
        Generate content using Google Search for real-time information.

        Args:
            prompt: Text prompt for generation
            temperature: Sampling temperature (0.0-2.0)
            max_output_tokens: Maximum tokens to generate

        Returns:
            GenerationResponse with generated content and citations

        Raises:
            Exception: If generation fails
            ValueError: If parameters are invalid
        """
        if not prompt:
            raise ValueError("prompt is required")

        # Use gemini-1.5-pro which has search capabilities
        search_model = "gemini-1.5-pro"

        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_output_tokens
            },
            "tools": [
                {
                    "googleSearch": {}
                }
            ]
        }

        response_data = await self._make_request(
            "POST",
            f"{self.BASE_URL}/models/{search_model}:generateContent",
            json_data=payload
        )

        candidates = response_data.get("candidates", [])
        if not candidates:
            raise Exception("No content generated")

        candidate = candidates[0]
        content_parts = candidate.get("content", {}).get("parts", [])
        generated_text = ""
        citations = []

        for part in content_parts:
            if "text" in part:
                generated_text += part["text"]

        # Extract citations if available
        citation_metadata = candidate.get("citationMetadata", {})
        if citation_metadata:
            citations = [
                citation.get("uri", "")
                for citation in citation_metadata.get("citations", [])
            ]

        return GenerationResponse(
            content=generated_text,
            model=search_model,
            finish_reason=candidate.get("finishReason", "STOP"),
            usage=response_data.get("usageMetadata"),
            citations=citations
        )

    # ==================== Upload File ====================

    async def upload_file(
        self,
        file_data: bytes,
        file_name: str,
        display_name: Optional[str] = None
    ) -> UploadedFile:
        """
        Upload a file for use with Gemini.

        Args:
            file_data: File data as bytes
            file_name: Name of the file
            display_name: Optional display name

        Returns:
            UploadedFile object with file details

        Raises:
            Exception: If upload fails
            ValueError: If parameters are invalid
        """
        if not file_data:
            raise ValueError("file_data is required")
        if not file_name:
            raise ValueError("file_name is required")

        # Determine MIME type
        import mimetypes
        mime_type, _ = mimetypes.guess_type(file_name)
        if not mime_type:
            mime_type = "application/octet-stream"

        url = f"{ self.BASE_URL}/files?key={self.api_key}"

        headers = {"Content-Type": mime_type}

        try:
            async with self.session.post(
                url,
                data=file_data,
                headers=headers,
                params={"displayName": display_name or file_name}
            ) as response:
                response_data = await response.json()

                if response.status >= 400:
                    error = response_data.get("error", {})
                    error_message = error.get("message", f"HTTP {response.status} error")
                    raise Exception(f"File upload error: {error_message}")

                return UploadedFile(
                    file_id=response_data.get("name", ""),
                    name=response_data.get("displayName", display_name or file_name),
                    mime_type=response_data.get("mimeType", mime_type),
                    size=response_data.get("sizeBytes", len(file_data)),
                    uri=response_data.get("uri", "")
                )

        except aiohttp.ClientError as e:
            raise Exception(f"Network error during upload: {str(e)}")

    # ==================== Utility Methods ====================

    async def count_tokens(
        self,
        prompt: str
    ) -> Dict[str, int]:
        """
        Count tokens in a prompt without generating content.

        Args:
            prompt: Text to count tokens for

        Returns:
            Dictionary with token counts

        Raises:
            Exception: If request fails
        """
        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ]
        }

        response_data = await self._make_request(
            "POST",
            f"{self.BASE_URL}/models/{self.model}:countTokens",
            json_data=payload
        )

        return response_data.get("totalTokens", 0)


# ==================== Example Usage ====================

async def main():
    """Example usage of Gemini client"""

    # Replace with your actual API key
    API_KEY = "your_google_cloud_api_key"

    async with GeminiClient(api_key=API_KEY, model="gemini-pro") as client:
        try:
            # Generate content
            response = await client.generate_content(
                prompt="Write a short poem about artificial intelligence",
                temperature=0.8
            )
            print(f"Generated content:\n{response.content}\n")
            print(f"Tokens used: {response.usage}")

            # Chat with conversation history
            messages = [
                {"role": "user", "content": "What is Python?"},
                {"role": "model", "content": "Python is a high-level programming language..."},
                {"role": "user", "content": "What can I build with it?"}
            ]
            chat_response = await client.chat(messages)
            print(f"Chat response:\n{chat_response.content}\n")

            # Generate content with URL context
            url_response = await client.generate_content_with_url(
                prompt="Summarize the key points from these webpages",
                urls=["https://example.com/article1", "https://example.com/article2"]
            )
            print(f"URL context response:\n{url_response.content}\n")

            # Upload a file
            file_data = b"Sample file content for demonstration"
            uploaded = await client.upload_file(
                file_data=file_data,
                file_name="sample.txt",
                display_name="Sample Document"
            )
            print(f"Uploaded file: {uploaded.file_id} ({uploaded.mime_type})")

            # Generate content with file
            file_response = await client.generate_content_with_file(
                prompt="What is this file about?",
                file_id=uploaded.file_id,
                file_mime_type=uploaded.mime_type,
                file_data=file_data
            )
            print(f"File context response:\n{file_response.content}\n")

            # Generate content with Google Search
            search_response = await client.generate_content_with_search(
                prompt="What are the latest developments in AI?"
            )
            print(f"Search response:\n{search_response.content}")
            print(f"Citations: {search_response.citations}")

        except Exception as e:
            print(f"Error: {str(e)}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())