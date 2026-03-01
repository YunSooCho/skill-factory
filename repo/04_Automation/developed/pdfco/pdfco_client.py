"""
PDFco - PDF Processing API

Supports comprehensive PDF operations: convert, merge, split, encrypt, etc.
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class ProcessedPDF:
    """Processed PDF result"""
    url: str
    filename: str
    pages: int


@dataclass
class UploadedFile:
    """Uploaded file result"""
    file_id: str
    url: str
    size: int


class PDFCoClient:
    """
    PDFco API client for PDF processing.

    API Documentation: https://apidocs.pdf.co
    Requires an API key from PDFco.
    """

    BASE_URL = "https://api.pdf.co/v1"

    def __init__(self, api_key: str):
        """
        Initialize PDFco client.

        Args:
            api_key: PDFco API key
        """
        self.api_key = api_key
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def _get_params(self, **kwargs) -> Dict[str, str]:
        """Get params with API key"""
        params = {"x-api-key": self.api_key}
        params.update(kwargs)
        return params

    async def upload_file(
        self,
        file_url: Optional[str] = None,
        file_data: Optional[bytes] = None,
        filename: Optional[str] = None
    ) -> UploadedFile:
        """
        Upload a file for processing.

        Args:
            file_url: Remote file URL (optional)
            file_data: File data as bytes (optional)
            filename: Filename (optional)

        Returns:
            UploadedFile with file details

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            params = self._get_params()

            if file_url:
                params["url"] = file_url
                async with self.session.post(
                    f"{self.BASE_URL}/file/upload/get-presigned-url",
                    params=params
                ) as response:
                    data = await response.json()
                    if response.status != 200 or data.get("error"):
                        raise Exception(f"PDFco error: {data.get('message', 'Unknown error')}")
                    return UploadedFile(
                        file_id=data["presignedUrl"],
                        url=data["url"],
                        size=0
                    )

        except Exception as e:
            raise Exception(f"Failed to upload file: {str(e)}")

    async def convert_pdf_to_excel(self, pdf_url: str) -> ProcessedPDF:
        """
        Convert PDF to Excel.

        Args:
            pdf_url: PDF file URL

        Returns:
            ProcessedPDF with Excel file

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "url": pdf_url,
                "pages": "-1"
            }

            params = self._get_params()

            async with self.session.post(
                f"{self.BASE_URL}/pdf/convert/to/xlsx",
                params=params,
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200 or data.get("error"):
                    raise Exception(f"PDFco error: {data.get('message', 'Unknown error')}")

                return ProcessedPDF(
                    url=data["url"],
                    filename=data.get("filename", ""),
                    pages=data.get("pages", 0)
                )

        except Exception as e:
            raise Exception(f"Failed to convert PDF to Excel: {str(e)}")

    async def convert_pdf_to_text(self, pdf_url: str) -> str:
        """
        Convert PDF to text.

        Args:
            pdf_url: PDF file URL

        Returns:
            Extracted text

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "url": pdf_url,
                "pages": "-1"
            }

            params = self._get_params()

            async with self.session.post(
                f"{self.BASE_URL}/pdf/convert/to/text",
                params=params,
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200 or data.get("error"):
                    raise Exception(f"PDFco error: {data.get('message', 'Unknown error')}")

                return data.get("body", "")

        except Exception as e:
            raise Exception(f"Failed to convert PDF to text: {str(e)}")

    async def split_pdf(
        self,
        pdf_url: str,
        ranges: str
    ) -> ProcessedPDF:
        """
        Split a PDF by page ranges.

        Args:
            pdf_url: PDF file URL
            ranges: Page ranges (e.g., "1-3,5,7-9")

        Returns:
            ProcessedPDF with split PDF

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "url": pdf_url,
                "ranges": ranges
            }

            params = self._get_params()

            async with self.session.post(
                f"{self.BASE_URL}/pdf/split",
                params=params,
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200 or data.get("error"):
                    raise Exception(f"PDFco error: {data.get('message', 'Unknown error')}")

                return ProcessedPDF(
                    url=data["url"],
                    filename=data.get("filename", ""),
                    pages=data.get("pages", 0)
                )

        except Exception as e:
            raise Exception(f"Failed to split PDF: {str(e)}")

    async def merge_pdfs(self, pdf_urls: list) -> ProcessedPDF:
        """
        Merge multiple PDFs into one.

        Args:
            pdf_urls: List of PDF URLs to merge

        Returns:
            ProcessedPDF with merged PDF

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "url": ",".join(pdf_urls)
            }

            params = self._get_params()

            async with self.session.post(
                f"{self.BASE_URL}/pdf/merge",
                params=params,
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200 or data.get("error"):
                    raise Exception(f"PDFco error: {data.get('message', 'Unknown error')}")

                return ProcessedPDF(
                    url=data["url"],
                    filename=data.get("filename", ""),
                    pages=data.get("pages", 0)
                )

        except Exception as e:
            raise Exception(f"Failed to merge PDFs: {str(e)}")

    async def convert_url_to_pdf(self, url: str) -> ProcessedPDF:
        """
        Convert a URL to PDF.

        Args:
            url: Webpage URL

        Returns:
            ProcessedPDF with PDF

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "url": url,
                "margins": "10px 10px 10px 10px"
            }

            params = self._get_params()

            async with self.session.post(
                f"{self.BASE_URL}/pdf/convert/from/url",
                params=params,
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200 or data.get("error"):
                    raise Exception(f"PDFco error: {data.get('message', 'Unknown error')}")

                return ProcessedPDF(
                    url=data["url"],
                    filename=data.get("filename", ""),
                    pages=data.get("pages", 1)
                )

        except Exception as e:
            raise Exception(f"Failed to convert URL to PDF: {str(e)}")

    async def html_to_pdf(
        self,
        html: str,
        page_size: str = "A4"
    ) -> ProcessedPDF:
        """
        Convert HTML to PDF.

        Args:
            html: HTML content
            page_size: Page size (A4, Letter, etc.)

        Returns:
            ProcessedPDF with PDF

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "html": html,
                "pageSize": page_size
            }

            params = self._get_params()

            async with self.session.post(
                f"{self.BASE_URL}/pdf/convert/from/html",
                params=params,
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200 or data.get("error"):
                    raise Exception(f"PDFco error: {data.get('message', 'Unknown error')}")

                return ProcessedPDF(
                    url=data["url"],
                    filename=data.get("filename", ""),
                    pages=data.get("pages", 1)
                )

        except Exception as e:
            raise Exception(f"Failed to convert HTML to PDF: {str(e)}")