"""
Cohere API - NLP API Client

Supports:
- Rerank
- Embed
- Chat
"""

import aiohttp
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class RerankResult:
    """Rerank result for a single document"""
    index: int
    relevance_score: float


@dataclass
class RerankResponse:
    """Rerank API response"""
    results: List[RerankResult]
    query: str
    model: str


@dataclass
class EmbedResponse:
    """Embed API response"""
    embeddings: List[List[float]]
    model: str
    input_text_count: int


@dataclass
class ChatMessage:
    """Chat message"""
    role: str  # 'USER', 'CHATBOT', 'SYSTEM'
    message: str


@dataclass
class ChatResponse:
    """Chat API response"""
    text: str
    model: str
    chat_history: List[Dict[str, str]]
    meta: Dict[str, Any]


class CohereAPIClient:
    """
    Cohere API client for NLP tasks.

    API Documentation: https://docs.cohere.com/reference/
    """

    BASE_URL = "https://api.cohere.ai/v1"

    def __init__(self, api_key: str):
        """
        Initialize Cohere API client.

        Args:
            api_key: Cohere API key from dashboard.cohere.com
        """
        self.api_key = api_key
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "X-Client-Name": "yoom-cohere-client"
            }
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def rerank(
        self,
        query: str,
        documents: List[str],
        model: str = "rerank-english-v2.0",
        top_n: Optional[int] = None
    ) -> RerankResponse:
        """
        Rerank documents based on their relevance to a query.

        Args:
            query: Query string
            documents: List of document strings to rerank
            model: Rerank model name
            top_n: Number of top results to return

        Returns:
            RerankResponse with ranked results

        Raises:
            ValueError: If query or documents is empty
            aiohttp.ClientError: If request fails
        """
        if not query:
            raise ValueError("Query cannot be empty")
        if not documents:
            raise ValueError("Documents list cannot be empty")

        payload = {
            "model": model,
            "query": query,
            "documents": documents
        }

        if top_n is not None:
            payload["top_n"] = top_n

        async with self.session.post(
            f"{self.BASE_URL}/rerank",
            json=payload
        ) as response:
            data = await response.json()

            if response.status != 200:
                error_msg = data.get("message", str(data))
                raise Exception(f"Cohere Rerank error: {error_msg}")

            results = [
                RerankResult(
                    index=r["index"],
                    relevance_score=r["relevance_score"]
                )
                for r in data.get("results", [])
            ]

            return RerankResponse(
                results=results,
                query=data.get("query", query),
                model=data.get("model", model)
            )

    async def embed(
        self,
        texts: List[str],
        model: str = "embed-english-v3.0",
        input_type: str = "search_document",
        truncate: str = "END"
    ) -> EmbedResponse:
        """
        Get embeddings for texts.

        Args:
            texts: List of text strings to embed
            model: Embedding model name
            input_type: Type of input text ('search_document', 'search_query', etc.)
            truncate: How to handle text overflow ('NONE', 'START', 'END')

        Returns:
            EmbedResponse with embeddings

        Raises:
            ValueError: If texts is empty
            aiohttp.ClientError: If request fails
        """
        if not texts:
            raise ValueError("Texts list cannot be empty")

        payload = {
            "model": model,
            "texts": texts,
            "input_type": input_type,
            "truncate": truncate
        }

        async with self.session.post(
            f"{self.BASE_URL}/embed",
            json=payload
        ) as response:
            data = await response.json()

            if response.status != 200:
                error_msg = data.get("message", str(data))
                raise Exception(f"Cohere Embed error: {error_msg}")

            return EmbedResponse(
                embeddings=data.get("embeddings", []),
                model=data.get("model", model),
                input_text_count=len(data.get("embeddings", []))
            )

    async def chat(
        self,
        message: str,
        chat_history: Optional[List[Dict[str, str]]] = None,
        model: str = "command-r",
        temperature: float = 0.7,
        preamble: Optional[str] = None,
        max_tokens: Optional[int] = None
    ) -> ChatResponse:
        """
        Send a chat message and get a response.

        Args:
            message: User message
            chat_history: Previous conversation history
            model: Chat model name
            temperature: Sampling temperature (0.0-5.0)
            preamble: System prompt / instructions
            max_tokens: Maximum tokens to generate

        Returns:
            ChatResponse with assistant message

        Raises:
            ValueError: If message is empty
            aiohttp.ClientError: If request fails
        """
        if not message:
            raise ValueError("Message cannot be empty")

        payload = {
            "model": model,
            "message": message,
            "temperature": temperature
        }

        if chat_history:
            payload["chat_history"] = chat_history
        if preamble:
            payload["preamble"] = preamble
        if max_tokens:
            payload["max_tokens"] = max_tokens

        async with self.session.post(
            f"{self.BASE_URL}/chat",
            json=payload
        ) as response:
            data = await response.json()

            if response.status != 200:
                error_msg = data.get("message", str(data))
                raise Exception(f"Cohere Chat error: {error_msg}")

            return ChatResponse(
                text=data.get("text", ""),
                model=data.get("model", model),
                chat_history=data.get("chat_history", []),
                meta=data.get("meta", {})
            )


async def main():
    """Example usage"""
    api_key = "your-api-key-here"

    async with CohereAPIClient(api_key) as client:
        # Rerank example
        documents = [
            "Machine learning is a subset of artificial intelligence.",
            "Python is a popular programming language.",
            "The sky is blue on a clear day."
        ]
        rerank_result = await client.rerank(
            query="What is machine learning?",
            documents=documents,
            top_n=2
        )
        print(f"Rerank results: {rerank_result.results}")

        # Embed example
        embed_result = await client.embed(
            texts=["Hello world", "How are you?"]
        )
        print(f"Embeddings shape: {len(embed_result.embeddings)} x {len(embed_result.embeddings[0])}")

        # Chat example
        chat_result = await client.chat(
            message="Explain machine learning in simple terms.",
            preamble="You are a helpful and knowledgeable assistant."
        )
        print(f"Chat response: {chat_result.text}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())