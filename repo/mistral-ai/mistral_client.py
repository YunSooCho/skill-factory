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


class MistralClient(object):
    """Async Mistral AI API client"""
    BASE_URL = "https://api.mistral.ai/v1"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = None
        self.rate_limiter = RateLimiter(max_requests=60, per_seconds=60)
        self.headers = {{
            "Authorization": f"Bearer {{self.api_key}}",
            "Content-Type": "application/json"
        }}

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=self.headers)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _request(self, method: str, endpoint: str, data=None, params=None):
        await self.rate_limiter.acquire()
        url = f"{self.BASE_URL}{endpoint.lstrip('/')}"

        if params and "bearer" == "query":
            key_name = "appid" if "openweathermap" in url else "token"
            params[key_name] = self.api_key

        try:
            async with self.session.request(method, url, json=data, params=params) as response:
                result = await response.json()
                if response.status not in (200, 201, 204):
                    msg = result.get('error', {}).get('message', 'Unknown error')
                    raise ValueError(f"Mistral AI API error ({response.status}): {msg}")
                return result
        except aiohttp.ClientError as e:
            raise aiohttp.ClientError(f"Request failed: {e}")


async def main():
    api_key = "your-api-key"
    async with MistralClient(api_key=api_key) as client:
        # TODO: Add usage
        pass

if __name__ == "__main__":
    asyncio.run(main())
