"""
Bland AI API Client - AI Phone Call Automation
"""

import requests
from typing import Optional, Dict, List, Any, BinaryIO
from datetime import datetime


class BlandAIError(Exception):
    """Base exception for Bland AI errors"""
    pass


class BlandAIClient:
    """Client for Bland AI API"""

    BASE_URL = "https://api.bland.ai/v1"

    def __init__(self, api_key: str):
        """
        Initialize Bland AI client

        Args:
            api_key: Bland AI API key
        """
        self.api_key = api_key
        self.headers = {
            "Authorization": api_key,
            "Content-Type": "application/json"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def _make_request(self, method: str, endpoint: str, json_data: Optional[Dict] = None,
                      params: Optional[Dict] = None, stream: bool = False) -> Any:
        """
        Make HTTP request to Bland AI API

        Args:
            method: HTTP method
            endpoint: API endpoint
            json_data: JSON payload
            params: Query parameters
            stream: Whether to stream response

        Returns:
            Response JSON data

        Raises:
            BlandAIError: If API request fails
        """
        url = f"{self.BASE_URL}{endpoint}"

        try:
            response = self.session.request(
                method=method,
                url=url,
                json=json_data,
                params=params,
                timeout=30,
                stream=stream
            )
            
            if response.status_code == 429:
                raise BlandAIError("Rate limit exceeded. Please try again later.")
            
            response.raise_for_status()
            
            if stream:
                return response
            return response.json()

        except requests.exceptions.RequestException as e:
            error_msg = f"API request failed: {str(e)}"
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    if 'errors' in error_data:
                        error_msg = f"API Error: {error_data['errors']}"
                    elif 'message' in error_data:
                        error_msg = error_data['message']
                except:
                    pass
            raise BlandAIError(error_msg) from e

    # Call Operations

    def send_call(self, phone_number: str, task: Optional[str] = None,
                  pathway_id: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """
        Send an AI phone call

        Args:
            phone_number: Phone number to call (E.164 format required)
            task: Task instructions for AI agent
            pathway_id: Pathway ID for pre-configured conversation
            **kwargs: Additional call parameters

        Returns:
            Call details with call_id

        Raises:
            BlandAIError: If call sending fails
        """
        if not task and not pathway_id:
            raise BlandAIError("Either task or pathway_id must be provided")

        call_data = {"phone_number": phone_number}

        if task:
            call_data["task"] = task

        if pathway_id:
            call_data["pathway_id"] = pathway_id

        call_data.update(kwargs)

        return self._make_request(
            method="POST",
            endpoint="/calls",
            json_data=call_data
        )

    def get_call(self, call_id: str) -> Dict[str, Any]:
        """
        Get call details

        Args:
            call_id: Call ID

        Returns:
            Call details

        Raises:
            BlandAIError: If call retrieval fails
        """
        return self._make_request(
            method="GET",
            endpoint=f"/calls/{call_id}"
        )

    def search_calls(self, phone_number: Optional[str] = None,
                     completed: Optional[bool] = None,
                     **kwargs) -> Dict[str, Any]:
        """
        Search for calls

        Args:
            phone_number: Filter by phone number
            completed: Filter by completed status
            **kwargs: Additional search parameters

        Returns:
            List of calls matching search criteria

        Raises:
            BlandAIError: If search fails
        """
        params = {}
        
        if phone_number:
            params["phone_number"] = phone_number
        
        if completed is not None:
            params["completed"] = str(completed).lower()
        
        params.update(kwargs)

        return self._make_request(
            method="GET",
            endpoint="/calls",
            params=params
        )

    def stop_call(self, call_id: str) -> Dict[str, Any]:
        """
        Stop an active call

        Args:
            call_id: Call ID to stop

        Returns:
            Stop confirmation

        Raises:
            BlandAIError: If stopping call fails
        """
        return self._make_request(
            method="POST",
            endpoint=f"/calls/{call_id}/stop"
        )

    # Transcript Operations

    def get_corrected_transcripts(self, call_id: str) -> Dict[str, Any]:
        """
        Get corrected transcripts for a call

        Args:
            call_id: Call ID

        Returns:
            Corrected transcript data

        Raises:
            BlandAIError: If transcript retrieval fails
        """
        return self._make_request(
            method="GET",
            endpoint=f"/calls/{call_id}/transcripts/corrected"
        )

    def get_transcripts(self, call_id: str) -> Dict[str, Any]:
        """
        Get transcripts for a call

        Args:
            call_id: Call ID

        Returns:
            Transcript data

        Raises:
            BlandAIError: If transcript retrieval fails
        """
        return self._make_request(
            method="GET",
            endpoint=f"/calls/{call_id}/transcripts"
        )

    # Audio Operations

    def get_audio_recording(self, call_id: str) -> Dict[str, Any]:
        """
        Get audio recording information

        Args:
            call_id: Call ID

        Returns:
            Audio recording information including URL

        Raises:
            BlandAIError: If audio info retrieval fails
        """
        return self._make_request(
            method="GET",
            endpoint=f"/calls/{call_id}/recording"
        )

    def download_recording(self, call_id: str, output_path: Optional[str] = None) -> BinaryIO:
        """
        Download call recording file

        Args:
            call_id: Call ID
            output_path: Optional path to save file

        Returns:
            Binary file content

        Raises:
            BlandAIError: If download fails
        """
        response = self._make_request(
            method="GET",
            endpoint=f"/calls/{call_id}/recording/download",
            stream=True
        )

        if output_path:
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

        return response

    # Knowledge Base Operations

    def create_knowledge_base(self, name: str, knowledge_base_type: str,
                               data: Any, **kwargs) -> Dict[str, Any]:
        """
        Create a knowledge base

        Args:
            name: Knowledge base name
            knowledge_base_type: Type of knowledge base (e.g., "text", "url")
            data: Knowledge base data (text content or URLs)
            **kwargs: Additional parameters

        Returns:
            Created knowledge base details

        Raises:
            BlandAIError: If knowledge base creation fails
        """
        kb_data = {
            "name": name,
            "type": knowledge_base_type,
            "data": data
        }

        kb_data.update(kwargs)

        return self._make_request(
            method="POST",
            endpoint="/knowledge-base",
            json_data=kb_data
        )

    def create_knowledge_base_from_text(self, name: str, text_content: str,
                                         **kwargs) -> Dict[str, Any]:
        """
        Create a knowledge base from text file

        Args:
            name: Knowledge base name
            text_content: Text content
            **kwargs: Additional parameters

        Returns:
            Created knowledge base details

        Raises:
            BlandAIError: If knowledge base creation fails
        """
        return self.create_knowledge_base(
            name=name,
            knowledge_base_type="text",
            data={"content": text_content},
            **kwargs
        )

    def create_knowledge_base_from_url(self, name: str, urls: List[str],
                                        **kwargs) -> Dict[str, Any]:
        """
        Create a knowledge base from URLs

        Args:
            name: Knowledge base name
            urls: List of URLs to scrape
            **kwargs: Additional parameters

        Returns:
            Created knowledge base details

        Raises:
            BlandAIError: If knowledge base creation fails
        """
        return self.create_knowledge_base(
            name=name,
            knowledge_base_type="url",
            data={"urls": urls},
            **kwargs
        )

    def get_knowledge_bases(self) -> Dict[str, Any]:
        """
        Get all knowledge bases

        Returns:
            List of knowledge bases

        Raises:
            BlandAIError: If retrieval fails
        """
        return self._make_request(
            method="GET",
            endpoint="/knowledge-base"
        )

    def delete_knowledge_base(self, knowledge_base_id: str) -> Dict[str, Any]:
        """
        Delete a knowledge base

        Args:
            knowledge_base_id: Knowledge base ID

        Returns:
            Deletion confirmation

        Raises:
            BlandAIError: If deletion fails
        """
        return self._make_request(
            method="DELETE",
            endpoint=f"/knowledge-base/{knowledge_base_id}"
        )

    # Analysis Operations

    def get_call_analysis(self, call_id: str) -> Dict[str, Any]:
        """
        Get call analysis

        Args:
            call_id: Call ID

        Returns:
            Call analysis data

        Raises:
            BlandAIError: If analysis retrieval fails
        """
        return self._make_request(
            method="GET",
            endpoint=f"/calls/{call_id}/analysis"
        )

    def get_citations(self, call_id: str) -> Dict[str, Any]:
        """
        Get citation data for call

        Args:
            call_id: Call ID

        Returns:
            Citation data

        Raises:
            BlandAIError: If citation retrieval fails
        """
        return self._make_request(
            method="GET",
            endpoint=f"/calls/{call_id}/citations"
        )

    # Trigger (Webhook simulation)

    def register_webhook(self, webhook_url: str, events: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Register webhook for receiving call events

        Args:
            webhook_url: Webhook URL
            events: List of events to subscribe (e.g., ["end_call", "call_ended"])

        Returns:
            Registration confirmation

        Raises:
            BlandAIError: If webhook registration fails
        """
        if events is None:
            events = ["end_call"]

        webhook_data = {
            "webhook_url": webhook_url,
            "events": events
        }

        return self._make_request(
            method="POST",
            endpoint="/webhooks",
            json_data=webhook_data
        )

    def close(self):
        """Close the session"""
        self.session.close()