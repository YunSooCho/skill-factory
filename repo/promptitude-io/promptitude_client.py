"""
Promptitude - Prompt Management API

Supports:
- Generate Text from Prompt
- Rate Prompt Output
- Manage Content
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class GeneratedText:
    """Generated text result"""
    id: str
    text: str
    model: str
    created_at: str


@dataclass
class Prompt:
    """Prompt representation"""
    id: str
    name: str
    content: str
    created_at: str


class PromptitudeClient:
    """
    Promptitude API client for prompt management.

    API Documentation: https://promptitude.io/docs/api
    Requires an API key from Promptitude.
    """

    BASE_URL = "https://api.promptitude.io/v1"

    def __init__(self, api_key: str):
        """
        Initialize Promptitude client.

        Args:
            api_key: Promptitude API key
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

    async def generate_text_from_prompt(
        self,
        prompt_id: str,
        variables: Optional[Dict[str, Any]] = None,
        model: Optional[str] = None
    ) -> GeneratedText:
        """
        Generate text using a prompt template.

        Args:
            prompt_id: Prompt ID to use
            variables: Variables to fill in prompt
            model: Model to use (optional)

        Returns:
            GeneratedText with result

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "prompt_id": prompt_id
            }

            if variables:
                payload["variables"] = variables
            if model:
                payload["model"] = model

            async with self.session.post(
                f"{self.BASE_URL}/generate",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Promptitude error: {data.get('error', 'Unknown error')}")

                return GeneratedText(
                    id=data["id"],
                    text=data["text"],
                    model=data.get("model", ""),
                    created_at=data.get("created_at", "")
                )

        except Exception as e:
            raise Exception(f"Failed to generate text: {str(e)}")

    async def rate_prompt_output(
        self,
        generation_id: str,
        rating: int,
        feedback: Optional[str] = None
    ) -> bool:
        """
        Rate a prompt generation output.

        Args:
            generation_id: Generation ID to rate
            rating: Rating (1-5)
            feedback: Optional feedback text

        Returns:
            True if successful

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "generation_id": generation_id,
                "rating": rating
            }

            if feedback:
                payload["feedback"] = feedback

            async with self.session.post(
                f"{self.BASE_URL}/rate",
                json=payload
            ) as response:
                if response.status != 200:
                    data = await response.json()
                    raise Exception(f"Promptitude error: {data.get('error', 'Unknown error')}")

                return True

        except Exception as e:
            raise Exception(f"Failed to rate prompt output: {str(e)}")

    async def manage_content(
        self,
        content_type: str,
        content_id: str,
        data: Dict[str, Any],
        operation: str = "update"
    ) -> Dict[str, Any]:
        """
        Manage prompt content.

        Args:
            content_type: Type of content (prompt, template)
            content_id: Content ID
            data: Content data
            operation: Operation (create, update, delete)

        Returns:
            Result data

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "type": content_type,
                "operation": operation,
                "data": data
            }

            async with self.session.post(
                f"{self.BASE_URL}/content/{content_id}",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Promptitude error: {data.get('error', 'Unknown error')}")

                return data

        except Exception as e:
            raise Exception(f"Failed to manage content: {str(e)}")