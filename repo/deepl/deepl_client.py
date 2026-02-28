"""
DeepL API - Translation API Client

Supports:
- Translate Text
- Translate Document
- Get Translation Status
"""

import aiohttp
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class TextTranslation:
    """Text translation result"""
    text: str
    detected_source_language: str


@dataclass
class TranslateResponse:
    """Translate text API response"""
    translations: List[TextTranslation]


@dataclass
class DocumentTranslation:
    """Document translation result"""
    document_id: str
    status: str
    seconds_remaining: Optional[int]
    billed_characters: Optional[int]
    error_message: Optional[str]


@dataclass
class DocumentUploadResponse:
    """Document upload response"""
    document_id: str
    status: str


class DeepLAPIClient:
    """
    DeepL API client for text and document translation.

    API Documentation: https://www.deepl.com/docs-api/
    """

    BASE_URL = "https://api-free.deepl.com/v2"  # Free tier
    # BASE_URL = "https://api.deepl.com/v2"  # Paid tier

    def __init__(self, api_key: str, use_free_tier: bool = True):
        """
        Initialize DeepL API client.

        Args:
            api_key: DeepL API key (from account.deepl.com)
            use_free_tier: Use free API endpoint (default: True)
        """
        self.api_key = api_key
        self.session = None
        if use_free_tier:
            self.BASE_URL = "https://api-free.deepl.com/v2"
        else:
            self.BASE_URL = "https://api.deepl.com/v2"

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={"Authorization": f"DeepL-Auth-Key {self.api_key}"}
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def translate_text(
        self,
        text: str,
        target_lang: str,
        source_lang: Optional[str] = None,
        formality: str = "default",
        preserve_formatting: bool = False
    ) -> TranslateResponse:
        """
        Translate text to target language.

        Args:
            text: Text to translate
            target_lang: Target language code (e.g., 'EN', 'DE', 'KO')
            source_lang: Source language code (auto-detected if not provided)
            formality: Formality level ('default', 'more', 'less')
            preserve_formatting: Whether to preserve formatting

        Returns:
            TranslateResponse with translated text

        Raises:
            ValueError: If text is empty
            aiohttp.ClientError: If request fails
        """
        if not text:
            raise ValueError("Text cannot be empty")

        params = {
            "text": text,
            "target_lang": target_lang,
            "formality": formality,
            "preserve_formatting": str(preserve_formatting).lower()
        }

        if source_lang:
            params["source_lang"] = source_lang

        async with self.session.post(
            f"{self.BASE_URL}/translate",
            data=params
        ) as response:
            data = await response.json()

            if response.status != 200:
                error_msg = data.get("message", str(data))
                raise Exception(f"DeepL Translate error: {error_msg}")

            translations = [
                TextTranslation(
                    text=t["text"],
                    detected_source_language=t.get("detected_source_language", "")
                )
                for t in data.get("translations", [])
            ]

            return TranslateResponse(translations=translations)

    async def translate_document(
        self,
        file_path: str,
        target_lang: str,
        source_lang: Optional[str] = None,
        formality: str = "default"
    ) -> DocumentUploadResponse:
        """
        Upload a document for translation.

        Args:
            file_path: Path to document file
            target_lang: Target language code
            source_lang: Source language code (auto-detected if not provided)
            formality: Formality level

        Returns:
            DocumentUploadResponse with document ID

        Raises:
            ValueError: If file doesn't exist
            aiohttp.ClientError: If request fails
        """
        import os

        if not os.path.exists(file_path):
            raise ValueError(f"File not found: {file_path}")

        # Read file
        with open(file_path, "rb") as f:
            file_data = f.read()

        filename = os.path.basename(file_path)

        data = aiohttp.FormData()
        data.add_field("file", file_data, filename=filename)
        data.add_field("target_lang", target_lang)

        if source_lang:
            data.add_field("source_lang", source_lang)
        data.add_field("formality", formality)

        async with self.session.post(
            f"{self.BASE_URL}/document",
            data=data
        ) as response:
            data = await response.json()

            if response.status != 200:
                error_msg = data.get("message", str(data))
                raise Exception(f"DeepL Document Upload error: {error_msg}")

            return DocumentUploadResponse(
                document_id=data.get("document_id", ""),
                status=data.get("status", "")
            )

    async def get_translation_status(
        self,
        document_id: str
    ) -> DocumentTranslation:
        """
        Get the status of a document translation.

        Args:
            document_id: Document ID from translation request

        Returns:
            DocumentTranslation with status information

        Raises:
            ValueError: If document_id is empty
            aiohttp.ClientError: If request fails
        """
        if not document_id:
            raise ValueError("Document ID cannot be empty")

        params = {"document_key": document_id}

        async with self.session.post(
            f"{self.BASE_URL}/document/{document_id}",
            data=params
        ) as response:
            data = await response.json()

            if response.status != 200:
                error_msg = data.get("message", str(data))
                raise Exception(f"DeepL Status error: {error_msg}")

            if response.status == 200 and data.get("status") == "done":
                # Download the translated document
                async with self.session.get(
                    f"{self.BASE_URL}/document/{document_id}/result",
                    params=params
                ) as result_response:
                    file_data = await result_response.read()
                    data["result_data"] = file_data

            return DocumentTranslation(
                document_id=data.get("document_id", document_id),
                status=data.get("status", ""),
                seconds_remaining=data.get("seconds_remaining"),
                billed_characters=data.get("billed_characters"),
                error_message=data.get("error_message")
            )

    async def download_translated_document(
        self,
        document_id: str,
        output_path: str
    ) -> None:
        """
        Download a translated document.

        Args:
            document_id: Document ID
            output_path: Path to save the translated file

        Raises:
            aiohttp.ClientError: If request fails
        """
        params = {"document_key": document_id}

        async with self.session.get(
            f"{self.BASE_URL}/document/{document_id}/result",
            params=params
        ) as response:
            if response.status != 200:
                raise Exception(f"Failed to download document: {response.status}")

            file_data = await response.read()
            with open(output_path, "wb") as f:
                f.write(file_data)


async def main():
    """Example usage"""
    api_key = "your-api-key-here"

    async with DeepLAPIClient(api_key) as client:
        # Translate text
        result = await client.translate_text(
            text="Hello, how are you?",
            target_lang="KO"  # Korean
        )
        print(f"Translation: {result.translations[0].text}")

        # Translate document
        # upload_result = await client.translate_document(
        #     file_path="document.pdf",
        #     target_lang="DE"
        # )
        # print(f"Document ID: {upload_result.document_id}")

        # Check status
        # status = await client.get_translation_status(upload_result.document_id)
        # print(f"Status: {status.status}")

        # Download translated document
        # await client.download_translated_document(
        #     document_id=upload_result.document_id,
        #     output_path="translated.pdf"
        # )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())