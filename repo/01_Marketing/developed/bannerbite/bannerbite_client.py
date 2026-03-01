"""
Bannerbite API - Media Generation Client

Actions: 5 (Get Bite, Render Media, Get Project, Search Bites, List Projects)
Trigger: 1 (Webhook)
"""

import aiohttp
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class Project:
    """Bannerbite project"""
    id: str
    name: str
    created_at: str


@dataclass
class Bite:
    """Bannerbite bite/media item"""
    id: str
    project_id: str
    status: str
    url: str = ""


@dataclass
class Media:
    """Rendered media"""
    id: str
    project_id: str
    render_url: str
    status: str


class BannerbiteClient:
    """Bannerbite API client"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers={
            "X-API-Key": self.api_key
        })
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    # Projects
    async def list_projects(
        self,
        limit: int = 50
    ) -> List[Project]:
        async with self.session.get(
            "https://api.bannerbite.com/v1/projects",
            params={"limit": limit}
        ) as response:
            data = await response.json()
            return [
                Project(
                    id=p.get("id", ""),
                    name=p.get("name", ""),
                    created_at=p.get("created_at", "")
                )
                for p in data.get("projects", [])
            ]

    async def get_project(self, project_id: str) -> Project:
        async with self.session.get(
            f"https://api.bannerbite.com/v1/projects/{project_id}"
        ) as response:
            data = await response.json()
            return Project(
                id=data.get("id", ""),
                name=data.get("name", ""),
                created_at=data.get("created_at", "")
            )

    # Bites
    async def search_bites(
        self,
        project_id: str
    ) -> List[Bite]:
        async with self.session.get(
            f"https://api.bannerbite.com/v1/projects/{project_id}/bites"
        ) as response:
            data = await response.json()
            return [
                Bite(
                    id=b.get("id", ""),
                    project_id=project_id,
                    status=b.get("status", ""),
                    url=b.get("url", "")
                )
                for b in data.get("bites", [])
            ]

    async def get_bite(self, bite_id: str) -> Bite:
        async with self.session.get(
            f"https://api.bannerbite.com/v1/bites/{bite_id}"
        ) as response:
            data = await response.json()
            return Bite(
                id=data.get("id", ""),
                project_id=data.get("project_id", ""),
                status=data.get("status", ""),
                url=data.get("url", "")
            )

    # Media Render
    async def render_media(
        self,
        project_id: str,
        bite_id: str,
        **kwargs
    ) -> Media:
        payload = {
            "project_id": project_id,
            "bite_id": bite_id,
            **kwargs
        }
        async with self.session.post(
            "https://api.bannerbite.com/v1/media/render",
            json=payload
        ) as response:
            data = await response.json()
            return Media(
                id=data.get("id", ""),
                project_id=project_id,
                render_url=data.get("render_url", ""),
                status=data.get("status", "")
            )


async def main():
    async with BannerbiteClient("test_key") as client:
        projects = await client.list_projects()
        print(f"Projects: {len(projects)}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())