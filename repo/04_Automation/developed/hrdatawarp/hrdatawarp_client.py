"""
Hrdatawarp - HR Data Processing API

Supports:
- Project Execution (File)
- Project Execution (JSON)
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class ProjectResult:
    """Project execution result"""
    project_id: str
    status: str
    result_url: Optional[str]


class HrdatawarpClient:
    """
    Hrdatawarp API client for HR data processing.

    API Documentation: https://developers.hrdatawarp.com/api
    Requires an API key from Hrdatawarp.
    """

    BASE_URL = "https://api.hrdatawarp.com/v1"

    def __init__(self, api_key: str):
        """
        Initialize Hrdatawarp client.

        Args:
            api_key: Hrdatawarp API key
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

    async def run_project_file(
        self,
        project_id: str,
        file_url: str,
        options: Optional[Dict[str, Any]] = None
    ) -> ProjectResult:
        """
        Process HR data project with file input.

        Args:
            project_id: Project ID to run
            file_url: URL of input data file
            options: Additional processing options

        Returns:
            ProjectResult with execution details

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "project_id": project_id,
                "file_url": file_url
            }

            if options:
                payload.update(options)

            async with self.session.post(
                f"{self.BASE_URL}/projects/run/file",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Hrdatawarp error: {data.get('error', 'Unknown error')}")

                return ProjectResult(
                    project_id=data["project_id"],
                    status=data["status"],
                    result_url=data.get("result_url")
                )

        except Exception as e:
            raise Exception(f"Failed to run project with file: {str(e)}")

    async def run_project_json(
        self,
        project_id: str,
        json_data: Dict[str, Any],
        options: Optional[Dict[str, Any]] = None
    ) -> ProjectResult:
        """
        Process HR data project with JSON input.

        Args:
            project_id: Project ID to run
            json_data: Input data as JSON
            options: Additional processing options

        Returns:
            ProjectResult with execution details

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "project_id": project_id,
                "data": json_data
            }

            if options:
                payload.update(options)

            async with self.session.post(
                f"{self.BASE_URL}/projects/run/json",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Hrdatawarp error: {data.get('error', 'Unknown error')}")

                return ProjectResult(
                    project_id=data["project_id"],
                    status=data["status"],
                    result_url=data.get("result_url")
                )

        except Exception as e:
            raise Exception(f"Failed to run project with JSON: {str(e)}")

    async def get_project_result(
        self,
        execution_id: str
    ) -> Dict[str, Any]:
        """
        Get project execution result.

        Args:
            execution_id: Execution ID

        Returns:
            Project result data

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            async with self.session.get(
                f"{self.BASE_URL}/projects/executions/{execution_id}"
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Hrdatawarp error: {data.get('error', 'Unknown error')}")

                return data

        except Exception as e:
            raise Exception(f"Failed to get project result: {str(e)}")