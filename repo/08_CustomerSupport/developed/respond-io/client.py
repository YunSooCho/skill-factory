"""
Respond.io Client
マルチチャンネルカスタマーサポートAPIクライアント
"""

import requests
from typing import Optional, Dict, List, Any


class RespondIOClient:
    """
    Respond.io API クライアント

    マルチチャンネルカスタマーサポート、メッセージ管理、顧客追跡のためのクライアント
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.respond.io/v1",
        timeout: int = 30
    ):
        """
        Respond.io クライアントの初期化

        Args:
            api_key: Respond.io API キー
            base_url：APIベースURL
            timeout：リクエストタイムアウト（秒）
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
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
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.request(
            method=method,
            url=url,
            json=data,
            params=params,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def create_message(
        self,
        channel_id: str,
        text: str,
        customer_id: Optional[str] = None,
        file_urls: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        メッセージ送信

        Args:
            channel_id：チャンネルID
            text: メッセージ内容
            customer_id：顧客ID（選択）
            file_urls：ファイルURLリスト
            metadata: 追加のメタデータ

        Returns:
            送信されたメッセージ情報
        """
        data = {
            'channelId': channel_id,
            'text': text
        }

        if customer_id:
            data['customerId'] = customer_id
        if file_urls:
            data['fileUrls'] = file_urls
        if metadata:
            data['metadata'] = metadata

        return self._request('POST', '/messages', data=data)

    def get_message(self, message_id: str) -> Dict[str, Any]:
        """
        メッセージの照会

        Args:
            message_id：メッセージID

        Returns:
            メッセージ情報
        """
        return self._request('GET', f'/messages/{message_id}')

    def list_messages(
        self,
        conversation_id: Optional[str] = None,
        channel_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        メッセージリストの照会

        Args:
            conversation_id: 会話 ID フィルタ
            channel_id：チャンネルIDフィルタ
            limit: 返す項目の数
            offset: オフセット

        Returns:
            メッセージ一覧
        """
        params = {'limit': limit, 'offset': offset}
        if conversation_id:
            params['conversationId'] = conversation_id
        if channel_id:
            params['channelId'] = channel_id

        response = self._request('GET', '/messages', params=params)
        return response.get('messages', [])

    def create_conversation(
        self,
        customer_id: str,
        channel_id: str,
        initial_message: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        新しい会話の作成

        Args:
            customer_id：顧客ID
            channel_id：チャンネルID
            initial_message: 初期メッセージ
            タグ：タグリスト

        Returns:
            生成された会話情報
        """
        data = {
            'customerId': customer_id,
            'channelId': channel_id
        }

        if initial_message:
            data['initialMessage'] = initial_message
        if tags:
            data['tags'] = tags

        return self._request('POST', '/conversations', data=data)

    def get_conversation(self, conversation_id: str) -> Dict[str, Any]:
        """
        会話の照会

        Args:
            conversation_id: 会話 ID

        Returns:
            会話情報
        """
        return self._request('GET', f'/conversations/{conversation_id}')

    def list_conversations(
        self,
        status: Optional[str] = None,
        channel_id: Optional[str] = None,
        assigned_to: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        会話リストの照会

        Args:
            status: ステータスフィルタ (open, pending, closed)
            channel_id：チャンネルIDフィルタ
            assigned_to：担当者IDフィルタ
            limit: 返す項目の数
            offset: オフセット

        Returns:
            会話リスト
        """
        params = {'limit': limit, 'offset': offset}
        if status:
            params['status'] = status
        if channel_id:
            params['channelId'] = channel_id
        if assigned_to:
            params['assignedTo'] = assigned_to

        response = self._request('GET', '/conversations', params=params)
        return response.get('conversations', [])

    def update_conversation(
        self,
        conversation_id: str,
        status: Optional[str] = None,
        assigned_to: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        会話の更新

        Args:
            conversation_id: 会話 ID
            status: 新しい状態
            assigned_to：新しい担当者
            タグ：新しいタグリスト

        Returns:
            更新された会話情報
        """
        data = {}
        if status:
            data['status'] = status
        if assigned_to:
            data['assignedTo'] = assigned_to
        if tags:
            data['tags'] = tags

        return self._request('PUT', f'/conversations/{conversation_id}', data=data)

    def close_conversation(self, conversation_id: str) -> Dict[str, Any]:
        """
        会話の終了

        Args:
            conversation_id: 会話 ID

        Returns:
            終了した会話情報
        """
        return self._request('POST', f'/conversations/{conversation_id}/close')

    def create_customer(
        self,
        external_id: str,
        name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        avatar_url: Optional[str] = None,
        custom_attributes: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        新しい顧客を作成

        Args:
            external_id：外部システムの顧客ID
            name: 名前
            email: メール
            phone: 電話番号
            avatar_url：アバターURL
            custom_attributes: カスタム属性

        Returns:
            生成された顧客情報
        """
        data = {'externalId': external_id}

        if name:
            data['name'] = name
        if email:
            data['email'] = email
        if phone:
            data['phone'] = phone
        if avatar_url:
            data['avatarUrl'] = avatar_url
        if custom_attributes:
            data['customAttributes'] = custom_attributes

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

    def update_customer(
        self,
        customer_id: str,
        name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        avatar_url: Optional[str] = None,
        custom_attributes: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        顧客の更新

        Args:
            customer_id：顧客ID
            name: 新しい名前
            email: 新しいメール
            phone: 新しい電話番号
            avatar_url：新しいアバターURL
            custom_attributes: カスタム属性

        Returns:
            更新された顧客情報
        """
        data = {}
        if name:
            data['name'] = name
        if email:
            data['email'] = email
        if phone:
            data['phone'] = phone
        if avatar_url:
            data['avatarUrl'] = avatar_url
        if custom_attributes:
            data['customAttributes'] = custom_attributes

        return self._request('PUT', f'/customers/{customer_id}', data=data)

    def list_channels(self) -> List[Dict[str, Any]]:
        """
        チャンネルリストを見る

        Returns:
            チャンネルリスト
        """
        response = self._request('GET', '/channels')
        return response.get('channels', [])

    def list_users(self) -> List[Dict[str, Any]]:
        """
        ユーザーリストの照会

        Returns:
            ユーザーリスト
        """
        response = self._request('GET', '/users')
        return response.get('users', [])

    def assign_conversation(
        self,
        conversation_id: str,
        user_id: str
    ) -> Dict[str, Any]:
        """
        会話担当者の指定

        Args:
            conversation_id: 会話 ID
            user_id：ユーザーID

        Returns:
            更新された会話情報
        """
        data = {
            'conversationId': conversation_id,
            'userId': user_id
        }

        return self._request('POST', '/conversations/assign', data=data)

    def add_note(
        self,
        conversation_id: str,
        content: str,
        author_id: str
    ) -> Dict[str, Any]:
        """
        会話にメモを追加する

        Args:
            conversation_id: 会話 ID
            content: ノートの内容
            author_id：作成者ID

        Returns:
            追加されたノート情報
        """
        data = {
            'conversationId': conversation_id,
            'content': content,
            'authorId': author_id
        }

        return self._request('POST', '/conversations/notes', data=data)

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
            params['startDate'] = start_date
        if end_date:
            params['endDate'] = end_date

        return self._request('GET', '/statistics', params=params)

    def close(self):
        """セッション終了"""
        self.session.close()