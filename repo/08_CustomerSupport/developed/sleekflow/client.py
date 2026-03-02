"""
Sleekflow Client
チャットとカスタマーサポートワークフローAPIクライアント
"""

import requests
from typing import Optional, Dict, List, Any


class SleekflowClient:
    """
    Sleekflow APIクライアント

    チャット、ワークフロー自動化、顧客トラッキングのためのクライアント
    """

    def __init__(
        self,
        api_key: str,
        workspace_id: str,
        base_url: str = "https://api.sleekflow.io/v1",
        timeout: int = 30
    ):
        """
        Sleekflowクライアントの初期化

        Args:
            api_key: Sleekflow API キー
            workspace_id: ワークスペース ID
            base_url：APIベースURL
            timeout：リクエストタイムアウト（秒）
        """
        self.api_key = api_key
        self.workspace_id = workspace_id
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-Key': api_key,
            'X-Workspace-Id': workspace_id,
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

    def create_chat_session(
        self,
        customer_id: str,
        channel: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        新しいチャットセッションの作成

        Args:
            customer_id：顧客ID
            channel: チャンネルタイプ (web, whatsapp, messenger, telegram)
            metadata: 追加のメタデータ

        Returns:
            生成されたチャットセッション情報
        """
        data = {
            'customerId': customer_id,
            'channel': channel
        }

        if metadata:
            data['metadata'] = metadata

        return self._request('POST', '/chat/sessions', data=data)

    def get_chat_session(self, session_id: str) -> Dict[str, Any]:
        """
        チャットセッションの検索

        Args:
            session_id: チャットセッションID

        Returns:
            チャットセッションについて
        """
        return self._request('GET', f'/chat/sessions/{session_id}')

    def list_chat_sessions(
        self,
        customer_id: Optional[str] = None,
        status: Optional[str] = None,
        channel: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        チャットセッションリストの検索

        Args:
            customer_id：顧客IDフィルタ
            status: ステータスフィルタ (active, closed, archived)
            channel: チャンネルフィルタ
            limit: 返す項目の数
            offset: オフセット

        Returns:
            チャットセッション一覧
        """
        params = {'limit': limit, 'offset': offset}
        if customer_id:
            params['customerId'] = customer_id
        if status:
            params['status'] = status
        if channel:
            params['channel'] = channel

        response = self._request('GET', '/chat/sessions', params=params)
        return response.get('sessions', [])

    def send_message(
        self,
        session_id: str,
        text: str,
        message_type: str = "text",
        sender_type: str = "agent",
        file_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        メッセージ送信

        Args:
            session_id: チャットセッションID
            text: メッセージ内容
            message_type：メッセージタイプ（text、image、video、file）
            sender_type：発信者タイプ（agent、customer、bot）
            file_url：ファイルURL

        Returns:
            送信されたメッセージ情報
        """
        data = {
            'sessionId': session_id,
            'text': text,
            'messageType': message_type,
            'senderType': sender_type
        }

        if file_url:
            data['fileUrl'] = file_url

        return self._request('POST', '/chat/messages', data=data)

    def get_messages(
        self,
        session_id: str,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        メッセージリストの照会

        Args:
            session_id: チャットセッションID
            limit: 返す項目の数
            offset: オフセット

        Returns:
            メッセージ一覧
        """
        params = {'limit': limit, 'offset': offset}
        response = self._request('GET', f'/chat/sessions/{session_id}/messages', params=params)
        return response.get('messages', [])

    def create_workflow(
        self,
        name: str,
        description: str,
        steps: List[Dict[str, Any]],
        trigger_type: str = "manual",
        is_active: bool = False
    ) -> Dict[str, Any]:
        """
        新しいワークフローの作成

        Args:
            name: ワークフロー名
            description: 説明
            steps: ワークフローステップのリスト
            trigger_type: トリガータイプ (manual, schedule, event)
            is_active: 有効かどうか

        Returns:
            生成されたワークフロー情報
        """
        data = {
            'name': name,
            'description': description,
            'steps': steps,
            'triggerType': trigger_type,
            'isActive': is_active
        }

        return self._request('POST', '/workflows', data=data)

    def get_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """
        ワークフロー照会

        Args:
            workflow_id: ワークフローID

        Returns:
            ワークフローの詳細
        """
        return self._request('GET', f'/workflows/{workflow_id}')

    def list_workflows(
        self,
        is_active: Optional[bool] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        ワークフローリストの照会

        Args:
            is_active: アクティブ状態フィルタ
            limit: 返す項目の数
            offset: オフセット

        Returns:
            ワークフローリスト
        """
        params = {'limit': limit, 'offset': offset}
        if is_active is not None:
            params['isActive'] = is_active

        response = self._request('GET', '/workflows', params=params)
        return response.get('workflows', [])

    def trigger_workflow(
        self,
        workflow_id: str,
        customer_id: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        ワークフロートリガー

        Args:
            workflow_id: ワークフローID
            customer_id：顧客ID
            parameters: ワークフローパラメータ

        Returns:
            トリガー結果
        """
        data = {
            'workflowId': workflow_id,
            'customerId': customer_id
        }

        if parameters:
            data['parameters'] = parameters

        return self._request('POST', '/workflows/trigger', data=data)

    def create_template(
        self,
        name: str,
        category: str,
        content: str,
        variables: Optional[List[str]] = None,
        language: str = "ko"
    ) -> Dict[str, Any]:
        """
        メッセージテンプレートの生成

        Args:
            name: テンプレート名
            category: カテゴリ (greeting, followup, notification)
            content: テンプレートの内容
            variables: 変数リスト
            language: 言語コード

        Returns:
            生成されたテンプレート情報
        """
        data = {
            'name': name,
            'category': category,
            'content': content,
            'language': language
        }

        if variables:
            data['variables'] = variables

        return self._request('POST', '/templates', data=data)

    def get_template(self, template_id: str) -> Dict[str, Any]:
        """
        テンプレート検索

        Args:
            template_id：テンプレートID

        Returns:
            テンプレート情報
        """
        return self._request('GET', f'/templates/{template_id}')

    def list_templates(
        self,
        category: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        テンプレートリストの照会

        Args:
            category: カテゴリフィルタ
            limit: 返す項目の数
            offset: オフセット

        Returns:
            テンプレートリスト
        """
        params = {'limit': limit, 'offset': offset}
        if category:
            params['category'] = category

        response = self._request('GET', '/templates', params=params)
        return response.get('templates', [])

    def create_bot(
        self,
        name: str,
        description: str,
        greeting_message: str,
        ai_model: str = "gpt-4",
        knowledge_base: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        AIチャットボットの作成

        Args:
            name: ボット名
            description: 説明
            greeting_message: ようこそメッセージ
            ai_model：AIモデル（gpt-3.5、gpt-4、claude）
            knowledge_base: 知識ベース ID

        Returns:
            生成されたボット情報
        """
        data = {
            'name': name,
            'description': description,
            'greetingMessage': greeting_message,
            'aiModel': ai_model
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

    def get_analytics(
        self,
        start_date: str,
        end_date: str,
        metric: str = "all",
        channel: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        分析データの照会

        Args:
            start_date：開始日（YYYY-MM-DD）
            end_date: 終了日 (YYYY-MM-DD)
            metric: メトリック (all, messages, sessions, satisfaction)
            channel: チャンネルフィルタ

        Returns:
            分析データ
        """
        params = {
            'startDate': start_date,
            'endDate': end_date,
            'metric': metric
        }

        if channel:
            params['channel'] = channel

        return self._request('GET', '/analytics', params=params)

    def track_customer_event(
        self,
        customer_id: str,
        event_name: str,
        properties: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        顧客イベントの追跡

        Args:
            customer_id：顧客ID
            event_name：イベント名
            properties: イベント属性

        Returns:
            追跡結果
        """
        data = {
            'customerId': customer_id,
            'eventName': event_name
        }

        if properties:
            data['properties'] = properties

        return self._request('POST', '/customers/events', data=data)

    def close(self):
        """セッション終了"""
        self.session.close()