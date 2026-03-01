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


class PushcutClient(object):
    """Async Pushcut API client for iOS automation"""
    BASE_URL = "https://api.pushcut.io/v1"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = None
        self.rate_limiter = RateLimiter(max_requests=60, per_seconds=60)
        self.headers = {
            "API-Key": api_key,
            "Content-Type": "application/json"
        }

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=self.headers)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _request(self, method: str, endpoint: str, data=None, params=None):
        await self.rate_limiter.acquire()
        url = f"{self.BASE_URL}{endpoint.lstrip('/')}"

        try:
            async with self.session.request(method, url, json=data, params=params) as response:
                result = await response.json() if response.content_length else {}
                if response.status not in (200, 201, 204):
                    msg = result.get('error', {}).get('message', result.get('message', 'Unknown error'))
                    raise ValueError(f"Pushcut API error ({response.status}): {msg}")
                return result
        except aiohttp.ClientError as e:
            raise aiohttp.ClientError(f"Request failed: {e}")

    async def send_notification(self, text: str, title: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """Send a notification"""
        data = {"text": text}
        if title:
            data["title"] = title
        data.update(kwargs)
        return await self._request("POST", "/notifications", data=data)

    async def list_notifications(self) -> Dict[str, Any]:
        """List all notifications"""
        return await self._request("GET", "/notifications")

    async def get_notification(self, notification_id: str) -> Dict[str, Any]:
        """Get a specific notification"""
        return await self._request("GET", f"/notifications/{notification_id}")

    async def register_device(self, device_name: str, **kwargs) -> Dict[str, Any]:
        """Register a new device"""
        data = {"name": device_name}
        data.update(kwargs)
        return await self._request("POST", "/register", data=data)

    async def list_devices(self) -> Dict[str, Any]:
        """List all registered devices"""
        return await self._request("GET", "/devices")

    async def list_actions(self) -> Dict[str, Any]:
        """List all actions"""
        return await self._request("GET", "/actions")

    async def trigger_action(self, action_id: str, **kwargs) -> Dict[str, Any]:
        """Trigger a specific action"""
        data = kwargs or {}
        return await self._request("POST", f"/actions/{action_id}/trigger", data=data)


async def main():
    api_key = "your-pushcut-api-key"
    async with PushcutClient(api_key=api_key) as client:
        try:
            result = await client.list_devices()
            print(result)
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())