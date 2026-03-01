"""
Abyssale API - Content Generation Client

Supports:
- Generate Content (banners, images, content)
- Get File (download generated content)
Trigger:
- New Generation (webhook notifications)
"""

import aiohttp
import asyncio
import hashlib
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class GenerationRequest:
    """Content generation request"""
    template_id: str
    format: str = "jpg"
    elements: Optional[Dict[str, Any]] = None
    async: bool = False
    transparent: bool = False
    webhook_url: Optional[str] = None


@dataclass
class GenerationResponse:
    """Content generation response"""
    generation_id: str
    status: str
    url: Optional[str] = None
    error: Optional[str] = None
    created_at: str = ""


@dataclass
class FileInfo:
    """File information response"""
    file_id: str
    name: str
    mime_type: str
    size: int
    url: str
    created_at: str


class AbyssaleClient:
    """
    Abyssale API client for content generation.

    API Documentation: https://api.abyssale.com/docs
    Uses API key for authentication.
    """

    BASE_URL = "https://api.abyssale.com"
    API_VERSION = "v1"

    def __init__(self, api_key: str):
        """
        Initialize Abyssale client.

        Args:
            api_key: Abyssale API key
        """
        self.api_key = api_key
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers={
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        })
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def _get_url(self, endpoint: str) -> str:
        """Build full API URL"""
        return f"{self.BASE_URL}/{self.API_VERSION}/{endpoint}"

    # ==================== Content Generation ====================

    async def generate_content(
        self,
        template_id: str,
        format: str = "jpg",
        elements: Optional[Dict[str, Any]] = None,
        async_mode: bool = False,
        transparent: bool = False,
        webhook_url: Optional[str] = None
    ) -> GenerationResponse:
        """
        Generate content using a template.

        Args:
            template_id: Template ID to use
            format: Output format (jpg, png, mp4)
            elements: Template elements to customize
            async_mode: Whether to process asynchronously
            transparent: Whether to make background transparent
            webhook_url: Webhook URL for async completion notification

        Returns:
            GenerationResponse with generation ID and status

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If network error occurs
        """
        payload = {
            "template_id": template_id,
            "format": format,
            "transparent": transparent,
        }

        if elements:
            payload["elements"] = elements

        if async_mode:
            payload["async"] = True
            if webhook_url:
                payload["webhook_url"] = webhook_url

        async with self.session.post(
            self._get_url("generations"),
            json=payload
        ) as response:
            data = await response.json()

            if response.status not in (200, 201, 202):
                raise Exception(f"Content generation failed: {data}")

            return GenerationResponse(
                generation_id=data.get("id", data.get("generation_id", "")),
                status=data.get("status", "pending"),
                url=data.get("url"),
                error=data.get("error"),
                created_at=datetime.utcnow().isoformat()
            )

    async def get_generation_status(self, generation_id: str) -> GenerationResponse:
        """
        Check the status of a generation request.

        Args:
            generation_id: Generation ID from generate_content

        Returns:
            GenerationResponse with updated status

        Raises:
            ValueError: If generation not found
            aiohttp.ClientError: If network error occurs
        """
        async with self.session.get(
            self._get_url(f"generations/{generation_id}")
        ) as response:
            data = await response.json()

            if response.status != 200:
                raise Exception(f"Failed to get generation status: {data}")

            return GenerationResponse(
                generation_id=data.get("id", generation_id),
                status=data.get("status", "unknown"),
                url=data.get("url"),
                error=data.get("error"),
                created_at=data.get("created_at", "")
            )

    # ==================== File Operations ====================

    async def get_file(self, generation_id: str) -> FileInfo:
        """
        Get information about a generated file.

        Args:
            generation_id: Generation ID to retrieve file info

        Returns:
            FileInfo with file details

        Raises:
            ValueError: If file not found
            aiohttp.ClientError: If network error occurs
        """
        async with self.session.get(
            self._get_url(f"generations/{generation_id}/file")
        ) as response:
            data = await response.json()

            if response.status != 200:
                raise Exception(f"Failed to get file info: {data}")

            return FileInfo(
                file_id=data.get("id", data.get("generation_id", generation_id)),
                name=data.get("name", f"generated_{generation_id}"),
                mime_type=data.get("mime_type", "image/jpeg"),
                size=data.get("size", 0),
                url=data.get("url", ""),
                created_at=data.get("created_at", "")
            )

    async def download_file(
        self,
        generation_id: str,
        output_path: Optional[str] = None
    ) -> bytes:
        """
        Download generated file content.

        Args:
            generation_id: Generation ID to download
            output_path: Optional file path to save download

        Returns:
            Binary content of the file

        Raises:
            ValueError: If file not found or download fails
            aiohttp.ClientError: If network error occurs
        """
        file_info = await self.get_file(generation_id)

        if not file_info.url:
            raise ValueError("No download URL available for this file")

        async with self.session.get(file_info.url) as response:
            if response.status != 200:
                raise Exception(f"Failed to download file: {response.status}")

            content = await response.read()

            if output_path:
                with open(output_path, 'wb') as f:
                    f.write(content)

            return content

    # ==================== Template Operations ====================

    async def list_templates(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """
        List available templates.

        Args:
            limit: Number of templates to return
            offset: Pagination offset

        Returns:
            List of template dictionaries

        Raises:
            aiohttp.ClientError: If network error occurs
        """
        params = {
            "limit": limit,
            "offset": offset
        }

        async with self.session.get(
            self._get_url("templates"),
            params=params
        ) as response:
            data = await response.json()

            if response.status != 200:
                raise Exception(f"Failed to list templates: {data}")

            return data.get("data", data.get("templates", []))

    async def get_template(self, template_id: str) -> Dict[str, Any]:
        """
        Get template details.

        Args:
            template_id: Template ID to retrieve

        Returns:
            Template details dictionary

        Raises:
            ValueError: If template not found
            aiohttp.ClientError: If network error occurs
        """
        async with self.session.get(
            self._get_url(f"templates/{template_id}")
        ) as response:
            data = await response.json()

            if response.status != 200:
                raise Exception(f"Failed to get template: {data}")

            return data

    # ==================== Webhook Support ====================

    @staticmethod
    def verify_webhook_signature(
        payload: bytes,
        signature: str,
        webhook_secret: str
    ) -> bool:
        """
        Verify webhook signature for security.

        Args:
            payload: Raw webhook payload bytes
            signature: Signature from X-Webhook-Signature header
            webhook_secret: Your webhook secret key

        Returns:
            True if signature is valid
        """
        expected_signature = hashlib.sha256(
            webhook_secret.encode() + payload
        ).hexdigest()

        return signature == expected_signature

    def handle_webhook_event(self, event_data: Dict[str, Any]) -> str:
        """
        Process webhook event data.

        Args:
            event_data: Webhook event payload

        Returns:
            Event type string (e.g., "generation.completed")
        """
        return event_data.get("event", event_data.get("type", "unknown"))


# ==================== Example Usage ====================

async def main():
    """Example usage of Abyssale client"""

    # Example configuration - replace with your actual API key
    api_key = "your_abyssale_api_key"

    async with AbyssaleClient(api_key=api_key) as client:
        # List available templates
        templates = await client.list_templates(limit=10)
        print(f"Found {len(templates)} templates")
        for t in templates[:3]:  # Show first 3
            print(f"  - {t.get('name', 'Unknown')} (ID: {t.get('id', 'Unknown')})")

        # Generate content using a template
        template_id = templates[0].get("id") if templates else "example_template_id"

        generation = await client.generate_content(
            template_id=template_id,
            format="jpg",
            elements={
                "title": "Hello World",
                "subtitle": "Generated with Abyssale API"
            },
            async_mode=False
        )
        print(f"Generation ID: {generation.generation_id}")
        print(f"Status: {generation.status}")

        # Get file info
        if generation.status == "completed":
            file_info = await client.get_file(generation.generation_id)
            print(f"File: {file_info.name} ({file_info.mime_type})")
            print(f"URL: {file_info.url}")

            # Download file
            content = await client.download_file(generation.generation_id)
            print(f"Downloaded {len(content)} bytes")

        # Check async generation status
        if generation.status == "pending":
            await asyncio.sleep(2)  # Wait for generation
            status = await client.get_generation_status(generation.generation_id)
            print(f"Updated status: {status.status}")


if __name__ == "__main__":
    asyncio.run(main())