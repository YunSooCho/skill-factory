"""
Alooma API Client (Deprecated)

Alooma was a data integration and pipeline platform that was acquired by Google
and is now part of Google Cloud Data Fusion.

This implementation is maintained for historical reference. For new projects,
consider using Google Cloud Data Fusion or other modern data integration tools.

API Actions (estimated 8-10 - Legacy):
1. Create Pipeline
2. Update Pipeline
3. Get Pipeline
4. List Pipelines
5. Start Pipeline
6. Stop Pipeline
7. Get Pipeline Status
8. Create Transformation
9. Get Pipeline Metrics

Triggers (estimated 3-4 - Legacy):
- Pipeline Started
- Pipeline Stopped
- Pipeline Error
- Data Received

Authentication: API Key (Legacy)
Historical URL: https://api.alooma.com/v1
Current Recommendation: Use Google Cloud Data Fusion
Documentation: https://cloud.google.com/data-fusion/docs
Rate Limiting: N/A (Deprecated)
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field

import warnings

warnings.warn(
    "Alooma has been acquired by Google Cloud and is part of Data Fusion. "
    "This implementation is for historical reference only.",
    DeprecationWarning,
    stacklevel=2
)


@dataclass
class Pipeline:
    """Pipeline model (Legacy)"""
    pipeline_id: str
    name: str
    status: str
    source_type: str
    target_type: str
    created_at: str
    is_active: bool = False


@dataclass
class PipelineStatus:
    """Pipeline status model (Legacy)"""
    pipeline_id: str
    status: str
    throughput: float
    error_rate: float
    last_update: str


@dataclass
class Transformation:
    """Transformation model (Legacy)"""
    transformation_id: str
    name: str
    description: str
    code: str = ""
    is_active: bool = True


class AloomaClient:
    """
    Alooma API client - DEPRECATED.

    Alooma was acquired by Google in 2019 and is now part of Google Cloud Data Fusion.
    This implementation is maintained for historical reference and migration purposes.

    For new data integration projects, use:
    - Google Cloud Data Fusion
    - Apache Airflow
    - dbt
    - Fivetran
    - Airbyte

    Authentication: Legacy API key
    """

    BASE_URL = "https://api.alooma.com/v1"  # Legacy

    def __init__(self, api_token: str):
        """
        Initialize Alooma client (Deprecated).

        Args:
            api_token: Legacy Alooma API token
        """
        warnings.warn(
            "Alooma API is deprecated. Migrate to Google Cloud Data Fusion.",
            DeprecationWarning,
            stacklevel=2
        )
        self.api_token = api_token
        self.session = None
        self._headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make API request (Legacy)"""
        warnings.warn(
            "Alooma API endpoints may not be available.",
            DeprecationWarning,
            stacklevel=3
        )

        url = f"{self.BASE_URL}{endpoint}"

        async with self.session.request(
            method,
            url,
            headers=self._headers,
            json=data,
            params=params
        ) as response:
            try:
                result = await response.json()
            except:
                result = {}

            if response.status not in [200, 201]:
                raise Exception(
                    f"Alooma API error: {response.status} - Service may be deprecated"
                )

            return result

    # ==================== Pipeline Operations (Legacy) ====================

    async def create_pipeline(
        self,
        name: str,
        source_type: str,
        target_type: str
    ) -> Pipeline:
        """
        Create a pipeline (Deprecated).

        Args:
            name: Pipeline name
            source_type: Source data type
            target_type: Destination data type

        Returns:
            Pipeline object

        Note: Use Google Cloud Data Fusion pipelines instead.
        """
        data = {
            "name": name,
            "sourceType": source_type,
            "targetType": target_type
        }
        response = await self._make_request("POST", "/pipelines", data=data)
        pipeline_data = response.get("data", response)
        return Pipeline(
            pipeline_id=pipeline_data.get("id", ""),
            name=pipeline_data.get("name", name),
            status=pipeline_data.get("status", ""),
            source_type=pipeline_data.get("sourceType", source_type),
            target_type=pipeline_data.get("targetType", target_type),
            created_at=pipeline_data.get("createdAt", datetime.now().isoformat()),
            is_active=pipeline_data.get("isActive", False)
        )

    async def get_pipeline(self, pipeline_id: str) -> Pipeline:
        """
        Get pipeline by ID (Deprecated).

        Args:
            pipeline_id: Pipeline ID

        Returns:
            Pipeline object
        """
        response = await self._make_request("GET", f"/pipelines/{pipeline_id}")
        pipeline_data = response.get("data", response)
        return Pipeline(
            pipeline_id=pipeline_data.get("id", ""),
            name=pipeline_data.get("name", ""),
            status=pipeline_data.get("status", ""),
            source_type=pipeline_data.get("sourceType", ""),
            target_type=pipeline_data.get("targetType", ""),
            created_at=pipeline_data.get("createdAt", ""),
            is_active=pipeline_data.get("isActive", False)
        )

    async def list_pipelines(
        self,
        status: Optional[str] = None
    ) -> List[Pipeline]:
        """
        List all pipelines (Deprecated).

        Args:
            status: Optional status filter

        Returns:
            List of Pipeline objects
        """
        params = {}
        if status:
            params["status"] = status

        response = await self._make_request("GET", "/pipelines", params=params)
        pipelines_data = response.get("data", [])
        return [
            Pipeline(
                pipeline_id=p.get("id", ""),
                name=p.get("name", ""),
                status=p.get("status", ""),
                source_type=p.get("sourceType", ""),
                target_type=p.get("targetType", ""),
                created_at=p.get("createdAt", ""),
                is_active=p.get("isActive", False)
            )
            for p in pipelines_data
        ]

    async def update_pipeline(
        self,
        pipeline_id: str,
        **fields
    ) -> Pipeline:
        """
        Update a pipeline (Deprecated).

        Args:
            pipeline_id: Pipeline ID
            **fields: Fields to update

        Returns:
            Updated Pipeline object
        """
        response = await self._make_request(
            "PUT",
            f"/pipelines/{pipeline_id}",
            data=fields
        )
        pipeline_data = response.get("data", response)
        return Pipeline(
            pipeline_id=pipeline_data.get("id", ""),
            name=pipeline_data.get("name", ""),
            status=pipeline_data.get("status", ""),
            source_type=pipeline_data.get("sourceType", ""),
            target_type=pipeline_data.get("targetType", ""),
            created_at=pipeline_data.get("createdAt", "")
        )

    async def start_pipeline(self, pipeline_id: str) -> bool:
        """
        Start a pipeline (Deprecated).

        Args:
            pipeline_id: Pipeline ID

        Returns:
            True if started successfully
        """
        await self._make_request("POST", f"/pipelines/{pipeline_id}/start")
        return True

    async def stop_pipeline(self, pipeline_id: str) -> bool:
        """
        Stop a pipeline (Deprecated).

        Args:
            pipeline_id: Pipeline ID

        Returns:
            True if stopped successfully
        """
        await self._make_request("POST", f"/pipelines/{pipeline_id}/stop")
        return True

    async def get_pipeline_status(self, pipeline_id: str) -> PipelineStatus:
        """
        Get pipeline status (Deprecated).

        Args:
            pipeline_id: Pipeline ID

        Returns:
            PipelineStatus object
        """
        response = await self._make_request("GET", f"/pipelines/{pipeline_id}/status")
        status_data = response.get("data", response)
        return PipelineStatus(
            pipeline_id=pipeline_id,
            status=status_data.get("status", ""),
            throughput=status_data.get("throughput", 0.0),
            error_rate=status_data.get("errorRate", 0.0),
            last_update=status_data.get("lastUpdate", "")
        )

    # ==================== Transformation Operations (Legacy) ====================

    async def create_transformation(
        self,
        name: str,
        description: str,
        code: str
    ) -> Transformation:
        """
        Create a transformation (Deprecated).

        Args:
            name: Transformation name
            description: Transformation description
            code: Transformation code

        Returns:
            Transformation object
        """
        data = {
            "name": name,
            "description": description,
            "code": code
        }
        response = await self._make_request("POST", "/transformations", data=data)
        transform_data = response.get("data", response)
        return Transformation(
            transformation_id=transform_data.get("id", ""),
            name=transform_data.get("name", name),
            description=transform_data.get("description", description),
            code=transform_data.get("code", code),
            is_active=transform_data.get("isActive", True)
        )

    # ==================== Metrics (Legacy) ====================

    async def get_pipeline_metrics(
        self,
        pipeline_id: str,
        period: str = "24h"
    ) -> Dict[str, Any]:
        """
        Get pipeline metrics (Deprecated).

        Args:
            pipeline_id: Pipeline ID
            period: Time period (1h, 24h, 7d, 30d)

        Returns:
            Metrics dictionary
        """
        params = {"period": period}
        response = await self._make_request(
            "GET",
            f"/pipelines/{pipeline_id}/metrics",
            params=params
        )
        return response.get("data", {})

    # ==================== Migration Recommendations ====================

    def get_migration_suggestions(self) -> Dict[str, str]:
        """
        Get suggestions for migrating from Alooma to modern alternatives.

        Returns:
            Dictionary of migration options
        """
        return {
            "google_data_fusion": "https://cloud.google.com/data-fusion",
            "airflow": "https://airflow.apache.org",
            "dbt": "https://www.getdbt.com",
            "fivetran": "https://fivetran.com",
            "airbyte": "https://airbyte.com",
            "note": "Consider your specific requirements: real-time vs batch, "
                   "self-hosted vs cloud, pricing model, and team expertise"
        }

    # ==================== Webhook Handling (Legacy) ====================

    def handle_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle webhook events (Deprecated).

        Args:
            webhook_data: Webhook payload

        Returns:
            Processed event data
        """
        warnings.warn(
            "Alooma webhooks may not be available.",
            DeprecationWarning,
            stacklevel=3
        )

        event_type = webhook_data.get("event_type", "unknown")
        pipeline_id = webhook_data.get("pipeline_id")

        return {
            "event_type": event_type,
            "pipeline_id": pipeline_id,
            "raw_data": webhook_data,
            "note": "Consider migrating to modern data integration platforms"
        }


async def main():
    """Example usage (for migration reference only)"""
    api_token = "legacy_alooma_token"

    async with AloomaClient(api_token) as client:
        # Get migration suggestions
        suggestions = client.get_migration_suggestions()
        print("Migration options:")
        for platform, url in suggestions.items():
            if platform != "note":
                print(f"  - {platform}: {url}")
        print(f"\n{suggestions['note']}")

        # Note: Actual API calls may fail as Alooma is deprecated
        # These are maintained only for migration reference
        try:
            # pipelines = await client.list_pipelines()
            # print(f"Found {len(pipelines)} pipelines (legacy)")
            pass
        except Exception as e:
            print(f"Expected error (service deprecated): {e}")


if __name__ == "__main__":
    asyncio.run(main())