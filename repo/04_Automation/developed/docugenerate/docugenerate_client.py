"""
Docugenerate - Document Generation API

Supports:
- Get Document
- List Documents
- Download Document
- Create Document
- Update Document
- Delete Document
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Document:
    """Document representation"""
    id: str
    name: str
    status: str
    template_id: str
    created_at: str
    updated_at: str
    download_url: Optional[str]


@dataclass
class DocumentList:
    """List of documents"""
    documents: List[Document]
    total: int
    page: int


class DocugenerateClient:
    """
    Docugenerate API client for document generation.

    API Documentation: https://www.docugenerate.com/docs/api
    Requires an API key from Docugenerate.
    """

    BASE_URL = "https://api.docugenerate.com/v1"

    def __init__(self, api_key: str):
        """
        Initialize Docugenerate client.

        Args:
            api_key: Docugenerate API key
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
        name: Optional[str] = None,
        output_format: str = "pdf"
    ) -> Document:
        """
        Create a new document from a template.

        Args:
            template_id: Template ID to use
            data: Data to fill in template
            name: Document name (optional)
            output_format: Output format (pdf, docx, html)

        Returns:
            Document with created document data

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "template_id": template_id,
                "data": data,
                "format": output_format
            }

            if name:
                payload["name"] = name

            async with self.session.post(
                f"{self.BASE_URL}/documents",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 201:
                    raise Exception(f"Docugenerate API error: {data.get('error', 'Unknown error')}")

                return Document(
                    id=data["id"],
                    name=data.get("name", ""),
                    status=data["status"],
                    template_id=data["template_id"],
                    created_at=data["created_at"],
                    updated_at=data["updated_at"],
                    download_url=data.get("download_url")
                )

        except Exception as e:
            raise Exception(f"Failed to create document: {str(e)}")

    async def get_document(self, document_id: str) -> Document:
        """
        Get details of a specific document.

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
                    raise Exception(f"Docugenerate API error: {data.get('error', 'Unknown error')}")

                return Document(
                    id=data["id"],
                    name=data.get("name", ""),
                    status=data["status"],
                    template_id=data["template_id"],
                    created_at=data["created_at"],
                    updated_at=data["updated_at"],
                    download_url=data.get("download_url")
                )

        except Exception as e:
            raise Exception(f"Failed to get document: {str(e)}")

    async def list_documents(
        self,
        template_id: Optional[str] = None,
        status: Optional[str] = None,
        page: int = 1,
        limit: int = 20
    ) -> DocumentList:
        """
        List all documents.

        Args:
            template_id: Filter by template ID (optional)
            status: Filter by status (optional)
            page: Page number
            limit: Items per page

        Returns:
            DocumentList with documents

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            params = {}
            if template_id:
                params["template_id"] = template_id
            if status:
                params["status"] = status
            params["page"] = page
            params["limit"] = limit

            async with self.session.get(
                f"{self.BASE_URL}/documents",
                params=params
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Docugenerate API error: {data.get('error', 'Unknown error')}")

                documents = [
                    Document(
                        id=doc["id"],
                        name=doc.get("name", ""),
                        status=doc["status"],
                        template_id=doc["template_id"],
                        created_at=doc["created_at"],
                        updated_at=doc["updated_at"],
                        download_url=doc.get("download_url")
                    )
                    for doc in data.get("documents", [])
                ]

                return DocumentList(
                    documents=documents,
                    total=data.get("total", 0),
                    page=data.get("page", 1)
                )

        except Exception as e:
            raise Exception(f"Failed to list documents: {str(e)}")

    async def update_document(
        self,
        document_id: str,
        data: Optional[Dict[str, Any]] = None,
        name: Optional[str] = None
    ) -> Document:
        """
        Update a document.

        Args:
            document_id: Document ID
            data: New data to fill in template (optional)
            name: New document name (optional)

        Returns:
            Document with updated data

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {}
            if data:
                payload["data"] = data
            if name:
                payload["name"] = name

            async with self.session.patch(
                f"{self.BASE_URL}/documents/{document_id}",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Docugenerate API error: {data.get('error', 'Unknown error')}")

                return Document(
                    id=data["id"],
                    name=data.get("name", ""),
                    status=data["status"],
                    template_id=data["template_id"],
                    created_at=data["created_at"],
                    updated_at=data["updated_at"],
                    download_url=data.get("download_url")
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
                    raise Exception(f"Docugenerate API error: {data.get('error', 'Unknown error')}")

                return True

        except Exception as e:
            raise Exception(f"Failed to delete document: {str(e)}")

    async def download_document(self, document_id: str) -> bytes:
        """
        Download a document as bytes.

        Args:
            document_id: Document ID

        Returns:
            Document data as bytes

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            async with self.session.get(
                f"{self.BASE_URL}/documents/{document_id}/download"
            ) as response:
                if response.status != 200:
                    raise Exception(f"Docugenerate API error: Failed to download document")

                return await response.read()

        except Exception as e:
            raise Exception(f"Failed to download document: {str(e)}")