"""
Bannerbear API - Image/Video Generation Client

Actions: 11 (Create, Get operations for images, videos, movies, collections, screenshots)
Triggers: 6 (Creation events via webhooks)
"""

import aiohttp
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class Generation:
    """Bannerbear generation result"""
    uid: str
    status: str
    image_url: str = ""
    created_at: str = ""


class BannerbearClient:
    """Bannerbear API client"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers={
            "Authorization": f"Bearer {self.api_key}"
        })
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    # Image
    async def create_image(
        self,
        template: str,
        modifications: List[Dict]
    ) -> Generation:
        payload = {"template": template, "modifications": modifications}
        async with self.session.post(
            "https://api.bannerbear.com/v2/images",
            json=payload
        ) as response:
            data = await response.json()
            return Generation(
                uid=data.get("uid", ""),
                status=data.get("status", ""),
                image_url=data.get("image_url", ""),
                created_at=data.get("created_at", "")
            )

    async def create_video(
        self,
        template: str,
        modifications: List[Dict]
    ) -> Generation:
        payload = {"template": template, "modifications": modifications}
        async with self.session.post(
            "https://api.bannerbear.com/v2/videos",
            json=payload
        ) as response:
            data = await response.json()
            return Generation(uid=data.get("uid", ""), status=data.get("status", ""))

    # Details
    async def get_image(self, uid: str) -> Generator:
        async with self.session.get(f"https://api.bannerbear.com/v2/images/{uid}") as response:
            data = await response.json()
            return Generation(
                uid=uid,
                status=data.get("status", ""),
                image_url=data.get("image_url", "")
            )

    async def get_video(self, uid: str) -> Generator:
        async with self.session.get(f"https://api.bannerbear.com/v2/videos/{uid}") as response:
            data = await response.json()
            return Generation(uid=uid, status=data.get("status", ""))

    async def get_collection(self, uid: str) -> Dict:
        async with self.session.get(f"https://api.bannerbear.com/v2/collections/{uid}") as response:
            return await response.json()

    async def create_collection(
        self,
        templates: List[str],
        modifications: List[Dict]
    ) -> Generation:
        payload = {"templates": templates, "modifications": modifications}
        async with self.session.post(
            "https://api.bannerbear.com/v2/collections",
            json=payload
        ) as response:
            data = await response.json()
            return Generation(uid=data.get("uid", ""), status="processing")

    # Screenshots
    async def create_screenshot(self, url: str, **kwargs) -> Generation:
        payload = {"url": url, **kwargs}
        async with self.session.post(
            "https://api.bannerbear.com/v2/screenshots",
            json=payload
        ) as response:
            data = await response.json()
            return Generation(
                uid=data.get("uid", ""),
                status=data.get("status", ""),
                image_url=data.get("image_url", "")
            )

    async def get_screenshot(self, uid: str) -> Generator:
        async with self.session.get(f"https://api.bannerbear.com/v2/screenshots/{uid}") as response:
            data = await response.json()
            return Generation(
                uid=uid,
                status=data.get("status", ""),
                image_url=data.get("image_url", "")
            )

    # Movies
    async def create_movie(self, frames: List[Dict]) -> Generation:
        payload = {"frames": frames}
        async with self.session.post(
            "https://api.bannerbear.com/v2/movies",
            json=payload
        ) as response:
            data = await response.json()
            return Generation(uid=data.get("uid", ""), status="processing")

    async def get_movie(self, uid: str) -> Generator:
        async with self.session.get(f"https://api.bannerbear.com/v2/movies/{uid}") as response:
            data = await response.json()
            return Generation(uid=uid, status=data.get("status", ""))

    # File data
    async def get_file_data(self, uid: str) -> bytes:
        gen = await self.get_image(uid)
        if gen.image_url:
            async with self.session.get(gen.image_url) as response:
                return await response.read()


async def main():
    async with BannerbearClient("test_key") as client:
        collection = await client.create(["template1"], [])
        print(f"Collection: {collection.uid}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())