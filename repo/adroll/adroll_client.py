"""
AdRoll API - Advertising Platform Client

Supports:
- List Segment (audience segments)
- Create Segment (audience segments)
"""

import aiohttp
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class Segment:
    """AdRoll segment"""
    eid: str
    name: str
    type: str
    created_at: str = ""
    ad_count: int = 0


class AdRollClient:
    """
    AdRoll API client for advertising operations.

    API Documentation: https://developers.adroll.com/docs/api/
    Uses API key and advertiser ID for authentication.
    """

    BASE_URL = "https://services.adroll.com/api/v1"

    def __init__(self, api_key: str, advertiser_eid: str):
        """
        Initialize AdRoll client.

        Args:
            api_key: AdRoll API key
            advertiser_eid: Advertiser entity ID
        """
        self.api_key = api_key
        self.advertiser_eid = advertiser_eid
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def _get_params(self, **kwargs) -> Dict[str, Any]:
        """Build API parameters"""
        params = {
            "apikey": self.api_key,
            "advertisable_eid": self.advertiser_eid
        }
        params.update(kwargs)
        return params

    # ==================== Segment Operations ====================

    async def list_segments(
        self,
        segment_type: Optional[str] = None,
        limit: int = 50
    ) -> List[Segment]:
        """
        List audience segments.

        Args:
            segment_type: Filter by segment type
            limit: Maximum segments to return

        Returns:
            List of Segment objects
        """
        params = self._get_params(limit=limit)
        if segment_type:
            params["segment_type"] = segment_type

        async with self.session.get(
            f"{self.BASE_URL}/segment/list",
            params=params
        ) as response:
            data = await response.json()

            if response.status != 200 or data.get("success") is not True:
                raise Exception(f"Failed to list segments: {data}")

            segments_data = data.get("segments", [])
            return [
                Segment(
                    eid=s.get("eid", ""),
                    name=s.get("name", ""),
                    type=s.get("segment_type", ""),
                    created_at=s.get("created_at", ""),
                    ad_count=s.get("ad_count", 0)
                )
                for s in segments_data
            ]

    async def create_segment(
        self,
        name: str,
        segment_type: str = "behavioral",
        description: Optional[str] = None
    ) -> Segment:
        """
        Create a new audience segment.

        Args:
            name: Segment name
            segment_type: Segment type (behavioral, conversion, etc.)
            description: Optional segment description

        Returns:
            Created Segment object
        """
        params = self._get_params(
            name=name,
            segment_type=segment_type
        )

        if description:
            params["description"] = description

        async with self.session.get(
            f"{self.BASE_URL}/segment/create",
            params=params
        ) as response:
            data = await response.json()

            if response.status != 200 or data.get("success") is not True:
                raise Exception(f"Failed to create segment: {data}")

            segment_data = data.get("segment", {})
            return Segment(
                eid=segment_data.get("eid", ""),
                name=segment_data.get("name", name),
                type=segment_type,
                created_at=segment_data.get("created_at", "")
            )


# Example usage
async def main():
    async with AdRollClient(
        api_key="your_api_key",
        advertiser_eid="your_advertiser_eid"
    ) as client:
        segments = await client.list_segments()
        print(f"Found {len(segments)} segments")

        new_segment = await client.create_segment(
            name="Test Segment",
            segment_type="behavioral"
        )
        print(f"Created: {new_segment.name}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())