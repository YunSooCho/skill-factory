"""
Dub API - Link Management and Analytics Client

Supports 8 API Actions:
- Link operations (create, get, search, upsert, update, delete)
- Tag operations (create, update)

Triggers:
- Link clicked
- Link created
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Link:
    """Link entity"""
    id: str
    short_url: str
    long_url: str
    title: Optional[str] = None
    description: Optional[str] = None
    tags: List[str] = None
    clicks: int = 0
    created_at: str = ""
    updated_at: str = ""
    archived: bool = False


@dataclass
class Tag:
    """Tag entity"""
    id: str
    name: str
    color: Optional[str] = None
    created_at: str = ""


@dataclass
class Click:
    """Click analytics entity"""
    id: str
    link_id: str
    ip: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    device: Optional[str] = None
    browser: Optional[str] = None
    timestamp: str = ""


class DubClient:
    """
    Dub API client for link management and analytics.

    API Documentation: https://dub.co/docs
    Uses API Token for authentication.
    """

    BASE_URL = "https://api.dub.co"

    def __init__(self, api_token: str, workspace_id: Optional[str] = None):
        """
        Initialize Dub client.

        Args:
            api_token: API token for authentication
            workspace_id: Optional workspace ID (defaults to user's default)
        """
        self.api_token = api_token
        self.workspace_id = workspace_id
        self.session = None

    async def __aenter__(self):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_token}"
        }

        self.session = aiohttp.ClientSession(headers=headers)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def _get_base_path(self) -> str:
        """Get base API path with optional workspace"""
        if self.workspace_id:
            return f"{self.BASE_URL}/workspaces/{self.workspace_id}"
        return self.BASE_URL

    async def _handle_response(self, response: aiohttp.ClientResponse) -> Dict[str, Any]:
        """Handle API response"""
        data = await response.json()

        if response.status not in (200, 201, 202, 204):
            error_msg = data.get('error', {}).get('message', 'Unknown error')
            raise Exception(f"API Error [{response.status}]: {error_msg}")

        return data

    # ==================== Link Operations ====================

    async def create_link(
        self,
        long_url: str,
        short_code: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        domain: Optional[str] = None,
        public_stats: bool = False,
        password: Optional[str] = None,
        expires_at: Optional[str] = None
    ) -> Link:
        """Create a new short link"""
        payload = {"url": long_url}

        if short_code:
            payload["key"] = short_code
        if title:
            payload["title"] = title
        if description:
            payload["description"] = description
        if tags:
            payload["tags"] = tags
        if domain:
            payload["domain"] = domain
        if public_stats:
            payload["publicStats"] = public_stats
        if password:
            payload["password"] = password
        if expires_at:
            payload["expiresAt"] = expires_at

        async with self.session.post(
            f"{self._get_base_path()}/links",
            json=payload
        ) as response:
            data = await self._handle_response(response)

            return Link(
                id=str(data.get("id", "")),
                short_url=data.get("shortLink", ""),
                long_url=data.get("url", long_url),
                title=data.get("title"),
                description=data.get("description"),
                tags=data.get("tags", []),
                clicks=data.get("clicks", 0),
                created_at=data.get("createdAt", ""),
                updated_at=data.get("updatedAt", ""),
                archived=data.get("archived", False)
            )

    async def get_link(self, link_id: str) -> Optional[Link]:
        """Get link details by ID"""
        async with self.session.get(
            f"{self._get_base_path()}/links/{link_id}"
        ) as response:
            if response.status == 404:
                return None
            data = await self._handle_response(response)

            return Link(
                id=str(data.get("id", link_id)),
                short_url=data.get("shortLink", ""),
                long_url=data.get("url", ""),
                title=data.get("title"),
                description=data.get("description"),
                tags=data.get("tags", []),
                clicks=data.get("clicks", 0),
                created_at=data.get("createdAt", ""),
                updated_at=data.get("updatedAt", ""),
                archived=data.get("archived", False)
            )

    async def get_link_by_domain_key(
        self,
        domain: str,
        key: str
    ) -> Optional[Link]:
        """Get link by domain and key (short code)"""
        async with self.session.get(
            f"{self._get_base_path()}/links/info",
            params={"domain": domain, "key": key}
        ) as response:
            if response.status == 404:
                return None
            data = await self._handle_response(response)

            return Link(
                id=str(data.get("id", "")),
                short_url=data.get("shortLink", ""),
                long_url=data.get("url", ""),
                title=data.get("title"),
                description=data.get("description"),
                tags=data.get("tags", []),
                clicks=data.get("clicks", 0),
                created_at=data.get("createdAt", ""),
                updated_at=data.get("updatedAt", ""),
                archived=data.get("archived", False)
            )

    async def update_link(
        self,
        link_id: str,
        url: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        archived: Optional[bool] = None
    ) -> Optional[Link]:
        """Update link details"""
        payload = {}
        if url is not None:
            payload["url"] = url
        if title is not None:
            payload["title"] = title
        if description is not None:
            payload["description"] = description
        if tags is not None:
            payload["tags"] = tags
        if archived is not None:
            payload["archived"] = archived

        async with self.session.patch(
            f"{self._get_base_path()}/links/{link_id}",
            json=payload
        ) as response:
            if response.status == 404:
                return None
            data = await self._handle_response(response)

            return Link(
                id=str(data.get("id", link_id)),
                short_url=data.get("shortLink", ""),
                long_url=data.get("url", url or ""),
                title=data.get("title"),
                description=data.get("description"),
                tags=data.get("tags", []),
                clicks=data.get("clicks", 0),
                created_at=data.get("createdAt", ""),
                updated_at=data.get("updatedAt", ""),
                archived=data.get("archived", False)
            )

    async def upsert_link(
        self,
        domain: str,
        key: str,
        url: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Link:
        """Create or update a link by domain and key"""
        payload = {"url": url}

        if title:
            payload["title"] = title
        if description:
            payload["description"] = description
        if tags:
            payload["tags"] = tags

        async with self.session.put(
            f"{self._get_base_path()}/links",
            params={"domain": domain, "key": key},
            json=payload
        ) as response:
            data = await self._handle_response(response)

            return Link(
                id=str(data.get("id", "")),
                short_url=data.get("shortLink", ""),
                long_url=data.get("url", url),
                title=data.get("title"),
                description=data.get("description"),
                tags=data.get("tags", []),
                clicks=data.get("clicks", 0),
                created_at=data.get("createdAt", ""),
                updated_at=data.get("updatedAt", ""),
                archived=data.get("archived", False)
            )

    async def delete_link(self, link_id: str) -> bool:
        """Delete a link"""
        async with self.session.delete(
            f"{self._get_base_path()}/links/{link_id}"
        ) as response:
            if response.status == 404:
                return False
            await self._handle_response(response)
            return True

    async def search_links(
        self,
        query: Optional[str] = None,
        tag_ids: Optional[List[str]] = None,
        domain: Optional[str] = None,
        archived: Optional[bool] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Link]:
        """Search links"""
        params: Dict[str, Any] = {"limit": limit, "offset": offset}

        if query:
            params["searchQuery"] = query
        if tag_ids:
            params["tagIds"] = ",".join(tag_ids)
        if domain:
            params["domain"] = domain
        if archived is not None:
            params["archived"] = str(archived).lower()

        async with self.session.get(
            f"{self._get_base_path()}/links",
            params=params
        ) as response:
            data = await self._handle_response(response)
            links_data = data.get("result", [])

            return [
                Link(
                    id=str(l.get("id", "")),
                    short_url=l.get("shortLink", ""),
                    long_url=l.get("url", ""),
                    title=l.get("title"),
                    description=l.get("description"),
                    tags=l.get("tags", []),
                    clicks=l.get("clicks", 0),
                    created_at=l.get("createdAt", ""),
                    updated_at=l.get("updatedAt", ""),
                    archived=l.get("archived", False)
                )
                for l in links_data
            ]

    # ==================== Tag Operations ====================

    async def create_tag(
        self,
        name: str,
        color: Optional[str] = None
    ) -> Tag:
        """Create a new tag"""
        payload = {"name": name}
        if color:
            payload["color"] = color

        async with self.session.post(
            f"{self._get_base_path()}/tags",
            json=payload
        ) as response:
            data = await self._handle_response(response)

            return Tag(
                id=str(data.get("id", "")),
                name=data.get("name", name),
                color=data.get("color"),
                created_at=data.get("createdAt", "")
            )

    async def update_tag(
        self,
        tag_id: str,
        name: Optional[str] = None,
        color: Optional[str] = None
    ) -> Optional[Tag]:
        """Update tag details"""
        payload = {}
        if name is not None:
            payload["name"] = name
        if color is not None:
            payload["color"] = color

        async with self.session.patch(
            f"{self._get_base_path()}/tags/{tag_id}",
            json=payload
        ) as response:
            if response.status == 404:
                return None
            data = await self._handle_response(response)

            return Tag(
                id=str(data.get("id", tag_id)),
                name=data.get("name", name or ""),
                color=data.get("color"),
                created_at=data.get("createdAt", "")
            )

    async def delete_tag(self, tag_id: str) -> bool:
        """Delete a tag"""
        async with self.session.delete(
            f"{self._get_base_path()}/tags/{tag_id}"
        ) as response:
            if response.status == 404:
                return False
            await self._handle_response(response)
            return True

    async def list_tags(self) -> List[Tag]:
        """List all tags"""
        async with self.session.get(
            f"{self._get_base_path()}/tags"
        ) as response:
            data = await self._handle_response(response)
            tags_data = data.get("result", [])

            return [
                Tag(
                    id=str(t.get("id", "")),
                    name=t.get("name", ""),
                    color=t.get("color"),
                    created_at=t.get("createdAt", "")
                )
                for t in tags_data
            ]

    # ==================== Analytics Operations ====================

    async def get_clicks(
        self,
        link_id: str,
        start: Optional[str] = None,
        end: Optional[str] = None,
        limit: int = 100
    ) -> List[Click]:
        """Get click analytics for a link"""
        params = {"limit": limit}
        if start:
            params["start"] = start
        if end:
            params["end"] = end

        async with self.session.get(
            f"{self._get_base_path()}/links/{link_id}/clicks",
            params=params
        ) as response:
            data = await self._handle_response(response)
            clicks_data = data.get("result", [])

            return [
                Click(
                    id=str(c.get("id", "")),
                    link_id=str(c.get("linkId", link_id)),
                    ip=c.get("ip"),
                    city=c.get("city"),
                    country=c.get("country"),
                    device=c.get("device"),
                    browser=c.get("browser"),
                    timestamp=c.get("timestamp", "")
                )
                for c in clicks_data
            ]


# ==================== Example Usage ====================

async def main():
    """Example usage of Dub client"""

    # Example configuration - replace with your actual credentials
    api_token = "your_api_token"
    workspace_id = "your_workspace_id"  # Optional

    async with DubClient(api_token=api_token, workspace_id=workspace_id) as client:
        # Create a short link
        link = await client.create_link(
            long_url="https://example.com/long-url",
            short_code="mylink",
            title="My Short Link",
            description="This is my short link",
            tags=["marketing", "campaign"]
        )
        print(f"Link created: {link.short_url} -> {link.long_url}")

        # Get link
        link = await client.get_link(link.id)
        print(f"Link clicks: {link.clicks}")

        # Search links
        links = await client.search_links(query="marketing")
        print(f"Found {len(links)} links")

        # Create tag
        tag = await client.create_tag(name="promo", color="#FF0000")
        print(f"Tag created: {tag.name}")

        # Upsert link (create or update)
        link = await client.upsert_link(
            domain="dub.co",
            key="promo-link",
            url="https://example.com/promo",
            title="Promo Link"
        )
        print(f"Link upserted: {link.short_url}")


if __name__ == "__main__":
    asyncio.run(main())