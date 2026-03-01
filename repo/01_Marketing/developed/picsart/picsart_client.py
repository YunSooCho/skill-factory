#!/usr/bin/env python3
"""
# Picsart API Client
Generated for Yoom Apps Integration
"""

import asyncio
import aiohttp
import hmac
import hashlib
import time
from typing import Dict, List, Optional, Any, Union
from datetime import datetime


class #PicsartClient:
    """
    # Picsart API Client with rate limiting and error handling
    """
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialize # Picsart API client
        
        Args:
            api_key: API key for authentication
            base_url: Base URL for API endpoints
        """
        self.api_key = api_key or os.getenv(f"PICSART_API_KEY")
        self.base_url = base_url or "https://api.picsart.io"
        
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

    async def ultra_upscale(self, **kwargs) -> Dict[str, Any]:
        """
        Ultra Upscale
        
        Returns:
            Response data
        """
        endpoint = "/ultra_upscale"
        return await self._request("POST", endpoint, data=kwargs)

    async def download_image_file(self, **kwargs) -> Dict[str, Any]:
        """
        Download Image File
        
        Returns:
            Response data
        """
        endpoint = "/download_image_file"
        return await self._request("POST", endpoint, data=kwargs)

    async def create_image(self, **kwargs) -> Dict[str, Any]:
        """
        Create Image
        
        Returns:
            Response data
        """
        endpoint = "/create_image"
        return await self._request("POST", endpoint, data=kwargs)

    async def inpaint_image(self, **kwargs) -> Dict[str, Any]:
        """
        Inpaint Image
        
        Returns:
            Response data
        """
        endpoint = "/inpaint_image"
        return await self._request("POST", endpoint, data=kwargs)

    async def expand_image(self, **kwargs) -> Dict[str, Any]:
        """
        Expand Image
        
        Returns:
            Response data
        """
        endpoint = "/expand_image"
        return await self._request("POST", endpoint, data=kwargs)

    async def create_sticker(self, **kwargs) -> Dict[str, Any]:
        """
        Create Sticker
        
        Returns:
            Response data
        """
        endpoint = "/create_sticker"
        return await self._request("POST", endpoint, data=kwargs)

    async def face_enhancement(self, **kwargs) -> Dict[str, Any]:
        """
        Face Enhancement
        
        Returns:
            Response data
        """
        endpoint = "/face_enhancement"
        return await self._request("POST", endpoint, data=kwargs)

    async def get_image(self, **kwargs) -> Dict[str, Any]:
        """
        Get Image
        
        Returns:
            Response data
        """
        endpoint = "/get_image"
        return await self._request("POST", endpoint, data=kwargs)

    async def remove_amp_change_background(self, **kwargs) -> Dict[str, Any]:
        """
        Remove &amp; Change Background
        
        Returns:
            Response data
        """
        endpoint = "/remove_amp_change_background"
        return await self._request("POST", endpoint, data=kwargs)

    async def get_sticker(self, **kwargs) -> Dict[str, Any]:
        """
        Get Sticker
        
        Returns:
            Response data
        """
        endpoint = "/get_sticker"
        return await self._request("POST", endpoint, data=kwargs)
