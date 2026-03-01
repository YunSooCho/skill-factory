"""
PDF Maker - PDF Generation API

Supports:
- Create PDF
- Download PDF
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class PDFDocument:
    """PDF document representation"""
    document_id: str
    status: str
    download_url: Optional[str]


class PDFMakerClient:
    """
    PDF Maker API client for PDF generation.

    API Documentation: https://pdfmaker.com/docs/api
    Requires an API key from PDF Maker.
    """

    BASE_URL = "https://api.pdfmaker.com/v1"

    def __init__(self, api_key: str):
        """
        Initialize PDF Maker client.

        Args:
            api_key: PDF Maker API key
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

    async def create_pdf(
        self,
        template_id: str,
        data: Dict[str, Any],
        output_filename: Optional[str] = None
    ) -> PDFDocument:
        """
        Create a PDF from template.

        Args:
            template_id: Template ID to use
            data: Data to fill in template
            output_filename: Output filename (optional)

        Returns:
            PDFDocument with PDF details

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "template_id": template_id,
                "data": data
            }

            if output_filename:
                payload["output_filename"] = output_filename

            async with self.session.post(
                f"{self.BASE_URL}/pdfs",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 201:
                    raise Exception(f"PDF Maker error: {data.get('error', 'Unknown error')}")

                return PDFDocument(
                    document_id=data["document_id"],
                    status=data["status"],
                    download_url=data.get("download_url")
                )

        except Exception as e:
            raise Exception(f"Failed to create PDF: {str(e)}")

    async def download_pdf(self, document_id: str) -> bytes:
        """
        Download a PDF document.

        Args:
            document_id: Document ID

        Returns:
            PDF data as bytes

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            async with self.session.get(
                f"{self.BASE_URL}/pdfs/{document_id}/download"
            ) as response:
                if response.status != 200:
                    raise Exception(f"PDF Maker error: Failed to download PDF")

                return await response.read()

        except Exception as e:
            raise Exception(f"Failed to download PDF: {str(e)}")