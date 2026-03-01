"""
PDFmonkey - PDF Generation API

Supports:
- Create a Document
- Download a Document
- Get Document Data
- Update a Document
- Delete a Document
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class Document:
    """Document representation"""
    id: str
    status: str
    download_url: Optional[str]
    template_id: str
    created_at: str


class PDFMonkeyClient:
    """
    PDFMonkey API client for PDF generation.

    API Documentation: https://developers.pdfmonkey.io
    Requires an API key from PDFMonkey.
    """

    BASE_URL = "https://api.pdfmonkey.io/api/v1"

    def __init__(self, api_key: str):
        """
        Initialize PDFMonkey client.

        Args:
            api_key: PDFMonkey API key
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

    async def create_document(
        self,
        template_id: str,
        data: Dict[str, Any],
        filename: Optional[str] = None,
        meta: Optional[Dict[str, Any]] = None
    ) -> Document:
        """
        Create a new document from a template.

        Args:
            template_id: Template ID
            data: Data to fill in template
            filename: Output filename (optional)
            meta: Custom metadata (optional)

        Returns:
            Document with document data

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "document": {
                    "document_template_id": template_id,
                    "payload": data
                }
            }

            if filename:
                payload["document"]["filename"] = filename
            if meta:
                payload["document"]["meta"] = meta

            async with self.session.post(
                f"{self.BASE_URL}/documents",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 201:
                    raise Exception(f"PDFMonkey error: {data.get('error', 'Unknown error')}")

                return Document(
                    id=data["document"]["id"],
                    status=data["document"]["status"],
                    download_url=data["document"].get("download_url"),
                    template_id=data["document"]["document_template_id"],
                    created_at=data["document"]["created_at"]
                )

        except Exception as e:
            raise Exception(f"Failed to create document: {str(e)}")

    async def get_document(self, document_id: str) -> Document:
        """
        Get document details.

        Args:
            document_id: Document ID

        Returns:
            Document with document data

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            async with self.session.get(
                f"{self.BASE_URL}/documents/{document_id}"
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"PDFMonkey error: {data.get('error', 'Unknown error')}")

                return Document(
                    id=data["document"]["id"],
                    status=data["document"]["status"],
                    download_url=data["document"].get("download_url"),
                    template_id=data["document"]["document_template_id"],
                    created_at=data["document"]["created_at"]
                )

        except Exception as e:
            raise Exception(f"Failed to get document: {str(e)}")

    async def update_document(
        self,
        document_id: str,
        data: Optional[Dict[str, Any]] = None,
        meta: Optional[Dict[str, Any]] = None
    ) -> Document:
        """
        Update a document.

        Args:
            document_id: Document ID
            data: New data (optional)
            meta: New metadata (optional)

        Returns:
            Document with updated data

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {"document": {}}

            if data:
                payload["document"]["payload"] = data
            if meta:
                payload["document"]["meta"] = meta

            async with self.session.put(
                f"{self.BASE_URL}/documents/{document_id}",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"PDFMonkey error: {data.get('error', 'Unknown error')}")

                return Document(
                    id=data["document"]["id"],
                    status=data["document"]["status"],
                    download_url=data["document"].get("download_url"),
                    template_id=data["document"]["document_template_id"],
                    created_at=data["document"]["created_at"]
                )

        except Exception as e:
            raise Exception(f"Failed to update document: {str(e)}")

    async def delete_document(self, document_id: str) -> bool:
        """
        Delete a document.

        Args:
            document_id: Document ID

        Returns:
            True if successful

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            async with self.session.delete(
                f"{self.BASE_URL}/documents/{document_id}"
            ) as response:
                if response.status != 204:
                    data = await response.json()
                    raise Exception(f"PDFMonkey error: {data.get('error', 'Unknown error')}")

                return True

        except Exception as e:
            raise Exception(f"Failed to delete document: {str(e)}")

    async def download_document(self, document_id: str) -> bytes:
        """
        Download a document.

        Args:
            document_id: Document ID

        Returns:
            Document data as bytes

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            doc = await self.get_document(document_id)

            if not doc.download_url:
                raise Exception("Document download URL not available")

            async with self.session.get(doc.download_url) as response:
                if response.status != 200:
                    raise Exception(f"Failed to download document")

                return await response.read()

        except Exception as e:
            raise Exception(f"Failed to download document: {str(e)}")