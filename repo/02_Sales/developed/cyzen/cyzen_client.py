"""
Cyzen API Client

Complete client for Cyzen - Japanese sales and field management system.
Supports appointments, spots, reports, and history tracking.
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
import json


class CyzenAPIError(Exception):
    """Base exception for Cyzen API errors"""

    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[Dict] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class CyzenRateLimitError(CyzenAPIError):
    """Raised when rate limit is exceeded"""


@dataclass
class Appointment:
    appointment_id: str
    title: str
    start_time: str
    end_time: Optional[str] = None
    customer_id: Optional[str] = None
    created_at: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Spot:
    spot_id: str
    name: str
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    created_at: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SpotCustomer:
    spot_customer_id: str
    spot_id: str
    name: str
    phone: Optional[str] = None
    created_at: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Report:
    report_id: str
    title: str
    date: str
    status: str
    created_at: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class HistoryRecord:
    history_id: str
    user_id: str
    timestamp: str
    location: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


class CyzenClient:
    """Cyzen API Client for Japanese sales and field management."""

    BASE_URL = "https://api.cyzen.jp/v1"

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        max_requests_per_minute: int = 100,
        timeout: int = 30
    ):
        self.api_key = api_key
        self.base_url = base_url or self.BASE_URL
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.session: Optional[aiohttp.ClientSession] = None
        self.max_requests_per_minute = max_requests_per_minute
        self._request_times: List[float] = []

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _check_rate_limit(self):
        now = asyncio.get_event_loop().time()
        self._request_times = [t for t in self._request_times if now - t < 60]

        if len(self._request_times) >= self.max_requests_per_minute:
            sleep_time = 60 - (now - self._request_times[0])
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
                self._request_times = []

        self._request_times.append(now)

    async def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        await self._check_rate_limit()
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        if not self.session:
            raise RuntimeError("Client must be used as async context manager")

        try:
            async with self.session.request(
                method, url, json=data, params=params, headers=headers
            ) as response:
                try:
                    response_data = await response.json()
                except:
                    response_data = await response.text()

                if response.status == 429:
                    raise CyzenRateLimitError("Rate limit exceeded", status_code=429)

                if response.status >= 400:
                    error_msg = response_data.get("error", str(response_data))
                    raise CyzenAPIError(error_msg, status_code=response.status)

                return response_data if isinstance(response_data, dict) else {}

        except aiohttp.ClientError as e:
            raise CyzenAPIError(f"Network error: {str(e)}")

    async def create_appointment(self, appointment_data: Dict[str, Any]) -> Appointment:
        data = await self._request("POST", "/appointments", data=appointment_data)
        return Appointment(
            appointment_id=data.get("id", ""),
            title=data.get("title", ""),
            start_time=data.get("start_time", ""),
            end_time=data.get("end_time"),
            customer_id=data.get("customer_id"),
            created_at=data.get("created_at"),
            additional_data={k: v for k, v in data.items() if k not in ["id", "title", "start_time", "end_time", "customer_id", "created_at"]}
        )

    async def update_appointment(self, appointment_id: str, update_data: Dict[str, Any]) -> Appointment:
        data = await self._request("PUT", f"/appointments/{appointment_id}", data=update_data)
        return Appointment(
            appointment_id=appointment_id,
            title=data.get("title", ""),
            start_time=data.get("start_time", ""),
            end_time=data.get("end_time"),
            customer_id=data.get("customer_id"),
            created_at=data.get("created_at"),
            additional_data={k: v for k, v in data.items() if k not in ["title", "start_time", "end_time", "customer_id", "created_at"]}
        )

    async def get_appointment(self, appointment_id: str) -> Appointment:
        data = await self._request("GET", f"/appointments/{appointment_id}")
        return Appointment(
            appointment_id=data.get("id", appointment_id),
            title=data.get("title", ""),
            start_time=data.get("start_time", ""),
            end_time=data.get("end_time"),
            customer_id=data.get("customer_id"),
            created_at=data.get("created_at"),
            additional_data={k: v for k, v in data.items() if k not in ["id", "title", "start_time", "end_time", "customer_id", "created_at"]}
        )

    async def delete_appointment(self, appointment_id: str) -> Dict[str, Any]:
        return await self._request("DELETE", f"/appointments/{appointment_id}")

    async def create_spot(self, spot_data: Dict[str, Any]) -> Spot:
        data = await self._request("POST", "/spots", data=spot_data)
        return Spot(
            spot_id=data.get("id", ""),
            name=data.get("name", ""),
            address=data.get("address"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            created_at=data.get("created_at"),
            additional_data={k: v for k, v in data.items() if k not in ["id", "name", "address", "latitude", "longitude", "created_at"]}
        )

    async def update_spot(self, spot_id: str, update_data: Dict[str, Any]) -> Spot:
        data = await self._request("PUT", f"/spots/{spot_id}", data=update_data)
        return Spot(
            spot_id=spot_id,
            name=data.get("name", ""),
            address=data.get("address"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            created_at=data.get("created_at"),
            additional_data={k: v for k, v in data.items() if k not in ["name", "address", "latitude", "longitude", "created_at"]}
        )

    async def get_spot(self, spot_id: str) -> Spot:
        data = await self._request("GET", f"/spots/{spot_id}")
        return Spot(
            spot_id=data.get("id", spot_id),
            name=data.get("name", ""),
            address=data.get("address"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            created_at=data.get("created_at"),
            additional_data={k: v for k, v in data.items() if k not in ["id", "name", "address", "latitude", "longitude", "created_at"]}
        )

    async def delete_spot(self, spot_id: str) -> Dict[str, Any]:
        return await self._request("DELETE", f"/spots/{spot_id}")

    async def create_spot_customer(self, customer_data: Dict[str, Any]) -> SpotCustomer:
        data = await self._request("POST", "/spot-customers", data=customer_data)
        return SpotCustomer(
            spot_customer_id=data.get("id", ""),
            spot_id=data.get("spot_id", ""),
            name=data.get("name", ""),
            phone=data.get("phone"),
            created_at=data.get("created_at"),
            additional_data={k: v for k, v in data.items() if k not in ["id", "spot_id", "name", "phone", "created_at"]}
        )

    async def update_spot_customer(self, customer_id: str, update_data: Dict[str, Any]) -> SpotCustomer:
        data = await self._request("PUT", f"/spot-customers/{customer_id}", data=update_data)
        return SpotCustomer(
            spot_customer_id=customer_id,
            spot_id=data.get("spot_id", ""),
            name=data.get("name", ""),
            phone=data.get("phone"),
            created_at=data.get("created_at"),
            additional_data={k: v for k, v in data.items() if k not in ["spot_id", "name", "phone", "created_at"]}
        )

    async def get_spot_customer(self, customer_id: str) -> SpotCustomer:
        data = await self._request("GET", f"/spot-customers/{customer_id}")
        return SpotCustomer(
            spot_customer_id=data.get("id", customer_id),
            spot_id=data.get("spot_id", ""),
            name=data.get("name", ""),
            phone=data.get("phone"),
            created_at=data.get("created_at"),
            additional_data={k: v for k, v in data.items() if k not in ["id", "spot_id", "name", "phone", "created_at"]}
        )

    async def delete_spot_customer(self, customer_id: str) -> Dict[str, Any]:
        return await self._request("DELETE", f"/spot-customers/{customer_id}")

    async def get_spot_share_link(self, spot_id: str) -> str:
        data = await self._request("GET", f"/spots/{spot_id}/share-link")
        return data.get("share_link", "")

    async def get_report(self, report_id: str) -> Report:
        data = await self._request("GET", f"/reports/{report_id}")
        return Report(
            report_id=data.get("id", report_id),
            title=data.get("title", ""),
            date=data.get("date", ""),
            status=data.get("status", ""),
            created_at=data.get("created_at"),
            additional_data={k: v for k, v in data.items() if k not in ["id", "title", "date", "status", "created_at"]}
        )

    async def get_report_share_link(self, report_id: str) -> str:
        data = await self._request("GET", f"/reports/{report_id}/share-link")
        return data.get("share_link", "")

    async def get_route_history(
        self,
        user_id: str,
        start_date: str,
        end_date: str,
        limit: int = 100
    ) -> List[HistoryRecord]:
        params = {
            "user_id": user_id,
            "start_date": start_date,
            "end_date": end_date,
            "limit": limit
        }
        data = await self._request("GET", "/history/route", params=params)
        results = data.get("records", [])

        return [HistoryRecord(
            history_id=r.get("id", ""),
            user_id=r.get("user_id", ""),
            timestamp=r.get("timestamp", ""),
            location=r.get("location"),
            additional_data={k: v for k, v in r.items() if k not in ["id", "user_id", "timestamp", "location"]}
        ) for r in results]

    async def get_timestamp_history(
        self,
        user_id: str,
        start_date: str,
        end_date: str,
        limit: int = 100
    ) -> List[HistoryRecord]:
        params = {
            "user_id": user_id,
            "start_date": start_date,
            "end_date": end_date,
            "limit": limit
        }
        data = await self._request("GET", "/history/timestamp", params=params)
        results = data.get("records", [])

        return [HistoryRecord(
            history_id=r.get("id", ""),
            user_id=r.get("user_id", ""),
            timestamp=r.get("timestamp", ""),
            location=r.get("location"),
            additional_data={k: v for k, v in r.items() if k not in ["id", "user_id", "timestamp", "location"]}
        ) for r in results]

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()


async def main():
    async with CyzenClient(api_key="your_api_key") as client:
        appointment = await client.create_appointment({
            "title": "Client Meeting",
            "start_time": "2024-01-20T10:00:00",
            "customer_id": "123"
        })
        print(f"Created appointment: {appointment.appointment_id}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())