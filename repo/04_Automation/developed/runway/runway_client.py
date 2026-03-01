"""
Runway - AI Video Generation API

Supports:
- Create Video
- Get Task
- Delete Task
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class VideoTask:
    """Video task representation"""
    task_id: str
    status: str
    video_url: Optional[str]
    created_at: str


class RunwayClient:
    """
    Runway API client for AI video generation.

    API Documentation: https://dev.runwayml.com/api
    Requires an API key from Runway.
    """

    BASE_URL = "https://api.runwayml.com/v1"

    def __init__(self, api_key: str):
        """
        Initialize Runway client.

        Args:
            api_key: Runway API key
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

    async def create_video(
        self,
        prompt: str,
        model: str = "gen3a_turbo",
        duration: int = 5,
        options: Optional[Dict[str, Any]] = None
    ) -> VideoTask:
        """
        Create a video generation task.

        Args:
            prompt: Text prompt for video generation
            model: Model to use (gen3a_turbo, gen3a, etc.)
            duration: Video duration in seconds
            options: Additional options (aspect_ratio, etc.)

        Returns:
            VideoTask with task details

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "prompt": prompt,
                "model": model,
                "duration": duration
            }

            if options:
                payload.update(options)

            async with self.session.post(
                f"{self.BASE_URL}/tasks/text-to-video",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 201:
                    raise Exception(f"Runway error: {data.get('error', 'Unknown error')}")

                return VideoTask(
                    task_id=data["id"],
                    status=data["status"],
                    video_url=data.get("output"),
                    created_at=data.get("createdAt", "")
                )

        except Exception as e:
            raise Exception(f"Failed to create video task: {str(e)}")

    async def get_task(self, task_id: str) -> VideoTask:
        """
        Get task status and details.

        Args:
            task_id: Task ID

        Returns:
            VideoTask with task data

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            async with self.session.get(
                f"{self.BASE_URL}/tasks/{task_id}"
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Runway error: {data.get('error', 'Unknown error')}")

                return VideoTask(
                    task_id=data["id"],
                    status=data["status"],
                    video_url=data.get("output"),
                    created_at=data.get("createdAt", "")
                )

        except Exception as e:
            raise Exception(f"Failed to get task: {str(e)}")

    async def delete_task(self, task_id: str) -> bool:
        """
        Delete a task.

        Args:
            task_id: Task ID

        Returns:
            True if successful

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            async with self.session.delete(
                f"{self.BASE_URL}/tasks/{task_id}"
            ) as response:
                if response.status != 204:
                    data = await response.json()
                    raise Exception(f"Runway error: {data.get('error', 'Unknown error')}")

                return True

        except Exception as e:
            raise Exception(f"Failed to delete task: {str(e)}")