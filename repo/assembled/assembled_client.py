"""
Assembled API Client

Workforce management platform for customer support teams including:
- Agent scheduling
- Real-time agent status
- Queue management
- Performance analytics

API Actions (estimated 10-12):
1. Create Schedule
2. Update Schedule
3. Get Schedule
4. Get Agent Status
5. Update Agent Status
6. Get Queue Status
7. Create Shift Assignment
8. Get Performance Metrics
9. Get Activity Logs
10. Create Adherence Alert

Triggers (estimated 4-5):
- Agent Signs On/Off
- Shift Started/Ended
- Adherence Breach
- Queue Threshold Exceeded
- Break Started/Ended

Authentication: API Key
Base URL: https://api.assembledhq.com/v1
Documentation: https://docs.assembledhq.com/
Rate Limiting: 1000 requests per minute
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field


@dataclass
class Agent:
    """Agent model"""
    agent_id: str
    name: str
    email: str
    status: str
    team_id: Optional[str] = None
    is_available: bool = False
    current_queue: Optional[str] = None


@dataclass
class Schedule:
    """Schedule model"""
    schedule_id: str
    name: str
    start_date: str
    end_date: str
    timezone: str
    created_at: str
    shifts: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class Shift:
    """Shift model"""
    shift_id: str
    agent_id: str
    start_time: str
    end_time: str
    activity: str
    queue: Optional[str] = None
    is_active: bool = False


@dataclass
class Queue:
    """Queue model"""
    queue_id: str
    name: str
    status: str
    waiting_count: int
    service_level: float
    average_wait_time: float


@dataclass
class PerformanceMetric:
    """Performance metric model"""
    metric_name: str
    value: float
    target: Optional[float] = None
    period_start: str
    period_end: str


@dataclass
class Adherence:
    """Adherence model"""
    agent_id: str
    schedule adherence: float
    is_in_adherence: bool
    breach_reason: Optional[str] = None
    current_activity: Optional[str] = None
    current_activity_start: Optional[str] = None


class AssembledClient:
    """
    Assembled API client for workforce management.

    Supports: Scheduling, Agents, Queues, Performance
    Rate limit: 1000 requests/minute
    """

    BASE_URL = "https://api.assembledhq.com/v1"
    RATE_LIMIT = 1000  # requests per minute

    def __init__(self, api_key: str):
        """
        Initialize Assembled client.

        Args:
            api_key: Your Assembled API key
        """
        self.api_key = api_key
        self.session = None
        self._headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self._request_count = 0
        self._request_window_start = datetime.now()

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _check_rate_limit(self):
        """Check and enforce rate limiting"""
        now = datetime.now()
        time_window = (now - self._request_window_start).total_seconds()

        if time_window >= 60:
            self._request_count = 0
            self._request_window_start = now

        if self._request_count >= self.RATE_LIMIT:
            wait_time = 60 - int(time_window)
            if wait_time > 0:
                await asyncio.sleep(wait_time)
                self._request_count = 0
                self._request_window_start = datetime.now()

        self._request_count += 1

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make API request with rate limiting"""
        await self._check_rate_limit()

        url = f"{self.BASE_URL}{endpoint}"

        async with self.session.request(
            method,
            url,
            headers=self._headers,
            json=data,
            params=params
        ) as response:
            result = await response.json()

            if response.status not in [200, 201]:
                error = result.get("error", str(result))
                raise Exception(
                    f"Assembled API error: {response.status} - {error}"
                )

            return result

    # ==================== Agent Operations ====================

    async def get_agent_status(self, agent_id: str) -> Agent:
        """Get current status of an agent"""
        response = await self._make_request("GET", f"/agents/{agent_id}/status")
        agent_data = response.get("data", response)
        return Agent(
            agent_id=agent_id,
            name=agent_data.get("name", ""),
            email=agent_data.get("email", ""),
            status=agent_data.get("status", ""),
            team_id=agent_data.get("teamId"),
            is_available=agent_data.get("isAvailable", False),
            current_queue=agent_data.get("currentQueue")
        )

    async def update_agent_status(
        self,
        agent_id: str,
        status: str,
        activity: Optional[str] = None,
        reason: Optional[str] = None
    ) -> Agent:
        """Update agent status"""
        data = {
            "status": status
        }
        if activity:
            data["activity"] = activity
        if reason:
            data["reason"] = reason

        response = await self._make_request(
            "POST",
            f"/agents/{agent_id}/status",
            data=data
        )
        agent_data = response.get("data", response)
        return Agent(
            agent_id=agent_id,
            name=agent_data.get("name", ""),
            email=agent_data.get("email", ""),
            status=agent_data.get("status", ""),
            team_id=agent_data.get("teamId"),
            is_available=agent_data.get("isAvailable", False),
            current_queue=agent_data.get("currentQueue")
        )

    async def list_agents(
        self,
        team_id: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 100
    ) -> List[Agent]:
        """List agents with optional filters"""
        params = {}
        if team_id:
            params["teamId"] = team_id
        if status:
            params["status"] = status
        if limit:
            params["limit"] = limit

        response = await self._make_request("GET", "/agents", params=params)
        agents_data = response.get("data", [])
        return [
            Agent(
                agent_id=a.get("id", ""),
                name=a.get("name", ""),
                email=a.get("email", ""),
                status=a.get("status", ""),
                team_id=a.get("teamId"),
                is_available=a.get("isAvailable", False),
                current_queue=a.get("currentQueue")
            )
            for a in agents_data[:limit]
        ]

    # ==================== Schedule Operations ====================

    async def create_schedule(
        self,
        name: str,
        start_date: str,
        end_date: str,
        timezone: str = "UTC"
    ) -> Schedule:
        """Create a new schedule"""
        data = {
            "name": name,
            "startDate": start_date,
            "endDate": end_date,
            "timezone": timezone
        }
        response = await self._make_request("POST", "/schedules", data=data)
        schedule_data = response.get("data", response)
        return Schedule(
            schedule_id=schedule_data.get("id", ""),
            name=schedule_data.get("name", name),
            start_date=schedule_data.get("startDate", start_date),
            end_date=schedule_data.get("endDate", end_date),
            timezone=schedule_data.get("timezone", timezone),
            created_at=schedule_data.get("createdAt", ""),
            shifts=schedule_data.get("shifts", [])
        )

    async def get_schedule(self, schedule_id: str) -> Schedule:
        """Get schedule by ID"""
        response = await self._make_request("GET", f"/schedules/{schedule_id}")
        schedule_data = response.get("data", response)
        return Schedule(
            schedule_id=schedule_data.get("id", ""),
            name=schedule_data.get("name", ""),
            start_date=schedule_data.get("startDate", ""),
            end_date=schedule_data.get("endDate", ""),
            timezone=schedule_data.get("timezone", ""),
            created_at=schedule_data.get("createdAt", ""),
            shifts=schedule_data.get("shifts", [])
        )

    async def update_schedule(
        self,
        schedule_id: str,
        **fields
    ) -> Schedule:
        """Update a schedule"""
        response = await self._make_request(
            "PUT",
            f"/schedules/{schedule_id}",
            data=fields
        )
        schedule_data = response.get("data", response)
        return Schedule(
            schedule_id=schedule_data.get("id", ""),
            name=schedule_data.get("name", ""),
            start_date=schedule_data.get("startDate", ""),
            end_date=schedule_data.get("endDate", ""),
            timezone=schedule_data.get("timezone", ""),
            created_at=schedule_data.get("createdAt", ""),
            shifts=schedule_data.get("shifts", [])
        )

    # ==================== Shift Operations ====================

    async def create_shift_assignment(
        self,
        schedule_id: str,
        agent_id: str,
        start_time: str,
        end_time: str,
        activity: str,
        queue: Optional[str] = None
    ) -> Shift:
        """Create a shift assignment"""
        data = {
            "scheduleId": schedule_id,
            "agentId": agent_id,
            "startTime": start_time,
            "endTime": end_time,
            "activity": activity
        }
        if queue:
            data["queue"] = queue

        response = await self._make_request("POST", "/shifts", data=data)
        shift_data = response.get("data", response)
        return Shift(
            shift_id=shift_data.get("id", ""),
            agent_id=shift_data.get("agentId", ""),
            start_time=shift_data.get("startTime", ""),
            end_time=shift_data.get("EndTime", ""),
            activity=shift_data.get("activity", ""),
            queue=shift_data.get("queue"),
            is_active=shift_data.get("isActive", False)
        )

    # ==================== Queue Operations ====================

    async def get_queue_status(self, queue_id: str) -> Queue:
        """Get current queue status"""
        response = await self._make_request("GET", f"/queues/{queue_id}/status")
        queue_data = response.get("data", response)
        return Queue(
            queue_id=queue_id,
            name=queue_data.get("name", ""),
            status=queue_data.get("status", ""),
            waiting_count=queue_data.get("waitingCount", 0),
            service_level=queue_data.get("serviceLevel", 0.0),
            average_wait_time=queue_data.get("averageWaitTime", 0.0)
        )

    async def list_queues(
        self,
        status: Optional[str] = None
    ) -> List[Queue]:
        """List all queues"""
        params = {}
        if status:
            params["status"] = status

        response = await self._make_request("GET", "/queues", params=params)
        queues_data = response.get("data", [])
        return [
            Queue(
                queue_id=q.get("id", ""),
                name=q.get("name", ""),
                status=q.get("status", ""),
                waiting_count=q.get("waitingCount", 0),
                service_level=q.get("serviceLevel", 0.0),
                average_wait_time=q.get("averageWaitTime", 0.0)
            )
            for q in queues_data
        ]

    # ==================== Performance Operations ====================

    async def get_performance_metrics(
        self,
        metric_type: str,
        agent_id: Optional[str] = None,
        queue_id: Optional[str] = None,
        period_start: Optional[str] = None,
        period_end: Optional[str] = None
    ) -> List[PerformanceMetric]:
        """Get performance metrics"""
        params = {"metricType": metric_type}
        if agent_id:
            params["agentId"] = agent_id
        if queue_id:
            params["queueId"] = queue_id
        if period_start:
            params["periodStart"] = period_start
        if period_end:
            params["periodEnd"] = period_end

        response = await self._make_request("GET", "/performance/metrics", params=params)
        metrics_data = response.get("data", [])
        return [
            PerformanceMetric(
                metric_name=m.get("metricName", ""),
                value=m.get("value", 0.0),
                target=m.get("target"),
                period_start=m.get("periodStart", ""),
                period_end=m.get("periodEnd", "")
            )
            for m in metrics_data
        ]

    # ==================== Adherence Operations ====================

    async def get_agent_adherence(self, agent_id: str) -> Adherence:
        """Get agent schedule adherence"""
        response = await self._make_request("GET", f"/agents/{agent_id}/adherence")
        adherence_data = response.get("data", response)
        return Adherence(
            agent_id=agent_id,
            schedule_adherence=adherence_data.get("scheduleAdherence", 0.0),
            is_in_adherence=adherence_data.get("isInAdherence", True),
            breach_reason=adherence_data.get("breachReason"),
            current_activity=adherence_data.get("currentActivity"),
            current_activity_start=adherence_data.get("currentActivityStart")
        )

    # ==================== Activity Operations ====================

    async def get_activity_logs(
        self,
        agent_id: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Get activity logs"""
        params = {}
        if agent_id:
            params["agentId"] = agent_id
        if limit:
            params["limit"] = limit

        response = await self._make_request("GET", "/activities", params=params)
        return response.get("data", [])

    # ==================== Webhook Handling ====================

    def handle_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle webhook events from Assembled"""
        event_type = webhook_data.get("event_type", "unknown")
        agent_id = webhook_data.get("agent_id")
        resource_type = webhook_data.get("resource_type", "unknown")

        return {
            "event_type": event_type,
            "agent_id": agent_id,
            "resource_type": resource_type,
            "raw_data": webhook_data
        }


async def main():
    """Example usage"""
    api_key = "your_assembled_api_key"

    async with AssembledClient(api_key) as client:
        # List agents
        agents = await client.list_agents(status="available", limit=10)
        print(f"Found {len(agents)} available agents")

        # Get queue status
        queues = await client.list_queues()
        if queues:
            queue = await client.get_queue_status(queues[0].queue_id)
            print(f"Queue '{queue.name}': {queue.waiting_count} waiting")

        # Get agent adherence
        if agents:
            adherence = await client.get_agent_adherence(agents[0].agent_id)
            print(f"Adherence: {adherence.schedule_adherence:.1%}")

if __name__ == "__main__":
    asyncio.run(main())