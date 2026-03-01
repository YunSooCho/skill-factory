"""
Gamma API - Document/Presentation Generation Client

Supports:
- Generate Gamma (Create documents, presentations, etc.)
- Get Generated File URL
- Get Generated File
"""

import aiohttp
import json
from typing import Optional, Dict, Any, Union
from dataclasses import dataclass


@dataclass
class GenerationResult:
    """Generation result object"""
    job_id: str
    status: str
    document_type: str
    created_at: Optional[str] = None
    completed_at: Optional[str] = None
    error: Optional[str] = None
    file_url: Optional[str] = None


@dataclass
class DocumentInfo:
    """Document information object"""
    id: str
    title: str
    type: str
    status: str
    url: Optional[str] = None
    file_size: Optional[int] = None
    pages: Optional[int] = None
    thumbnail_url: Optional[str] = None
    created_at: Optional[str] = None


@dataclass
class DownloadResult:
    """Download result object"""
    file_content: bytes
    file_name: str
    content_type: str


class GammaClient:
    """
    Gamma API client for document and presentation generation.

    Gamma is an AI-powered tool for creating documents, presentations,
    and other content. This client handles the API interactions for
    generating and retrieving content.

    API Documentation: https://lp.yoom.fun/apps/gamma
    Requires an API key from Gamma.
    """

    BASE_URL = "https://api.gamma.app/v1"

    def __init__(self, api_key: str):
        """
        Initialize Gamma client.

        Args:
            api_key: Gamma API key
        """
        self.api_key = api_key
        self.session = None
        self._rate_limit_delay = 0.1

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

                if response.status >= 400:
                    error_message = response_data.get("error", response_data.get("message", "Unknown error"))
                    raise Exception(
                        f"Gamma API error (Status {response.status}): {error_message}"
                    )

                return response_data

        except aiohttp.ClientError as e:
            raise Exception(f"Network error: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON response: {str(e)}")

    # ==================== Generate Gamma ====================

    async def generate_gamma(
        self,
        content: str,
        content_type: str = "presentation",
        title: Optional[str] = None,
        style: Optional[str] = None,
        template_id: Optional[str] = None,
        custom_metadata: Optional[Dict[str, Any]] = None
    ) -> GenerationResult:
        """
        Generate a document or presentation using Gamma.

        Args:
            content: Content prompt or structured data for generation
            content_type: Type of content to generate (presentation, document, page)
            title: Optional title for the generated content
            style: Optional style/theme identifier
            template_id: Optional template ID to use
            custom_metadata: Optional custom metadata for the document

        Returns:
            GenerationResult with job information

        Raises:
            Exception: If generation fails
            ValueError: If parameters are invalid
        """
        if not content:
            raise ValueError("content is required")

        if content_type not in ["presentation", "document", "page"]:
            raise ValueError(
                f"Invalid content_type: {content_type}. "
                "Must be presentation, document, or page"
            )

        payload = {
            "content": content,
            "type": content_type
        }

        if title:
            payload["title"] = title
        if style:
            payload["style"] = style
        if template_id:
            payload["template_id"] = template_id
        if custom_metadata:
            payload["metadata"] = custom_metadata

        response_data = await self._make_request(
            "POST",
            "/generate",
            json_data=payload
        )

        return GenerationResult(
            job_id=response_data.get("job_id", ""),
            status=response_data.get("status", "processing"),
            document_type=response_data.get("type", content_type),
            created_at=response_data.get("created_at"),
            completed_at=response_data.get("completed_at"),
            error=response_data.get("error"),
            file_url=response_data.get("file_url")
        )

    async def generate_from_template(
        self,
        template_id: str,
        data: Dict[str, Any],
        title: Optional[str] = None
    ) -> GenerationResult:
        """
        Generate content from a predefined template.

        Args:
            template_id: Template identifier
            data: Data to populate the template
            title: Optional title for the generated content

        Returns:
            GenerationResult with job information

        Raises:
            Exception: If generation fails
            ValueError: If template_id or data is invalid
        """
        if not template_id:
            raise ValueError("template_id is required")
        if not data:
            raise ValueError("data is required")

        payload = {
            "template_id": template_id,
            "data": data
        }

        if title:
            payload["title"] = title

        response_data = await self._make_request(
            "POST",
            "/generate/from-template",
            json_data=payload
        )

        return GenerationResult(
            job_id=response_data.get("job_id", ""),
            status=response_data.get("status", "processing"),
            document_type=response_data.get("type", "document"),
            created_at=response_data.get("created_at"),
            completed_at=response_data.get("completed_at"),
            error=response_data.get("error"),
            file_url=response_data.get("file_url")
        )

    # ==================== Get Generated File URL ====================

    async def get_generated_file_url(self, job_id: str) -> str:
        """
        Get the URL of a generated file.

        Args:
            job_id: Job ID from a previous generation request

        Returns:
            File URL string

        Raises:
            Exception: If request fails or job is not found/ready
            ValueError: If job_id is empty
        """
        if not job_id:
            raise ValueError("job_id is required")

        response_data = await self._make_request(
            "GET",
            f"/jobs/{job_id}/url"
        )

        file_url = response_data.get("url")

        if not file_url:
            raise Exception("File URL not available - job may still be processing")

        return file_url

    async def get_document_info(self, job_id: str) -> DocumentInfo:
        """
        Get detailed information about a generated document.

        Args:
            job_id: Job ID or document ID

        Returns:
            DocumentInfo object with document details

        Raises:
            Exception: If request fails
        """
        response_data = await self._make_request(
            "GET",
            f"/documents/{job_id}"
        )

        return DocumentInfo(
            id=response_data.get("id", ""),
            title=response_data.get("title", ""),
            type=response_data.get("type", ""),
            status=response_data.get("status", ""),
            url=response_data.get("url"),
            file_size=response_data.get("file_size"),
            pages=response_data.get("pages"),
            thumbnail_url=response_data.get("thumbnail_url"),
            created_at=response_data.get("created_at")
        )

    # ==================== Get Generated File ====================

    async def get_generated_file(
        self,
        job_id: str,
        output_path: Optional[str] = None
    ) -> Union[bytes, DownloadResult]:
        """
        Download a generated file.

        Args:
            job_id: Job ID from a previous generation request
            output_path: Optional file path to save the downloaded file

        Returns:
            If output_path is provided: file bytes
            If output_path is None: DownloadResult object

        Raises:
            Exception: If download fails or job is not found
            ValueError: If job_id is empty
        """
        if not job_id:
            raise ValueError("job_id is required")

        url = f"{self.BASE_URL}/files/{job_id}/download"

        try:
            async with self.session.get(url) as response:
                if response.status != 200:
                    response_text = await response.text()
                    raise Exception(
                        f"Download failed (Status {response.status}): {response_text}"
                    )

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

    # ==================== Utility Methods ====================

    async def get_job_status(self, job_id: str) -> Dict[str, Any]:
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

    async def list_documents(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        status: Optional[str] = None
    ) -> list[DocumentInfo]:
        """
        List generated documents.

        Args:
            limit: Maximum number of documents to return
            offset: Number of documents to skip
            status: Filter by status (completed, processing, failed)

        Returns:
            List of DocumentInfo objects

        Raises:
            Exception: If request fails
        """
        params = {}

        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if status:
            params["status"] = status

        response_data = await self._make_request(
            "GET",
            "/documents",
            params=params
        )

        documents_list = response_data.get("documents", [])

        return [
            DocumentInfo(
                id=doc.get("id", ""),
                title=doc.get("title", ""),
                type=doc.get("type", ""),
                status=doc.get("status", ""),
                url=doc.get("url"),
                file_size=doc.get("file_size"),
                pages=doc.get("pages"),
                thumbnail_url=doc.get("thumbnail_url"),
                created_at=doc.get("created_at")
            )
            for doc in documents_list
        ]

    async def delete_document(self, document_id: str) -> None:
        """
        Delete a generated document.

        Args:
            document_id: Document ID to delete

        Raises:
            Exception: If deletion fails
            ValueError: If document_id is empty
        """
        if not document_id:
            raise ValueError("document_id is required")

        await self._make_request(
            "DELETE",
            f"/documents/{document_id}"
        )


# ==================== Example Usage ====================

async def main():
    """Example usage of Gamma client"""

    # Replace with your actual API key
    API_KEY = "your_gamma_api_key"

    async with GammaClient(api_key=API_KEY) as client:
        try:
            # Generate a presentation
            generation = await client.generate_gamma(
                content="Create a presentation about artificial intelligence",
                content_type="presentation",
                title="AI Overview",
                style="modern"
            )
            print(f"Generation job: {generation.job_id}")
            print(f"Status: {generation.status}")

            # Check job status
            status = await client.get_job_status(generation.job_id)
            print(f"Job progress: {status.get('progress', 0)}%")

            # Get file URL
            file_url = await client.get_generated_file_url(generation.job_id)
            print(f"File URL: {file_url}")

            # Get document info
            doc_info = await client.get_document_info(generation.job_id)
            print(f"Document: {doc_info.title} ({doc_info.type})")

            # Download file
            download = await client.get_generated_file(generation.job_id)
            print(f"Downloaded: {download.file_name} ({len(download.file_content)} bytes)")

            # Generate from template
            if status["status"] == "completed":
                template_generation = await client.generate_from_template(
                    template_id="template_123",
                    data={
                        "company": "Example Corp",
                        "topic": "Q4 Results",
                        "key_points": ["Revenue growth", "New customers", "Expansion"]
                    },
                    title="Q4 2024 Results"
                )
                print(f"Template generation job: {template_generation.job_id}")

            # List documents
            documents = await client.list_documents(limit=10)
            print(f"Total documents: {len(documents)}")
            for doc in documents[:3]:
                print(f"  - {doc.title} ({doc.status})")

        except Exception as e:
            print(f"Error: {str(e)}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())