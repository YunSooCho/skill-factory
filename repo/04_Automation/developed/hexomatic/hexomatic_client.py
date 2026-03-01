"""
Hexomatic - Web Automation Platform API

Supports webhooks and workflow triggers for automation.
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any


class HexomaticClient:
    """
    Hexomatic API client for web automation workflows.

    API Documentation: https://developers.hexomatic.com/api
    Requires an API key from Hexomatic.
    """

    BASE_URL = "https://api.hexomatic.com/v1"

    def __init__(self, api_key: str):
        """
        Initialize Hexomatic client.

        Args:
            api_key: Hexomatic API key
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

    async def trigger_workflow(
        self,
        workflow_id: str,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Trigger a workflow execution.

        Args:
            workflow_id: Workflow ID to trigger
            data: Input data for workflow

        Returns:
            Triggered workflow details

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {"workflow_id": workflow_id}

            if data:
                payload["data"] = data

            async with self.session.post(
                f"{self.BASE_URL}/workflows/trigger",
                json=payload
            ) as response:
                result = await response.json()

                if response.status != 200:
                    raise Exception(f"Hexomatic error: {result.get('error', 'Unknown error')}")

                return result

        except Exception as e:
            raise Exception(f"Failed to trigger workflow: {str(e)}")

    async def get_workflow_status(
        self,
        execution_id: str
    ) -> Dict[str, Any]:
        """
        Get status of a workflow execution.

        Args:
            execution_id: Execution ID

        Returns:
            Workflow execution status

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            async with self.session.get(
                f"{self.BASE_URL}/workflows/executions/{execution_id}"
            ) as response:
                result = await response.json()

                if response.status != 200:
                    raise Exception(f"Hexomatic error: {result.get('error', 'Unknown error')}")

                return result

        except Exception as e:
            raise Exception(f"Failed to get workflow status: {str(e)}")

    async def list_workflows(
        self,
        page: int = 1,
        limit: int = 20
    ) -> Dict[str, Any]:
        """
        List available workflows.

        Args:
            page: Page number
            limit: Items per page

        Returns:
            List of workflows

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            params = {
                "page": page,
                "limit": limit
            }

            async with self.session.get(
                f"{self.BASE_URL}/workflows",
                params=params
            ) as response:
                result = await response.json()

                if response.status != 200:
                    raise Exception(f"Hexomatic error: {result.get('error', 'Unknown error')}")

                return result

        except Exception as e:
            raise Exception(f"Failed to list workflows: {str(e)}")