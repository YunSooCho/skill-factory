"""
Landbot PlatformAPI - Chatbot Platform API

Supports:
- Send Text Message
- Send Image Message
- Get Channel
- List Channels
- Get Customer
- List Customers
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class Channel:
    """Channel representation"""
    id: str
    name: str
    type: str
    status: str


@dataclass
class Customer:
    """Customer representation"""
    customer_id: str
    name: str
    email: Optional[str]
    phone: Optional[str]
    metadata: Dict[str, Any]


@dataclass
class Message:
    """Message representation"""
    id: str
    type: str
    content: Dict[str, Any]
    status: str


class LandbotClient:
    """
    Landbot API client for chatbot platform operations.

    API Documentation: https://developers.landbot.io/api/v1.0
    Requires an API token from Landbot.
    """

    BASE_URL = "https://api.landbot.io/v1"

    def __init__(self, api_token: str):
        """
        Initialize Landbot client.

        Args:
            api_token: Landbot API token
        """
        self.api_token = api_token
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={"Authorization": f"Token {self.api_token}"}
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    # ==================== Channel Operations ====================

    async def get_channel(self, channel_id: str) -> Channel:
        """
        Get channel details.

        Args:
            channel_id: Channel ID

        Returns:
            Channel with channel data

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            async with self.session.get(
                f"{self.BASE_URL}/channels/{channel_id}"
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Landbot error: {data.get('error', 'Unknown error')}")

                return Channel(
                    id=data["id"],
                    name=data.get("name", ""),
                    type=data.get("type", ""),
                    status=data.get("status", "")
                )

        except Exception as e:
            raise Exception(f"Failed to get channel: {str(e)}")

    async def list_channels(self, limit: int = 20) -> List[Channel]:
        """
        List all channels.

        Args:
            limit: Maximum number of channels

        Returns:
            List of Channel

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            params = {"limit": limit}

            async with self.session.get(
                f"{self.BASE_URL}/channels",
                params=params
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Landbot error: {data.get('error', 'Unknown error')}")

                channels = [
                    Channel(
                        id=ch["id"],
                        name=ch.get("name", ""),
                        type=ch.get("type", ""),
                        status=ch.get("status", "")
                    )
                    for ch in data.get("channels", [])
                ]

                return channels

        except Exception as e:
            raise Exception(f"Failed to list channels: {str(e)}")

    # ==================== Customer Operations ====================

    async def get_customer(self, customer_id: str) -> Customer:
        """
        Get customer details.

        Args:
            customer_id: Customer ID

        Returns:
            Customer with customer data

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            async with self.session.get(
                f"{self.BASE_URL}/customers/{customer_id}"
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Landbot error: {data.get('error', 'Unknown error')}")

                return Customer(
                    customer_id=data["customer_id"],
                    name=data.get("name", ""),
                    email=data.get("email"),
                    phone=data.get("phone"),
                    metadata=data.get("metadata", {})
                )

        except Exception as e:
            raise Exception(f"Failed to get customer: {str(e)}")

    async def list_customers(self, limit: int = 20) -> List[Customer]:
        """
        List all customers.

        Args:
            limit: Maximum number of customers

        Returns:
            List of Customer

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            params = {"limit": limit}

            async with self.session.get(
                f"{self.BASE_URL}/customers",
                params=params
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Landbot error: {data.get('error', 'Unknown error')}")

                customers = [
                    Customer(
                        customer_id=c["customer_id"],
                        name=c.get("name", ""),
                        email=c.get("email"),
                        phone=c.get("phone"),
                        metadata=c.get("metadata", {})
                    )
                    for c in data.get("customers", [])
                ]

                return customers

        except Exception as e:
            raise Exception(f"Failed to list customers: {str(e)}")

    # ==================== Message Operations ====================

    async def send_text_message(
        self,
        channel_id: str,
        customer_id: str,
        message: str
    ) -> Message:
        """
        Send a text message to a customer.

        Args:
            channel_id: Channel ID
            customer_id: Customer ID
            message: Message text

        Returns:
            Message with delivery status

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "customer_id": customer_id,
                "channel_id": channel_id,
                "type": "text",
                "message": message
            }

            async with self.session.post(
                f"{self.BASE_URL}/messages/send",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Landbot error: {data.get('error', 'Unknown error')}")

                return Message(
                    id=data.get("id", ""),
                    type=data["type"],
                    content=data.get("content", {}),
                    status=data.get("status", "sent")
                )

        except Exception as e:
            raise Exception(f"Failed to send text message: {str(e)}")

    async def send_image_message(
        self,
        channel_id: str,
        customer_id: str,
        image_url: str,
        caption: Optional[str] = None
    ) -> Message:
        """
        Send an image message to a customer.

        Args:
            channel_id: Channel ID
            customer_id: Customer ID
            image_url: Image URL
            caption: Optional caption

        Returns:
            Message with delivery status

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "customer_id": customer_id,
                "channel_id": channel_id,
                "type": "image",
                "url": image_url
            }

            if caption:
                payload["caption"] = caption

            async with self.session.post(
                f"{self.BASE_URL}/messages/send",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Landbot error: {data.get('error', 'Unknown error')}")

                return Message(
                    id=data.get("id", ""),
                    type=data["type"],
                    content=data.get("content", {}),
                    status=data.get("status", "sent")
                )

        except Exception as e:
            raise Exception(f"Failed to send image message: {str(e)}")