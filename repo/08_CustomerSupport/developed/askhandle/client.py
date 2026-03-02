"""
AskHandle Client
顧客の問い合わせとリクエスト管理APIクライアント
"""

import requests
from typing import Optional, Dict, List, Any
from datetime import datetime


class AskHandleClient:
    """
    AskHandle APIクライアント

    顧客の問い合わせ、要求、チケット管理のためのクライアント
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.askhandle.com/v1",
        timeout: int = 30
    ):
        """
        AskHandleクライアントの初期化

        Args:
            api_key: AskHandle API キー
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

    def create_ticket(
        self,
        title: str,
        description: str,
        requester_name: str,
        requester_email: str,
        priority: str = "medium",
        category: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        新しいチケットの作成

        Args:
            title: チケットのタイトル
            description: チケットの説明
            requester_name: リクエスタ名
            requester_email：リクエスタメール
            priority: 優先順位 (low, medium, high, urgent)
            category: チケットカテゴリ
            タグ：チケットタグリスト

        Returns:
            生成されたチケット情報
        """
        data = {
            'title': title,
            'description': description,
            'requester': {
                'name': requester_name,
                'email': requester_email
            },
            'priority': priority
        }

        if category:
            data['category'] = category
        if tags:
            data['tags'] = tags

        return self._request('POST', '/tickets', data=data)

    def get_ticket(self, ticket_id: str) -> Dict[str, Any]:
        """
        チケット詳細検索

        Args:
            ticket_id：チケットID

        Returns:
            チケット詳細
        """
        return self._request('GET', f'/tickets/{ticket_id}')

    def list_tickets(
        self,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        チケットリストを見る

        Args:
            status: ステータスフィルタ (open, in_progress, resolved, closed)
            priority: 優先順位フィルタ
            limit: 返す項目の数
            offset: オフセット

        Returns:
            チケット一覧
        """
        params = {'limit': limit, 'offset': offset}
        if status:
            params['status'] = status
        if priority:
            params['priority'] = priority

        response = self._request('GET', '/tickets', params=params)
        return response.get('tickets', [])

    def update_ticket(
        self,
        ticket_id: str,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        assignee_id: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        チケットの更新

        Args:
            ticket_id：チケットID
            status: 新しい状態
            priority: 新しい優先順位
            assignee_id：担当者ID
            tags: 更新するタグのリスト

        Returns:
            更新されたチケット情報
        """
        data = {}
        if status:
            data['status'] = status
        if priority:
            data['priority'] = priority
        if assignee_id:
            data['assignee_id'] = assignee_id
        if tags:
            data['tags'] = tags

        return self._request('PUT', f'/tickets/{ticket_id}', data=data)

    def add_comment(
        self,
        ticket_id: str,
        comment: str,
        author_name: str,
        author_email: str,
        is_internal: bool = False
    ) -> Dict[str, Any]:
        """
        チケットにコメントを追加

        Args:
            ticket_id：チケットID
            comment: コメント内容
            author_name：作成者名
            author_email：作成者のEメール
            is_internal：内部でコメントするかどうか

        Returns:
            追加されたコメント情報
        """
        data = {
            'comment': comment,
            'author': {
                'name': author_name,
                'email': author_email
            },
            'is_internal': is_internal
        }

        return self._request('POST', f'/tickets/{ticket_id}/comments', data=data)

    def get_ticket_comments(self, ticket_id: str) -> List[Dict[str, Any]]:
        """
        チケットのコメントリストを見る

        Args:
            ticket_id：チケットID

        Returns:
            コメントリスト
        """
        response = self._request('GET', f'/tickets/{ticket_id}/comments')
        return response.get('comments', [])

    def create_customer(
        self,
        name: str,
        email: str,
        phone: Optional[str] = None,
        company: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        新しい顧客を作成

        Args:
            name：顧客名
            email：顧客の電子メール
            phone: 電話番号
            company：会社名
            metadata: 追加のメタデータ

        Returns:
            生成された顧客情報
        """
        data = {
            'name': name,
            'email': email
        }

        if phone:
            data['phone'] = phone
        if company:
            data['company'] = company
        if metadata:
            data['metadata'] = metadata

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
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        顧客リストの照会

        Args:
            search: 検索語
            limit: 返す項目の数
            offset: オフセット

        Returns:
            顧客リスト
        """
        params = {'limit': limit, 'offset': offset}
        if search:
            params['search'] = search

        response = self._request('GET', '/customers', params=params)
        return response.get('customers', [])

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

    def close(self):
        """セッション終了"""
        self.session.close()