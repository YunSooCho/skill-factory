"""
Parseur - Document Parsing API

Supports:
- Upload Document
- Create Mailbox
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class ParsedDocument:
    """Parsed document result"""
    document_id: str
    mailbox_id: str
    status: str
    parsed_data: Dict[str, Any]
    url: Optional[str]


@dataclass
class Mailbox:
    """Mailbox representation"""
    mailbox_id: str
    name: str
    email: str
    created_at: str


class ParseurClient:
    """
    Parseur API client for document parsing.

    API Documentation: https://parseur.com/docs/api
    Requires an API key from Parseur.
    """

    BASE_URL = "https://api.parseur.com/v1"

    def __init__(self, api_key: str):
        """
        Initialize Parseur client.

        Args:
            api_key: Parseur API key
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

    async def create_mailbox(
        self,
        name: str,
        options: Optional[Dict[str, Any]] = None
    ) -> Mailbox:
        """
        Create a new mailbox.

        Args:
            name: Mailbox name
            options: Additional options

        Returns:
            Mailbox with mailbox data

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {"name": name}

            if options:
                payload.update(options)

            async with self.session.post(
                f"{self.BASE_URL}/mailboxes",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 201:
                    raise Exception(f"Parseur error: {data.get('error', 'Unknown error')}")

                return Mailbox(
                    mailbox_id=data["mailbox_id"],
                    name=data["name"],
                    email=data.get("email", ""),
                    created_at=data.get("created_at", "")
                )

        except Exception as e:
            raise Exception(f"Failed to create mailbox: {str(e)}")

    async def upload_document(
        self,
        mailbox_id: str,
        document_url: Optional[str] = None,
        file_data: Optional[bytes] = None
    ) -> ParsedDocument:
        """
        Upload a document for parsing.

        Args:
            mailbox_id: Mailbox ID
            document_url: URL of document (optional)
            file_data: File data as bytes (optional)

        Returns:
            ParsedDocument with parsed data

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {"mailbox_id": mailbox_id}

            if document_url:
                payload["url"] = document_url

            async with self.session.post(
                f"{self.BASE_URL}/documents",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 201:
                    raise Exception(f"Parseur error: {data.get('error', 'Unknown error')}")

                return ParsedDocument(
                    document_id=data["document_id"],
                    mailbox_id=data["mailbox_id"],
                    status=data["status"],
                    parsed_data=data.get("parsed_data", {}),
                    url=data.get("url")
                )

        except Exception as e:
            raise Exception(f"Failed to upload document: {str(e)}")