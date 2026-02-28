#!/usr/bin/env python3
"""
# Rd Station API Client
Generated for Yoom Apps Integration
"""

import asyncio
import aiohttp
import hmac
import hashlib
import time
from typing import Dict, List, Optional, Any, Union
from datetime import datetime


class #RdStationClient:
    """
    # Rd Station API Client with rate limiting and error handling
    """
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialize # Rd Station API client
        
        Args:
            api_key: API key for authentication
            base_url: Base URL for API endpoints
        """
        self.api_key = api_key or os.getenv(f"RD_STATION_API_KEY")
        self.base_url = base_url or "https://api.rd.services"
        
        # Rate limiting configuration
        self.rate_limit = {
            "requests_per_second": 10,
            "requests_per_minute": 1000,
        }
        
        self._last_request_time = 0
        self._request_count = 0
        self._minute_start_time = time.time()
    
    async def _wait_for_rate_limit(self):
        """Wait if necessary to respect rate limits"""
        current_time = time.time()
        
        # Reset counter if minute passed
        if current_time - self._minute_start_time >= 60:
            self._request_count = 0
            self._minute_start_time = current_time
        
        # Check per-second limit
        time_since_last_request = current_time - self._last_request_time
        if time_since_last_request < (1 / self.rate_limit["requests_per_second"]):
            await asyncio.sleep((1 / self.rate_limit["requests_per_second"]) - time_since_last_request)
        
        # Check per-minute limit
        if self._request_count >= self.rate_limit["requests_per_minute"]:
            time_until_reset = 60 - (current_time - self._minute_start_time)
            if time_until_reset > 0:
                await asyncio.sleep(time_until_reset)
                self._request_count = 0
                self._minute_start_time = time.time()
    
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers"""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        return headers
    
    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        files: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Make HTTP request with error handling
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            endpoint: API endpoint
            params: Query parameters
            data: Request body data
            files: Files to upload
            
        Returns:
            Response data as dictionary
            
        Raises:
            Exception: If request fails
        """
        await self._wait_for_rate_limit()
        
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers()
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    params=params,
                    json=data,
                    files=files,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    self._last_request_time = time.time()
                    self._request_count += 1
                    
                    # Handle response
                    response_text = await response.text()
                    
                    if response.status >= 400:
                        error_msg = f"API request failed: {response.status} - {response_text}"
                        if response.status == 429:
                            error_msg += " (Rate limit exceeded)"
                        elif response.status == 401:
                            error_msg += " (Unauthorized - check API key)"
                        elif response.status == 404:
                            error_msg += " (Resource not found)"
                        raise Exception(error_msg)
                    
                    if response_text:
                        try:
                            return await response.json()
                        except json.JSONDecodeError:
                            return {"status": "success", "raw_response": response_text}
                    
                    return {"status": "success"}
                    
        except aiohttp.ClientError as e:
            raise Exception(f"Network error: {str(e)}")
        except asyncio.TimeoutError:
            raise Exception("Request timeout")
        except Exception as e:
            raise Exception(f"Request failed: {str(e)}")

    async def create_default_conversion_event(self, **kwargs) -> Dict[str, Any]:
        """
        Create Default Conversion Event
        
        Returns:
            Response data
        """
        endpoint = "/create_default_conversion_event"
        return await self._request("POST", endpoint, data=kwargs)

    async def update_contact_information(self, **kwargs) -> Dict[str, Any]:
        """
        Update Contact Information
        
        Returns:
            Response data
        """
        endpoint = "/update_contact_information"
        return await self._request("POST", endpoint, data=kwargs)

    async def create_contact(self, **kwargs) -> Dict[str, Any]:
        """
        Create Contact
        
        Returns:
            Response data
        """
        endpoint = "/create_contact"
        return await self._request("POST", endpoint, data=kwargs)

    async def add_tag_to_lead(self, **kwargs) -> Dict[str, Any]:
        """
        Add Tag to Lead
        
        Returns:
            Response data
        """
        endpoint = "/add_tag_to_lead"
        return await self._request("POST", endpoint, data=kwargs)

    async def create_closing_event(self, **kwargs) -> Dict[str, Any]:
        """
        Create Closing Event
        
        Returns:
            Response data
        """
        endpoint = "/create_closing_event"
        return await self._request("POST", endpoint, data=kwargs)

    async def update_contact(self, **kwargs) -> Dict[str, Any]:
        """
        Update Contact
        
        Returns:
            Response data
        """
        endpoint = "/update_contact"
        return await self._request("POST", endpoint, data=kwargs)

    async def create_call_event(self, **kwargs) -> Dict[str, Any]:
        """
        Create Call Event
        
        Returns:
            Response data
        """
        endpoint = "/create_call_event"
        return await self._request("POST", endpoint, data=kwargs)

    async def create_abandonment_event(self, **kwargs) -> Dict[str, Any]:
        """
        Create Abandonment Event
        
        Returns:
            Response data
        """
        endpoint = "/create_abandonment_event"
        return await self._request("POST", endpoint, data=kwargs)

    async def get_contact(self, **kwargs) -> Dict[str, Any]:
        """
        Get Contact
        
        Returns:
            Response data
        """
        endpoint = "/get_contact"
        return await self._request("POST", endpoint, data=kwargs)

    async def delete_contact(self, **kwargs) -> Dict[str, Any]:
        """
        Delete Contact
        
        Returns:
            Response data
        """
        endpoint = "/delete_contact"
        return await self._request("POST", endpoint, data=kwargs)

    async def get_contact_information(self, **kwargs) -> Dict[str, Any]:
        """
        Get Contact Information
        
        Returns:
            Response data
        """
        endpoint = "/get_contact_information"
        return await self._request("POST", endpoint, data=kwargs)

    async def create_chat_starter_event(self, **kwargs) -> Dict[str, Any]:
        """
        Create Chat Starter Event
        
        Returns:
            Response data
        """
        endpoint = "/create_chat_starter_event"
        return await self._request("POST", endpoint, data=kwargs)
