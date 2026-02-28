"""
Exa AI - AI Search and Retrieval API

Supports:
- Create Task
- Search URL
- Get Page Contents
- Search Contents
- Get Answer
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class Task:
    """Task representation"""
    task_id: str
    status: str
    created_at: str


@dataclass
class SearchResult:
    """Search result"""
    url: str
    title: str
    relevance_score: float


@dataclass
class PageContent:
    """Page content result"""
    url: str
    content: str
    title: str


@dataclass
class AnswerResult:
    """Answer result"""
    answer: str
    sources: List[Dict[str, Any]]
    confidence: float


class ExaAIClient:
    """
    Exa AI API client for AI-powered search and retrieval.

    API Documentation: https://exa.ai/docs/api
    Requires an API key from Exa AI.
    """

    BASE_URL = "https://api.exa.ai/v1"

    def __init__(self, api_key: str):
        """
        Initialize Exa AI client.

        Args:
            api_key: Exa AI API key
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

    async def create_task(
        self,
        query: str,
        task_type: str = "search",
        options: Optional[Dict[str, Any]] = None
    ) -> Task:
        """
        Create a new task.

        Args:
            query: Search query
            task_type: Type of task (search, retrieve, analyze)
            options: Additional options

        Returns:
            Task with task details

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "query": query,
                "type": task_type
            }

            if options:
                payload.update(options)

            async with self.session.post(
                f"{self.BASE_URL}/tasks",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 201:
                    raise Exception(f"Exa AI error: {data.get('error', 'Unknown error')}")

                return Task(
                    task_id=data["task_id"],
                    status=data["status"],
                    created_at=data["created_at"]
                )

        except Exception as e:
            raise Exception(f"Failed to create task: {str(e)}")

    async def search_url(
        self,
        query: str,
        num_results: int = 10,
        use_autoprompt: bool = True
    ) -> List[SearchResult]:
        """
        Search URLs based on query.

        Args:
            query: Search query
            num_results: Number of results to return
            use_autoprompt: Use automatic query enhancement

        Returns:
            List of SearchResult

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "query": query,
                "numResults": num_results,
                "useAutoprompt": use_autoprompt
            }

            async with self.session.post(
                f"{self.BASE_URL}/search",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Exa AI error: {data.get('error', 'Unknown error')}")

                results = [
                    SearchResult(
                        url=result["url"],
                        title=result.get("title", ""),
                        relevance_score=result.get("score", 0.0)
                    )
                    for result in data.get("results", [])
                ]

                return results

        except Exception as e:
            raise Exception(f"Failed to search URLs: {str(e)}")

    async def get_page_contents(
        self,
        urls: List[str],
        options: Optional[Dict[str, Any]] = None
    ) -> List[PageContent]:
        """
        Get contents of web pages.

        Args:
            urls: List of URLs to fetch content from
            options: Additional options (maxLength, etc.)

        Returns:
            List of PageContent

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {"urls": urls}

            if options:
                payload.update(options)

            async with self.session.post(
                f"{self.BASE_URL}/contents",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Exa AI error: {data.get('error', 'Unknown error')}")

                contents = [
                    PageContent(
                        url=content["url"],
                        content=content["text"],
                        title=content.get("title", "")
                    )
                    for content in data.get("results", [])
                ]

                return contents

        except Exception as e:
            raise Exception(f"Failed to get page contents: {str(e)}")

    async def search_contents(
        self,
        query: str,
        num_results: int = 10,
        include_content: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Search and get page contents in one call.

        Args:
            query: Search query
            num_results: Number of results
            include_content: Include full page content

        Returns:
            List of results with content

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "query": query,
                "numResults": num_results,
                "contents": include_content
            }

            async with self.session.post(
                f"{self.BASE_URL}/search_with_contents",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Exa AI error: {data.get('error', 'Unknown error')}")

                return data.get("results", [])

        except Exception as e:
            raise Exception(f"Failed to search contents: {str(e)}")

    async def get_answer(
        self,
        query: str,
        num_results: int = 5,
        use_autoprompt: bool = True
    ) -> AnswerResult:
        """
        Get an answer to a query with sources.

        Args:
            query: Question/query
            num_results: Number of sources to use
            use_autoprompt: Use automatic query enhancement

        Returns:
            AnswerResult with answer and sources

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "query": query,
                "numResults": num_results,
                "useAutoprompt": use_autoprompt
            }

            async with self.session.post(
                f"{self.BASE_URL}/answer",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Exa AI error: {data.get('error', 'Unknown error')}")

                return AnswerResult(
                    answer=data["answer"],
                    sources=data.get("sources", []),
                    confidence=data.get("confidence", 0.0)
                )

        except Exception as e:
            raise Exception(f"Failed to get answer: {str(e)}")