"""
Parsio - Document Parsing API

Supports:
- Upload and Parse File
- Get Parsed Data
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class ParsedData:
    """Parsed data result"""
    document_id: str
    status: str
    data: Dict[str, Any]
    tables: List[Dict[str, Any]]


class ParsioClient:
    """
    Parsio API client for document parsing.

    API Documentation: https://parsio.io/docs/api
    Requires an API key from Parsio.
    """

    BASE_URL = "https://api.parsio.io/v1"

    def __init__(self, api_key: str):
        """
        Initialize Parsio client.

        Args:
            api_key: Parsio API key
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

    async def upload_and_parse_file(
        self,
        mailbox_id: str,
        file_url: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None
    ) -> ParsedData:
        """
        Upload and parse a file.

        Args:
            mailbox_id: Mailbox ID
            file_url: URL of file to parse (optional)
            options: Additional options

        Returns:
            ParsedData with parsed results

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {"mailbox_id": mailbox_id}

            if file_url:
                payload["url"] = file_url

            if options:
                payload.update(options)

            async with self.session.post(
                f"{self.BASE_URL}/documents/parse",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 201:
                    raise Exception(f"Parsio error: {data.get('error', 'Unknown error')}")

                return ParsedData(
                    document_id=data["document_id"],
                    status=data["status"],
                    data=data.get("data", {}),
                    tables=data.get("tables", [])
                )

        except Exception as e:
            raise Exception(f"Failed to upload and parse file: {str(e)}")

    async def get_parsed_data(self, document_id: str) -> ParsedData:
        """
        Get parsed data for a document.

        Args:
            document_id: Document ID

        Returns:
            ParsedData with parsed results

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
                    raise Exception(f"Parsio error: {data.get('error', 'Unknown error')}")

                return ParsedData(
                    document_id=data["document_id"],
                    status=data["status"],
                    data=data.get("data", {}),
                    tables=data.get("tables", [])
                )

        except Exception as e:
            raise Exception(f"Failed to get parsed data: {str(e)}")