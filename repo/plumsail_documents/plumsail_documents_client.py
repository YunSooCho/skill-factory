"""
Plumsail Documents - Document Generation API

Supports:
- Generate File
- Convert File
- Download File
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class GeneratedFile:
    """Generated file result"""
    file_id: str
    filename: str
    url: str
    size: int


class PlumsailDocumentsClient:
    """
    Plumsail Documents API client for document generation.

    API Documentation: https://plumsail.com/documents/api/
    Requires an API key from Plumsail.
    """

    BASE_URL = "https://docs.plumsail.com/api/v1"

    def __init__(self, api_key: str):
        """
        Initialize Plumsail Documents client.

        Args:
            api_key: Plumsail API key
        """
        self.api_key = api_key
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={"X-API-Key": self.api_key}
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def generate_file(
        self,
        template_id: str,
        data: Dict[str, Any],
        output_format: str = "pdf",
        filename: Optional[str] = None
    ) -> GeneratedFile:
        """
        Generate a document from a template.

        Args:
            template_id: Template ID
            data: Data to fill in template
            output_format: Output format (pdf, docx, xlsx)
            filename: Output filename (optional)

        Returns:
            GeneratedFile with file data

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "templateId": template_id,
                "data": data,
                "outputFormat": output_format
            }

            if filename:
                payload["filename"] = filename

            async with self.session.post(
                f"{self.BASE_URL}/templates/{template_id}/generate",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 201:
                    raise Exception(f"Plumsail error: {data.get('error', 'Unknown error')}")

                return GeneratedFile(
                    file_id=data["fileId"],
                    filename=data.get("filename", ""),
                    url=data["url"],
                    size=data.get("size", 0)
                )

        except Exception as e:
            raise Exception(f"Failed to generate file: {str(e)}")

    async def convert_file(
        self,
        file_url: str,
        output_format: str,
        filename: Optional[str] = None
    ) -> GeneratedFile:
        """
        Convert a file to another format.

        Args:
            file_url: URL of file to convert
            output_format: Target format (pdf, docx, xlsx, etc.)
            filename: Output filename (optional)

        Returns:
            GeneratedFile with converted file

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "fileUrl": file_url,
                "outputFormat": output_format
            }

            if filename:
                payload["filename"] = filename

            async with self.session.post(
                f"{self.BASE_URL}/convert",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 201:
                    raise Exception(f"Plumsail error: {data.get('error', 'Unknown error')}")

                return GeneratedFile(
                    file_id=data["fileId"],
                    filename=data.get("filename", ""),
                    url=data["url"],
                    size=data.get("size", 0)
                )

        except Exception as e:
            raise Exception(f"Failed to convert file: {str(e)}")

    async def download_file(self, file_id: str) -> bytes:
        """
        Download a generated file.

        Args:
            file_id: File ID

        Returns:
            File data as bytes

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            async with self.session.get(
                f"{self.BASE_URL}/files/{file_id}/download"
            ) as response:
                if response.status != 200:
                    raise Exception(f"Plumsail error: Failed to download file")

                return await response.read()

        except Exception as e:
            raise Exception(f"Failed to download file: {str(e)}")