"""
Promptitude API Client - Prompt Management & Text Generation
"""

import requests
from typing import Optional, Dict, List, Any
from datetime import datetime


class PromptitudeError(Exception):
    """Base exception for Promptitude errors"""
    pass


class PromptitudeClient:
    """Client for Promptitude API"""

    BASE_URL = "https://api.promptitude.io/v1"

    def __init__(self, api_key: str):
        """
        Initialize Promptitude client

        Args:
            api_key: Promptitude API key
        """
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def _make_request(self, method: str, endpoint: str, json_data: Optional[Dict] = None,
                      params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make HTTP request to Promptitude API

        Args:
            method: HTTP method
            endpoint: API endpoint
            json_data: JSON payload
            params: Query parameters

        Returns:
            Response JSON data

        Raises:
            PromptitudeError: If API request fails
        """
        url = f"{self.BASE_URL}{endpoint}"

        try:
            response = self.session.request(
                method=method,
                url=url,
                json=json_data,
                params=params,
                timeout=60  # Longer timeout for generation
            )

            if response.status_code == 429:
                raise PromptitudeError("Rate limit exceeded. Please try again later.")

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            error_msg = f"API request failed: {str(e)}"
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    if 'error' in error_data:
                        error_msg = error_data['error']
                    elif 'message' in error_data:
                        error_msg = error_data['message']
                except:
                    pass
            raise PromptitudeError(error_msg) from e

    # Prompt Generation Methods

    def generate_text(self, prompt: str, model: Optional[str] = None,
                      max_tokens: Optional[int] = None,
                      temperature: Optional[float] = None,
                      **kwargs) -> Dict[str, Any]:
        """
        Generate text from a prompt

        Args:
            prompt: Input prompt for text generation
            model: Model to use (default: platform default)
            max_tokens: Maximum tokens to generate
            temperature: Temperature (0-1, controls randomness)
            **kwargs: Additional generation parameters

        Returns:
            Generated text with metadata

        Raises:
            PromptitudeError: If generation fails
        """
        generation_data = {
            "prompt": prompt
        }

        if model:
            generation_data["model"] = model

        if max_tokens:
            generation_data["max_tokens"] = max_tokens

        if temperature is not None:
            generation_data["temperature"] = temperature

        generation_data.update(kwargs)

        return self._make_request(
            method="POST",
            endpoint="/generate",
            json_data=generation_data
        )

    def generate_text_from_template(self, template_id: str,
                                     variables: Optional[Dict[str, Any]] = None,
                                     **kwargs) -> Dict[str, Any]:
        """
        Generate text from a saved template

        Args:
            template_id: ID of the template to use
            variables: Variables to substitute in template
            **kwargs: Additional generation parameters

        Returns:
            Generated text with metadata

        Raises:
            PromptitudeError: If generation fails
        """
        generation_data = {
            "template_id": template_id
        }

        if variables:
            generation_data["variables"] = variables

        generation_data.update(kwargs)

        return self._make_request(
            method="POST",
            endpoint="/generate/from-template",
            json_data=generation_data
        )

    # Rating Methods

    def rate_prompt_output(self, prompt_id: str, rating: float,
                           feedback: Optional[str] = None,
                           metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Rate a prompt output

        Args:
            prompt_id: ID of the prompt/output to rate
            rating: Rating score (typically 1-5 or 1-10)
            feedback: Optional text feedback
            metadata: Additional metadata for the rating

        Returns:
            Rating confirmation

        Raises:
            PromptitudeError: If rating fails
        """
        rating_data = {
            "prompt_id": prompt_id,
            "rating": rating
        }

        if feedback:
            rating_data["feedback"] = feedback

        if metadata:
            rating_data["metadata"] = metadata

        return self._make_request(
            method="POST",
            endpoint="/ratings",
            json_data=rating_data
        )

    def get_ratings(self, prompt_id: Optional[str] = None,
                    limit: Optional[int] = None) -> Dict[str, Any]:
        """
        Get ratings for prompts

        Args:
            prompt_id: Optional prompt ID to filter
            limit: Maximum number of ratings to return

        Returns:
            Ratings data

        Raises:
            PromptitudeError: If retrieval fails
        """
        params = {}
        
        if prompt_id:
            params["prompt_id"] = prompt_id
        
        if limit:
            params["limit"] = limit

        return self._make_request(
            method="GET",
            endpoint="/ratings",
            params=params
        )

    # Content Management Methods

    def create_prompt_template(self, name: str, template: str,
                                description: Optional[str] = None,
                                tags: Optional[List[str]] = None,
                                variables: Optional[List[str]] = None,
                                **kwargs) -> Dict[str, Any]:
        """
        Create a new prompt template

        Args:
            name: Template name
            template: Template content with variable placeholders
            description: Optional template description
            tags: Optional tags for organization
            variables: List of variable names used in template
            **kwargs: Additional template parameters

        Returns:
            Created template details

        Raises:
            PromptitudeError: If creation fails
        """
        template_data = {
            "name": name,
            "template": template
        }

        if description:
            template_data["description"] = description

        if tags:
            template_data["tags"] = tags

        if variables:
            template_data["variables"] = variables

        template_data.update(kwargs)

        return self._make_request(
            method="POST",
            endpoint="/templates",
            json_data=template_data
        )

    def update_prompt_template(self, template_id: str, **kwargs) -> Dict[str, Any]:
        """
        Update an existing prompt template

        Args:
            template_id: ID of template to update
            **kwargs: Fields to update

        Returns:
            Updated template details

        Raises:
            PromptitudeError: If update fails
        """
        return self._make_request(
            method="PUT",
            endpoint=f"/templates/{template_id}",
            json_data=kwargs
        )

    def get_prompt_templates(self, tags: Optional[List[str]] = None,
                            limit: Optional[int] = None) -> Dict[str, Any]:
        """
        Get all prompt templates

        Args:
            tags: Filter by tags
            limit: Maximum number of templates to return

        Returns:
            List of templates

        Raises:
            PromptitudeError: If retrieval fails
        """
        params = {}
        
        if tags:
            params["tags"] = ",".join(tags)
        
        if limit:
            params["limit"] = limit

        return self._make_request(
            method="GET",
            endpoint="/templates",
            params=params
        )

    def get_prompt_template(self, template_id: str) -> Dict[str, Any]:
        """
        Get a specific prompt template

        Args:
            template_id: Template ID

        Returns:
            Template details

        Raises:
            PromptitudeError: If retrieval fails
        """
        return self._make_request(
            method="GET",
            endpoint=f"/templates/{template_id}"
        )

    def delete_prompt_template(self, template_id: str) -> Dict[str, Any]:
        """
        Delete a prompt template

        Args:
            template_id: Template ID

        Returns:
            Deletion confirmation

        Raises:
            PromptitudeError: If deletion fails
        """
        return self._make_request(
            method="DELETE",
            endpoint=f"/templates/{template_id}"
        )

    # Content Organization Methods

    def create_folder(self, name: str, parent_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a folder for organizing templates

        Args:
            name: Folder name
            parent_id: Optional parent folder ID

        Returns:
            Created folder details

        Raises:
            PromptitudeError: If creation fails
        """
        folder_data = {"name": name}
        
        if parent_id:
            folder_data["parent_id"] = parent_id

        return self._make_request(
            method="POST",
            endpoint="/folders",
            json_data=folder_data
        )

    def get_folders(self, parent_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get all folders

        Args:
            parent_id: Optional parent folder to filter

        Returns:
            List of folders

        Raises:
            PromptitudeError: If retrieval fails
        """
        params = {}
        
        if parent_id:
            params["parent_id"] = parent_id

        return self._make_request(
            method="GET",
            endpoint="/folders",
            params=params
        )

    def move_content(self, content_id: str, content_type: str,
                     target_folder_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Move content to a different folder

        Args:
            content_id: ID of content to move
            content_type: Type of content ("template" or "folder")
            target_folder_id: Target folder ID (None for root)

        Returns:
            Move confirmation

        Raises:
            PromptitudeError: If move fails
        """
        move_data = {
            "content_id": content_id,
            "content_type": content_type
        }
        
        if target_folder_id:
            move_data["target_folder_id"] = target_folder_id

        return self._make_request(
            method="POST",
            endpoint="/content/move",
            json_data=move_data
        )

    # Analytics Methods

    def get_generation_stats(self, template_id: Optional[str] = None,
                            start_date: Optional[str] = None,
                            end_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Get generation statistics

        Args:
            template_id: Optional template ID to filter
            start_date: Start date (ISO format)
            end_date: End date (ISO format)

        Returns:
            Statistics data

        Raises:
            PromptitudeError: If retrieval fails
        """
        params = {}
        
        if template_id:
            params["template_id"] = template_id
        
        if start_date:
            params["start_date"] = start_date
        
        if end_date:
            params["end_date"] = end_date

        return self._make_request(
            method="GET",
            endpoint="/analytics/generations",
            params=params
        )

    # Model Methods

    def get_available_models(self) -> Dict[str, Any]:
        """
        Get list of available models

        Returns:
            List of available models with capabilities

        Raises:
            PromptitudeError: If retrieval fails
        """
        return self._make_request(
            method="GET",
            endpoint="/models"
        )

    def close(self):
        """Close the session"""
        self.session.close()