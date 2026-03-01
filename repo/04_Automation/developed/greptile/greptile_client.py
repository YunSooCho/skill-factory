"""
Greptile - Repository Query and Analysis API

Supports:
- Index Repository
- Query Repository
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class IndexStatus:
    """Repository index status"""
    repository_id: str
    status: str
    indexed_files: int
    last_updated: str


@dataclass
class QueryResult:
    """Query result from repository"""
    answer: str
    sources: List[Dict[str, Any]]
    confidence: float


class GreptileClient:
    """
    Greptile API client for repository indexing and querying.

    API Documentation: https://docs.greptile.com
    Requires an API key from Greptile.
    """

    BASE_URL = "https://api.greptile.com/v1"

    def __init__(self, api_key: str):
        """
        Initialize Greptile client.

        Args:
            api_key: Greptile API key
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

    async def index_repository(
        self,
        repository_url: str,
        branch: str = "main",
        git_provider: str = "github"
    ) -> IndexStatus:
        """
        Index a repository for querying.

        Args:
            repository_url: Repository URL or owner/repo
            branch: Branch to index (default: main)
            git_provider: Git provider (github, gitlab, etc.)

        Returns:
            IndexStatus with indexing details

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "repository_url": repository_url,
                "branch": branch,
                "git_provider": git_provider
            }

            async with self.session.post(
                f"{self.BASE_URL}/index",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Greptile error: {data.get('error', 'Unknown error')}")

                return IndexStatus(
                    repository_id=data["repository_id"],
                    status=data["status"],
                    indexed_files=data.get("indexed_files", 0),
                    last_updated=data.get("last_updated", "")
                )

        except Exception as e:
            raise Exception(f"Failed to index repository: {str(e)}")

    async def query_repositories(
        self,
        query: str,
        repositories: List[Dict[str, str]],
        session_id: Optional[str] = None
    ) -> QueryResult:
        """
        Query indexed repositories.

        Args:
            query: Natural language query
            repositories: List of repo dicts with url and branch
            session_id: Session ID for context continuation

        Returns:
            QueryResult with answer and sources

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "query": query,
                "repositories": repositories
            }

            if session_id:
                payload["session_id"] = session_id

            async with self.session.post(
                f"{self.BASE_URL}/query",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Greptile error: {data.get('error', 'Unknown error')}")

                return QueryResult(
                    answer=data["answer"],
                    sources=data.get("sources", []),
                    confidence=data.get("confidence", 0.0)
                )

        except Exception as e:
            raise Exception(f"Failed to query repositories: {str(e)}")