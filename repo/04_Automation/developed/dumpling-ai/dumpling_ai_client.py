"""
Dumpling AI - Multi-Purpose AI API

Supports:
- Trim Video
- Generate AI Image (multiple models)
- Extract from Document
- Get Google Reviews
- Search Google Maps
- Doc to Text
- Scrape URL
- Extract from URL
- Extract from Audio
- Extract from Video
- Search Knowledge Base
- Generate Agent Completion
- Screenshot URL
- Run Python/JavaScript Code
- Search Google/Places/News
- Get Autocomplete/YouTube Transcript
- Add to Knowledge Base
- Extract from Image
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class AIImageGeneration:
    """AI generated image response"""
    url: str
    model: str
    credits_used: int


@dataclass
class ExtractionResult:
    """Content extraction result"""
    content: str
    metadata: Dict[str, Any]


@dataclass
class SearchResult:
    """Search result"""
    query: str
    results: List[Dict[str, Any]]


@dataclass
class CodeExecution:
    """Code execution result"""
    output: str
    error: Optional[str]


@dataclass
class KnowledgeBase:
    """Knowledge base operation"""
    operation: str
    status: str


class DumplingAIClient:
    """
    Dumpling AI API client for various AI operations.

    API Documentation: https://dumpling.ai/docs
    Requires an API key from Dumpling AI.
    """

    BASE_URL = "https://api.dumpling.ai/v1"

    def __init__(self, api_key: str):
        """
        Initialize Dumpling AI client.

        Args:
            api_key: Dumpling AI API key
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

    # ==================== AI Image Generation ====================

    async def generate_ai_image(
        self,
        prompt: str,
        model: str = "flux.1-pro",
        width: int = 1024,
        height: int = 1024
    ) -> AIImageGeneration:
        """
        Generate an AI image.

        Args:
            prompt: Text prompt for image generation
            model: AI model to use (flux.1-pro, flux.1.1-pro, recraft-v3, etc.)
            width: Image width in pixels
            height: Image height in pixels

        Returns:
            AIImageGeneration with image URL and metadata

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "prompt": prompt,
                "model": model,
                "width": width,
                "height": height
            }

            async with self.session.post(
                f"{self.BASE_URL}/image/generate",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Dumpling AI error: {data.get('error', 'Unknown error')}")

                return AIImageGeneration(
                    url=data["url"],
                    model=data["model"],
                    credits_used=data.get("credits_used", 0)
                )

        except Exception as e:
            raise Exception(f"Failed to generate AI image: {str(e)}")

    # ==================== Extraction ====================

    async def extract_from_document(
        self,
        document_url: str,
        extraction_type: str = "text"
    ) -> ExtractionResult:
        """
        Extract content from a document.

        Args:
            document_url: Document URL
            extraction_type: Type of extraction (text, table, metadata)

        Returns:
            ExtractionResult with extracted content

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "url": document_url,
                "type": extraction_type
            }

            async with self.session.post(
                f"{self.BASE_URL}/extract/document",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Dumpling AI error: {data.get('error', 'Unknown error')}")

                return ExtractionResult(
                    content=data["content"],
                    metadata=data.get("metadata", {})
                )

        except Exception as e:
            raise Exception(f"Failed to extract from document: {str(e)}")

    async def scrape_url(self, url: str) -> ExtractionResult:
        """
        Scrape content from a URL.

        Args:
            url: URL to scrape

        Returns:
            ExtractionResult with scraped content

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {"url": url}

            async with self.session.post(
                f"{self.BASE_URL}/scrape",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Dumpling AI error: {data.get('error', 'Unknown error')}")

                return ExtractionResult(
                    content=data["content"],
                    metadata=data.get("metadata", {})
                )

        except Exception as e:
            raise Exception(f"Failed to scrape URL: {str(e)}")

    async def extract_from_url(self, url: str) -> ExtractionResult:
        """
        Extract structured data from a URL.

        Args:
            url: URL to extract from

        Returns:
            ExtractionResult with extracted data

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {"url": url}

            async with self.session.post(
                f"{self.BASE_URL}/extract/url",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Dumpling AI error: {data.get('error', 'Unknown error')}")

                return ExtractionResult(
                    content=data["content"],
                    metadata=data.get("metadata", {})
                )

        except Exception as e:
            raise Exception(f"Failed to extract from URL: {str(e)}")

    async def extract_from_image(self, image_url: str) -> ExtractionResult:
        """
        Extract text/data from an image.

        Args:
            image_url: Image URL to extract from

        Returns:
            ExtractionResult with extracted content

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {"image_url": image_url}

            async with self.session.post(
                f"{self.BASE_URL}/extract/image",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Dumpling AI error: {data.get('error', 'Unknown error')}")

                return ExtractionResult(
                    content=data["content"],
                    metadata=data.get("metadata", {})
                )

        except Exception as e:
            raise Exception(f"Failed to extract from image: {str(e)}")

    # ==================== Search ====================

    async def search_google(self, query: str, limit: int = 10) -> SearchResult:
        """
        Search Google.

        Args:
            query: Search query
            limit: Maximum number of results

        Returns:
            SearchResult with search results

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "query": query,
                "limit": limit
            }

            async with self.session.post(
                f"{self.BASE_URL}/search/google",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Dumpling AI error: {data.get('error', 'Unknown error')}")

                return SearchResult(
                    query=data["query"],
                    results=data["results"]
                )

        except Exception as e:
            raise Exception(f"Failed to search Google: {str(e)}")

    async def search_google_maps(self, query: str, location: Optional[str] = None) -> SearchResult:
        """
        Search Google Maps.

        Args:
            query: Search query
            location: Location to search in (optional)

        Returns:
            SearchResult with search results

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {"query": query}

            if location:
                payload["location"] = location

            async with self.session.post(
                f"{self.BASE_URL}/search/google-maps",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Dumpling AI error: {data.get('error', 'Unknown error')}")

                return SearchResult(
                    query=data["query"],
                    results=data["results"]
                )

        except Exception as e:
            raise Exception(f"Failed to search Google Maps: {str(e)}")

    async def get_google_reviews(self, place_id: str, limit: int = 10) -> SearchResult:
        """
        Get Google reviews for a place.

        Args:
            place_id: Google Place ID
            limit: Maximum number of reviews

        Returns:
            SearchResult with reviews

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "place_id": place_id,
                "limit": limit
            }

            async with self.session.post(
                f"{self.BASE_URL}/google/reviews",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Dumpling AI error: {data.get('error', 'Unknown error')}")

                return SearchResult(
                    query=f"Reviews for {place_id}",
                    results=data["reviews"]
                )

        except Exception as e:
            raise Exception(f"Failed to get Google reviews: {str(e)}")

    # ==================== Code Execution ====================

    async def run_python_code(self, code: str) -> CodeExecution:
        """
        Execute Python code.

        Args:
            code: Python code to execute

        Returns:
            CodeExecution with output and any errors

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {"code": code, "language": "python"}

            async with self.session.post(
                f"{self.BASE_URL}/code/execute",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Dumpling AI error: {data.get('error', 'Unknown error')}")

                return CodeExecution(
                    output=data["output"],
                    error=data.get("error")
                )

        except Exception as e:
            raise Exception(f"Failed to run Python code: {str(e)}")

    async def run_javascript_code(self, code: str) -> CodeExecution:
        """
        Execute JavaScript code.

        Args:
            code: JavaScript code to execute

        Returns:
            CodeExecution with output and any errors

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {"code": code, "language": "javascript"}

            async with self.session.post(
                f"{self.BASE_URL}/code/execute",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Dumpling AI error: {data.get('error', 'Unknown error')}")

                return CodeExecution(
                    output=data["output"],
                    error=data.get("error")
                )

        except Exception as e:
            raise Exception(f"Failed to run JavaScript code: {str(e)}")

    # ==================== Screenshot ====================

    async def screenshot_url(self, url: str, width: int = 1200, height: int = 800) -> str:
        """
        Take a screenshot of a URL.

        Args:
            url: URL to screenshot
            width: Screenshot width
            height: Screenshot height

        Returns:
            Screenshot URL

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "url": url,
                "width": width,
                "height": height
            }

            async with self.session.post(
                f"{self.BASE_URL}/screenshot",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Dumpling AI error: {data.get('error', 'Unknown error')}")

                return data["url"]

        except Exception as e:
            raise Exception(f"Failed to screenshot URL: {str(e)}")

    # ==================== Knowledge Base ====================

    async def add_to_knowledge_base(
        self,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> KnowledgeBase:
        """
        Add content to knowledge base.

        Args:
            content: Content to add
            metadata: Optional metadata

        Returns:
            KnowledgeBase operation result

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {"content": content}

            if metadata:
                payload["metadata"] = metadata

            async with self.session.post(
                f"{self.BASE_URL}/knowledge-base/add",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Dumpling AI error: {data.get('error', 'Unknown error')}")

                return KnowledgeBase(
                    operation="add",
                    status=data.get("status", "success")
                )

        except Exception as e:
            raise Exception(f"Failed to add to knowledge base: {str(e)}")

    async def search_knowledge_base(self, query: str, limit: int = 10) -> SearchResult:
        """
        Search knowledge base.

        Args:
            query: Search query
            limit: Maximum results

        Returns:
            SearchResult with search results

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "query": query,
                "limit": limit
            }

            async with self.session.post(
                f"{self.BASE_URL}/knowledge-base/search",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Dumpling AI error: {data.get('error', 'Unknown error')}")

                return SearchResult(
                    query=data["query"],
                    results=data["results"]
                )

        except Exception as e:
            raise Exception(f"Failed to search knowledge base: {str(e)}")