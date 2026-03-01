"""
ParseHub - Web Scraping Platform API

Supports:
- Get Project
- Run Project
- Get Extracted Data
- Delete Run
- Cancel Run
- Get Project List
- Get Last Ready Data
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class Project:
    """Project representation"""
    project_key: str
    title: str
    last_run: str
    status: str


@dataclass
class Run:
    """Project run representation"""
    run_key: str
    project_key: str
    status: str
    ready: bool
    finish_time: Optional[str]


@dataclass
class ExtractedData:
    """Extracted data from project"""
    run_key: str
    data: List[Dict[str, Any]]


class ParseHubClient:
    """
    ParseHub API client for web scraping projects.

    API Documentation: https://www.parsehub.com/docs/api
    Requires an API key from ParseHub.
    """

    BASE_URL = "https://www.parsehub.com/api/v2"

    def __init__(self, api_key: str):
        """
        Initialize ParseHub client.

        Args:
            api_key: ParseHub API key
        """
        self.api_key = api_key
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def _get_params(self, **kwargs) -> Dict[str, str]:
        """Get API params with api_key"""
        params = {"api_key": self.api_key}
        params.update(kwargs)
        return params

    async def get_project(self, project_key: str) -> Project:
        """
        Get project details.

        Args:
            project_key: Project key

        Returns:
            Project with project data

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            params = self._get_params()

            async with self.session.get(
                f"{self.BASE_URL}/project/{project_key}",
                params=params
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"ParseHub error: {data.get('error', 'Unknown error')}")

                return Project(
                    project_key=data["project_key"],
                    title=data.get("title", ""),
                    last_run=data.get("last_run", ""),
                    status=data.get("status", "")
                )

        except Exception as e:
            raise Exception(f"Failed to get project: {str(e)}")

    async def list_projects(self) -> List[Project]:
        """
        List all projects.

        Returns:
            List of Project

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            params = self._get_params()

            async with self.session.get(
                f"{self.BASE_URL}/projects",
                params=params
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"ParseHub error: {data.get('error', 'Unknown error')}")

                projects = [
                    Project(
                        project_key=proj["project_key"],
                        title=proj.get("title", ""),
                        last_run=proj.get("last_run", ""),
                        status=proj.get("status", "")
                    )
                    for proj in data.get("projects", [])
                ]

                return projects

        except Exception as e:
            raise Exception(f"Failed to list projects: {str(e)}")

    async def run_project(
        self,
        project_key: str,
        start_url: Optional[str] = None,
        start_template: Optional[str] = None
    ) -> Run:
        """
        Run a scraping project.

        Args:
            project_key: Project key
            start_url: Optional start URL
            start_template: Optional start template

        Returns:
            Run with run data

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            params = self._get_params()

            if start_url:
                params["start_url"] = start_url
            if start_template:
                params["start_template"] = start_template

            async with self.session.post(
                f"{self.BASE_URL}/project/{project_key}/run",
                params=params
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"ParseHub error: {data.get('error', 'Unknown error')}")

                return Run(
                    run_key=data["run_key"],
                    project_key=project_key,
                    status=data.get("status", ""),
                    ready=data.get("ready", False),
                    finish_time=data.get("finish_time")
                )

        except Exception as e:
            raise Exception(f"Failed to run project: {str(e)}")

    async def get_run(self, project_key: str, run_key: str) -> Run:
        """
        Get run status.

        Args:
            project_key: Project key
            run_key: Run key

        Returns:
            Run with run data

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            params = self._get_params()

            async with self.session.get(
                f"{self.BASE_URL}/run/{run_key}",
                params=params
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"ParseHub error: {data.get('error', 'Unknown error')}")

                return Run(
                    run_key=data["run_key"],
                    project_key=data.get("project_key", project_key),
                    status=data.get("status", ""),
                    ready=data.get("ready", False),
                    finish_time=data.get("finish_time")
                )

        except Exception as e:
            raise Exception(f"Failed to get run: {str(e)}")

    async def cancel_run(self, project_key: str, run_key: str) -> bool:
        """
        Cancel a running project.

        Args:
            project_key: Project key
            run_key: Run key

        Returns:
            True if successful

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            params = self._get_params()

            async with self.session.put(
                f"{self.BASE_URL}/run/{run_key}/cancel",
                params=params
            ) as response:
                if response.status != 200:
                    data = await response.json()
                    raise Exception(f"ParseHub error: {data.get('error', 'Unknown error')}")

                return True

        except Exception as e:
            raise Exception(f"Failed to cancel run: {str(e)}")

    async def delete_run(self, project_key: str, run_key: str) -> bool:
        """
        Delete a run.

        Args:
            project_key: Project key
            run_key: Run key

        Returns:
            True if successful

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            params = self._get_params()

            async with self.session.delete(
                f"{self.BASE_URL}/run/{run_key}",
                params=params
            ) as response:
                if response.status != 200:
                    data = await response.json()
                    raise Exception(f"ParseHub error: {data.get('error', 'Unknown error')}")

                return True

        except Exception as e:
            raise Exception(f"Failed to delete run: {str(e)}")

    async def get_extracted_data(
        self,
        project_key: str,
        run_key: str,
        format: str = "json"
    ) -> ExtractedData:
        """
        Get extracted data from a run.

        Args:
            project_key: Project key
            run_key: Run key
            format: Output format (json, csv)

        Returns:
            ExtractedData with data

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            params = self._get_params(format=format)

            async with self.session.get(
                f"{self.BASE_URL}/runs/{run_key}/data",
                params=params
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"ParseHub error: {data.get('error', 'Unknown error')}")

                return ExtractedData(
                    run_key=run_key,
                    data=data
                )

        except Exception as e:
            raise Exception(f"Failed to get extracted data: {str(e)}")

    async def get_last_ready_data(
        self,
        project_key: str,
        format: str = "json"
    ) -> ExtractedData:
        """
        Get data from the last ready run.

        Args:
            project_key: Project key
            format: Output format (json, csv)

        Returns:
            ExtractedData with data

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            params = self._get_params(format=format)

            async with self.session.get(
                f"{self.BASE_URL}/projects/{project_key}/last_ready_run/data",
                params=params
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"ParseHub error: {data.get('error', 'Unknown error')}")

                return ExtractedData(
                    run_key=project_key,
                    data=data
                )

        except Exception as e:
            raise Exception(f"Failed to get last ready data: {str(e)}")