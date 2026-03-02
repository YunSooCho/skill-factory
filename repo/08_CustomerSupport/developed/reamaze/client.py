"""
Reamaze Client
顧客関係管理およびサポートチケットAPIクライアント
"""

import requests
from typing import Optional, Dict, List, Any


class ReamazeClient:
    """
    Reamaze API クライアント

    顧客関係管理、サポートチケット、チャット管理のためのクライアント
    """

    def __init__(
        self,
        api_key: str,
        account: str,
        base_url: str = "https://api.reamaze.com",
        timeout: int = 30
    ):
        """
        Reamaze クライアントの初期化

        Args:
            api_key: Reamaze API キー
            account: Reamaze アカウント (ブランド)
            base_url：APIベースURL
            timeout：リクエストタイムアウト（秒）
        """
        self.api_key = api_key
        self.account = account
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.auth = (api_key, '')
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        APIリクエストの送信

        Args:
            method: HTTP メソッド
            endpoint: API エンドポイント
            data: 要求本文データ
            params: URL パラメータ

        Returns:
            API応答データ

        Raises:
            requests.RequestException: API リクエストに失敗しました
        """
        url = f"{self.base_url}/{self.account}/{endpoint.lstrip('/')}"
        response = self.session.request(
            method=method,
            url=url,
            json=data,
            params=params,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def create_conversation(
        self,
        subject: str,
        message: str,
        customer_email: str,
        customer_name: Optional[str] = None,
        channel: str = "email",
        tags: Optional[List[str]] = None,
        user_assignee: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        新しい会話（チケット）の作成

        Args:
            subject: タイトル
            message: メッセージ内容
            customer_email：顧客の電子メール
            customer_name：顧客名
            channel: チャンネルタイプ (email, chat, facebook, twitter)
            タグ：タグリスト
            user_assignee: 担当者のメール

        Returns:
            生成された会話情報
        """
        data = {
            'conversation': {
                'subject': subject,
                'message': {
                    'body': message
                },
                'customer': {
                    'email': customer_email,
                    'name': customer_name
                },
                'channel': channel
            }
        }

        if tags:
            data['conversation']['tags'] = tags
        if user_assignee:
            data['conversation']['user'] = {'email': user_assignee}

        return self._request('POST', '/conversations', data=data)

    def get_conversation(self, conversation_id: str) -> Dict[str, Any]:
        """
        会話の照会

        Args:
            conversation_id: 会話 ID (slug)

        Returns:
            会話の詳細
        """
        return self._request('GET', f'/conversations/{conversation_id}')

    def list_conversations(
        self,
        status: Optional[str] = None,
        channel: Optional[str] = None,
        limit: int = 50,
        page: int = 1
    ) -> List[Dict[str, Any]]:
        """
        会話リストの照会

        Args:
            status: ステータスフィルタ (open, pending, resolved, archived)
            channel: チャンネルフィルタ
            limit: 返す項目の数
            page: ページ番号

        Returns:
            会話リスト
        """
        params = {'limit': limit, 'page': page}
        if status:
            params['status'] = status
        if channel:
            params['channel'] = channel

        response = self._request('GET', '/conversations', params=params)
        return response.get('conversations', [])

    def update_conversation(
        self,
        conversation_id: str,
        status: Optional[str] = None,
        user_assignee: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        会話の更新

        Args:
            conversation_id: 会話 ID
            status: 新しい状態
            user_assignee: 新しい担当者
            タグ：新しいタグリスト

        Returns:
            更新された会話情報
        """
        data = {}
        if status:
            data['status'] = status
        if user_assignee:
            data['user'] = {'email': user_assignee}
        if tags:
            data['tags'] = tags

        return self._request('PUT', f'/conversations/{conversation_id}', data={'conversation': data})

    def add_message(
        self,
        conversation_id: str,
        body: str,
        internal: bool = False,
        attachments: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        会話にメッセージを追加する

        Args:
            conversation_id: 会話 ID
            body：メッセージ内容
            internal：内部メッセージがあるかどうか
            attachments: 添付ファイル URLs

        Returns:
            追加されたメッセージ情報
        """
        data = {
            'message': {
                'body': body,
                'internal': internal
            }
        }

        if attachments:
            data['message']['attachments'] = attachments

        return self._request('POST', f'/conversations/{conversation_id}/messages', data=data)

    def list_messages(
        self,
        conversation_id: str,
        limit: int = 50,
        page: int = 1
    ) -> List[Dict[str, Any]]:
        """
        会話メッセージリストの照会

        Args:
            conversation_id: 会話 ID
            limit: 返す項目の数
            page: ページ番号

        Returns:
            メッセージ一覧
        """
        params = {'limit': limit, 'page': page}
        response = self._request('GET', f'/conversations/{conversation_id}/messages', params=params)
        return response.get('messages', [])

    def create_customer(
        self,
        email: str,
        name: Optional[str] = None,
        phone: Optional[str] = None,
        company: Optional[str] = None,
        location: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        新しい顧客を作成

        Args:
            email：顧客の電子メール
            name：顧客名
            phone: 電話番号
            company：会社名
            location: 場所
            metadata: 追加のメタデータ

        Returns:
            生成された顧客情報
        """
        data = {
            'customer': {
                'email': email
            }
        }

        if name:
            data['customer']['name'] = name
        if phone:
            data['customer']['phone'] = phone
        if company:
            data['customer']['company'] = company
        if location:
            data['customer']['location'] = location
        if metadata:
            data['customer']['customAttributes'] = metadata

        return self._request('POST', '/customers', data=data)

    def get_customer(self, customer_id: str) -> Dict[str, Any]:
        """
        顧客の照会

        Args:
            customer_id：顧客ID

        Returns:
            顧客情報
        """
        return self._request('GET', f'/customers/{customer_id}')

    def list_customers(
        self,
        search: Optional[str] = None,
        limit: int = 50,
        page: int = 1
    ) -> List[Dict[str, Any]]:
        """
        顧客リストの照会

        Args:
            search：クエリ（名前、Eメール、会社）
            limit: 返す項目の数
            page: ページ番号

        Returns:
            顧客リスト
        """
        params = {'limit': limit, 'page': page}
        if search:
            params['q'] = search

        response = self._request('GET', '/customers', params=params)
        return response.get('customers', [])

    def get_user(self, user_id: str) -> Dict[str, Any]:
        """
        ユーザー（従業員）の照会

        Args:
            user_id：ユーザーID

        Returns:
            ユーザー情報
        """
        return self._request('GET', f'/users/{user_id}')

    def list_users(self) -> List[Dict[str, Any]]:
        """
        ユーザー（従業員）リストの照会

        Returns:
            ユーザーリスト
        """
        response = self._request('GET', '/users')
        return response.get('users', [])

    def get_statistics(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        統計情報の照会

        Args:
            start_date：開始日（YYYY-MM-DD）
            end_date: 終了日 (YYYY-MM-DD)

        Returns:
            統計情報
        """
        params = {}
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date

        return self._request('GET', '/statistics', params=params)

    def create_article(
        self,
        title: str,
        content: str,
        category_id: str,
        published: bool = False
    ) -> Dict[str, Any]:
        """
        ヘルプドキュメント（記事）の作成

        Args:
            title: ドキュメントのタイトル
            content: 文書の内容 (HTML/Markdown)
            category_id：カテゴリID
            published: 公開するかどうか

        Returns:
            生成された文書情報
        """
        data = {
            'article': {
                'title': title,
                'content': content,
                'category_id': category_id,
                'published': published
            }
        }

        return self._request('POST', '/articles', data=data)

    def list_channels(self) -> List[Dict[str, Any]]:
        """
        チャンネルリストを見る

        Returns:
            チャンネルリスト
        """
        response = self._request('GET', '/channels')
        return response.get('channels', [])

    def close(self):
        """セッション終了"""
        self.session.close()