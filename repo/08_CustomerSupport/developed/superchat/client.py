"""
Superchat Client
ライブチャットとカスタマーサポートAPIクライアント
"""

import requests
from typing import Optional, Dict, List, Any


class SuperchatClient:
    """
    Superchat API クライアント

    ライブチャット、カスタマーサポート、チャットボット管理のためのクライアント
    """

    def __init__(
        self,
        api_key: str,
        account_id: str,
        base_url: str = "https://api.superchat.com/v1",
        timeout: int = 30
    ):
        """
        Superchat クライアントの初期化

        Args:
            api_key: Superchat API キー
            account_id：アカウントID
            base_url：APIベースURL
            timeout：リクエストタイムアウト（秒）
        """
        self.api_key = api_key
        self.account_id = account_id
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-Key': api_key,
            'X-Account-Id': account_id,
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

    def start_chat(
        self,
        customer_name: str,
        customer_email: Optional[str] = None,
        initial_message: Optional[str] = None,
        channel: str = "web",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        新しいチャットを開始

        Args:
            customer_name：顧客名
            customer_email：顧客の電子メール
            initial_message: 初期メッセージ
            channel: チャンネルタイプ (web, whatsapp, messenger, telegram)
            metadata: 追加のメタデータ

        Returns:
            生成されたチャット情報
        """
        data = {
            'customerName': customer_name,
            'channel': channel
        }

        if customer_email:
            data['customerEmail'] = customer_email
        if initial_message:
            data['initialMessage'] = initial_message
        if metadata:
            data['metadata'] = metadata

        return self._request('POST', '/chats', data=data)

    def get_chat(self, chat_id: str) -> Dict[str, Any]:
        """
        チャットを見る

        Args:
            chat_id：チャットID

        Returns:
            チャットの詳細
        """
        return self._request('GET', f'/chats/{chat_id}')

    def list_chats(
        self,
        status: Optional[str] = None,
        channel: Optional[str] = None,
        assigned_to: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        チャットリストを見る

        Args:
            status: ステータスフィルタ (active, closed, archived)
            channel: チャンネルフィルタ
            assigned_to：担当者IDフィルタ
            limit: 返す項目の数
            offset: オフセット

        Returns:
            チャットリスト
        """
        params = {'limit': limit, 'offset': offset}
        if status:
            params['status'] = status
        if channel:
            params['channel'] = channel
        if assigned_to:
            params['assignedTo'] = assigned_to

        response = self._request('GET', '/chats', params=params)
        return response.get('chats', [])

    def send_message(
        self,
        chat_id: str,
        message: str,
        message_type: str = "text",
        sender_type: str = "agent",
        file_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        メッセージ送信

        Args:
            chat_id：チャットID
            message: メッセージ内容
            message_type：メッセージタイプ（text、image、video、file、location）
            sender_type：発信者タイプ（agent、customer、bot、system）
            file_url：ファイルURL

        Returns:
            送信されたメッセージ情報
        """
        data = {
            'chatId': chat_id,
            'message': message,
            'messageType': message_type,
            'senderType': sender_type
        }

        if file_url:
            data['fileUrl'] = file_url

        return self._request('POST', '/messages', data=data)

    def get_messages(
        self,
        chat_id: str,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        メッセージリストの照会

        Args:
            chat_id：チャットID
            limit: 返す項目の数
            offset: オフセット

        Returns:
            メッセージ一覧
        """
        params = {'limit': limit, 'offset': offset}
        response = self._request('GET', f'/chats/{chat_id}/messages', params=params)
        return response.get('messages', [])

    def update_chat(
        self,
        chat_id: str,
        status: Optional[str] = None,
        assigned_to: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        チャットの更新

        Args:
            chat_id：チャットID
            status: 新しい状態
            assigned_to：新しい担当者
            タグ：タグリスト

        Returns:
            更新されたチャット情報
        """
        data = {}
        if status:
            data['status'] = status
        if assigned_to:
            data['assignedTo'] = assigned_to
        if tags:
            data['tags'] = tags

        return self._request('PUT', f'/chats/{chat_id}', data=data)

    def close_chat(self, chat_id: str) -> Dict[str, Any]:
        """
        チャット終了

        Args:
            chat_id：チャットID

        Returns:
            終了したチャット情報
        """
        return self._request('POST', f'/chats/{chat_id}/close')

    def assign_chat(
        self,
        chat_id: str,
        agent_id: str
    ) -> Dict[str, Any]:
        """
        チャット担当者の指定

        Args:
            chat_id：チャットID
            agent_id：エージェントID

        Returns:
            更新されたチャット情報
        """
        data = {
            'chatId': chat_id,
            'agentId': agent_id
        }

        return self._request('POST', '/chats/assign', data=data)

    def create_customer(
        self,
        name: str,
        email: str,
        phone: Optional[str] = None,
        avatar_url: Optional[str] = None,
        company: Optional[str] = None,
        custom_attributes: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        新しい顧客を作成

        Args:
            name: 名前
            email: メール
            phone: 電話番号
            avatar_url：アバターURL
            company: 会社
            custom_attributes: カスタム属性

        Returns:
            生成された顧客情報
        """
        data = {
            'name': name,
            'email': email
        }

        if phone:
            data['phone'] = phone
        if avatar_url:
            data['avatarUrl'] = avatar_url
        if company:
            data['company'] = company
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
        company: Optional[str] = None,
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
            company: 新しい会社
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
        if company:
            data['company'] = company
        if custom_attributes:
            data['customAttributes'] = custom_attributes

        return self._request('PUT', f'/customers/{customer_id}', data=data)

    def create_bot(
        self,
        name: str,
        welcome_message: str,
        handoff_message: str,
        ai_provider: str = "openai",
        ai_model: str = "gpt-4o-mini",
        knowledge_base: Optional[str] = None,
        is_active: bool = False
    ) -> Dict[str, Any]:
        """
        AIチャットボットの作成

        Args:
            name: ボット名
            welcome_message: ようこそメッセージ
            handoff_message: エージェント転送メッセージ
            ai_provider：AIプロバイダ（openai、anthropic、google）
            ai_model：AIモデル
            knowledge_base: 知識ベース ID
            is_active: 有効かどうか

        Returns:
            生成されたボット情報
        """
        data = {
            'name': name,
            'welcomeMessage': welcome_message,
            'handoffMessage': handoff_message,
            'aiProvider': ai_provider,
            'aiModel': ai_model,
            'isActive': is_active
        }

        if knowledge_base:
            data['knowledgeBase'] = knowledge_base

        return self._request('POST', '/bots', data=data)

    def get_bot(self, bot_id: str) -> Dict[str, Any]:
        """
        ボットを見る

        Args:
            bot_id: ボット ID

        Returns:
            ボット情報
        """
        return self._request('GET', f'/bots/{bot_id}')

    def list_bots(self) -> List[Dict[str, Any]]:
        """
        ボットリストの照会

        Returns:
            ボット一覧
        """
        response = self._request('GET', '/bots')
        return response.get('bots', [])

    def update_bot(
        self,
        bot_id: str,
        name: Optional[str] = None,
        welcome_message: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        ボットアップデート

        Args:
            bot_id: ボット ID
            name: 新しい名前
            welcome_message: 新しいウェルカムメッセージ
            is_active: アクティブ状態

        Returns:
            更新されたボット情報
        """
        data = {}
        if name:
            data['name'] = name
        if welcome_message:
            data['welcomeMessage'] = welcome_message
        if is_active is not None:
            data['isActive'] = is_active

        return self._request('PUT', f'/bots/{bot_id}', data=data)

    def create_canned_response(
        self,
        title: str,
        content: str,
        shortcuts: Optional[List[str]] = None,
        category: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        テンプレート応答の生成

        Args:
            title: タイトル
            content: 内容
            ショートカット：ショートカットリスト
            category：カテゴリ

        Returns:
            生成されたテンプレート応答情報
        """
        data = {
            'title': title,
            'content': content
        }

        if shortcuts:
            data['shortcuts'] = shortcuts
        if category:
            data['category'] = category

        return self._request('POST', '/canned-responses', data=data)

    def list_canned_responses(
        self,
        category: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        テンプレート応答リストの照会

        Args:
            category: カテゴリフィルタ
            limit: 返す項目の数

        Returns:
            テンプレート応答リスト
        """
        params = {'limit': limit}
        if category:
            params['category'] = category

        response = self._request('GET', '/canned-responses', params=params)
        return response.get('cannedResponses', [])

    def get_analytics(
        self,
        start_date: str,
        end_date: str,
        metric: str = "all"
    ) -> Dict[str, Any]:
        """
        分析データの照会

        Args:
            start_date：開始日（YYYY-MM-DD）
            end_date: 終了日 (YYYY-MM-DD)
            metric: メトリック (all, messages, chats, satisfaction, response_time)

        Returns:
            分析データ
        """
        params = {
            'startDate': start_date,
            'endDate': end_date,
            'metric': metric
        }

        return self._request('GET', '/analytics', params=params)

    def list_agents(self) -> List[Dict[str, Any]]:
        """
        エージェントリストの照会

        Returns:
            エージェント一覧
        """
        response = self._request('GET', '/agents')
        return response.get('agents', [])

    def close(self):
        """セッション終了"""
        self.session.close()