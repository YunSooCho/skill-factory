"""
Phantombuster - Web Scraping API

Supports:
- Launch Phantom
- Get Phantom's Output
- Schedule Phantom Launch
- Get Result Object by Container ID
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class PhantomLaunch:
    """Phantom launch result"""
    id: str
    phantom_id: str
    status: str
    created_at: str


@dataclass
class PhantomOutput:
    """Phantom output result"""
    id: str
    status: str
    results: Optional[List[Dict[str, Any]]]
    errors: Optional[List[str]]


@dataclass
class ScheduledLaunch:
    """Scheduled launch result"""
    id: str
    schedule: str
    phantom_id: str
    status: str


class PhantombusterClient:
    """
    Phantombuster API client for web scraping.

    API Documentation: https://phantombuster.com/api
    Requires an API key from Phantombuster.
    """

    BASE_URL = "https://phantombuster.com/api/v2"

    def __init__(self, api_key: str):
        """
        Initialize Phantombuster client.

        Args:
            api_key: Phantombuster API key
        """
        self.api_key = api_key
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={"X-Phantombuster-Key": self.api_key}
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def launch_phantom(
        self,
        phantom_id: str,
        args: Dict[str, Any],
        container_id: Optional[str] = None
    ) -> PhantomLaunch:
        """
        Launch a phantom scraping task.

        Args:
            phantom_id: Phantom ID to launch
            args: Arguments for the phantom
            container_id: Container ID for organization (optional)

        Returns:
            PhantomLaunch with launch data

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "id": phantom_id,
                "args": args
            }

            if args:
                payload["argument"] = args

            async with self.session.post(
                f"{self.BASE_URL}/agents/launch",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200 or not data.get("success"):
                    raise Exception(f"Phantombuster error: {data.get('message', 'Unknown error')}")

                return PhantomLaunch(
                    id=data.get("containerId", ""),
                    phantom_id=phantom_id,
                    status="launched",
                    created_at=""
                )

        except Exception as e:
            raise Exception(f"Failed to launch phantom: {str(e)}")

    async def get_phantom_output(
        self,
        container_id: str
    ) -> PhantomOutput:
        """
        Get output from a phantom run.

        Args:
            container_id: Container ID of the run

        Returns:
            PhantomOutput with results

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            async with self.session.get(
                f"{self.BASE_URL}/agents/{container_id}/fetch"
            ) as response:
                data = await response.json()

                if response.status != 200 or not data.get("success"):
                    raise Exception(f"Phantombuster error: {data.get('message', 'Unknown error')}")

                return PhantomOutput(
                    id=container_id,
                    status=data.get("status", "unknown"),
                    results=data.get("output"),
                    errors=data.get("error")
                )

        except Exception as e:
            raise Exception(f"Failed to get phantom output: {str(e)}")

    async def schedule_phantom_launch(
        self,
        phantom_id: str,
        args: Dict[str, Any],
        interval: str = "hourly"
    ) -> ScheduledLaunch:
        """
        Schedule recurring phantom launches.

        Args:
            phantom_id: Phantom ID
            args: Arguments for the phantom
            interval: Schedule interval

        Returns:
            ScheduledLaunch with schedule details

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "id": phantom_id,
                "interval": interval,
                "argument": args
            }

            async with self.session.post(
                f"{self.BASE_URL}/agents/launch/schedule",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200 or not data.get("success"):
                    raise Exception(f"Phantombuster error: {data.get('message', 'Unknown error')}")

                return ScheduledLaunch(
                    id=data.get("scheduleId", ""),
                    schedule=interval,
                    phantom_id=phantom_id,
                    status="scheduled"
                )

        except Exception as e:
            raise Exception(f"Failed to schedule phantom: {str(e)}")

    async def get_result_object(
        self,
        container_id: str,
        object_id: str
    ) -> Dict[str, Any]:
        """
        Get a specific result object.

        Args:
            container_id: Container ID
            object_id: Object ID within container

        Returns:
            Result object data

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            async with self.session.get(
                f"{self.BASE_URL}/containers/{container_id}/objects/{object_id}"
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Phantombuster error: {data.get('error', 'Unknown error')}")

                return data

        except Exception as e:
            raise Exception(f"Failed to get result object: {str(e)}")