"""
BlogTrekker API Client

Supports:
- Analyze Blog Post
- Get SEO Analysis
- Get Content Suggestions
- Analyze Competitor Blog
- Track Keyword Rankings
- Get Backlink Analysis
"""

import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class BlogAnalysis:
    """Blog post analysis result"""
    url: Optional[str] = None
    title: Optional[str] = None
    word_count: Optional[int] = None
    readability_score: Optional[float] = None
    seo_score: Optional[float] = None
    keywords: List[str] = None
    suggestions: List[str] = None
    analyzed_at: Optional[str] = None

    def __post_init__(self):
        if self.keywords is None:
            self.keywords = []
        if self.suggestions is None:
            self.suggestions = []


@dataclass
class SEOAnalysis:
    """SEO analysis data"""
    url: Optional[str] = None
    title_optimization: Dict[str, Any] = None
    meta_description: Dict[str, Any] = None
    heading_structure: Dict[str, Any] = None
    keyword_density: Dict[str, float] = None
    internal_links: int = 0
    external_links: int = 0
    overall_score: Optional[float] = None

    def __post_init__(self):
        if self.title_optimization is None:
            self.title_optimization = {}
        if self.meta_description is None:
            self.meta_description = {}
        if self.heading_structure is None:
            self.heading_structure = {}
        if self.keyword_density is None:
            self.keyword_density = {}


@dataclass
class ContentSuggestion:
    """Content improvement suggestion"""
    category: Optional[str] = None
    suggestion: Optional[str] = None
    priority: Optional[str] = None
    impact: Optional[str] = None


@dataclass
class KeywordRanking:
    """Keyword ranking data"""
    keyword: Optional[str] = None
    rank: Optional[int] = None
    volume: Optional[int] = None
    difficulty: Optional[float] = None
    trend: Optional[str] = None


@dataclass
class BacklinkAnalysis:
    """Backlink analysis"""
    total_backlinks: int = 0
    unique_domains: int = 0
    dofollow: int = 0
    nofollow: int = 0
    top_sources: List[Dict[str, Any]] = None
    anchor_text_distribution: Dict[str, int] = None

    def __post_init__(self):
        if self.top_sources is None:
            self.top_sources = []
        if self.anchor_text_distribution is None:
            self.anchor_text_distribution = {}


class BlogTrekkerClient:
    """
    BlogTrekker API client for blog analysis and SEO optimization.

    Authentication: API Key (Header: X-API-Key)
    Base URL: https://api.blogtrekkor.com/v1
    """

    BASE_URL = "https://api.blogtrekkor.com/v1"

    def __init__(self, api_key: str):
        """
        Initialize BlogTrekker client.

        Args:
            api_key: BlogTrekker API key
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

    # ==================== Blog Post Analysis ====================

    def analyze_blog_post(
        self,
        url: str,
        target_keywords: Optional[List[str]] = None
    ) -> BlogAnalysis:
        """
        Analyze a blog post for SEO and readability.

        Args:
            url: Blog post URL
            target_keywords: List of target keywords to track

        Returns:
            BlogAnalysis object
        """
        if not url:
            raise ValueError("Blog post URL is required")

        payload: Dict[str, Any] = {"url": url}

        if target_keywords:
            payload["keywords"] = target_keywords

        result = self._request("POST", "/analyze", json=payload)
        return self._parse_blog_analysis(result)

    def get_seo_analysis(self, url: str) -> SEOAnalysis:
        """
        Get detailed SEO analysis for a blog post.

        Args:
            url: Blog post URL

        Returns:
            SEOAnalysis object
        """
        if not url:
            raise ValueError("Blog post URL is required")

        result = self._request("POST", "/seo/analyze", json={"url": url})
        return self._parse_seo_analysis(result)

    # ==================== Content Suggestions ====================

    def get_content_suggestions(
        self,
        url: Optional[str] = None,
        content: Optional[str] = None,
        focus: Optional[List[str]] = None
    ) -> List[ContentSuggestion]:
        """
        Get content improvement suggestions.

        Args:
            url: Blog post URL (alternative to content)
            content: Raw blog content (alternative to URL)
            focus: Focus areas (seo, readability, engagement)

        Returns:
            List of ContentSuggestion objects
        """
        payload: Dict[str, Any] = {}

        if url:
            payload["url"] = url
        elif content:
            payload["content"] = content
        else:
            raise ValueError("Either URL or content is required")

        if focus:
            payload["focus"] = focus

        result = self._request("POST", "/suggestions", json=payload)
        return [self._parse_suggestion(s) for s in result.get("suggestions", [])]

    # ==================== Competitor Analysis ====================

    def analyze_competitor_blog(self, url: str, your_blog_url: str) -> Dict[str, Any]:
        """
        Analyze competitor's blog post compared to yours.

        Args:
            url: Competitor's blog post URL
            your_blog_url: Your blog post URL for comparison

        Returns:
            Comparison analysis data
        """
        if not url or not your_blog_url:
            raise ValueError("Both competitor and your blog URLs are required")

        payload = {
            "competitor_url": url,
            "your_url": your_blog_url
        }

        return self._request("POST", "/competitor/analyze", json=payload)

    # ==================== Keyword Tracking ====================

    def track_keyword_rankings(
        self,
        keywords: List[str],
        domain: str
    ) -> List[KeywordRanking]:
        """
        Track keyword rankings for a domain.

        Args:
            keywords: List of keywords to track
            domain: Domain to check rankings for

        Returns:
            List of KeywordRanking objects
        """
        if not keywords:
            raise ValueError("Keywords list is required")
        if not domain:
            raise ValueError("Domain is required")

        payload = {
            "keywords": keywords,
            "domain": domain
        }

        result = self._request("POST", "/keywords/rankings", json=payload)
        return [self._parse_keyword_ranking(k) for k in result.get("rankings", [])]

    # ==================== Backlink Analysis ====================

    def get_backlink_analysis(self, url: str) -> BacklinkAnalysis:
        """
        Get backlink analysis for a URL.

        Args:
            url: URL to analyze backlinks for

        Returns:
            BacklinkAnalysis object
        """
        if not url:
            raise ValueError("URL is required")

        result = self._request("GET", "/backlinks/analyze", params={"url": url})
        return self._parse_backlink_analysis(result)

    # ==================== Helper Methods ====================

    def _parse_blog_analysis(self, data: Dict[str, Any]) -> BlogAnalysis:
        """Parse blog analysis data from API response"""
        return BlogAnalysis(
            url=data.get("url"),
            title=data.get("title"),
            word_count=data.get("word_count"),
            readability_score=data.get("readability_score"),
            seo_score=data.get("seo_score"),
            keywords=data.get("keywords", []),
            suggestions=data.get("suggestions", []),
            analyzed_at=data.get("analyzed_at")
        )

    def _parse_seo_analysis(self, data: Dict[str, Any]) -> SEOAnalysis:
        """Parse SEO analysis data from API response"""
        return SEOAnalysis(
            url=data.get("url"),
            title_optimization=data.get("title_optimization", {}),
            meta_description=data.get("meta_description", {}),
            heading_structure=data.get("heading_structure", {}),
            keyword_density=data.get("keyword_density", {}),
            internal_links=data.get("internal_links", 0),
            external_links=data.get("external_links", 0),
            overall_score=data.get("overall_score")
        )

    def _parse_suggestion(self, data: Dict[str, Any]) -> ContentSuggestion:
        """Parse suggestion data from API response"""
        return ContentSuggestion(
            category=data.get("category"),
            suggestion=data.get("suggestion"),
            priority=data.get("priority"),
            impact=data.get("impact")
        )

    def _parse_keyword_ranking(self, data: Dict[str, Any]) -> KeywordRanking:
        """Parse keyword ranking data from API response"""
        return KeywordRanking(
            keyword=data.get("keyword"),
            rank=data.get("rank"),
            volume=data.get("volume"),
            difficulty=data.get("difficulty"),
            trend=data.get("trend")
        )

    def _parse_backlink_analysis(self, data: Dict[str, Any]) -> BacklinkAnalysis:
        """Parse backlink analysis data from API response"""
        return BacklinkAnalysis(
            total_backlinks=data.get("total_backlinks", 0),
            unique_domains=data.get("unique_domains", 0),
            dofollow=data.get("dofollow", 0),
            nofollow=data.get("nofollow", 0),
            top_sources=data.get("top_sources", []),
            anchor_text_distribution=data.get("anchor_text_distribution", {})
        )

    def close(self):
        """Close the HTTP session"""
        self.session.close()


def main():
    """Example usage"""
    api_key = "your_blogtrekkor_api_key"

    client = BlogTrekkerClient(api_key=api_key)

    try:
        # Analyze blog post
        analysis = client.analyze_blog_post(
            url="https://example.com/blog/post",
            target_keywords=["digital marketing", "SEO"]
        )
        print(f"Analysis: SEO Score: {analysis.seo_score}, Readability: {analysis.readability_score}")

        # Get detailed SEO analysis
        seo = client.get_seo_analysis("https://example.com/blog/post")
        print(f"SEO Score: {seo.overall_score}")
        print(f"Keywords: {seo.keyword_density}")

        # Get content suggestions
        suggestions = client.get_content_suggestions(
            url="https://example.com/blog/post",
            focus=["seo", "readability"]
        )
        print(f"Suggestions: {len(suggestions)} found")
        for s in suggestions[:3]:
            print(f"  - [{s.priority}] {s.category}: {s.suggestion}")

        # Track keyword rankings
        rankings = client.track_keyword_rankings(
            keywords=["digital marketing", "blogging"],
            domain="example.com"
        )
        for r in rankings:
            print(f"Keyword: {r.keyword}, Rank: {r.rank}, Volume: {r.volume}")

        # Backlink analysis
        backlinks = client.get_backlink_analysis("https://example.com/blog/post")
        print(f"Backlinks: {backlinks.total_backlinks} from {backlinks.unique_domains} domains")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        client.close()


if __name__ == "__main__":
    main()