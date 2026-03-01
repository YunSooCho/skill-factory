"""
Canva API - Design Platform Client

Supports:
- List Folder Items
- Get Design Download Link
- Search Design
- Create Folder
- Move Folder Item
- Rename Folder
- Create Export Job
- List Folders
Plus webhooks for: Design Updated
"""

import aiohttp
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class Folder:
    """Canva folder"""
    id: str
    name: str
    created_at: str
    updated_at: str


@dataclass
class Design:
    """Canva design"""
    id: str
    name: str
    title: str
    thumbnail_url: str
    design_url: str
    created_at: str
    updated_at: str
    design_type: str
    folder_id: Optional[str]


@dataclass
class FolderItem:
    """Item in a folder (design or subfolder)"""
    type: str  # 'design' or 'folder'
    id: str
    name: str
    created_at: str


@dataclass
class DownloadLink:
    """Design download link"""
    url: str
    expires_at: str
    format: str


@dataclass
class ExportJob:
    """Export job status"""
    job_id: str
    status: str  # 'in_progress', 'completed', 'failed'
    download_url: Optional[str]
    progress: float


@dataclass
class DesignResult:
    """Design search result"""
    designs: List[Design]
    total: int
    page: int
    page_size: int


class CanvaAPIClient:
    """
    Canva API client for design operations.

    API Documentation: https://www.canva.com/developers/api-docs/
    """

    BASE_URL = "https://api.canva.com/rest/v1"

    def __init__(self, api_key: str, base_url: Optional[str] = None):
        """
        Initialize Canva API client.

        Args:
            api_key: Canva API key from developer portal
            base_url: Custom base URL (optional)
        """
        self.api_key = api_key
        self.BASE_URL = base_url or self.BASE_URL
        self.session = None

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=self._get_headers())
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def list_folders(
        self,
        team_id: Optional[str] = None,
        limit: int = 50
    ) -> Dict[str, Any]:
        """
        List all folders.

        Args:
            team_id: Optional team ID
            limit: Maximum results (default: 50)

        Returns:
            Dict with folders list

        Raises:
            aiohttp.ClientError: If request fails
        """
        params = {"limit": limit}

        if team_id:
            params["team_id"] = team_id

        async with self.session.get(
            f"{self.BASE_URL}/folders",
            params=params
        ) as response:
            data = await response.json()

            if response.status != 200:
                error_msg = data.get("error", {}).get("message", str(data))
                raise Exception(f"Canva List Folders error: {error_msg}")

            folders = [
                Folder(
                    id=f.get("id", ""),
                    name=f.get("name", ""),
                    created_at=f.get("created_at", ""),
                    updated_at=f.get("updated_at", "")
                )
                for f in data.get("folders", [])
            ]

            return {
                "folders": folders,
                "total": len(folders)
            }

    async def list_folder_items(
        self,
        folder_id: str,
        item_type: Optional[str] = None,
        limit: int = 50
    ) -> Dict[str, Any]:
        """
        List items in a folder.

        Args:
            folder_id: Folder ID
            item_type: Optional filter by type ('design' or 'folder')
            limit: Maximum results (default: 50)

        Returns:
            Dict with folder items

        Raises:
            ValueError: If folder_id is empty
            aiohttp.ClientError: If request fails
        """
        if not folder_id:
            raise ValueError("Folder ID cannot be empty")

        params = {"limit": limit}

        if item_type:
            params["type"] = item_type

        async with self.session.get(
            f"{self.BASE_URL}/folders/{folder_id}/items",
            params=params
        ) as response:
            data = await response.json()

            if response.status != 200:
                error_msg = data.get("error", {}).get("message", str(data))
                raise Exception(f"Canva List Folder Items error: {error_msg}")

            items = [
                FolderItem(
                    type=item.get("type", ""),
                    id=item.get("id", ""),
                    name=item.get("name", ""),
                    created_at=item.get("created_at", "")
                )
                for item in data.get("items", [])
            ]

            return {
                "items": items,
                "total": len(items),
                "folder_id": folder_id
            }

    async def get_design_download_link(
        self,
        design_id: str,
        format: str = "pdf",
        quality: str = "standard"
    ) -> DownloadLink:
        """
        Get a download link for a design.

        Args:
            design_id: Design ID
            format: Export format ('pdf', 'png', 'jpg')
            quality: Export quality ('standard', 'high')

        Returns:
            DownloadLink with download URL

        Raises:
            ValueError: If design_id is empty
            aiohttp.ClientError: If request fails
        """
        if not design_id:
            raise ValueError("Design ID cannot be empty")

        async with self.session.get(
            f"{self.BASE_URL}/designs/{design_id}/export",
            params={
                "format": format,
                "quality": quality
            }
        ) as response:
            data = await response.json()

            if response.status != 200:
                error_msg = data.get("error", {}).get("message", str(data))
                raise Exception(f"Canva Get Download Link error: {error_msg}")

            return DownloadLink(
                url=data.get("url", ""),
                expires_at=data.get("expires_at", ""),
                format=format
            )

    async def search_design(
        self,
        query: str,
        folder_id: Optional[str] = None,
        limit: int = 50
    ) -> DesignResult:
        """
        Search for designs.

        Args:
            query: Search query string
            folder_id: Optional folder ID to search within
            limit: Maximum results (default: 50)

        Returns:
            DesignResult with matching designs

        Raises:
            ValueError: If query is empty
            aiohttp.ClientError: If request fails
        """
        if not query:
            raise ValueError("Query cannot be empty")

        params = {
            "query": query,
            "limit": limit
        }

        if folder_id:
            params["folder_id"] = folder_id

        async with self.session.get(
            f"{self.BASE_URL}/designs/search",
            params=params
        ) as response:
            data = await response.json()

            if response.status != 200:
                error_msg = data.get("error", {}).get("message", str(data))
                raise Exception(f"Canva Search Design error: {error_msg}")

            designs = [
                Design(
                    id=d.get("id", ""),
                    name=d.get("name", ""),
                    title=d.get("title", ""),
                    thumbnail_url=d.get("thumbnail_url", ""),
                    design_url=d.get("design_url", ""),
                    created_at=d.get("created_at", ""),
                    updated_at=d.get("updated_at", ""),
                    design_type=d.get("design_type", ""),
                    folder_id=d.get("folder_id")
                )
                for d in data.get("designs", [])
            ]

            return DesignResult(
                designs=designs,
                total=len(designs),
                page=1,
                page_size=limit
            )

    async def create_folder(
        self,
        name: str,
        parent_id: Optional[str] = None
    ) -> Folder:
        """
        Create a new folder.

        Args:
            name: Folder name
            parent_id: Optional parent folder ID

        Returns:
            Created Folder object

        Raises:
            ValueError: If name is empty
            aiohttp.ClientError: If request fails
        """
        if not name:
            raise ValueError("Folder name cannot be empty")

        payload = {"name": name}

        if parent_id:
            payload["parent_id"] = parent_id

        async with self.session.post(
            f"{self.BASE_URL}/folders",
            json=payload
        ) as response:
            data = await response.json()

            if response.status not in [200, 201]:
                error_msg = data.get("error", {}).get("message", str(data))
                raise Exception(f"Canva Create Folder error: {error_msg}")

            folder_data = data
            return Folder(
                id=folder_data.get("id", ""),
                name=folder_data.get("name", ""),
                created_at=folder_data.get("created_at", ""),
                updated_at=folder_data.get("updated_at", "")
            )

    async def move_folder_item(
        self,
        folder_id: str,
        item_id: str,
        item_type: str,
        target_folder_id: Optional[str] = None
    ) -> bool:
        """
        Move an item to a different folder.

        Args:
            folder_id: Source folder ID
            item_id: Item ID to move
            item_type: Item type ('design' or 'folder')
            target_folder_id: Target folder ID (None to move to root)

        Returns:
            bool: True if successful

        Raises:
            ValueError: If required parameters are missing
            aiohttp.ClientError: If request fails
        """
        if not folder_id:
            raise ValueError("Source folder ID cannot be empty")
        if not item_id:
            raise ValueError("Item ID cannot be empty")
        if not item_type:
            raise ValueError("Item type cannot be empty")

        payload = {
            "item_id": item_id,
            "item_type": item_type
        }

        if target_folder_id:
            payload["target_folder_id"] = target_folder_id

        async with self.session.post(
            f"{self.BASE_URL}/folders/{folder_id}/items/move",
            json=payload
        ) as response:
            if response.status in [200, 204]:
                return True
            else:
                data = await response.json()
                error_msg = data.get("error", {}).get("message", str(data))
                raise Exception(f"Canva Move Item error: {error_msg}")

    async def rename_folder(
        self,
        folder_id: str,
        new_name: str
    ) -> Folder:
        """
        Rename a folder.

        Args:
            folder_id: Folder ID
            new_name: New folder name

        Returns:
            Updated Folder object

        Raises:
            ValueError: If required parameters are missing
            aiohttp.ClientError: If request fails
        """
        if not folder_id:
            raise ValueError("Folder ID cannot be empty")
        if not new_name:
            raise ValueError("New name cannot be empty")

        payload = {"name": new_name}

        async with self.session.patch(
            f"{self.BASE_URL}/folders/{folder_id}",
            json=payload
        ) as response:
            data = await response.json()

            if response.status != 200:
                error_msg = data.get("error", {}).get("message", str(data))
                raise Exception(f"Canva Rename Folder error: {error_msg}")

            return Folder(
                id=data.get("id", ""),
                name=data.get("name", ""),
                created_at=data.get("created_at", ""),
                updated_at=data.get("updated_at", "")
            )

    async def create_export_job(
        self,
        design_id: str,
        format: str = "pdf",
        quality: str = "standard",
        pages: Optional[List[int]] = None
    ) -> ExportJob:
        """
        Create an export job for a design.

        Args:
            design_id: Design ID
            format: Export format ('pdf', 'png', 'jpg')
            quality: Export quality ('standard', 'high')
            pages: Optional list of page numbers to export

        Returns:
            ExportJob with job status

        Raises:
            ValueError: If design_id is empty
            aiohttp.ClientError: If request fails
        """
        if not design_id:
            raise ValueError("Design ID cannot be empty")

        payload = {
            "design_id": design_id,
            "format": format,
            "quality": quality
        }

        if pages:
            payload["pages"] = pages

        async with self.session.post(
            f"{self.BASE_URL}/designs/export",
            json=payload
        ) as response:
            data = await response.json()

            if response.status not in [200, 201]:
                error_msg = data.get("error", {}).get("message", str(data))
                raise Exception(f"Canva Create Export Job error: {error_msg}")

            return ExportJob(
                job_id=data.get("job_id", ""),
                status=data.get("status", ""),
                download_url=data.get("download_url"),
                progress=data.get("progress", 0.0)
            )

    async def get_export_job_status(
        self,
        job_id: str
    ) -> ExportJob:
        """
        Get the status of an export job.

        Args:
            job_id: Export job ID

        Returns:
            ExportJob with current status

        Raises:
            ValueError: If job_id is empty
            aiohttp.ClientError: If request fails
        """
        if not job_id:
            raise ValueError("Job ID cannot be empty")

        async with self.session.get(
            f"{self.BASE_URL}/designs/export/{job_id}"
        ) as response:
            data = await response.json()

            if response.status != 200:
                error_msg = data.get("error", {}).get("message", str(data))
                raise Exception(f"Canva Get Export Status error: {error_msg}")

            return ExportJob(
                job_id=data.get("job_id", job_id),
                status=data.get("status", ""),
                download_url=data.get("download_url"),
                progress=data.get("progress", 0.0)
            )

    def verify_webhook(self, payload: Dict[str, Any], signature: str, secret: str) -> bool:
        """
        Verify webhook signature.

        Args:
            payload: Webhook payload
            signature: Signature from webhook headers
            secret: Webhook secret

        Returns:
            bool: True if signature is valid
        """
        import hmac
        import hashlib
        import json

        payload_str = json.dumps(payload, separators=(',', ':'), sort_keys=True)
        expected_signature = hmac.new(
            secret.encode(),
            payload_str.encode(),
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(expected_signature, signature)

    def parse_webhook_event(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse webhook event payload.

        Args:
            payload: Webhook payload

        Returns:
            Dict with event details
        """
        event_type = payload.get("type", "")
        event_data = payload.get("data", {})

        result = {
            "event_type": event_type,
            "event_id": payload.get("id", ""),
            "timestamp": payload.get("timestamp", ""),
            "data": event_data
        }

        # Design updated event
        if event_type == "design.updated":
            result["design_id"] = event_data.get("design_id", "")
            result["changes"] = event_data.get("changes", {})

        return result


async def main():
    """Example usage"""
    api_key = "your-api-key-here"

    async with CanvaAPIClient(api_key) as client:
        # List folders
        folders_result = await client.list_folders(limit=20)
        print(f"Found {folders_result['total']} folders")

        # List items in a folder
        if folders_result['folders']:
            folder_id = folders_result['folders'][0].id
            items_result = await client.list_folder_items(folder_id)
            print(f"Items in {folders_result['folders'][0].name}: {items_result['total']}")

        # Search designs
        search_result = await client.search_design("marketing", limit=10)
        print(f"Found {search_result.total} designs matching 'marketing'")

        # Get download link
        if search_result.designs:
            design_id = search_result.designs[0].id
            download_link = await client.get_design_download_link(design_id, format="pdf")
            print(f"Download URL: {download_link.url}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())