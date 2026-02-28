"""
CodeGPT API - AI Coding Assistant Client

Supports:
- Chat Completion
- Update Document
- Upload Document
- Search Documents
"""

import aiohttp
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class Message:
    """Chat message"""
    role: str  # 'user', 'assistant', 'system'
    content: str


@dataclass
class ChatCompletionResponse:
    """Chat completion response"""
    content: str
    model: str
    usage: Dict[str, int]


@dataclass
class Document:
    """Document representation"""
    id: str
    name: str
    content: str
    created_at: str
    updated_at: str


@dataclass
class DocumentResponse:
    """Document operation response"""
    success: bool
    document: Optional[Document]
    message: str


@dataclass
class SearchHit:
    """Search result hit"""
    document_id: str
    document_name: str
    score: float
    snippet: str


@dataclass
class SearchResponse:
    """Document search response"""
    results: List[SearchHit]
    total: int
    query: str


class CodeGPTAPIClient:
    """
    CodeGPT API client for AI-powered coding assistance.

    API Documentation: https://codegpt.co/api-docs
    """

    BASE_URL = "https://api.codegpt.co/v1"

    def __init__(self, api_key: str):
        """
        Initialize CodeGPT API client.

        Args:
            api_key: CodeGPT API key
        """
        self.api_key = api_key
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "codegpt-4",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        context: Optional[str] = None
    ) -> ChatCompletionResponse:
        """
        Get AI code completion/suggestions.

        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model name to use
            temperature: Sampling temperature (0.0-2.0)
            max_tokens: Maximum tokens to generate
            context: Additional context for codebase

        Returns:
            ChatCompletionResponse with assistant message

        Raises:
            ValueError: If messages is empty
            aiohttp.ClientError: If request fails
        """
        if not messages:
            raise ValueError("Messages list cannot be empty")

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature
        }

        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        if context:
            payload["context"] = context

        async with self.session.post(
            f"{self.BASE_URL}/chat/completions",
            json=payload
        ) as response:
            data = await response.json()

            if response.status != 200:
                error_msg = data.get("error", {}).get("message", str(data))
                raise Exception(f"CodeGPT Chat error: {error_msg}")

            return ChatCompletionResponse(
                content=data["choices"][0]["message"]["content"],
                model=data.get("model", model),
                usage=data.get("usage", {})
            )

    async def update_document(
        self,
        document_id: str,
        content: str,
        name: Optional[str] = None
    ) -> DocumentResponse:
        """
        Update an existing document.

        Args:
            document_id: ID of the document to update
            content: New document content
            name: Optional new name for the document

        Returns:
            DocumentResponse with updated document

        Raises:
            ValueError: If document_id or content is empty
            aiohttp.ClientError: If request fails
        """
        if not document_id:
            raise ValueError("Document ID cannot be empty")
        if not content:
            raise ValueError("Content cannot be empty")

        payload = {
            "document_id": document_id,
            "content": content
        }

        if name:
            payload["name"] = name

        async with self.session.put(
            f"{self.BASE_URL}/documents/{document_id}",
            json=payload
        ) as response:
            data = await response.json()

            if response.status != 200:
                error_msg = data.get("error", {}).get("message", str(data))
                raise Exception(f"CodeGPT Update Document error: {error_msg}")

            return DocumentResponse(
                success=data.get("success", False),
                message=data.get("message", ""),
                document=Document(
                    id=data.get("document", {}).get("id", ""),
                    name=data.get("document", {}).get("name", ""),
                    content=data.get("document", {}).get("content", ""),
                    created_at=data.get("document", {}).get("created_at", ""),
                    updated_at=data.get("document", {}).get("updated_at", "")
                ) if data.get("document") else None
            )

    async def upload_document(
        self,
        content: str,
        name: str,
        language: Optional[str] = None,
        file_type: str = "code"
    ) -> DocumentResponse:
        """
        Upload a new document.

        Args:
            content: Document content (code/text)
            name: Document name
            language: Programming language (e.g., 'python', 'javascript')
            file_type: Type of document ('code', 'text', 'markdown')

        Returns:
            DocumentResponse with created document

        Raises:
            ValueError: If content or name is empty
            aiohttp.ClientError: If request fails
        """
        if not content:
            raise ValueError("Content cannot be empty")
        if not name:
            raise ValueError("Name cannot be empty")

        payload = {
            "content": content,
            "name": name,
            "file_type": file_type
        }

        if language:
            payload["language"] = language

        async with self.session.post(
            f"{self.BASE_URL}/documents",
            json=payload
        ) as response:
            data = await response.json()

            if response.status != 201:
                error_msg = data.get("error", {}).get("message", str(data))
                raise Exception(f"CodeGPT Upload Document error: {error_msg}")

            return DocumentResponse(
                success=data.get("success", True),
                message=data.get("message", ""),
                document=Document(
                    id=data.get("document", {}).get("id", ""),
                    name=data.get("document", {}).get("name", ""),
                    content=data.get("document", {}).get("content", ""),
                    created_at=data.get("document", {}).get("created_at", ""),
                    updated_at=data.get("document", {}).get("updated_at", "")
                ) if data.get("document") else None
            )

    async def search_documents(
        self,
        query: str,
        limit: int = 10,
        language: Optional[str] = None,
        file_type: Optional[str] = None
    ) -> SearchResponse:
        """
        Search documents in your codebase.

        Args:
            query: Search query string
            limit: Maximum number of results (default: 10)
            language: Filter by programming language
            file_type: Filter by file type

        Returns:
            SearchResponse with matching documents

        Raises:
            ValueError: If query is empty
            aiohttp.ClientError: If request fails
        """
        if not query:
            raise ValueError("Query cannot be empty")

        params = {
            "q": query,
            "limit": limit
        }

        if language:
            params["language"] = language
        if file_type:
            params["file_type"] = file_type

        async with self.session.get(
            f"{self.BASE_URL}/documents/search",
            params=params
        ) as response:
            data = await response.json()

            if response.status != 200:
                error_msg = data.get("error", {}).get("message", str(data))
                raise Exception(f"CodeGPT Search Documents error: {error_msg}")

            results = [
                SearchHit(
                    document_id=r.get("document_id", ""),
                    document_name=r.get("document_name", ""),
                    score=r.get("score", 0.0),
                    snippet=r.get("snippet", "")
                )
                for r in data.get("results", [])
            ]

            return SearchResponse(
                results=results,
                total=data.get("total", len(results)),
                query=data.get("query", query)
            )


async def main():
    """Example usage"""
    api_key = "your-api-key-here"

    async with CodeGPTAPIClient(api_key) as client:
        # Chat completion example
        messages = [
            {"role": "system", "content": "You are a helpful coding assistant."},
            {"role": "user", "content": "Write a Python function to calculate fibonacci numbers."}
        ]

        chat_result = await client.chat_completion(
            messages=messages,
            model="codegpt-4"
        )
        print(f"Chat response: {chat_result.content}")

        # Upload document example
        upload_result = await client.upload_document(
            content="def hello():\n    print('Hello, World!')",
            name="hello.py",
            language="python",
            file_type="code"
        )
        print(f"Uploaded document ID: {upload_result.document.id if upload_result.document else 'N/A'}")

        # Search documents example
        search_result = await client.search_documents(
            query="fibonacci",
            language="python",
            limit=5
        )
        print(f"Found {search_result.total} results")
        for hit in search_result.results:
            print(f"  - {hit.document_name}: {hit.snippet}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())