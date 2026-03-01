"""
DataForSEO API Client
SEO data and analytics
"""

import requests
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
import time


class DataForSEOError(Exception):
    """DataForSEO API 에러"""
    pass


class RateLimitError(DataForSEOError):
    """Rate limit exceeded"""
    pass


class DataForSEOClient:
    """
    DataForSEO API Client
    SEO metrics, SERP data, backlinks analysis and more
    """

    def __init__(
        self,
        api_login: str,
        api_password: str,
        base_url: str = "https://api.dataforseo.com/v3"
    ):
        """
        DataForSEO API 클라이언트 초기화

        Args:
            api_login: DataForSEO API login
            api_password: DataForSEO API password
            base_url: API 기본 URL
        """
        self.api_login = api_login
        self.api_password = api_password
        self.base_url = base_url
        self.session = requests.Session()
        self.session.auth = (api_login, api_password)
        self.session.headers.update({
            'Content-Type': 'application/json'
        })
        self.last_request_time = 0
        self.min_request_interval = 0.02  # 50 requests/second

    def _handle_rate_limit(self, response: Optional[requests.Response] = None) -> None:
        """Rate limiting 처리"""
        if response:
            # 응답 헤더에서 rate limit 정보 확인
            limit_remaining = int(response.headers.get('X-RateLimit-Remaining', 10))
            if limit_remaining <= 1:
                time.sleep(0.1)

        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last_request)
        self.last_request_time = time.time()

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        API 요청 실행

        Args:
            method: HTTP 메서드 (GET, POST, DELETE)
            endpoint: API 엔드포인트
            data: 요청 본문 데이터
            params: 쿼리 파라미터

        Returns:
            API 응답

        Raises:
            DataForSEOError: API 에러 발생 시
            RateLimitError: Rate limit 초과 시
        """
        url = f"{self.base_url}{endpoint}"

        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                timeout=60
            )

            self._handle_rate_limit(response)

            if response.status_code == 429:
                raise RateLimitError("Rate limit exceeded")

            response.raise_for_status()

            result = response.json()

            # 에러 처리
            if result.get('status_code') not in [20000, 20100]:
                error_message = result.get('status_message', 'Unknown error')
                raise DataForSEOError(f"API error ({result.get('status_code')}): {error_message}")

            return result

        except requests.exceptions.RequestException as e:
            if e.response:
                if e.response.status_code == 401:
                    raise DataForSEOError("Invalid API credentials")
                elif e.response.status_code == 402:
                    raise DataForSEOError("Account balance insufficient")
                elif e.response.status_code == 404:
                    raise DataForSEOError("Endpoint not found or task not found")

            raise DataForSEOError(f"API request failed: {str(e)}")

    def get_search_volume(
        self,
        keywords: List[str],
        location_code: int = 2840,  # 기본값: Global
        language_code: str = "en"
    ) -> Dict[str, Any]:
        """
        검색량 및 경쟁 데이터 조회

        Args:
            keywords: 키워드 목록 (최대 100개)
            location_code: 위치 코드 (DataForSEO 지역 코드)
            language_code: 언어 코드 (ISO 639-1)

        Returns:
            키워드 데이터
            {
                "status_code": 20000,
                "tasks": [
                    {
                        "id": str,
                        "result": [
                            {
                                "keyword": str,
                                "search_volume": int,
                                "cpc": float,
                                "competition": float,
                                "competition_index": int,
                                "monthly_searches": [
                                    {"month": int, "year": int, "search_volume": int},
                                    ...
                                ]
                            }
                        ]
                    }
                ]
            }
        """
        data = [{
            "keywords": keywords,
            "location_code": location_code,
            "language_code": language_code
        }]

        return self._make_request('POST', '/keywords_data/google_ads/search_volume/live', data=data)

    def get_serp_data(
        self,
        keyword: str,
        location_code: int = 2840,
        language_code: str = "en",
        search_engine: str = "google",
        depth: int = 10
    ) -> Dict[str, Any]:
        """
        SERP (Search Engine Results Page) 데이터 조회

        Args:
            keyword: 검색 키워드
            location_code: 위치 코드
            language_code: 언어 코드
            search_engine: 검색 엔진 (google, bing, etc.)
            depth: 결과 깊이 (기본값: 10)

        Returns:
            SERP 결과
        """
        data = [{
            "keyword": keyword,
            "location_code": location_code,
            "language_code": language_code,
            "depth": depth
        }]

        endpoint = f'/serp/{search_engine}/organic/live'
        return self._make_request('POST', endpoint, data=data)

    def get_domain_rank_overview(
        self,
        target: str,
        language_code: str = "en"
    ) -> Dict[str, Any]:
        """
        도메인 랭크 개요 조회

        Args:
            target: 도메인 또는 URL
            language_code: 언어 코드

        Returns:
            도메인 랭크 데이터
            {
                "status_code": 20000,
                "tasks": [
                    {
                        "result": [
                            {
                                "target": str,
                                "domain_authority": int,
                                "page_authority": int,
                                "rank": int,
                                "links": {
                                    "total": int,
                                    "external": int,
                                    "followed": int
                                },
                                "traffic": int
                            }
                        ]
                    }
                ]
            }
        """
        data = [{
            "target": target,
            "language_code": language_code
        }]

        return self._make_request('POST', '/domain_analytics/domain_intersections/live', data=data)

    def get_backlink_data(
        self,
        target: str,
        limit: int = 100,
        filters: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        백링크 데이터 조회

        Args:
            target: 도메인 또는 URL
            limit: 반환할 최대 결과 수 (최대 1000)
            filters: 필터 조건
                [
                    ["dofollow", "=", true],
                    ["type", "in", ["link", "redirect"]]
                ]

        Returns:
            백링크 데이터
            {
                "status_code": 20000,
                "tasks": [
                    {
                        "result": [
                            {
                                "target": str,
                                "backlinks": [
                                    {
                                        "url_from": str,
                                        "url_to": str,
                                        "domain_from": str,
                                        "domain_to": str,
                                        "page_authority": int,
                                        "domain_authority": int,
                                        "type": str,
                                        "dofollow": bool,
                                        "anchor": str
                                    },
                                    ...
                                ],
                                "total_count": int
                            }
                        ]
                    }
                ]
            }
        """
        data = [{
            "target": target,
            "limit": limit
        }]

        if filters:
            data[0]["filters"] = filters

        return self._make_request('POST', '/backlinks/live', data=data)

    def get_backlink_summary(
        self,
        target: str
    ) -> Dict[str, Any]:
        """
        백링크 요약 조회

        Args:
            target: 도메인 또는 URL

        Returns:
            백링크 요약 데이터
            {
                "status_code": 20000,
                "tasks": [
                    {
                        "result": [
                            {
                                "target": str,
                                "total": int,
                                "pages": int,
                                "domains": int,
                                "dofollow": int,
                                "nofollow": int,
                                "text": int,
                                "image": int,
                                "distribution": {
                                    "edu": int,
                                    "gov": int,
                                    "com": int,
                                    ...
                                }
                            }
                        ]
                    }
                ]
            }
        """
        data = [{
            "target": target
        }]

        return self._make_request('POST', '/backlinks/summary/live', data=data)

    def search_business_listings(
        self,
        query: str,
        location_name: Optional[str] = None,
        location_code: Optional[int] = None,
        depth: int = 20
    ) -> Dict[str, Any]:
        """
        비즈니스 목록 검색 (Google Maps, Yandex Maps, etc.)

        Args:
            query: 검색 쿼리 (예: "restaurants", "plumber")
            location_name: 위치 이름 (예: "New York", "Tokyo")
            location_code: 위치 코드 (DataForSEO 코드)
            depth: 결과 깊이

        Returns:
            비즈니스 목록 데이터
            {
                "status_code": 20000,
                "tasks": [
                    {
                        "result": [
                            {
                                "items": [
                                    {
                                        "title": str,
                                        "type": str,
                                        "address": str,
                                        "phone": str,
                                        "rating": float,
                                        "reviews_count": int,
                                        "website": str,
                                        "latitude": float,
                                        "longitude": float,
                                        "photos": list,
                                        "hours": dict
                                    },
                                    ...
                                ]
                            }
                        ]
                    }
                ]
            }
        """
        data = [{
            "keyword": query,
            "depth": depth
        }]

        if location_name:
            data[0]["location_name"] = location_name

        if location_code:
            data[0]["location_code"] = location_code

        return self._make_request('POST', '/serp/google_maps/local_pack/live', data=data)

    def get_task_result(self, task_id: str) -> Dict[str, Any]:
        """
        비동기 작업 결과 조회

        Args:
            task_id: 작업 ID

        Returns:
            작업 결과
        """
        return self._make_request('GET', f'/serp/task_get/{task_id}')


def create_dataforseo_client(api_login: str, api_password: str) -> DataForSEOClient:
    """
    DataForSEO 클라이언트 생성 (Factory function)

    Args:
        api_login: DataForSEO API login
        api_password: DataForSEO API password

    Returns:
        DataForSEOClient 인스턴스
    """
    return DataForSEOClient(api_login, api_password)


if __name__ == "__main__":
    import os

    # 테스트 코드
    api_login = os.environ.get('DATAFORSEO_API_LOGIN', 'your-api-login')
    api_password = os.environ.get('DATAFORSEO_API_PASSWORD', 'your-api-password')
    client = create_dataforseo_client(api_login, api_password)

    try:
        # 검색량 조회 테스트
        volume_result = client.get_search_volume(['python programming', 'machine learning'])
        print("Search volume:", volume_result)

        # SERP 데이터 조회 테스트
        serp_result = client.get_serp_data('python tutorial')
        print("SERP data:", serp_result)

        # 도메인 랭크 조회 테스트
        rank_result = client.get_domain_rank_overview('example.com')
        print("Domain rank:", rank_result)

        # 백링크 데이터 조회 테스트
        backlink_result = client.get_backlink_data('example.com', limit=10)
        print("Backlink data:", backlink_result)

        # 백링크 요약 조회 테스트
        summary_result = client.get_backlink_summary('example.com')
        print("Backlink summary:", summary_result)

        # 비즈니스 목록 검색 테스트
        business_result = client.search_business_listings(
            query='restaurants',
            location_name='New York',
            depth=10
        )
        print("Business listings:", business_result)

    except Exception as e:
        print(f"Error: {str(e)}")