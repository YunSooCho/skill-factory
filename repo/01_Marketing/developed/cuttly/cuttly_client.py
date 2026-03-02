"""
Cuttly API Client
API Documentation: https://cutt.ly/api
"""

import requests
import base64
from typing import Dict, List, Optional, Any
from datetime import datetime
import time


class CuttlyError(Exception):
    """Cuttly API エラー""""
    pass


class RateLimitError(CuttlyError):
    """Rate limit exceeded"""
    pass


class CuttlyClient:
    """
    Cuttly API Client
    URL Shortener and Analytics API
    """

    def __init__(self, api_key: str, base_url: str = "https://cutt.ly/api/api.php"):
        """
        Cuttly APIクライアントの初期化

        Args:
            api_key: Cuttly API key
            base_url：APIベースURL
        """
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.last_request_time = 0
        self.min_request_interval = 0.1  # 100ms between requests (10 requests/second)

    def _handle_rate_limit(self) -> None:
        """Rate limiting 処理""""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last_request)
        self.last_request_time = time.time()

    def _make_request(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        APIリクエストの実行

        Args:
            params: リクエストパラメータ

        Returns:
            APIレスポンス

        Raises:
            CuttlyError：APIエラーが発生したとき
            RateLimitError: Rate limit 超過時
        """
        self._handle_rate_limit()

        params['key'] = self.api_key

        try:
            response = self.session.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            # エラー処理
            if data.get('url', {}).get('status') == '4':
                raise RateLimitError(f"Rate limit exceeded: {data.get('url', {}).get('title')}")
            elif data.get('url', {}).get('status') == '2':
                raise CuttlyError(f"Invalid URL: {data.get('url', {}).get('title')}")
            elif data.get('url', {}).get('status') == '3':
                raise CuttlyError(f"Invalid API key: {data.get('url', {}).get('title')}")
            elif data.get('url', {}).get('status') == '5':
                raise CuttlyError(f"Short URL already exists: {data.get('url', {}).get('title')}")

            return data

        except requests.exceptions.RequestException as e:
            raise CuttlyError(f"API request failed: {str(e)}")

    def shorten_url(
        self,
        url: str,
        name: Optional[str] = None,
        tags: Optional[List[str]] = None,
        public: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        URLの短縮

        Args:
            url：短縮する元のURL
            name：カスタムショートカットURL名（オプション）
            タグ：タグリスト（オプション）
            public：公開するかどうか（選択）

        Returns:
            短縮URL情報
            {
                "url": {
                    "status": int,
                    "shortLink": str,
                    "title": str,
                    ...
                }
            }
        """
        params = {'short': url}

        if name:
            params['name'] = name

        if tags:
            params['tags'] = ','.join(tags)

        if public is not None:
            params['public'] = '1' if public else '0'

        return self._make_request(params)

    def get_analytics(
        self,
        url: str,
        limit: Optional[int] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        短縮URL分析データの照会

        Args:
            url：分析する短縮URL
            limit：返す最大結果数（選択）
            date_from：開始日（YYYY-MM-DD、選択）
            date_to：終了日（YYYY-MM-DD、選択）

        Returns:
            分析データ
            {
                "url": {
                    "status": int,
                    "fullLink": str,
                    "title": str,
                    "clicks": int,
                    "date": str,
                    ...
                }
            }
        """
        params = {'stats': url}

        if limit:
            params['limit'] = str(limit)

        if date_from:
            params['dateFrom'] = date_from

        if date_to:
            params['dateTo'] = date_to

        return self._make_request(params)


class CuttlyClientV2:
    """
    Cuttly API V2 Client (Advanced features)
    This provides more advanced analytics and management features.
    """

    def __init__(self, api_key: str, base_url: str = "https://api.cutt.ly"):
        """
        Cuttly V2 APIクライアントの初期化

        Args:
            api_key: Cuttly API key
            base_url：APIベースURL
        """
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        self.last_request_time = 0
        self.min_request_interval = 0.1

    def _handle_rate_limit(self) -> None:
        """Rate limiting 処理""""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last_request)
        self.last_request_time = time.time()

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        APIリクエストの実行

        Args:
            method: HTTP メソッド (GET、POST、PUT、DELETE)
            endpoint: API エンドポイント
            data: 要求本文データ
            params: クエリパラメータ

        Returns:
            APIレスポンス
        """
        self._handle_rate_limit()

        url = f"{self.base_url}{endpoint}"

        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=self.headers,
                json=data,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            if e.response and e.response.status_code == 429:
                raise RateLimitError("Rate limit exceeded")
            raise CuttlyError(f"API request failed: {str(e)}")


# Factory function for easy instantiation
def create_cuttly_client(api_key: str, use_v2: bool = False) -> Any:
    """
    Cuttly クライアントの作成

    Args:
        api_key: Cuttly API key
        use_v2: V2 API を使用するかどうか

    Returns:
        CuttlyClient または CuttlyClientV2 インスタンス
    """
    if use_v2:
        return CuttlyClientV2(api_key)
    return CuttlyClient(api_key)


if __name__ == "__main__":
    #テストコード
    import os

    api_key = os.environ.get('CUTTLY_API_KEY', 'your-api-key')
    client = create_cuttly_client(api_key)

    try:
        # URL短縮テスト
        result = client.shorten_url('https://example.com', name='test-link')
        print("Shortened URL:", result)

        ＃分析データ検索テスト
        short_link = result.get('url', {}).get('shortLink')
        if short_link:
            analytics = client.get_analytics(short_link)
            print("Analytics:", analytics)

    except Exception as e:
        print(f"Error: {str(e)}")