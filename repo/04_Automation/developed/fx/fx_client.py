"""
FX - File Transformation and Processing API

Supports:
- Decrypt PDF
- Generate Image from Text
- Encrypt ZIP
- Check if Date is Holiday
- Convert CSV to Array
- Generate QR Code
- Render HTML to Image
- Split PDF
- Resize Image
- Overlay Image on Background
- Image Scaling
- Extract Audio
- Encrypt PDF
- Render HTML/URL to Image
- Decrypt ZIP
- Add Watermark to PDF
- Upload Asset File
- Convert Asset URL to Base64
- Convert Timezone
- Convert Office to PDF
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class ProcessedFile:
    """Processed file result"""
    url: str
    filename: str
    mime_type: str
    size: int


@dataclass
class ImageResult:
    """Image processing result"""
    url: str
    width: int
    height: int
    format: str


@dataclass
class AssetUpload:
    """Asset upload result"""
    asset_id: str
    url: str
    size: int


class FXClient:
    """
    FX API client for file transformation and processing.

    API Documentation: https://fx.api.com/docs
    Requires an API key from FX.
    """

    BASE_URL = "https://api.fx.com/v1"

    def __init__(self, api_key: str):
        """
        Initialize FX client.

        Args:
            api_key: FX API key
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

    # ==================== PDF Operations ====================

    async def encrypt_pdf(
        self,
        file_url: str,
        password: str,
        output_filename: Optional[str] = None
    ) -> ProcessedFile:
        """
        Encrypt a PDF file with a password.

        Args:
            file_url: URL of the PDF file
            password: Password to protect the PDF
            output_filename: Output filename (optional)

        Returns:
            ProcessedFile with encrypted PDF

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "file_url": file_url,
                "password": password
            }

            if output_filename:
                payload["output_filename"] = output_filename

            async with self.session.post(
                f"{self.BASE_URL}/pdf/encrypt",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"FX error: {data.get('error', 'Unknown error')}")

                return ProcessedFile(
                    url=data["url"],
                    filename=data["filename"],
                    mime_type=data["mime_type"],
                    size=data["size"]
                )

        except Exception as e:
            raise Exception(f"Failed to encrypt PDF: {str(e)}")

    async def decrypt_pdf(
        self,
        file_url: str,
        password: str,
        output_filename: Optional[str] = None
    ) -> ProcessedFile:
        """
        Decrypt a PDF file.

        Args:
            file_url: URL of the encrypted PDF file
            password: Password to decrypt the PDF
            output_filename: Output filename (optional)

        Returns:
            ProcessedFile with decrypted PDF

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "file_url": file_url,
                "password": password
            }

            if output_filename:
                payload["output_filename"] = output_filename

            async with self.session.post(
                f"{self.BASE_URL}/pdf/decrypt",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"FX error: {data.get('error', 'Unknown error')}")

                return ProcessedFile(
                    url=data["url"],
                    filename=data["filename"],
                    mime_type=data["mime_type"],
                    size=data["size"]
                )

        except Exception as e:
            raise Exception(f"Failed to decrypt PDF: {str(e)}")

    async def split_pdf(
        self,
        file_url: str,
        pages: str,
        output_filename: Optional[str] = None
    ) -> ProcessedFile:
        """
        Split a PDF file by pages.

        Args:
            file_url: URL of the PDF file
            pages: Page ranges (e.g., "1-3,5,7-9")
            output_filename: Output filename (optional)

        Returns:
            ProcessedFile with split PDF

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "file_url": file_url,
                "pages": pages
            }

            if output_filename:
                payload["output_filename"] = output_filename

            async with self.session.post(
                f"{self.BASE_URL}/pdf/split",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"FX error: {data.get('error', 'Unknown error')}")

                return ProcessedFile(
                    url=data["url"],
                    filename=data["filename"],
                    mime_type=data["mime_type"],
                    size=data["size"]
                )

        except Exception as e:
            raise Exception(f"Failed to split PDF: {str(e)}")

    async def add_watermark_to_pdf(
        self,
        file_url: str,
        watermark_text: str,
        output_filename: Optional[str] = None
    ) -> ProcessedFile:
        """
        Add watermark to a PDF file.

        Args:
            file_url: URL of the PDF file
            watermark_text: Watermark text to add
            output_filename: Output filename (optional)

        Returns:
            ProcessedFile with watermarked PDF

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "file_url": file_url,
                "watermark": watermark_text
            }

            if output_filename:
                payload["output_filename"] = output_filename

            async with self.session.post(
                f"{self.BASE_URL}/pdf/watermark",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"FX error: {data.get('error', 'Unknown error')}")

                return ProcessedFile(
                    url=data["url"],
                    filename=data["filename"],
                    mime_type=data["mime_type"],
                    size=data["size"]
                )

        except Exception as e:
            raise Exception(f"Failed to add watermark to PDF: {str(e)}")

    async def convert_office_to_pdf(
        self,
        file_url: str,
        output_filename: Optional[str] = None
    ) -> ProcessedFile:
        """
        Convert Office file to PDF.

        Args:
            file_url: URL of the Office file
            output_filename: Output filename (optional)

        Returns:
            ProcessedFile with converted PDF

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {"file_url": file_url}

            if output_filename:
                payload["output_filename"] = output_filename

            async with self.session.post(
                f"{self.BASE_URL}/convert/office-to-pdf",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"FX error: {data.get('error', 'Unknown error')}")

                return ProcessedFile(
                    url=data["url"],
                    filename=data["filename"],
                    mime_type=data["mime_type"],
                    size=data["size"]
                )

        except Exception as e:
            raise Exception(f"Failed to convert Office to PDF: {str(e)}")

    # ==================== Image Operations ====================

    async def generate_image_from_text(
        self,
        text: str,
        width: int = 800,
        height: int = 200,
        options: Optional[Dict[str, Any]] = None
    ) -> ImageResult:
        """
        Generate image from text.

        Args:
            text: Text to render as image
            width: Image width
            height: Image height
            options: Additional options (font, color, etc.)

        Returns:
            ImageResult with generated image

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "text": text,
                "width": width,
                "height": height
            }

            if options:
                payload.update(options)

            async with self.session.post(
                f"{self.BASE_URL}/image/text-to-image",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"FX error: {data.get('error', 'Unknown error')}")

                return ImageResult(
                    url=data["url"],
                    width=data.get("width", width),
                    height=data.get("height", height),
                    format=data.get("format", "png")
                )

        except Exception as e:
            raise Exception(f"Failed to generate image from text: {str(e)}")

    async def resize_image(
        self,
        file_url: str,
        width: int,
        height: int,
        output_filename: Optional[str] = None
    ) -> ImageResult:
        """
        Resize an image.

        Args:
            file_url: URL of the image
            width: New width
            height: New height
            output_filename: Output filename (optional)

        Returns:
            ImageResult with resized image

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "file_url": file_url,
                "width": width,
                "height": height
            }

            if output_filename:
                payload["output_filename"] = output_filename

            async with self.session.post(
                f"{self.BASE_URL}/image/resize",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"FX error: {data.get('error', 'Unknown error')}")

                return ImageResult(
                    url=data["url"],
                    width=data.get("width", width),
                    height=data.get("height", height),
                    format=data.get("format", "png")
                )

        except Exception as e:
            raise Exception(f"Failed to resize image: {str(e)}")

    async def overlay_image_on_background(
        self,
        overlay_url: str,
        background_url: str,
        position: str = "center",
        output_filename: Optional[str] = None
    ) -> ImageResult:
        """
        Overlay image on background.

        Args:
            overlay_url: URL of overlay image
            background_url: URL of background image
            position: Position (center, top-left, etc.)
            output_filename: Output filename (optional)

        Returns:
            ImageResult with overlay result

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "overlay_url": overlay_url,
                "background_url": background_url,
                "position": position
            }

            if output_filename:
                payload["output_filename"] = output_filename

            async with self.session.post(
                f"{self.BASE_URL}/image/overlay",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"FX error: {data.get('error', 'Unknown error')}")

                return ImageResult(
                    url=data["url"],
                    width=data.get("width", 0),
                    height=data.get("height", 0),
                    format=data.get("format", "png")
                )

        except Exception as e:
            raise Exception(f"Failed to overlay images: {str(e)}")

    async def generate_qr_code(
        self,
        content: str,
        size: int = 200,
        format: str = "png"
    ) -> ImageResult:
        """
        Generate QR code.

        Args:
            content: Content to encode
            size: QR code size
            format: Output format (png, jpg, svg)

        Returns:
            ImageResult with QR code

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "content": content,
                "size": size,
                "format": format
            }

            async with self.session.post(
                f"{self.BASE_URL}/qr/generate",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"FX error: {data.get('error', 'Unknown error')}")

                return ImageResult(
                    url=data["url"],
                    width=data.get("width", size),
                    height=data.get("height", size),
                    format=format
                )

        except Exception as e:
            raise Exception(f"Failed to generate QR code: {str(e)}")

    async def render_html_to_image(
        self,
        html: str,
        width: int = 1200,
        height: int = 800
    ) -> ImageResult:
        """
        Render HTML to image.

        Args:
            html: HTML content
            width: Image width
            height: Image height

        Returns:
            ImageResult with rendered image

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "html": html,
                "width": width,
                "height": height
            }

            async with self.session.post(
                f"{self.BASE_URL}/render/html-to-image",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"FX error: {data.get('error', 'Unknown error')}")

                return ImageResult(
                    url=data["url"],
                    width=data.get("width", width),
                    height=data.get("height", height),
                    format=data.get("format", "png")
                )

        except Exception as e:
            raise Exception(f"Failed to render HTML to image: {str(e)}")

    # ==================== Other Operations ====================

    async def upload_asset_file(
        self,
        file_data: bytes,
        filename: str,
        mime_type: str
    ) -> AssetUpload:
        """
        Upload an asset file.

        Args:
            file_data: File data as bytes
            filename: Filename
            mime_type: MIME type

        Returns:
            AssetUpload with upload details

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            async with self.session.post(
                f"{self.BASE_URL}/assets/upload",
                data=file_data,
                headers={"Content-Type": mime_type}
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"FX error: {data.get('error', 'Unknown error')}")

                return AssetUpload(
                    asset_id=data["asset_id"],
                    url=data["url"],
                    size=data["size"]
                )

        except Exception as e:
            raise Exception(f"Failed to upload asset file: {str(e)}")

    async def convert_asset_url_to_base64(self, asset_url: str) -> str:
        """
        Convert asset URL to base64.

        Args:
            asset_url: Asset URL

        Returns:
            Base64 encoded string

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {"asset_url": asset_url}

            async with self.session.post(
                f"{self.BASE_URL}/assets/to-base64",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"FX error: {data.get('error', 'Unknown error')}")

                return data["base64"]

        except Exception as e:
            raise Exception(f"Failed to convert asset to base64: {str(e)}")

    async def check_holiday(self, date: str, country: str = "US") -> Dict[str, Any]:
        """
        Check if a date is a holiday.

        Args:
            date: Date in YYYY-MM-DD format
            country: Country code

        Returns:
            Dictionary with holiday info

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "date": date,
                "country": country
            }

            async with self.session.post(
                f"{self.BASE_URL}/date/holiday",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"FX error: {data.get('error', 'Unknown error')}")

                return data

        except Exception as e:
            raise Exception(f"Failed to check holiday: {str(e)}")