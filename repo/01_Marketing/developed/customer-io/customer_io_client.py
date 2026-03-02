"""
Customer.io API Client
Customer engagement and automation platform
"""

import requests
from typing import Dict, List, Optional, Any
from datetime import datetime
import time


class CustomerIOError(Exception):
    """Customer.io APIエラー"""
    pass


class RateLimitError(CustomerIOError):
    """Rate limit exceeded"""
    pass


class CustomerIOClient:
    """
    Customer.io API Client
    Customer data, segmentation, and event tracking
    """

    def __init__(
        self,
        site_id: str,
        api_key: str,
        region: str = "us",  # 'us' or 'eu'
        base_url: Optional[str] = None
    ):
        """
        Customer.io API クライアントの初期化

        Args:
            site_id: Customer.io Site ID
            api_key: Customer.io API key
            region: リージョン ('us' or 'eu')
            base_url：APIベースURL（Noneの場合は自動設定）
        """
        self.site_id = site_id
        self.api_key = api_key
        self.region = region

        if base_url:
            self.base_url = base_url
        else:
            if region == "eu":
                self.base_url = "https://api-eu.customer.io/v1"
            else:
                self.base_url = "https://api.customer.io/v1"

        self.session = requests.Session()
        self.session.auth = (site_id, api_key)
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        self.last_request_time = 0
        self.min_request_interval = 0.05  # 60ms between requests

        # Track API URL
        if region == "eu":
            self.track_url = "https://track-eu.customer.io/v1"
        else:
            self.track_url = "https://track.customer.io/v1"

        self.track_session = requests.Session()
        self.track_session.auth = (site_id, api_key)
        self.track_session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })

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
        use_track_api: bool = False,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        APIリクエストの実行

        Args:
            method: HTTP メソッド (GET、POST、PUT、DELETE)
            endpoint: API エンドポイント
            use_track_api: Track API を使用するかどうか
            params: クエリパラメータ
            data: 要求本文データ

        Returns:
            APIレスポンス

        Raises:
            CustomerIOError：APIエラーが発生したとき
            RateLimitError: Rate limit 超過時
        """
        self._handle_rate_limit()

        if use_track_api:
            url = f"{self.track_url}{endpoint}"
            session = self.track_session
        else:
            url = f"{self.base_url}{endpoint}"
            session = self.session

        try:
            response = session.request(
                method=method,
                url=url,
                params=params,
                json=data,
                timeout=30
            )

            # Rate limit 処理
            if response.status_code == 429:
                retry_after = response.headers.get('Retry-After', 10)
                raise RateLimitError(f"Rate limit exceeded. Retry after {retry_after} seconds")

            response.raise_for_status()

            if response.text:
                return response.json()
            return {}

        except requests.exceptions.RequestException as e:
            if e.response:
                if e.response.status_code == 401:
                    raise CustomerIOError("Invalid API credentials")
                elif e.response.status_code == 404:
                    raise CustomerIOError("Resource not found")
                elif e.response.status_code == 422:
                    error_data = e.response.json() if e.response.text else {}
                    raise CustomerIOError(f"Validation error: {error_data}")

            raise CustomerIOError(f"API request failed: {str(e)}")

    def create_customer(
        self,
        id: str,
        email: Optional[str] = None,
        name: Optional[str] = None,
        attributes: Optional[Dict[str, Any]] = None,
        created_at: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        顧客作成

        Args:
            id：顧客ID（必須、変更不可）
            email: メールアドレス
            name: 名前
            attributes: 追加属性辞書
            created_at: 作成日 (Unix timestamp)

        Returns:
            生成された顧客情報
        """
        data = {'id': id}

        if email:
            data['email'] = email

        if name:
            data['name'] = name

        if attributes:
            data.update(attributes)

        if created_at:
            data['created_at'] = created_at

        return self._make_request('PUT', f'/customers/{id}', data=data)

    def update_customer(
        self,
        id: str,
        email: Optional[str] = None,
        name: Optional[str] = None,
        attributes: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        顧客情報の更新

        Args:
            id：顧客ID
            email: 新しいメール
            name: 新しい名前
            attributes: 更新する属性

        Returns:
            更新された顧客情報
        """
        data = {}

        if email:
            data['email'] = email

        if name:
            data['name'] = name

        if attributes:
            data.update(attributes)

        return self._make_request('PUT', f'/customers/{id}', data=data)

    def delete_customer(self, id: str) -> Dict[str, Any]:
        """
        顧客を削除

        Args:
            id：顧客ID

        Returns:
            削除結果
        """
        return self._make_request('DELETE', f'/customers/{id}')

    def get_customer(self, id: str) -> Dict[str, Any]:
        """
        顧客情報の照会

        Args:
            id：顧客ID

        Returns:
            顧客の詳細
        """
        return self._make_request('GET', f'/customers/{id}')

    def add_customer_to_segment(
        self,
        customer_id: str,
        segment_id: int
    ) -> Dict[str, Any]:
        """
        手動セグメントに顧客を追加する

        Args:
            customer_id：顧客ID
            segment_id：セグメントID

        Returns:
            結果
        """
        return self._make_request(
            'POST',
            f'/customers/{customer_id}/segments/{segment_id}'
        )

    def remove_customer_from_segment(
        self,
        customer_id: str,
        segment_id: int
    ) -> Dict[str, Any]:
        """
        手動セグメントから顧客を削除する

        Args:
            customer_id：顧客ID
            segment_id：セグメントID

        Returns:
            結果
        """
        return self._make_request(
            'DELETE',
            f'/customers/{customer_id}/segments/{segment_id}'
        )

    def track_customer_event(
        self,
        customer_id: str,
        name: str,
        data: Optional[Dict[str, Any]] = None,
        timestamp: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        顧客イベントの追跡

        Args:
            customer_id：顧客ID
            name: イベント名
            data: イベントデータ
            timestamp: イベントタイムスタンプ (Unix timestamp)

        Returns:
            追跡結果
        """
        event_data = {
            'name': name
        }

        if data:
            event_data['data'] = data

        if timestamp:
            event_data['timestamp'] = timestamp

        return self._make_request(
            'POST',
            f'/customers/{customer_id}/events',
            data=event_data,
            use_track_api=True
        )

    def track_anonymous_event(
        self,
        name: str,
        data: Optional[Dict[str, Any]] = None,
        timestamp: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        匿名イベントの追跡（名前のないユーザーイベント）

        Args:
            name: イベント名
            data: イベントデータ
            timestamp: イベントタイムスタンプ (Unix timestamp)

        Returns:
            追跡結果
        """
        event_data = {
            'name': name
        }

        if data:
            event_data['data'] = data

        if timestamp:
            event_data['timestamp'] = timestamp

        return self._make_request(
            'POST',
            '/events',
            data=event_data,
            use_track_api=True
        )

    def submit_form(
        self,
        form_id: int,
        customer_id: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        フォーム提出

        Args:
            form_id：フォームID
            customer_id：顧客ID
            data: フォームデータ

        Returns:
            提出結果
        """
        form_data = {
            'data': data
        }

        return self._make_request(
            'POST',
            f'/forms/{form_id}/submitions',
            data=form_data
        )

    def list_customers(
        self,
        limit: Optional[int] = None,
        start: Optional[str] = None,
        email: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        顧客リストの照会

        Args:
            limit: 返す最大結果数
            start：ページング開始点（顧客ID）
            email：電子メールでフィルタリング

        Returns:
            顧客リスト
        """
        params = {}

        if limit:
            params['limit'] = limit

        if start:
            params['start'] = start

        if email:
            params['email'] = email

        return self._make_request('GET', '/customers', params=params)

    def get_customer_activities(
        self,
        customer_id: str,
        limit: Optional[int] = None,
        start: Optional[str] = None,
        type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        顧客活動履歴の照会

        Args:
            customer_id：顧客ID
            limit: 返す最大結果数
            start: ページング開始点
            type: アクティビティタイプフィルタ
                ('email_actioned', 'email_opened', 'email_clicked', etc.)

        Returns:
            活動一覧
        """
        params = {}

        if limit:
            params['limit'] = limit

        if start:
            params['start'] = start

        if type:
            params['type'] = type

        return self._make_request('GET', f'/customers/{customer_id}/activities', params=params)


def create_customerio_client(
    site_id: str,
    api_key: str,
    region: str = "us"
) -> CustomerIOClient:
    """
    Customer.io クライアントの作成 (Factory function)

    Args:
        site_id: Customer.io Site ID
        api_key: Customer.io API key
        region: リージョン ('us' or 'eu')

    Returns:
        CustomerIOClient インスタンス
    """
    return CustomerIOClient(site_id, api_key, region)


if __name__ == "__main__":
    import os

    #テストコード
    site_id = os.environ.get('CUSTOMERIO_SITE_ID', 'your-site-id')
    api_key = os.environ.get('CUSTOMERIO_API_KEY', 'your-api-key')
    client = create_customerio_client(site_id, api_key)

    try:
        # 顧客生成テスト
        result = client.create_customer(
            id='customer_123',
            email='test@example.com',
            name='Test User',
            attributes={'plan': 'premium', 'signup_date': '2026-02-28'}
        )
        print("Created customer:", result)

        #カスタマーアップデートテスト
        update_result = client.update_customer(
            id='customer_123',
            attributes={'last_login': '2026-02-28'}
        )
        print("Updated customer:", update_result)

        # イベント追跡テスト
        event_result = client.track_customer_event(
            customer_id='customer_123',
            name='purchase_completed',
            data={'amount': 99.99, 'product': 'Premium Plan'}
        )
        print("Tracked event:", event_result)

        #匿名イベント追跡テスト
        anon_result = client.track_anonymous_event(
            name='page_viewed',
            data={'page': '/pricing', 'referrer': 'google.com'}
        )
        print("Tracked anonymous event:", anon_result)

        #セグメント追加テスト
        segment_result = client.add_customer_to_segment(
            customer_id='customer_123',
            segment_id=1
        )
        print("Added to segment:", segment_result)

        #セグメント削除テスト
        remove_result = client.remove_customer_from_segment(
            customer_id='customer_123',
            segment_id=1
        )
        print("Removed from segment:", remove_result)

        # 顧客削除テスト
        delete_result = client.delete_customer(id='customer_123')
        print("Deleted customer:", delete_result)

    except Exception as e:
        print(f"Error: {str(e)}")