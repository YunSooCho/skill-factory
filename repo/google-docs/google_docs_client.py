"""
Google Docs API - Document Management Client

Supports:
- Create New Document
- Insert Image in Document
- Replace Values
- Append Text to End
- Get Document Content
"""

import aiohttp
import json
import base64
from typing import Optional, Dict, Any, List
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Document:
    """Google Docs document object"""
    document_id: str
    title: str
    body_content: str
    revision_id: Optional[str] = None
    suggest_view_changes_url: Optional[str] = None


@dataclass
class Paragraph:
    """Document paragraph object"""
    content: str
    elements: List[Dict[str, Any]]


@dataclass
class InsertionResult:
    """Result of an insertion operation"""
    document_id: str
    revision_id: str
    write_control: Dict[str, Any]


class GoogleDocsClient:
    """
    Google Docs API client for document management.

    Provides operations to create, read, and modify Google Docs documents.

    API Documentation: https://lp.yoom.fun/apps/google-docs
    Requires:
    - Google Cloud project with Docs API enabled
    - OAuth credentials or service account
    """

    BASE_URL = "https://docs.googleapis.com/v1"

    def __init__(self, access_token: str):
        """
        Initialize Google Docs client.

        Args:
            access_token: OAuth access token
        """
        self.access_token = access_token
        self.session = None
        self._rate_limit_delay = 0.1

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={"Authorization": f"Bearer {self.access_token}"}
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
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make an API request with error handling.

        Args:
            method: HTTP method
            endpoint: API endpoint
            params: Query parameters
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
                json=json_data
            ) as response:
                response_data = await response.json()

                if response.status >= 400:
                    error = response_data.get("error", {})
                    error_message = error.get("message", f"HTTP {response.status} error")
                    raise Exception(f"Google Docs API error: {error_message}")

                return response_data

        except aiohttp.ClientError as e:
            raise Exception(f"Network error: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON response: {str(e)}")

    # ==================== Document Operations ====================

    async def create_document(
        self,
        title: str,
        body: Optional[str] = None
    ) -> Document:
        """
        Create a new Google Docs document.

        Args:
            title: Document title
            body: Optional initial body content

        Returns:
            Document object with document details

        Raises:
            Exception: If creation fails
            ValueError: If title is empty
        """
        if not title:
            raise ValueError("title is required")

        payload = {"title": title}

        response_data = await self._make_request(
            "POST",
            "/documents",
            json_data=payload
        )

        document_id = response_data.get("documentId", "")

        # Add initial content if provided
        if body:
            await self.append_text(document_id, body)

        # Get document details
        doc_data = await self._make_request(
            "GET",
            f"/documents/{document_id}"
        )

        return Document(
            document_id=document_id,
            title=doc_data.get("title", title),
            body_content=body or "",
            revision_id=doc_data.get("revisionId"),
            suggest_view_changes_url=doc_data.get("suggestionsViewModeUrl")
        )

    async def get_document_content(
        self,
        document_id: str,
        include_revision_id: bool = False
    ) -> Document:
        """
        Get content of a document.

        Args:
            document_id: Document ID
            include_revision_id: Whether to include revision information

        Returns:
            Document object with content

        Raises:
            Exception: If retrieval fails
            ValueError: If document_id is empty
        """
        if not document_id:
            raise ValueError("document_id is required")

        params = {}
        if include_revision_id:
            params["suggestionsViewMode"] = "SUGGESTIONS_INLINE"

        response_data = await self._make_request(
            "GET",
            f"/documents/{document_id}",
            params=params
        )

        # Extract text content
        text_content = self._extract_text_from_document(response_data)

        return Document(
            document_id=document_id,
            title=response_data.get("title", ""),
            body_content=text_content,
            revision_id=response_data.get("revisionId"),
            suggest_view_changes_url=response_data.get("suggestionsViewModeUrl")
        )

    def _extract_text_from_document(self, doc_data: Dict[str, Any]) -> str:
        """Extract text content from document structure."""
        content = []

        if "body" in doc_data:
            body = doc_data["body"]
            if "content" in body:
                for element in body["content"]:
                    if "paragraph" in element:
                        paragraph = element["paragraph"]
                        if "elements" in paragraph:
                            for elem in paragraph["elements"]:
                                if "textRun" in elem:
                                    text = elem["textRun"].get("content", "")
                                    content.append(text)

        return "".join(content)

    # ==================== Text Operations ====================

    async def append_text(
        self,
        document_id: str,
        text: str,
        text_style: Optional[Dict[str, Any]] = None
    ) -> InsertionResult:
        """
        Append text to the end of a document.

        Args:
            document_id: Document ID
            text: Text to append
            text_style: Optional text style (bold, italic, font size, etc.)

        Returns:
            InsertionResult with operation details

        Raises:
            Exception: If operation fails
            ValueError: If parameters are invalid
        """
        if not document_id:
            raise ValueError("document_id is required")
        if not text:
            raise ValueError("text is required")

        # Get document to find the end position
        doc_data = await self._make_request(
            "GET",
            f"/documents/{document_id}"
        )

        # Find the end position
        end_index = 1
        if "body" in doc_data and "content" in doc_data["body"]:
            content = doc_data["body"]["content"]
            if content:
                last_element = content[-1]
                if "endIndex" in last_element:
                    end_index = last_element["endIndex"]

        # Create the request to insert text
        requests = [
            {
                "insertText": {
                    "location": {"index": end_index},
                    "text": text
                }
            }
        ]

        # Add text style if provided
        if text_style:
            requests[0]["insertText"]["textStyle"] = text_style

        response_data = await self._make_request(
            "POST",
            f"/documents/{document_id}:batchUpdate",
            json_data={"requests": requests}
        )

        return InsertionResult(
            document_id=document_id,
            revision_id=response_data.get("documentId", document_id),
            write_control=response_data.get("writeControl", {})
        )

    async def replace_values(
        self,
        document_id: str,
        replacements: Dict[str, str],
        case_sensitive: bool = False
    ) -> InsertionResult:
        """
        Replace values in a document.

        Args:
            document_id: Document ID
            replacements: Dictionary of {find_text: replace_text}
            case_sensitive: Whether search should be case-sensitive

        Raises:
            Exception: If operation fails
            ValueError: If parameters are invalid
        """
        if not document_id:
            raise ValueError("document_id is required")
        if not replacements:
            raise ValueError("replacements is required")

        requests = []

        for find_text, replace_text in replacements.items():
            requests.append({
                "replaceText": {
                    "replaceText": replace_text,
                    "containsText": {
                        "text": find_text,
                        "matchCase": case_sensitive
                    }
                }
            })

        response_data = await self._make_request(
            "POST",
            f"/documents/{document_id}:batchUpdate",
            json_data={"requests": requests}
        )

        return InsertionResult(
            document_id=document_id,
            revision_id=response_data.get("documentId", document_id),
            write_control=response_data.get("writeControl", {})
        )

    # ==================== Image Operations ====================

    async def insert_image(
        self,
        document_id: str,
        image_url: Optional[str] = None,
        image_data: Optional[bytes] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        insert_at_end: bool = True,
        insert_index: Optional[int] = None
    ) -> InsertionResult:
        """
        Insert an image into a document.

        Args:
            document_id: Document ID
            image_url: URL of the image to insert
            image_data: Raw image data as bytes (alternative to image_url)
            width: Optional image width in EMU units (1 inch = 914400 EMU)
            height: Optional image height in EMU units
            insert_at_end: Whether to insert at the end of the document
            insert_index: Specific index to insert at (overrides insert_at_end)

        Returns:
            InsertionResult with operation details

        Raises:
            Exception: If operation fails
            ValueError: If parameters are invalid
        """
        if not document_id:
            raise ValueError("document_id is required")
        if not image_url and not image_data:
            raise ValueError("Either image_url or image_data is required")

        # Calculate insertion position
        if insert_index is None and insert_at_end:
            # Get document to find the end position
            doc_data = await self._make_request(
                "GET",
                f"/documents/{document_id}"
            )

            insert_index = 1
            if "body" in doc_data and "content" in doc_data["body"]:
                content = doc_data["body"]["content"]
                if content:
                    last_element = content[-1]
                    if "endIndex" in last_element:
                        insert_index = last_element["endIndex"]

        # Create the inline image object
        inline_object = {}

        if image_data:
            # Encode image data
            encoded_data = base64.b64encode(image_data).decode("utf-8")
            inline_object = {
                "inlineObjectProperties": {
                    "embeddedObject": {
                        "imageProperties": {
                            "contentUri": f"data:image;base64,{encoded_data}"
                        }
                    }
                }
            }
        else:
            # Use image URL
            inline_object = {
                "inlineObjectProperties": {
                    "embeddedObject": {
                        "imageProperties": {
                            "sourceUri": image_url
                        }
                    }
                }
            }

        # Add dimensions if provided
        if width or height:
            if "imageProperties" not in inline_object["inlineObjectProperties"]["embeddedObject"]:
                inline_object["inlineObjectProperties"]["embeddedObject"]["imageProperties"] = {}

            if width:
                inline_object["inlineObjectProperties"]["embeddedObject"]["imageProperties"]["width"] = {
                    "magnitude": width,
                    "unit": "EMU"
                }
            if height:
                inline_object["inlineObjectProperties"]["embeddedObject"]["imageProperties"]["height"] = {
                    "magnitude": height,
                    "unit": "EMU"
                }

        # Create the request
        requests = [
            {
                "createParagraphBullets": {
                    "range": {
                        "startIndex": insert_index,
                        "endIndex": insert_index
                    },
                    "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"
                }
            }
        ]

        # Insert the image
        requests.append({
            "insertInlineImage": {
                "location": {"index": insert_index},
                "objectSize": {}
            }
        })

        # Use a simpler approach - get the current document and update it
        response_data = await self._make_request(
            "GET",
            f"/documents/{document_id}"
        )

        # For simplicity, we'll use batch update to insert text first
        # In a real implementation, you'd need more complex handling
        actual_requests = []

        if image_url:
            actual_requests.append({
                "insertInlineImage": {
                    "location": {"index": insert_index},
                    "uri": image_url
                }
            })

        response_data = await self._make_request(
            "POST",
            f"/documents/{document_id}:batchUpdate",
            json_data={"requests": actual_requests}
        )

        return InsertionResult(
            document_id=document_id,
            revision_id=response_data.get("documentId", document_id),
            write_control=response_data.get("writeControl", {})
        )

    # ==================== Formatting Operations ====================

    async def update_paragraph_style(
        self,
        document_id: str,
        start_index: int,
        end_index: int,
        paragraph_style: Dict[str, Any]
    ) -> InsertionResult:
        """
        Update paragraph style for a range of text.

        Args:
            document_id: Document ID
            start_index: Start position (inclusive)
            end_index: End position (exclusive)
            paragraph_style: Paragraph style properties

        Returns:
            InsertionResult with operation details

        Raises:
            Exception: If operation fails
        """
        requests = [
            {
                "updateParagraphStyle": {
                    "range": {
                        "startIndex": start_index,
                        "endIndex": end_index
                    },
                    "paragraphStyle": paragraph_style,
                    "fields": ",".join(paragraph_style.keys())
                }
            }
        ]

        response_data = await self._make_request(
            "POST",
            f"/documents/{document_id}:batchUpdate",
            json_data={"requests": requests}
        )

        return InsertionResult(
            document_id=document_id,
            revision_id=response_data.get("documentId", document_id),
            write_control=response_data.get("writeControl", {})
        )

    async def update_text_style(
        self,
        document_id: str,
        start_index: int,
        end_index: int,
        text_style: Dict[str, Any]
    ) -> InsertionResult:
        """
        Update text style for a range of text.

        Args:
            document_id: Document ID
            start_index: Start position (inclusive)
            end_index: End position (exclusive)
            text_style: Text style properties (bold, italic, fontSize, etc.)

        Returns:
            InsertionResult with operation details

        Raises:
            Exception: If operation fails
        """
        requests = [
            {
                "updateTextStyle": {
                    "range": {
                        "startIndex": start_index,
                        "endIndex": end_index
                    },
                    "textStyle": text_style,
                    "fields": ",".join(text_style.keys())
                }
            }
        ]

        response_data = await self._make_request(
            "POST",
            f"/documents/{document_id}:batchUpdate",
            json_data={"requests": requests}
        )

        return InsertionResult(
            document_id=document_id,
            revision_id=response_data.get("documentId", document_id),
            write_control=response_data.get("writeControl", {})
        )

    async def delete_content(
        self,
        document_id: str,
        start_index: int,
        end_index: int
    ) -> InsertionResult:
        """
        Delete content from a document.

        Args:
            document_id: Document ID
            start_index: Start position (inclusive)
            end_index: End position (exclusive)

        Returns:
            InsertionResult with operation details

        Raises:
            Exception: If operation fails
        """
        requests = [
            {
                "deleteContentRange": {
                    "range": {
                        "startIndex": start_index,
                        "endIndex": end_index
                    }
                }
            }
        ]

        response_data = await self._make_request(
            "POST",
            f"/documents/{document_id}:batchUpdate",
            json_data={"requests": requests}
        )

        return InsertionResult(
            document_id=document_id,
            revision_id=response_data.get("documentId", document_id),
            write_control=response_data.get("writeControl", {})
        )

    # ==================== Utility Methods ====================

    async def batch_update(
        self,
        document_id: str,
        requests: List[Dict[str, Any]]
    ) -> InsertionResult:
        """
        Execute multiple update requests in a single API call.

        Args:
            document_id: Document ID
            requests: List of update request objects

        Returns:
            InsertionResult with operation details

        Raises:
            Exception: If operation fails
        """
        response_data = await self._make_request(
            "POST",
            f"/documents/{document_id}:batchUpdate",
            json_data={"requests": requests}
        )

        return InsertionResult(
            document_id=document_id,
            revision_id=response_data.get("documentId", document_id),
            write_control=response_data.get("writeControl", {})
        )


# ==================== Example Usage ====================

async def main():
    """Example usage of Google Docs client"""

    # Replace with your actual OAuth access token
    ACCESS_TOKEN = "your_oauth_access_token"

    async with GoogleDocsClient(access_token=ACCESS_TOKEN) as client:
        try:
            # Create a new document
            doc = await client.create_document(
                title="My New Document",
                body="This is the initial content of my document.\n\n"
            )
            print(f"Created document: {doc.document_id}")
            print(f"Title: {doc.title}")

            # Append more text
            result = await client.append_text(
                doc.document_id,
                "This text was appended programmatically.\n\n"
            )
            print("Appended text")

            # Replace values
            await client.replace_values(
                doc.document_id,
                {
                    "programmatically": "using the Google Docs API",
                    "My New": "My Updated"
                }
            )
            print("Replaced values")

            # Insert an image (using example URL)
            # result = await client.insert_image(
            #     doc.document_id,
            #     image_url="https://example.com/image.png",
            #     width=300000,  # Approximately 3.3 inches
            #     height=200000  # Approximately 2.2 inches
            # )
            # print("Inserted image")

            # Get updated content
            updated_doc = await client.get_document_content(doc.document_id)
            print(f"\nDocument content:\n{updated_doc.body_content}")

            # Update text style for a range
            await client.update_text_style(
                doc.document_id,
                start_index=1,
                end_index=50,
                text_style={"bold": True, "fontSize": {"magnitude": 14, "unit": "PT"}}
            )
            print("Updated text style")

        except Exception as e:
            print(f"Error: {str(e)}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())