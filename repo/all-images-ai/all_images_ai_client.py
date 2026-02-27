"""
All Images AI - Image Generation Client

Supports:
- Create Image Generation
- Get Image Generation
- Get Image (download)
- Search Image Generation
- Delete Image Generation
Trigger:
- Print Completed
"""

import aiohttp
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class ImageGeneration:
    """Image generation entity"""
    generation_id: str
    prompt: str
    status: str
    url: Optional[str] = ""
    created_at: str = ""


class AllImagesAIClient:
    """
    All Images AI client for image generation.
    Uses API key authentication.
    """

    BASE_URL = "https://api.allimages.ai/api"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers={
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    # ==================== Image Generation ====================

    async def create_image_generation(
        self,
        prompt: str,
        **kwargs
    ) -> ImageGeneration:
        """Create a new image generation"""
        payload = {"prompt": prompt}
        payload.update(kwargs)

        async with self.session.post(
            f"{self.BASE_URL}/generations",
            json=payload
        ) as response:
            data = await response.json()

            if response.status not in (200, 201):
                raise Exception(f"Failed: {data}")

            return ImageGeneration(
                generation_id=data.get("id", ""),
                prompt=prompt,
                status=data.get("status", "pending"),
                url=data.get("url"),
                created_at=data.get("created_at", "")
            )

    async def get_image_generation(self, generation_id: str) -> ImageGeneration:
        """Get generation status"""
        async with self.session.get(
            f"{self.BASE_URL}/generations/{generation_id}"
        ) as response:
            data = await response.json()

            return ImageGeneration(
                generation_id=generation_id,
                prompt=data.get("prompt", ""),
                status=data.get("status", ""),
                url=data.get("url"),
                created_at=data.get("created_at", "")
            )

    async def search_image_generations(
        self,
        kwargs: Optional[Dict] = None
    ) -> List[ImageGeneration]:
        """Search generations"""
        async with self.session.get(
            f"{self.BASE_URL}/generations/search",
            params=kwargs or {}
        ) as response:
            data = await response.json()
            return [
                ImageGeneration(
                    generation_id=g.get("id", ""),
                    prompt=g.get("prompt", ""),
                    status=g.get("status", ""),
                    url=g.get("url"),
                    created_at=g.get("created_at", "")
                )
                for g in data.get("generations", [])
            ]

    async def get_image(self, generation_id: str) -> bytes:
        """Download image"""
        gen = await self.get_image_generation(generation_id)

        if not gen.url:
            raise ValueError("No URL available")

        async with self.session.get(gen.url) as response:
            if response.status == 200:
                return await response.read()

    async def delete_image_generation(self, generation_id: str) -> bool:
        """Delete generation"""
        async with self.session.delete(
            f"{self.BASE_URL}/generations/{generation_id}"
        ) as response:
            return response.status == 200


async def main():
    async with AllImagesAIClient(api_key="test") as client:
        gen = await client.create_image_generation("test prompt")
        print(f"Created: {gen.generation_id}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())