import aiohttp
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any, List


class RateLimiter:
    def __init__(self, max_requests: int = 30, per_seconds: int = 60):
        self.max_requests = max_requests
        self.per_seconds = per_seconds
        self.requests: List[datetime] = []
        self.lock = asyncio.Lock()

    async def acquire(self) -> None:
        async with self.lock:
            now = datetime.now(timezone.utc)
            cutoff = now - timedelta(seconds=self.per_seconds)
            self.requests = [req for req in self.requests if req > cutoff]
            if len(self.requests) >= self.max_requests:
                oldest = sorted(self.requests)[0]
                sleep = (oldest + timedelta(seconds=self.per_seconds) - now).total_seconds()
                if sleep > 0:
                    await asyncio.sleep(sleep)
            self.requests.append(now)


class HuggingFaceClient:
    BASE_URL = "https://api-inference.huggingface.co"

    def __init__(self, api_key: str, max_requests_per_minute: int = 30):
        self.api_key = api_key
        self.session = None
        self.rate_limiter = RateLimiter(max_requests=max_requests_per_minute, per_seconds=60)
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=self.headers)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def inference(self, model_name: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        await self.rate_limiter.acquire()
        async with self.session.post(f"{self.BASE_URL}/models/{model_name}", json=inputs) as response:
            data = await response.json()
            if response.status != 200:
                raise ValueError(f"HuggingFace API error: {data}")
            return data

    async def question_answering(self, question: str, context: str) -> Dict[str, Any]:
        await self.rate_limiter.acquire()
        async with self.session.post(
            f"{self.BASE_URL}/models/deepset/roberta-base-squad2",
            json={"inputs": {"question": question, "context": context}}
        ) as response:
            data = await response.json()
            if response.status != 200:
                raise ValueError(f"HuggingFace API error: {data}")
            return data

    async def text_generation(self, prompt: str) -> Dict[str, Any]:
        await self.rate_limiter.acquire()
        async with self.session.post(
            f"{self.BASE_URL}/models/gpt2",
            json={"inputs": prompt}
        ) as response:
            data = await response.json()
            if response.status != 200:
                raise ValueError(f"HuggingFace API error: {data}")
            return data

    async def summarization(self, text: str) -> Dict[str, Any]:
        await self.rate_limiter.acquire()
        async with self.session.post(
            f"{self.BASE_URL}/models/facebook/bart-large-cnn",
            json={"inputs": text}
        ) as response:
            data = await response.json()
            if response.status != 200:
                raise ValueError(f"HuggingFace API error: {data}")
            return data

    async def translation(self, text: str, model: str = "Helsinki-NLP/opus-mt-ko-en") -> Dict[str, Any]:
        await self.rate_limiter.acquire()
        async with self.session.post(
            f"{self.BASE_URL}/models/{model}",
            json={"inputs": text}
        ) as response:
            data = await response.json()
            if response.status != 200:
                raise ValueError(f"HuggingFace API error: {data}")
            return data


async def main():
    api_key = "your-huggingface-api-key"
    async with HuggingFaceClient(api_key=api_key) as client:
        try:
            result = await client.summarization("Your long text here...")
            print(result)
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())