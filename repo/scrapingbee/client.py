"""
ScrapingBee API Client - Web Scraping with Headless Browser
"""

import requests
from typing import Optional, Dict, Any
from urllib.parse import quote


class ScrapingBeeError(Exception):
    """Base exception for ScrapingBee errors"""
    pass


class ScrapingBeeClient:
    """Client for ScrapingBee Web Scraping API"""

    BASE_URL = "https://app.scrapingbee.com/api/v1/scrape"

    def __init__(self, api_key: str):
        """
        Initialize ScrapingBee client

        Args:
            api_key: ScrapingBee API key
        """
        self.api_key = api_key
        self.timeout = 30

    def scrape(self, url: str, 
               render_js: bool = False,
               extract_rules: Optional[Dict] = None,
               screenshot: bool = False,
               premium_proxy: bool = False,
               country_code: Optional[str] = None,
               wait: Optional[int] = None,
               **kwargs) -> Dict[str, Any]:
        """
        Scrape a web page

        Args:
            url: URL to scrape
            render_js: Whether to execute JavaScript
            extract_rules: CSS selector rules to extract data
            screenshot: Take a screenshot of the page
            premium_proxy: Use premium proxy
            country_code: Country code for proxy
            wait: Wait time before scraping (ms)
            **kwargs: Additional parameters

        Returns:
            Scraped data

        Raises:
            ScrapingBeeError: If scraping fails
        """
        params = {
            "api_key": self.api_key,
            "url": url,
            "render_js": str(render_js).lower()
        }

        if extract_rules:
            import json
            params["extract_rules"] = json.dumps(extract_rules)

        if screenshot:
            params["screenshot"] = "true"

        if premium_proxy:
            params["premium_proxy"] = "true"

        if country_code:
            params["country_code"] = country_code

        if wait:
            params["wait"] = wait

        params.update(kwargs)

        try:
            response = requests.get(
                self.BASE_URL,
                params=params,
                timeout=self.timeout
            )

            if response.status_code == 429:
                raise ScrapingBeeError("Rate limit exceeded. Please try again later.")

            response.raise_for_status()

            # Parse JSON if response is JSON, otherwise return text content
            try:
                return response.json()
            except:
                return {"raw_content": response.text}

        except requests.exceptions.RequestException as e:
            error_msg = f"Scraping failed: {str(e)}"
            raise ScrapingBeeError(error_msg) from e

    def scrape_html(self, url: str, **kwargs) -> str:
        """
        Scrape and return HTML content as string

        Args:
            url: URL to scrape
            **kwargs: Additional scraping parameters

        Returns:
            HTML content as string

        Raises:
            ScrapingBeeError: If scraping fails
        """
        result = self.scrape(url, **kwargs)
        return result.get("raw_content") if isinstance(result, dict) else result

    def scrape_text(self, url: str, extract_rules: Optional[Dict] = None, **kwargs) -> Dict[str, Any]:
        """
        Scrape and extract text content using CSS selectors

        Args:
            url: URL to scrape
            extract_rules: CSS selector rules
            **kwargs: Additional scraping parameters

        Returns:
            Extracted data

        Raises:
            ScrapingBeeError: If scraping fails
        """
        if extract_rules:
            result = self.scrape(url, extract_rules=extract_rules, **kwargs)
            return result.get("data", {})
        else:
            # If no extract rules, scrape with render_js and return content
            return {"content": self.scrape_html(url, **kwargs)}