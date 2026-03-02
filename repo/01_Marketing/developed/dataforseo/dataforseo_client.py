"""
DataForSEO API Client
SEO data and analytics
"""

import requests
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
import time


class DataForSEOError(Exception):
    """DataForSEO APIエラー"""
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
        DataForSEO APIクライアントの初期化

        Args:
            api_login: DataForSEO API login
            api_password: DataForSEO API password
            base_url：APIベースURL
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
        """Rate limiting 処理""""
        if response:
            ＃応答ヘッダーのレート制限情報を確認する
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
        APIリクエストの実行

        Args:
            method: HTTP メソッド (GET, POST, DELETE)
            endpoint: API エンドポイント
            data: 要求本文データ
            params: クエリパラメータ

        Returns:
            APIレスポンス

        Raises:
            DataForSEOError：APIエラーが発生したとき
            RateLimitError: Rate limit 超過時
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

            # エラー処理
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
        location_code: int = 2840, # デフォルト: Global
        language_code: str = "en"
    ) -> Dict[str, Any]:
        """
        検索量と競争データの照会

        Args:
            キーワード：キーワードリスト（最大100個）
            location_code：位置コード（DataForSEO地域コード）
            language_code：言語コード（ISO 639-1）

        Returns:
            キーワードデータ
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
        SERP (Search Engine Results Page) データの照会

        Args:
            keyword：検索キーワード
            location_code：位置コード
            language_code: 言語コード
            search_engine: 検索エンジン (google, bing, etc.)
            depth：結果の深さ（デフォルト：10）

        Returns:
            SERP結果
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
        ドメインランクの概要を表示

        Args:
            target: ドメインまたは URL
            language_code: 言語コード

        Returns:
            ドメインランクデータ
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
        バックリンクデータの照会

        Args:
            target: ドメインまたは URL
            limit：返す最大結果数（最大1000）
            filters: フィルタ条件
                [
                    ["dofollow", "=", true],
                    ["type", "in", ["link", "redirect"]]
                ]

        Returns:
            バックリンクデータ
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
        バックリンクサマリービュー

        Args:
            target: ドメインまたは URL

        Returns:
            バックリンクサマリーデータ
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
        ビジネスリストの検索（Google Maps、Yandex Maps、etc.）

        Args:
            query: 検索クエリ (例: "restaurants", "plumber")
            location_name：場所名（例：「ニューヨーク」、「東京」）
            location_code：位置コード（DataForSEOコード）
            depth: 結果の深さ

        Returns:
            ビジネスリストデータ
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
        非同期操作結果の照会

        Args:
            task_id：ジョブID

        Returns:
            作業結果
        """
        return self._make_request('GET', f'/serp/task_get/{task_id}')


def create_dataforseo_client(api_login: str, api_password: str) -> DataForSEOClient:
    """
    DataForSEO クライアントの作成 (Factory function)

    Args:
        api_login: DataForSEO API login
        api_password: DataForSEO API password

    Returns:
        DataForSEOClient インスタンス
    """
    return DataForSEOClient(api_login, api_password)


if __name__ == "__main__":
    import os

    #テストコード
    api_login = os.environ.get('DATAFORSEO_API_LOGIN', 'your-api-login')
    api_password = os.environ.get('DATAFORSEO_API_PASSWORD', 'your-api-password')
    client = create_dataforseo_client(api_login, api_password)

    try:
        # 検索ボリューム照会テスト
        volume_result = client.get_search_volume(['python programming', 'machine learning'])
        print("Search volume:", volume_result)

        #SERPデータ検索テスト
        serp_result = client.get_serp_data('python tutorial')
        print("SERP data:", serp_result)

        #ドメインランクルックアップテスト
        rank_result = client.get_domain_rank_overview('example.com')
        print("Domain rank:", rank_result)

        ＃バックリンクデータ検索テスト
        backlink_result = client.get_backlink_data('example.com', limit=10)
        print("Backlink data:", backlink_result)

        ＃バックリンクサマリールックアップテスト
        summary_result = client.get_backlink_summary('example.com')
        print("Backlink summary:", summary_result)

        # ビジネスリスト検索テスト
        business_result = client.search_business_listings(
            query='restaurants',
            location_name='New York',
            depth=10
        )
        print("Business listings:", business_result)

    except Exception as e:
        print(f"Error: {str(e)}")