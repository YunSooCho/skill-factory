"""
Exa AI API Client - AI-Powered Web Search
"""

import requests
from typing import Optional, Dict, List, Any
from datetime import datetime


class ExaAIError(Exception):
    """Base exception for Exa AI errors"""
    pass


class ExaAIClient:
    """Client for Exa AI API"""

    BASE_URL = "https://api.exa.ai"

    def __init__(self, api_key: str):
        """
        Initialize Exa AI client

        Args:
            api_key: Exa AI API key
        """
        self.api_key = api_key
        self.headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def _make_request(self, method: str, endpoint: str, json_data: Optional[Dict] = None,
                      params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make HTTP request to Exa AI API

        Args:
            method: HTTP method
            endpoint: API endpoint
            json_data: JSON payload
            params: Query parameters

        Returns:
            Response JSON data

        Raises:
            ExaAIError: If API request fails
        """
        url = f"{self.BASE_URL}{endpoint}"

        try:
            response = self.session.request(
                method=method,
                url=url,
                json=json_data,
                params=params,
                timeout=30
            )

            if response.status_code == 429:
                raise ExaAIError("Rate limit exceeded. Please try again later.")

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
            raise ExaAIError(error_msg) from e

    # Search Operations

    def search_url(self, query: str, query_type: str = "auto",
                   num_results: int = 10, **kwargs) -> Dict[str, Any]:
        """
        Search for URLs based on a query

        Args:
            query: Search query
            query_type: Type of search ("auto", "neural", "keyword", "magic")
            num_results: Number of results to return (max 100)
            **kwargs: Additional search parameters

        Returns:
            Search results with URLs

        Raises:
            ExaAIError: If search fails
        """
        search_data = {
            "query": query,
            "type": query_type,
            "numResults": num_results
        }

        search_data.update(kwargs)

        return self._make_request(
            method="POST",
            endpoint="/search",
            json_data=search_data
        )

    def search_contents(self, query: str, query_type: str = "auto",
                        num_results: int = 10, max_characters: Optional[int] = None,
                        **kwargs) -> Dict[str, Any]:
        """
        Search for URLs with full page contents

        Args:
            query: Search query
            query_type: Type of search
            num_results: Number of results
            max_characters: Maximum characters per result
            **kwargs: Additional parameters

        Returns:
            Search results with full text content

        Raises:
            ExaAIError: If search fails
        """
        contents_config = {
            "text": {}
        }

        if max_characters:
            contents_config["text"]["maxCharacters"] = max_characters

        search_data = {
            "query": query,
            "type": query_type,
            "numResults": num_results,
            "contents": contents_config
        }

        search_data.update(kwargs)

        return self._make_request(
            method="POST",
            endpoint="/search",
            json_data=search_data
        )

    def search_highlights(self, query: str, query_type: str = "auto",
                          num_results: int = 10, max_characters: int = 4000,
                          **kwargs) -> Dict[str, Any]:
        """
        Search for URLs with highlighted content

        Args:
            query: Search query
            query_type: Type of search
            num_results: Number of results
            max_characters: Maximum characters for highlights
            **kwargs: Additional parameters

        Returns:
            Search results with highlighted content

        Raises:
            ExaAIError: If search fails
        """
        search_data = {
            "query": query,
            "type": query_type,
            "numResults": num_results,
            "contents": {
                "highlights": {
                    "maxCharacters": max_characters
                }
            }
        }

        search_data.update(kwargs)

        return self._make_request(
            method="POST",
            endpoint="/search",
            json_data=search_data
        )

    # Content Operations

    def get_page_contents(self, urls: List[str], 
                          max_characters: Optional[int] = None) -> Dict[str, Any]:
        """
        Get contents of specific URLs

        Args:
            urls: List of URLs to fetch
            max_characters: Maximum characters per page

        Returns:
            Page contents for each URL

        Raises:
            ExaAIError: If content retrieval fails
        """
        contents_data = {
            "urls": urls,
            "contents": {
                "text": {}
            }
        }

        if max_characters:
            contents_data["contents"]["text"]["maxCharacters"] = max_characters

        return self._make_request(
            method="POST",
            endpoint="/contents",
            json_data=contents_data
        )

    def find_similar(self, url: str, num_results: int = 10, **kwargs) -> Dict[str, Any]:
        """
        Find pages similar to a given URL

        Args:
            url: URL to find similar pages for
            num_results: Number of results
            **kwargs: Additional parameters

        Returns:
            Similar pages

        Raises:
            ExaAIError: If search fails
        """
        search_data = {
            "url": url,
            "numResults": num_results
        }

        search_data.update(kwargs)

        return self._make_request(
            method="POST",
            endpoint="/findSimilar",
            json_data=search_data
        )

    def autocomplete_query(self, query: str, num_results: int = 5, **kwargs) -> Dict[str, Any]:
        """
        Autocomplete/suggest queries

        Args:
            query: Partial query
            num_results: Number of suggestions
            **kwargs: Additional parameters

        Returns:
            Query suggestions

        Raises:
            ExaAIError: If autocomplete fails
        """
        search_data = {
            "query": query,
            "numResults": num_results
        }

        search_data.update(kwargs)

        return self._make_request(
            method="POST",
            endpoint="/autocomplete",
            json_data=search_data
        )

    # Task Operations

    def create_task(self, task_type: str, query: Optional[str] = None,
                    urls: Optional[List[str]] = None, **kwargs) -> Dict[str, Any]:
        """
        Create a search/analysis task

        Args:
            task_type: Type of task ("search", "findSimilar", "contents")
            query: Search query (for search tasks)
            urls: URLs (for contents/findSimilar tasks)
            **kwargs: Additional task parameters

        Returns:
            Task results

        Raises:
            ExaAIError: If task creation fails
        """
        task_data = {
            "type": task_type
        }

        if query:
            task_data["query"] = query

        if urls:
            task_data["urls"] = urls

        task_data.update(kwargs)

        endpoint_map = {
            "search": "/search",
            "findSimilar": "/findSimilar",
            "contents": "/contents"
        }

        endpoint = endpoint_map.get(task_type, "/search")

        return self._make_request(
            method="POST",
            endpoint=endpoint,
            json_data=task_data
        )

    # Advanced Operations

    def get_answer(self, question: str, search_context: Optional[Dict] = None,
                   **kwargs) -> Dict[str, Any]:
        """
        Get an answer to a question using search results

        Args:
            question: Question to answer
            search_context: Optional search context
            **kwargs: Additional parameters

        Returns:
            Answer with citations

        Raises:
            ExaAIError: If answer retrieval fails
        """
        # First search for relevant content
        search_result = self.search_highlights(
            query=question,
            num_results=kwargs.get("num_results", 5),
            max_characters=kwargs.get("max_characters", 4000)
        )

        # Extract answer from search results
        results = search_result.get("results", [])
        
        if not results:
            return {
                "answer": "No relevant information found.",
                "citations": [],
                "question": question
            }

        # Combine highlights for context
        highlights = []
        citations = []
        
        for result in results:
            if "highlights" in result.get("contents", {}):
                highlights.extend(result["contents"]["highlights"])
            
            citations.append({
                "title": result.get("title"),
                "url": result.get("url"),
                "score": result.get("score")
            })

        # In a real implementation, you would use an LLM to generate the answer
        # This is a simplified version
        context_text = " ".join(highlights[:3]) if highlights else "No context available"
        
        return {
            "answer": f"Based on search results: {context_text[:500] if context_text else 'No answer available'}",
            "citations": citations,
            "question": question,
            "search_results": results
        }

    # Filter and Category Operations

    def search_with_category(self, query: str, category: str, 
                             query_type: str = "auto",
                             num_results: int = 10, **kwargs) -> Dict[str, Any]:
        """
        Search with specific category filters

        Args:
            query: Search query
            category: Category filter (e.g., "company", "researchPaper", "news")
            query_type: Type of search
            num_results: Number of results
            **kwargs: Additional parameters

        Returns:
            Filtered search results

        Raises:
            ExaAIError: If search fails
        """
        search_data = {
            "query": query,
            "type": query_type,
            "numResults": num_results,
            "category": category
        }

        search_data.update(kwargs)

        return self._make_request(
            method="POST",
            endpoint="/search",
            json_data=search_data
        )

    def search_with_domain(self, query: str, domain: str,
                           query_type: str = "auto",
                           num_results: int = 10, **kwargs) -> Dict[str, Any]:
        """
        Search within specific domains

        Args:
            query: Search query
            domain: Domain to search within
            query_type: Type of search
            num_results: Number of results
            **kwargs: Additional parameters

        Returns:
            Domain-specific search results

        Raises:
            ExaAIError: If search fails
        """
        search_data = {
            "query": query,
            "type": query_type,
            "numResults": num_results,
            "includeDomains": [domain]
        }

        search_data.update(kwargs)

        return self._make_request(
            method="POST",
            endpoint="/search",
            json_data=search_data
        )

    def close(self):
        """Close the session"""
        self.session.close()