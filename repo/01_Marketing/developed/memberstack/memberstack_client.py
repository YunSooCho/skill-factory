#!/usr/bin/env python3
"""
# Memberstack API Client
Generated for Yoom Apps Integration
"""

import asyncio
import aiohttp
import hmac
import hashlib
import time
from typing import Dict, List, Optional, Any, Union
from datetime import datetime


class #MemberstackClient:
    """
    # Memberstack API Client with rate limiting and error handling
    """
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialize # Memberstack API client
        
        Args:
            api_key: API key for authentication
            base_url: Base URL for API endpoints
        """
        self.api_key = api_key or os.getenv(f"MEMBERSTACK_API_KEY")
        self.base_url = base_url or "https://api.memberstack.com"
        
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

    async def delete_a_member(self, **kwargs) -> Dict[str, Any]:
        """
        Delete a member
        
        Returns:
            Response data
        """
        endpoint = "/delete_a_member"
        return await self._request("POST", endpoint, data=kwargs)

    async def list_all_members(self, **kwargs) -> Dict[str, Any]:
        """
        List all members
        
        Returns:
            Response data
        """
        endpoint = "/list_all_members"
        return await self._request("POST", endpoint, data=kwargs)

    async def verify_member_39_s_token(self, **kwargs) -> Dict[str, Any]:
        """
        Verify Member&#39;s Token
        
        Returns:
            Response data
        """
        endpoint = "/verify_member_39_s_token"
        return await self._request("POST", endpoint, data=kwargs)

    async def retrieve_a_member(self, **kwargs) -> Dict[str, Any]:
        """
        Retrieve a member
        
        Returns:
            Response data
        """
        endpoint = "/retrieve_a_member"
        return await self._request("POST", endpoint, data=kwargs)

    async def remove_a_free_plan_from_a_member(self, **kwargs) -> Dict[str, Any]:
        """
        Remove a free plan from a member
        
        Returns:
            Response data
        """
        endpoint = "/remove_a_free_plan_from_a_member"
        return await self._request("POST", endpoint, data=kwargs)

    async def add_a_free_plan_to_a_member(self, **kwargs) -> Dict[str, Any]:
        """
        Add a free plan to a member
        
        Returns:
            Response data
        """
        endpoint = "/add_a_free_plan_to_a_member"
        return await self._request("POST", endpoint, data=kwargs)

    async def create_a_member(self, **kwargs) -> Dict[str, Any]:
        """
        Create a member
        
        Returns:
            Response data
        """
        endpoint = "/create_a_member"
        return await self._request("POST", endpoint, data=kwargs)

    async def update_a_member(self, **kwargs) -> Dict[str, Any]:
        """
        Update a member
        
        Returns:
            Response data
        """
        endpoint = "/update_a_member"
        return await self._request("POST", endpoint, data=kwargs)

    async def handle_member_updated_trigger(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle Member Updated trigger event
        
        Args:
            payload: Event payload
            
        Returns:
            Response data
        """
        # Validate webhook signature if applicable
        # Process trigger event
        return {
            "status": "success",
            "trigger": "Member Updated",
            "processed_at": datetime.now().isoformat()
        }

    async def handle_new_member_trigger(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle New Member trigger event
        
        Args:
            payload: Event payload
            
        Returns:
            Response data
        """
        # Validate webhook signature if applicable
        # Process trigger event
        return {
            "status": "success",
            "trigger": "New Member",
            "processed_at": datetime.now().isoformat()
        }

    async def handle_member_39_s_plan_updated_trigger(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle Member&#39;s Plan Updated trigger event
        
        Args:
            payload: Event payload
            
        Returns:
            Response data
        """
        # Validate webhook signature if applicable
        # Process trigger event
        return {
            "status": "success",
            "trigger": "Member&#39;s Plan Updated",
            "processed_at": datetime.now().isoformat()
        }

    async def handle_member_39_s_plan_canceled_trigger(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle Member&#39;s Plan Canceled trigger event
        
        Args:
            payload: Event payload
            
        Returns:
            Response data
        """
        # Validate webhook signature if applicable
        # Process trigger event
        return {
            "status": "success",
            "trigger": "Member&#39;s Plan Canceled",
            "processed_at": datetime.now().isoformat()
        }

    async def handle_member_deleted_trigger(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle Member Deleted trigger event
        
        Args:
            payload: Event payload
            
        Returns:
            Response data
        """
        # Validate webhook signature if applicable
        # Process trigger event
        return {
            "status": "success",
            "trigger": "Member Deleted",
            "processed_at": datetime.now().isoformat()
        }

    async def handle_member_39_s_plan_added_trigger(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle Member&#39;s Plan Added trigger event
        
        Args:
            payload: Event payload
            
        Returns:
            Response data
        """
        # Validate webhook signature if applicable
        # Process trigger event
        return {
            "status": "success",
            "trigger": "Member&#39;s Plan Added",
            "processed_at": datetime.now().isoformat()
        }
