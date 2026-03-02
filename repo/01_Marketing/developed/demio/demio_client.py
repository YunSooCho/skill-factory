"""
Demio API Client
Webinar platform for virtual events
"""

import requests
from typing import Dict, List, Optional, Any
from datetime import datetime
import time


class DemioError(Exception):
    """Demio APIエラー""""
    pass


class RateLimitError(DemioError):
    """Rate limit exceeded"""
    pass


class DemioClient:
    """
    Demio API Client
    Webinar hosting and registration automation
    """

    def __init__(self, api_key: str, api_secret: str, base_url: str = "https://api.demio.com/v1"):
        """
        Demio APIクライアントの初期化

        Args:
            api_key: Demio API key
            api_secret: Demio API secret
            base_url：APIベースURL
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.session = requests.Session()
        self.session.auth = (api_key, api_secret)
        self.session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
        self.last_request_time = 0
        self.min_request_interval = 0.1  # 100ms between requests (10 requests/second)

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
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        APIリクエストの実行

        Args:
            method: HTTP メソッド (GET、POST、PUT、DELETE)
            endpoint: API エンドポイント
            params: クエリパラメータ
            data: 要求本文データ

        Returns:
            APIレスポンス

        Raises:
            DemioError：APIエラーが発生したとき
            RateLimitError: Rate limit 超過時
        """
        self._handle_rate_limit()

        url = f"{self.base_url}{endpoint}"

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=data,
                timeout=30
            )

            # Rate limit 処理
            if response.status_code == 429:
                raise RateLimitError("Rate limit exceeded")

            response.raise_for_status()

            if response.text:
                return response.json()
            return {}

        except requests.exceptions.RequestException as e:
            if e.response:
                if e.response.status_code == 401:
                    raise DemioError("Invalid API credentials")
                elif e.response.status_code == 403:
                    raise DemioError("Access forbidden")
                elif e.response.status_code == 404:
                    raise DemioError("Resource not found")

            raise DemioError(f"API request failed: {str(e)}")

    def list_events(
        self,
        status: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        イベントリストの照会

        Args:
            status: ステータスフィルタ ('scheduled', 'completed', 'active', 'cancelled')
            limit: 返す最大結果数
            offset: ページオフセット

        Returns:
            イベント一覧
            {
                "events": [
                    {
                        "id": int,
                        "name": str,
                        "status": str,
                        "start_date": str,
                        "end_date": str,
                        "timezone": str,
                        "is_recurring": bool,
                        "registrants_count": int,
                        "attendees_count": int
                    },
                    ...
                ],
                "total": int
            }
        """
        params = {}

        if status:
            params['status'] = status

        if limit:
            params['limit'] = limit

        if offset:
            params['offset'] = offset

        return self._make_request('GET', '/events', params=params)

    def get_event(self, event_id: int) -> Dict[str, Any]:
        """
        イベント詳細の照会

        Args:
            event_id：イベントID

        Returns:
            イベント詳細
            {
                "id": int,
                "name": str,
                "description": str,
                "status": str,
                "start_date": str,
                "end_date": str,
                "timezone": str,
                "duration": int,
                "registration_link": str,
                "registrants_count": int,
                "attendees_count": int,
                "is_recurring": bool,
                "presenter": dict,
                "rooms": list
            }
        """
        return self._make_request('GET', f'/events/{event_id}')

    def list_event_participants(
        self,
        event_id: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        イベント参加者リストの照会

        Args:
            event_id：イベントID
            limit: 返す最大結果数
            offset: ページオフセット

        Returns:
            参加者リスト
            {
                "participants": [
                    {
                        "uuid": str,
                        "name": str,
                        "email": str,
                        "first_name": str,
                        "last_name": str,
                        "joined_at": str,
                        "left_at": str,
                        "attendance_duration": int,
                        "is_attended": bool,
                        "join_link": str
                    },
                    ...
                ],
                "total": int
            }
        """
        params = {}

        if limit:
            params['limit'] = limit

        if offset:
            params['offset'] = offset

        return self._make_request('GET', f'/events/{event_id}/participants', params=params)

    def get_event_registrants(
        self,
        event_id: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        イベント登録者リストの照会

        Args:
            event_id：イベントID
            limit: 返す最大結果数
            offset: ページオフセット

        Returns:
            登録者リスト
            {
                "registrants": [
                    {
                        "uuid": str,
                        "name": str,
                        "email": str,
                        "first_name": str,
                        "last_name": str,
                        "registered_at": str,
                        "join_link": str,
                        "attended": bool
                    },
                    ...
                ],
                "total": int
            }
        """
        params = {}

        if limit:
            params['limit'] = limit

        if offset:
            params['offset'] = offset

        return self._make_request('GET', f'/events/{event_id}/registrants', params=params)

    def register_event_participant(
        self,
        event_id: int,
        email: str,
        name: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        イベント参加者登録

        Args:
            event_id：イベントID
            email：参加者のメール
            name：参加者名
            first_name：名前（オプション、nameと優先順位）
            last_name: 姓 (選択)
            custom_fields: カスタムフィールド辞書

        Returns:
            登録結果
            {
                "uuid": str,
                "name": str,
                "email": str,
                "join_link": str,
                "registered_at": str
            }
        """
        data = {
            'email': email,
            'name': name
        }

        if first_name:
            data['firstName'] = first_name

        if last_name:
            data['lastName'] = last_name

        if custom_fields:
            data['customFields'] = custom_fields

        return self._make_request('POST', f'/events/{event_id}/register', data=data)

    def cancel_registration(self, event_id: int, email: str) -> Dict[str, Any]:
        """
        参加者登録解除

        Args:
            event_id：イベントID
            email：参加者のメール

        Returns:
            キャンセル結果
        """
        return self._make_request('POST', f'/events/{event_id}/registrations/cancel', data={'email': email})

    def get_upcoming_events(self, limit: Optional[int] = None) -> Dict[str, Any]:
        """
        今後のイベントリストの検索

        Args:
            limit: 返す最大結果数

        Returns:
            今後のイベント一覧
        """
        return self.list_events(status='scheduled', limit=limit)

    def get_completed_events(self, limit: Optional[int] = None) -> Dict[str, Any]:
        """
        完了したイベントリストの検索

        Args:
            limit: 返す最大結果数

        Returns:
            完了したイベントのリスト
        """
        return self.list_events(status='completed', limit=limit)


if __name__ == "__main__":
    import os

    #テストコード
    api_key = os.environ.get('DEMIO_API_KEY', 'your-api-key')
    api_secret = os.environ.get('DEMIO_API_SECRET', 'your-api-secret')
    client = DemioClient(api_key, api_secret)

    try:
        # イベントリスト検索テスト
        events = client.list_events(status='scheduled', limit=5)
        print("Events:", events)

        #特定のイベント検索テスト
        if events.get('events'):
            event_id = events['events'][0]['id']
            event = client.get_event(event_id)
            print("Event details:", event)

            #参加者リスト検索テスト
            participants = client.list_event_participants(event_id)
            print("Participants:", participants)

            # 登録者リスト検索テスト
            registrants = client.get_event_registrants(event_id)
            print("Registrants:", registrants)

            #新しい参加者登録テスト
            registration_result = client.register_event_participant(
                event_id=event_id,
                email='new@example.com',
                name='New Participant'
            )
            print("Registration result:", registration_result)

    except Exception as e:
        print(f"Error: {str(e)}")