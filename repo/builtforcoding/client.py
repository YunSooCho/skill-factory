"""
BuiltForCoding API Client

Supports:
- Get Developer Resources
- Search Code Snippets
- Get Code Template
- Submit Code Snippet
- Rate Code Snippet
"""

import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class DeveloperResource:
    """Developer resource"""
    id: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    category: Optional[str] = None
    language: Optional[str] = None
    tags: List[str] = None
    added_at: Optional[str] = None
    rating: Optional[float] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []


@dataclass
class CodeSnippet:
    """Code snippet"""
    id: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    code: Optional[str] = None
    language: Optional[str] = None
    author: Optional[str] = None
    tags: List[str] = None
    rating: Optional[float] = None
    views: int = 0
    created_at: Optional[str] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []


@dataclass
class CodeTemplate:
    """Code template"""
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    framework: Optional[str] = None
    language: Optional[str] = None
    file_count: int = 0
    template_url: Optional[str] = None
    documentation_url: Optional[str] = None


class BuiltForCodingClient:
    """
    BuiltForCoding API client for developer resources and code snippets.

    Authentication: API Key (Header: X-API-Key)
    Base URL: https://api.builtforcoding.com/v1
    """

    BASE_URL = "https://api.builtforcoding.com/v1"

    def __init__(self, api_key: str):
        """
        Initialize BuiltForCoding client.

        Args:
            api_key: BuiltForCoding API key
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "X-API-Key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make API request with error handling and rate limiting"""
        url = f"{self.BASE_URL}{endpoint}"

        try:
            response = self.session.request(method, url, **kwargs)

            if response.status_code in (200, 201, 202, 204):
                if response.status_code == 204:
                    return {}
                data = response.json()
                return data
            elif response.status_code == 401:
                raise Exception("Authentication failed: Invalid API key")
            elif response.status_code == 404:
                raise Exception(f"Resource not found: {endpoint}")
            elif response.status_code == 429:
                raise Exception("Rate limit exceeded. Please retry later.")
            elif response.status_code >= 500:
                raise Exception(f"Server error: {response.status_code}")
            else:
                error_data = response.json() if response.content else {}
                raise Exception(f"API error {response.status_code}: {error_data}")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    # ==================== Developer Resources ====================

    def get_developer_resources(
        self,
        category: Optional[str] = None,
        language: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Get developer resources.

        Args:
            category: Filter by category
            language: Filter by programming language
            limit: Number of results
            offset: Pagination offset

        Returns:
            Resource list and pagination info
        """
        params: Dict[str, Any] = {
            "limit": limit,
            "offset": offset
        }

        if category:
            params["category"] = category
        if language:
            params["language"] = language

        result = self._request("GET", "/resources", params=params)

        resources = [self._parse_resource(r) for r in result.get("resources", [])]
        total = result.get("total", 0)

        return {
            "resources": resources,
            "total": total,
            "limit": limit,
            "offset": offset
        }

    # ==================== Code Snippets ====================

    def search_code_snippets(
        self,
        query: str,
        language: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 20,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Search for code snippets.

        Args:
            query: Search query
            language: Filter by programming language
            tags: Filter by tags
            limit: Number of results
            offset: Pagination offset

        Returns:
            Snippet list and pagination info
        """
        if not query:
            raise ValueError("Search query is required")

        params: Dict[str, Any] = {
            "q": query,
            "limit": limit,
            "offset": offset
        }

        if language:
            params["language"] = language
        if tags:
            params["tags"] = ",".join(tags)

        result = self._request("GET", "/snippets/search", params=params)

        snippets = [self._parse_snippet(s) for s in result.get("snippets", [])]
        total = result.get("total", 0)

        return {
            "snippets": snippets,
            "total": total,
            "limit": limit,
            "offset": offset
        }

    def get_code_snippet(self, snippet_id: str) -> CodeSnippet:
        """
        Get a specific code snippet.

        Args:
            snippet_id: Snippet ID

        Returns:
            CodeSnippet object
        """
        if not snippet_id:
            raise ValueError("Snippet ID is required")

        result = self._request("GET", f"/snippets/{snippet_id}")
        return self._parse_snippet(result)

    def submit_code_snippet(
        self,
        title: str,
        code: str,
        language: str,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        author: Optional[str] = None
    ) -> CodeSnippet:
        """
        Submit a new code snippet.

        Args:
            title: Snippet title
            code: Code content
            language: Programming language
            description: Snippet description
            tags: Tags for categorization
            author: Author name

        Returns:
            Created CodeSnippet object
        """
        if not title:
            raise ValueError("Title is required")
        if not code:
            raise ValueError("Code is required")
        if not language:
            raise ValueError("Language is required")

        payload: Dict[str, Any] = {
            "title": title,
            "code": code,
            "language": language
        }

        if description:
            payload["description"] = description
        if tags:
            payload["tags"] = tags
        if author:
            payload["author"] = author

        result = self._request("POST", "/snippets", json=payload)
        return self._parse_snippet(result)

    def rate_code_snippet(self, snippet_id: str, rating: int) -> Dict[str, Any]:
        """
        Rate a code snippet.

        Args:
            snippet_id: Snippet ID
            rating: Rating (1-5)

        Returns:
            Rating response
        """
        if not snippet_id:
            raise ValueError("Snippet ID is required")
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")

        payload = {"rating": rating}
        return self._request("POST", f"/snippets/{snippet_id}/rate", json=payload)

    # ==================== Code Templates ====================

    def get_code_templates(
        self,
        framework: Optional[str] = None,
        language: Optional[str] = None,
        limit: int = 20
    ) -> List[CodeTemplate]:
        """
        Get code templates.

        Args:
            framework: Filter by framework
            language: Filter by programming language
            limit: Number of results

        Returns:
            List of CodeTemplate objects
        """
        params: Dict[str, Any] = {"limit": limit}

        if framework:
            params["framework"] = framework
        if language:
            params["language"] = language

        result = self._request("GET", "/templates", params=params)
        return [self._parse_template(t) for t in result.get("templates", [])]

    def get_code_template(self, template_id: str) -> CodeTemplate:
        """
        Get a specific code template.

        Args:
            template_id: Template ID

        Returns:
            CodeTemplate object
        """
        if not template_id:
            raise ValueError("Template ID is required")

        result = self._request("GET", f"/templates/{template_id}")
        return self._parse_template(result)

    # ==================== Helper Methods ====================

    def _parse_resource(self, data: Dict[str, Any]) -> DeveloperResource:
        """Parse resource data from API response"""
        return DeveloperResource(
            id=data.get("id"),
            title=data.get("title"),
            description=data.get("description"),
            url=data.get("url"),
            category=data.get("category"),
            language=data.get("language"),
            tags=data.get("tags", []),
            added_at=data.get("added_at"),
            rating=data.get("rating")
        )

    def _parse_snippet(self, data: Dict[str, Any]) -> CodeSnippet:
        """Parse snippet data from API response"""
        return CodeSnippet(
            id=data.get("id"),
            title=data.get("title"),
            description=data.get("description"),
            code=data.get("code"),
            language=data.get("language"),
            author=data.get("author"),
            tags=data.get("tags", []),
            rating=data.get("rating"),
            views=data.get("views", 0),
            created_at=data.get("created_at")
        )

    def _parse_template(self, data: Dict[str, Any]) -> CodeTemplate:
        """Parse template data from API response"""
        return CodeTemplate(
            id=data.get("id"),
            name=data.get("name"),
            description=data.get("description"),
            framework=data.get("framework"),
            language=data.get("language"),
            file_count=data.get("file_count", 0),
            template_url=data.get("template_url"),
            documentation_url=data.get("documentation_url")
        )

    def close(self):
        """Close the HTTP session"""
        self.session.close()


def main():
    """Example usage"""
    api_key = "your_builtforcoding_api_key"

    client = BuiltForCodingClient(api_key=api_key)

    try:
        # Get developer resources
        resources_response = client.get_developer_resources(
            category="testing",
            language="python",
            limit=5
        )
        print(f"Resources: {len(resources_response['resources'])}")
        for r in resources_response['resources']:
            print(f"  - {r.title} ({r.rating}★)")

        # Search code snippets
        search_response = client.search_code_snippets(
            query="http request",
            language="python",
            limit=5
        )
        print(f"\nCode Snippets: {len(search_response['snippets'])}")
        for s in search_response['snippets'][:3]:
            print(f"  - {s.title} ({s.language})")

        # Submit code snippet
        snippet = client.submit_code_snippet(
            title="Simple HTTP Client",
            code="import requests\n\ndef fetch(url):\n    return requests.get(url).json()",
            language="python",
            description="Simple HTTP GET request function",
            tags=["http", "requests", "api"],
            author="Developer"
        )
        print(f"\nSnippet submitted: {snippet.id}")
        print(f"Title: {snippet.title}")

        # Rate the snippet
        client.rate_code_snippet(snippet.id, rating=5)
        print(f"Snippet rated: 5 stars")

        # Get code templates
        templates = client.get_code_templates(
            framework="react",
            language="javascript",
            limit=3
        )
        print(f"\nTemplates: {len(templates)}")
        for t in templates:
            print(f"  - {t.name} ({t.file_count} files)")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        client.close()


if __name__ == "__main__":
    main()