"""
Retell AI - Voice AI and Phone Call API

Supports:
- Create Phone Call
- Create Web Call
- Get Phone Call
- Get Web Call
- Search Web Call
- Search Phone Call
- Get Phone Number Details
- Purchase and Assign Phone Number
- Add Sources to Knowledge Base (URL)
- Add Sources to Knowledge Base (Text)
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class PhoneCall:
    """Phone call representation"""
    call_id: str
    phone_number: str
    status: str
    duration: int
    started_at: str


@dataclass
class WebCall:
    """Web call representation"""
    call_id: str
    status: str
    duration: int
    started_at: str


@dataclass
class PhoneNumber:
    """Phone number details"""
    phone_number: str
    country_code: str
    assigned: bool


class RetellAIClient:
    """
    Retell AI API client for voice AI and phone calls.

    API Documentation: https://docs.retellai.com/api
    Requires an API key from Retell AI.
    """

    BASE_URL = "https://api.retellai.com/v1"

    def __init__(self, api_key: str):
        """
        Initialize Retell AI client.

        Args:
            api_key: Retell AI API key
        """
        self.api_key = api_key
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    # ==================== Phone Calls ====================

    async def create_phone_call(
        self,
        phone_number: str,
        agent_id: str,
        from_number: Optional[str] = None
    ) -> PhoneCall:
        """
        Create a phone call.

        Args:
            phone_number: Phone number to call
            agent_id: AI agent ID
            from_number: From number (optional)

        Returns:
            PhoneCall with call details

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "phone_number": phone_number,
                "agent_id": agent_id
            }

            if from_number:
                payload["from_number"] = from_number

            async with self.session.post(
                f"{self.BASE_URL}/phone-calls",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 201:
                    raise Exception(f"Retell AI error: {data.get('error', 'Unknown error')}")

                return PhoneCall(
                    call_id=data["call_id"],
                    phone_number=data["phone_number"],
                    status=data["status"],
                    duration=data.get("duration", 0),
                    started_at=data.get("started_at", "")
                )

        except Exception as e:
            raise Exception(f"Failed to create phone call: {str(e)}")

    async def get_phone_call(self, call_id: str) -> PhoneCall:
        """
        Get phone call details.

        Args:
            call_id: Call ID

        Returns:
            PhoneCall with call data

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            async with self.session.get(
                f"{self.BASE_URL}/phone-calls/{call_id}"
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Retell AI error: {data.get('error', 'Unknown error')}")

                return PhoneCall(
                    call_id=data["call_id"],
                    phone_number=data["phone_number"],
                    status=data["status"],
                    duration=data.get("duration", 0),
                    started_at=data.get("started_at", "")
                )

        except Exception as e:
            raise Exception(f"Failed to get phone call: {str(e)}")

    async def search_phone_calls(
        self,
        query: Optional[str] = None,
        limit: int = 20
    ) -> List[PhoneCall]:
        """
        Search phone calls.

        Args:
            query: Search query (optional)
            limit: Maximum results

        Returns:
            List of PhoneCall

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            params = {"limit": limit}

            if query:
                params["query"] = query

            async with self.session.get(
                f"{self.BASE_URL}/phone-calls/search",
                params=params
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Retell AI error: {data.get('error', 'Unknown error')}")

                calls = [
                    PhoneCall(
                        call_id=c["call_id"],
                        phone_number=c["phone_number"],
                        status=c["status"],
                        duration=c.get("duration", 0),
                        started_at=c.get("started_at", "")
                    )
                    for c in data.get("calls", [])
                ]

                return calls

        except Exception as e:
            raise Exception(f"Failed to search phone calls: {str(e)}")

    # ==================== Web Calls ====================

    async def create_web_call(self, agent_id: str) -> WebCall:
        """
        Create a web call.

        Args:
            agent_id: AI agent ID

        Returns:
            WebCall with call details

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {"agent_id": agent_id}

            async with self.session.post(
                f"{self.BASE_URL}/web-calls",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 201:
                    raise Exception(f"Retell AI error: {data.get('error', 'Unknown error')}")

                return WebCall(
                    call_id=data["call_id"],
                    status=data["status"],
                    duration=data.get("duration", 0),
                    started_at=data.get("started_at", "")
                )

        except Exception as e:
            raise Exception(f"Failed to create web call: {str(e)}")

    async def get_web_call(self, call_id: str) -> WebCall:
        """
        Get web call details.

        Args:
            call_id: Call ID

        Returns:
            WebCall with call data

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            async with self.session.get(
                f"{self.BASE_URL}/web-calls/{call_id}"
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Retell AI error: {data.get('error', 'Unknown error')}")

                return WebCall(
                    call_id=data["call_id"],
                    status=data["status"],
                    duration=data.get("duration", 0),
                    started_at=data.get("started_at", "")
                )

        except Exception as e:
            raise Exception(f"Failed to get web call: {str(e)}")

    async def search_web_calls(
        self,
        query: Optional[str] = None,
        limit: int = 20
    ) -> List[WebCall]:
        """
        Search web calls.

        Args:
            query: Search query (optional)
            limit: Maximum results

        Returns:
            List of WebCall

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            params = {"limit": limit}

            if query:
                params["query"] = query

            async with self.session.get(
                f"{self.BASE_URL}/web-calls/search",
                params=params
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Retell AI error: {data.get('error', 'Unknown error')}")

                calls = [
                    WebCall(
                        call_id=c["call_id"],
                        status=c["status"],
                        duration=c.get("duration", 0),
                        started_at=c.get("started_at", "")
                    )
                    for c in data.get("calls", [])
                ]

                return calls

        except Exception as e:
            raise Exception(f"Failed to search web calls: {str(e)}")

    # ==================== Phone Numbers ====================

    async def purchase_and_assign_phone_number(
        self,
        country_code: str = "US",
        area_code: Optional[str] = None
    ) -> PhoneNumber:
        """
        Purchase and assign a phone number.

        Args:
            country_code: Country code
            area_code: Desired area code (optional)

        Returns:
            PhoneNumber with phone number details

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "country_code": country_code
            }

            if area_code:
                payload["area_code"] = area_code

            async with self.session.post(
                f"{self.BASE_URL}/phone-numbers/purchase",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 201:
                    raise Exception(f"Retell AI error: {data.get('error', 'Unknown error')}")

                return PhoneNumber(
                    phone_number=data["phone_number"],
                    country_code=data["country_code"],
                    assigned=data["assigned"]
                )

        except Exception as e:
            raise Exception(f"Failed to purchase phone number: {str(e)}")

    async def get_phone_number_details(self, phone_number: str) -> PhoneNumber:
        """
        Get phone number details.

        Args:
            phone_number: Phone number

        Returns:
            PhoneNumber with details

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            async with self.session.get(
                f"{self.BASE_URL}/phone-numbers/{phone_number}"
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Retell AI error: {data.get('error', 'Unknown error')}")

                return PhoneNumber(
                    phone_number=data["phone_number"],
                    country_code=data["country_code"],
                    assigned=data["assigned"]
                )

        except Exception as e:
            raise Exception(f"Failed to get phone number details: {str(e)}")

    # ==================== Knowledge Base ====================

    async def add_sources_to_knowledge_base_url(
        self,
        urls: List[str],
        knowledge_base_id: Optional[str] = None
    ) -> bool:
        """
        Add URLs to knowledge base.

        Args:
            urls: List of URLs to add
            knowledge_base_id: Knowledge base ID (optional)

        Returns:
            True if successful

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {"urls": urls}

            if knowledge_base_id:
                payload["knowledge_base_id"] = knowledge_base_id

            async with self.session.post(
                f"{self.BASE_URL}/knowledge-base/sources/url",
                json=payload
            ) as response:
                if response.status != 200:
                    data = await response.json()
                    raise Exception(f"Retell AI error: {data.get('error', 'Unknown error')}")

                return True

        except Exception as e:
            raise Exception(f"Failed to add URLs to knowledge base: {str(e)}")

    async def add_sources_to_knowledge_base_text(
        self,
        texts: List[str],
        knowledge_base_id: Optional[str] = None
    ) -> bool:
        """
        Add text content to knowledge base.

        Args:
            texts: List of text content to add
            knowledge_base_id: Knowledge base ID (optional)

        Returns:
            True if successful

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {"texts": texts}

            if knowledge_base_id:
                payload["knowledge_base_id"] = knowledge_base_id

            async with self.session.post(
                f"{self.BASE_URL}/knowledge-base/sources/text",
                json=payload
            ) as response:
                if response.status != 200:
                    data = await response.json()
                    raise Exception(f"Retell AI error: {data.get('error', 'Unknown error')}")

                return True

        except Exception as e:
            raise Exception(f"Failed to add text to knowledge base: {str(e)}")