import aiohttp
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any, List


class RateLimiter:
    def __init__(self, max_requests: int = 60, per_seconds: int = 60):
        self.max_requests = max_requests
        self.per_seconds = per_seconds
        self.requests = []
        self.lock = asyncio.Lock()

    async def acquire(self):
        async with self.lock:
            now = datetime.now(timezone.utc)
            cutoff = now - timedelta(seconds=self.per_seconds)
            self.requests = [r for r in self.requests if r > cutoff]
            if len(self.requests) >= self.max_requests:
                oldest = sorted(self.requests)[0]
                wait = (oldest + timedelta(seconds=self.per_seconds) - now).total_seconds()
                if wait > 0:
                    await asyncio.sleep(wait)
            self.requests.append(now)


class MemClient(object):
    """Async Mem API client"""
    BASE_URL = "https://api.mem.ai/v1"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = None
        self.rate_limiter = RateLimiter(max_requests=60, per_seconds=60)
        self.headers = {{
            "Authorization": f"Bearer {{self.api_key}}",
            "Content-Type": "application/json"
        }}

    async def __aenter__(self):
        if self.headers:
            self.session = aiohttp.ClientSession(headers=self.headers)
        else:
            self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _request(self, method: str, endpoint: str, data=None, params=None):
        await self.rate_limiter.acquire()
        url = f"{self.BASE_URL}{endpoint.lstrip('/')}"

        # Add API key to params for query-based auth
        if params and "bearer" == "query":
            params["api_key"] = self.api_key

        try:
            async with self.session.request(method, url, json=data, params=params) as response:
                result = await response.json() if response.content_length else {}
                if response.status not in (200, 201, 204):
                    msg = result.get('error', {}).get('message', result.get('message', 'Unknown error'))
                    raise ValueError(f"Mem API error ({response.status}): {msg}")
                return result
        except aiohttp.ClientError as e:
            raise aiohttp.ClientError(f"Request failed: {e}")

    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """GET request helper"""
        return await self._request("GET", endpoint, params=params)

    async def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """POST request helper"""
        return await self._request("POST", endpoint, data=data)

    async def put(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """PUT request helper"""
        return await self._request("PUT", endpoint, data=data)

    async def delete(self, endpoint: str) -> Dict[str, Any]:
        """DELETE request helper"""
        return await self._request("DELETE", endpoint)

    # Generic methods for CRUD operations
    async def list_resources(self, resource_type: str) -> Dict[str, Any]:
        """List resources of a given type"""
        return await self.get(f"/{resource_type}")

    async def get_resource(self, resource_type: str, resource_id: str) -> Dict[str, Any]:
        """Get a specific resource"""
        return await self.get(f"/{resource_type}/{resource_id}")

    async def create_resource(self, resource_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new resource"""
        return await self.post(f"/{resource_type}", data)

    async def update_resource(self, resource_type: str, resource_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a resource"""
        return await self.put(f"/{resource_type}/{resource_id}", data)

    async def delete_resource(self, resource_type: str, resource_id: str) -> Dict[str, Any]:
        """Delete a resource"""
        return await self.delete(f"/{resource_type}/{resource_id}")


async def main():
    api_key = "your-api-key"
    async with MemClient(api_key=api_key) as client:
        # Example usage
        try:
            result = await client.get("/health")
            print(result)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
