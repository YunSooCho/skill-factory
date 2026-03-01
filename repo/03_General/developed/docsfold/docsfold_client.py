"""
DocsFold API - Document Generation Client

Supports:
- Download Generated File
- Generate Image
- Generate PDF
"""

import aiohttp
import json
from typing import Optional, Dict, Any, Union
from dataclasses import dataclass


@dataclass
class GenerationResult:
    """Document generation result"""
    job_id: str
    status: str
    file_url: Optional[str] = None
    file_name: Optional[str] = None
    file_size: Optional[int] = None
    created_at: Optional[str] = None


@dataclass
class DownloadResult:
    """Download result"""
    file_content: bytes
    file_name: str
    content_type: str


@dataclass
class ImageGenerationResult:
    """Image generation result"""
    job_id: str
    status: str
    image_url: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    format: Optional[str] = None


@dataclass
class PDFGenerationResult:
    """PDF generation result"""
    job_id: str
    status: str
    pdf_url: Optional[str] = None
    pages: Optional[int] = None
    file_size: Optional[int] = None


class DocsFoldClient:
    """
    DocsFold API client for document generation.

    DocsFold allows programmatic document and image generation from templates.
    
    API Documentation: https://lp.yoom.fun/apps/docsfold
    Requires an API key from DocsFold.
    """

    BASE_URL = "https://api.docsfold.com/v1"

    def __init__(self, api_key: str):
        """
        Initialize DocsFold client.

        Args:
            api_key: DocsFold API key
        """
        self.api_key = api_key
        self.session = None
        self._rate_limit_delay = 0.1  # 100ms between requests for rate limiting

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make an API request with error handling.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            params: Query parameters
            data: Form data
            json_data: JSON body data

        Returns:
            Response data as dictionary

        Raises:
            Exception: If request fails or returns error
        """
        url = f"{self.BASE_URL}{endpoint}"

        try:
            async with self.session.request(
                method,
                url,
                params=params,
                data=data,
                json=json_data
            ) as response:
                response_data = await response.json()

                if response.status != 200:
                    error_message = response_data.get("error", response_data.get("message", "Unknown error"))
                    raise Exception(
                        f"DocsFold API error (Status {response.status}): {error_message}"
                    )

                return response_data

        except aiohttp.ClientError as e:
            raise Exception(f"Network error: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON response: {str(e)}")

    # ==================== Download Generated File ====================

    async def download_generated_file(
        self,
        job_id: str,
        output_path: Optional[str] = None
    ) -> Union[bytes, DownloadResult]:
        """
        Download a generated file.

        Args:
            job_id: Job ID of the generation task
            output_path: Optional file path to save the downloaded file

        Returns:
            If output_path is provided: file bytes
            If output_path is None: DownloadResult object

        Raises:
            Exception: If download fails or job is not found
        """
        url = f"{self.BASE_URL}/files/{job_id}/download"

        try:
            async with self.session.get(url) as response:
                if response.status != 200:
                    response_text = await response.text()
                    raise Exception(f"Download failed (Status {response.status}): {response_text}")

                file_content = await response.read()
                content_type = response.headers.get("Content-Type", "application/octet-stream")

                # Get filename from Content-Disposition header if available
                content_disp = response.headers.get("Content-Disposition", "")
                file_name = job_id
                if "filename=" in content_disp:
                    file_name = content_disp.split("filename=")[-1].strip('"')

                if output_path:
                    with open(output_path, "wb") as f:
                        f.write(file_content)
                    return file_content
                else:
                    return DownloadResult(
                        file_content=file_content,
                        file_name=file_name,
                        content_type=content_type
                    )

        except aiohttp.ClientError as e:
            raise Exception(f"Network error during download: {str(e)}")

    # ==================== Generate Image ====================

    async def generate_image(
        self,
        template_id: str,
        data: Dict[str, Any],
        format: str = "png",
        width: Optional[int] = None,
        height: Optional[int] = None,
        quality: Optional[int] = None
    ) -> ImageGenerationResult:
        """
        Generate an image from a template.

        Args:
            template_id: Template ID to use for generation
            data: Dictionary of data to populate the template
            format: Image format (png, jpg, webp)
            width: Optional image width
            height: Optional image height
            quality: Optional image quality (1-100)

        Returns:
            ImageGenerationResult with job information

        Raises:
            Exception: If generation fails
            ValueError: If parameters are invalid
        """
        if format not in ["png", "jpg", "jpeg", "webp"]:
            raise ValueError(f"Invalid format: {format}. Must be png, jpg, or webp")

        if quality is not None and (quality < 1 or quality > 100):
            raise ValueError("Quality must be between 1 and 100")

        payload = {
            "template_id": template_id,
            "data": data,
            "format": format
        }

        if width:
            payload["width"] = width
        if height:
            payload["height"] = height
        if quality:
            payload["quality"] = quality

        response_data = await self._make_request(
            "POST",
            "/images/generate",
            json_data=payload
        )

        return ImageGenerationResult(
            job_id=response_data.get("job_id", ""),
            status=response_data.get("status", "processing"),
            image_url=response_data.get("image_url"),
            width=response_data.get("width"),
            height=response_data.get("height"),
            format=response_data.get("format")
        )

    # ==================== Generate PDF ====================

    async def generate_pdf(
        self,
        template_id: str,
        data: Dict[str, Any],
        output_name: Optional[str] = None,
        margin: Optional[Dict[str, float]] = None,
        page_size: Optional[str] = None,
        orientation: Optional[str] = None
    ) -> PDFGenerationResult:
        """
        Generate a PDF document from a template.

        Args:
            template_id: Template ID to use for generation
            data: Dictionary of data to populate the template
            output_name: Optional output filename
            margin: Optional margin settings (e.g., {"top": 10, "bottom": 10, "left": 10, "right": 10})
            page_size: Optional page size (a4, letter, legal)
            orientation: Optional page orientation (portrait, landscape)

        Returns:
            PDFGenerationResult with job information

        Raises:
            Exception: If generation fails
            ValueError: If parameters are invalid
        """
        if page_size and page_size.lower() not in ["a4", "letter", "legal"]:
            raise ValueError(f"Invalid page_size: {page_size}. Must be a4, letter, or legal")

        if orientation and orientation.lower() not in ["portrait", "landscape"]:
            raise ValueError(f"Invalid orientation: {orientation}. Must be portrait or landscape")

        payload = {
            "template_id": template_id,
            "data": data
        }

        if output_name:
            payload["output_name"] = output_name
        if margin:
            payload["margin"] = margin
        if page_size:
            payload["page_size"] = page_size
        if orientation:
            payload["orientation"] = orientation

        response_data = await self._make_request(
            "POST",
            "/pdfs/generate",
            json_data=payload
        )

        return PDFGenerationResult(
            job_id=response_data.get("job_id", ""),
            status=response_data.get("status", "processing"),
            pdf_url=response_data.get("pdf_url"),
            pages=response_data.get("pages"),
            file_size=response_data.get("file_size")
        )

    # ==================== Utility Methods ====================

    async def get_generation_status(self, job_id: str) -> Dict[str, Any]:
        """
        Check the status of a generation job.

        Args:
            job_id: Job ID to check

        Returns:
            Dictionary with job status information

        Raises:
            Exception: If request fails
        """
        response_data = await self._make_request(
            "GET",
            f"/jobs/{job_id}"
        )

        return {
            "job_id": response_data.get("job_id"),
            "status": response_data.get("status"),
            "progress": response_data.get("progress", 0),
            "file_url": response_data.get("file_url"),
            "error": response_data.get("error"),
            "created_at": response_data.get("created_at"),
            "completed_at": response_data.get("completed_at")
        }

    async def list_templates(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> list[Dict[str, Any]]:
        """
        List available templates.

        Args:
            limit: Maximum number of templates to return
            offset: Number of templates to skip

        Returns:
            List of template dictionaries

        Raises:
            Exception: If request fails
        """
        params = {}
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset

        response_data = await self._make_request(
            "GET",
            "/templates",
            params=params
        )

        return response_data.get("templates", [])


# ==================== Example Usage ====================

async def main():
    """Example usage of DocsFold client"""

    # Replace with your actual API key
    API_KEY = "your_docsfold_api_key"

    async with DocsFoldClient(api_key=API_KEY) as client:
        # Generate an image
        try:
            image_result = await client.generate_image(
                template_id="template_123",
                data={
                    "title": "Welcome",
                    "subtitle": "Example Document",
                    "content": "This is a sample document generation."
                },
                format="png",
                width=800,
                height=600
            )
            print(f"Image generation job: {image_result.job_id}")
            print(f"Status: {image_result.status}")

            # Check status
            status = await client.get_generation_status(image_result.job_id)
            print(f"Job status: {status}")

            # Generate a PDF
            pdf_result = await client.generate_pdf(
                template_id="pdf_template_456",
                data={
                    "company_name": "Example Corp",
                    "recipient": "John Doe",
                    "amount": 1000.00,
                    "date": "2024-02-28"
                },
                output_name="invoice.pdf",
                page_size="a4",
                orientation="portrait"
            )
            print(f"PDF generation job: {pdf_result.job_id}")
            print(f"Status: {pdf_result.status}")

            # Download generated file
            if image_result.image_url or pdf_result.pdf_url:
                # Use job_id from completed generation
                job_id = pdf_result.job_id
                download = await client.download_generated_file(job_id)
                print(f"Downloaded file: {download.file_name}")
                print(f"File size: {len(download.file_content)} bytes")

            # List templates
            templates = await client.list_templates(limit=5)
            print(f"Found {len(templates)} templates")
            for t in templates:
                print(f"  - {t.get('name', t.get('id'))}")

        except Exception as e:
            print(f"Error: {str(e)}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())