"""
Delighted API Client
Customer feedback and NPS surveys
"""

import requests
from typing import Dict, List, Optional, Any
from datetime import datetime
from flask import Flask, request, jsonify
import time
import threading


class DelightedError(Exception):
    """Delighted APIエラー"""
    pass


class RateLimitError(DelightedError):
    """Rate limit exceeded"""
    pass


class DelightedClient:
    """
    Delighted API Client
    Customer satisfaction surveys and feedback collection
    """

    def __init__(self, api_key: str, base_url: str = "https://api.delighted.com/v1"):
        """
        Delighted API クライアントの初期化

        Args:
            api_key: Delighted API key
            base_url：APIベースURL
        """
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.auth = (api_key, '')
        self.session.headers.update({
            'Accept': 'application/json'
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
            DelightedError：APIエラーが発生したとき
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
                retry_after = int(response.headers.get('Retry-After', 1))
                raise RateLimitError(f"Rate limit exceeded. Retry after {retry_after} seconds")

            response.raise_for_status()

            if response.text:
                return response.json()
            return {}

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise DelightedError("Invalid API key")
            elif e.response.status_code == 403:
                raise DelightedError("API feature not available on current plan")
            elif e.response.status_code == 422:
                error_data = e.response.json()
                raise DelightedError(f"Validation error: {error_data}")
            raise DelightedError(f"API request failed: {str(e)}")

        except requests.exceptions.RequestException as e:
            raise DelightedError(f"API request failed: {str(e)}")

    def get_metrics(
        self,
        since: Optional[str] = None,
        until: Optional[str] = None,
        trend: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        NPSメトリック照会

        Args:
            since: 開始日 (YYYY-MM-DD)
            until：終了日（YYYY-MM-DD）
            trend：トレンド期間（30d、90d、etc.）

        Returns:
            メトリックデータ
            {
                "nps": float,
                "promoters": int,
                "passives": int,
                "detractors": int,
                "promoters_percentage": float,
                "passives_percentage": float,
                "detractors_percentage": float,
                "average_score": float,
                "total_responses": int
            }
        """
        params = {}
        if since:
            params['since'] = since
        if until:
            params['until'] = until
        if trend:
            params['trend'] = trend

        return self._make_request('GET', '/metrics', params=params)

    def create_person(self, person: Dict[str, Any]) -> Dict[str, Any]:
        """
        人の作成

        Args:
            person: 人情報
                {
                    "email": str,
                    "name": str,
                    "properties": dict,
                    "locale": str,  # en, es, fr, de, pt, it, nl, cs, da, pt-BR
                    "send": bool # アンケートをすぐに送信するかどうか
                }

        Returns:
            作成された人情報
        """
        return self._make_request('POST', '/people', data=person)

    def update_person(
        self,
        person_id: str,
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        人情報更新

        Args:
            person_id：人ID
            updates: 更新する情報
                {
                    "email": str,
                    "name": str,
                    "properties": dict,
                    "properties_to_delete": list
                }

        Returns:
            更新された人情報
        """
        return self._make_request('PUT', f'/people/{person_id}', data=updates)

    def create_or_update_person(self, person: Dict[str, Any]) -> Dict[str, Any]:
        """
        人の作成または更新（電子メールに基づいて）

        Args:
            person: 人情報

        Returns:
            人情報
        """
        return self._make_request('PUT', '/people', data=person)

    def search_people(
        self,
        email: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        人検索

        Args:
            email：Eメールアドレスで検索
            limit: 返す最大結果数
            page: ページ番号

        Returns:
            人リスト
        """
        params = {}
        if email:
            params['email'] = email
        if limit:
            params['per_page'] = limit
        if page:
            params['page'] = page

        return self._make_request('GET', '/people', params=params)

    def unsubscribe_people(
        self,
        email: Optional[str] = None,
        person_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        人の購読をキャンセル（アンケートから除く）

        Args:
            email: メールアドレス
            person_id：人ID（2つのうちの1つが必要です）

        Returns:
            結果
        """
        data = {}
        if email:
            data['email'] = email
        if person_id:
            data['person_id'] = person_id

        if not data:
            raise DelightedError("Either email or person_id must be provided")

        return self._make_request('POST', '/unsubscribes', data=data)

    def search_survey_responses(
        self,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
        since: Optional[str] = None,
        until: Optional[str] = None,
        trend: Optional[str] = None,
        min_score: Optional[int] = None,
        max_score: Optional[int] = None,
        person_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        アンケート調査回答の検索

        Args:
            per_page：ページあたりの結果数
            page: ページ番号
            since: 開始日 (YYYY-MM-DD)
            until：終了日（YYYY-MM-DD）
            trend：トレンド期間
            min_score：最小スコア（0-10）
            max_score：最大スコア（0-10）
            person_id：特定の人の回答を検索する

        Returns:
            レスポンスリスト
        """
        params = {}
        if per_page:
            params['per_page'] = per_page
        if page:
            params['page'] = page
        if since:
            params['since'] = since
        if until:
            params['until'] = until
        if trend:
            params['trend'] = trend
        if min_score is not None:
            params['min_score'] = min_score
        if max_score is not None:
            params['max_score'] = max_score
        if person_id:
            params['person_id'] = person_id

        return self._make_request('GET', '/responses', params=params)

    def add_survey_response(
        self,
        person_email: str,
        score: int,
        comment: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        アンケート調査の回答を追加（ソースから）
        注意: これは主に他のソースからの回答を追加する場合に使用

        Args:
            person_email：人のEメール
            スコア：スコア（0-10）
            comment: コメント
            properties: 追加プロパティ

        Returns:
            追加された応答情報
        """
        data = {
            'person_email': person_email,
            'score': score
        }

        if comment:
            data['comment'] = comment

        if properties:
            data.update(properties)

        return self._make_request('POST', '/responses', data=data)

    def delete_person(self, person_id: str) -> Dict[str, Any]:
        """
        人を削除

        Args:
            person_id：人ID

        Returns:
            削除結果
        """
        return self._make_request('DELETE', f'/people/{person_id}')


class DelightedWebhookHandler:
    """
    Delighted Webハンドラ
    FlaskサーバーによるWebフックの受信と処理
    """

    def __init__(self, port: int = 5000, webhook_path: str = '/webhook'):
        """
        Webフックハンドラの初期化

        Args:
            port：サーバーポート
            webhook_path：Webフックパス
        """
        self.app = Flask(__name__)
        self.port = port
        self.webhook_path = webhook_path
        self.response_handlers = {
            'response.created': [],
            'comment.created': [],
            'person.unsubscribed': []
        }
        self._setup_routes()

    def _setup_routes(self):
        """Flask ルート設定"""
        @self.app.route(self.webhook_path, methods=['POST'])
        def handle_webhook():
            event = request.get_json()

            if not event:
                return jsonify({'error': 'Invalid payload'}), 400

            event_type = event.get('event')
            event_data = event.get('data', {})

            ＃イベントタイプ別ハンドラの実行
            handlers = self.response_handlers.get(event_type, [])
            if handlers:
                for handler in handlers:
                    try:
                        handler(event_data)
                    except Exception as e:
                        print(f"Error in webhook handler: {e}")

            return jsonify({'status': 'received'}), 200

        @self.app.route('/health', methods=['GET'])
        def health_check():
            return jsonify({'status': 'healthy'}), 200

    def on_new_response(self, handler: callable):
        """
        新しい応答イベントハンドラの登録
        """
        self.response_handlers['response.created'].append(handler)

    def on_new_unsubscribe(self, handler: callable):
        """
        サブスクリプションキャンセルイベントハンドラの登録
        """
        self.response_handlers['person.unsubscribed'].append(handler)

    def on_new_comment(self, handler: callable):
        """
        新しいコメントイベントハンドラの登録
        """
        self.response_handlers['comment.created'].append(handler)

    def run(self, host: str = '0.0.0.0', debug: bool = False):
        """
        Webフックサーバーの起動

        Args:
            host：ホストアドレス
            debug: デバッグモード
        """
        def run_server():
            self.app.run(host=host, port=self.port, debug=debug, threaded=True)

        thread = threading.Thread(target=run_server, daemon=True)
        thread.start()
        print(f"Delighted webhook server started on port {self.port}")
        return thread


def create_delighted_client(api_key: str) -> DelightedClient:
    """
    Delighted クライアントの作成 (Factory function)

    Args:
        api_key: Delighted API key

    Returns:
        DelightedClient インスタンス
    """
    return DelightedClient(api_key)


if __name__ == "__main__":
    import os

    #テストコード
    api_key = os.environ.get('DELIGHTED_API_KEY', 'your-api-key')
    client = create_delighted_client(api_key)

    try:
        # メトリック検索テスト
        metrics = client.get_metrics()
        print("Metrics:", metrics)

        #人生成テスト
        result = client.create_person({
            'email': 'test@example.com',
            'name': 'Test User',
            'properties': {'plan': 'premium'},
            'send': False
        })
        print("Created person:", result)

        # レスポンス検索テスト
        responses = client.search_survey_responses(per_page=5)
        print("Survey responses:", responses)

        ＃Webフックサーバーのテスト
        def handle_new_response(data):
            print(f"New response received: {data}")

        def handle_new_unsubscribe(data):
            print(f"Person unsubscribed: {data}")

        webhook_handler = DelightedWebhookHandler(port=5001)
        webhook_handler.on_new_response(handle_new_response)
        webhook_handler.on_new_unsubscribe(handle_new_unsubscribe)
        webhook_handler.run()

        ＃サーバーの維持
        while True:
            time.sleep(1)

    except Exception as e:
        print(f"Error: {str(e)}")