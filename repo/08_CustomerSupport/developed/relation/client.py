"""
Relation Client
顧客関係管理APIクライアント
"""

import requests
from typing import Optional, Dict, List, Any
from datetime import datetime


class RelationClient:
    """
    Relation API クライアント

    顧客関係管理、セグメント、キャンペーン管理のためのクライアント
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.relation.io/v1",
        timeout: int = 30
    ):
        """
        Relation クライアントの初期化

        Args:
            api_key: Relation API キー
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

    def create_contact(
        self,
        email: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        phone: Optional[str] = None,
        company: Optional[str] = None,
        title: Optional[str] = None,
        tags: Optional[List[str]] = None,
        attributes: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        新しい連絡先の作成

        Args:
            email：Eメール（必須）
            first_name：名前
            last_name: 姓
            phone: 電話番号
            company: 会社
            title: 役職
            タグ：タグリスト
            attributes: 追加属性

        Returns:
            生成された連絡先情報
        """
        data = {'email': email}

        if first_name:
            data['firstName'] = first_name
        if last_name:
            data['lastName'] = last_name
        if phone:
            data['phone'] = phone
        if company:
            data['company'] = company
        if title:
            data['title'] = title
        if tags:
            data['tags'] = tags
        if attributes:
            data['attributes'] = attributes

        return self._request('POST', '/contacts', data=data)

    def get_contact(self, contact_id: str) -> Dict[str, Any]:
        """
        お問い合わせ

        Args:
            contact_id：連絡先ID

        Returns:
            連絡先情報
        """
        return self._request('GET', f'/contacts/{contact_id}')

    def update_contact(
        self,
        contact_id: str,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        phone: Optional[str] = None,
        company: Optional[str] = None,
        title: Optional[str] = None,
        add_tags: Optional[List[str]] = None,
        remove_tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        連絡先の更新

        Args:
            contact_id：連絡先ID
            email: 新しいメール
            first_name：新しい名前
            last_name: 新しい姓
            phone: 新しい電話番号
            company: 新しい会社
            title: 新しい役職
            add_tags：追加するタグ
            remove_tags: 削除するタグ

        Returns:
            更新された連絡先情報
        """
        data = {}
        if email:
            data['email'] = email
        if first_name:
            data['firstName'] = first_name
        if last_name:
            data['lastName'] = last_name
        if phone:
            data['phone'] = phone
        if company:
            data['company'] = company
        if title:
            data['title'] = title
        if add_tags:
            data['addTags'] = add_tags
        if remove_tags:
            data['removeTags'] = remove_tags

        return self._request('PUT', f'/contacts/{contact_id}', data=data)

    def list_contacts(
        self,
        tags: Optional[List[str]] = None,
        created_after: Optional[str] = None,
        created_before: Optional[str] = None,
        search: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        連絡先リストの照会

        Args:
            タグ：タグフィルタ
            created_after：作成日以降（YYYY-MM-DD）
            created_before：作成日前（YYYY-MM-DD）
            search: 検索語
            limit: 返す項目の数
            offset: オフセット

        Returns:
            連絡先リスト
        """
        params = {'limit': limit, 'offset': offset}
        if tags:
            params['tags'] = tags
        if created_after:
            params['createdAfter'] = created_after
        if created_before:
            params['createdBefore'] = created_before
        if search:
            params['search'] = search

        response = self._request('GET', '/contacts', params=params)
        return response.get('contacts', [])

    def delete_contact(self, contact_id: str) -> Dict[str, Any]:
        """
        連絡先の削除

        Args:
            contact_id：連絡先ID

        Returns:
            削除結果
        """
        return self._request('DELETE', f'/contacts/{contact_id}')

    def create_segment(
        self,
        name: str,
        description: Optional[str] = None,
        criteria: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        新しいセグメントの作成

        Args:
            name: セグメント名
            description: 説明
            criteria: フィルタリング基準

        Returns:
            生成されたセグメント情報
        """
        data = {'name': name}

        if description:
            data['description'] = description
        if criteria:
            data['criteria'] = criteria

        return self._request('POST', '/segments', data=data)

    def get_segment(self, segment_id: str) -> Dict[str, Any]:
        """
        セグメント照会

        Args:
            segment_id：セグメントID

        Returns:
            セグメント情報
        """
        return self._request('GET', f'/segments/{segment_id}')

    def list_segments(
        self,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        セグメントリストの照会

        Args:
            limit: 返す項目の数
            offset: オフセット

        Returns:
            セグメントリスト
        """
        params = {'limit': limit, 'offset': offset}
        response = self._request('GET', '/segments', params=params)
        return response.get('segments', [])

    def get_segment_contacts(
        self,
        segment_id: str,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        セグメントに属する連絡先の検索

        Args:
            segment_id：セグメントID
            limit: 返す項目の数
            offset: オフセット

        Returns:
            連絡先リスト
        """
        params = {'limit': limit, 'offset': offset}
        response = self._request('GET', f'/segments/{segment_id}/contacts', params=params)
        return response.get('contacts', [])

    def create_note(
        self,
        contact_id: str,
        content: str,
        author_id: Optional[str] = None,
        note_type: str = "general"
    ) -> Dict[str, Any]:
        """
        ノートの作成

        Args:
            contact_id：連絡先ID
            content: ノートの内容
            author_id：作成者ID
            note_type: ノートタイプ (general, meeting, call, email)

        Returns:
            生成されたノート情報
        """
        data = {
            'contactId': contact_id,
            'content': content,
            'noteType': note_type
        }

        if author_id:
            data['authorId'] = author_id

        return self._request('POST', '/notes', data=data)

    def get_notes(
        self,
        contact_id: str,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        連絡先ノートリストの表示

        Args:
            contact_id：連絡先ID
            limit: 返す項目の数
            offset: オフセット

        Returns:
            ノートリスト
        """
        params = {'limit': limit, 'offset': offset}
        response = self._request('GET', f'/contacts/{contact_id}/notes', params=params)
        return response.get('notes', [])

    def create_task(
        self,
        contact_id: str,
        title: str,
        description: Optional[str] = None,
        due_date: Optional[str] = None,
        assignee_id: Optional[str] = None,
        priority: str = "medium"
    ) -> Dict[str, Any]:
        """
        タスクの作成

        Args:
            contact_id：連絡先ID
            title: タイトル
            description: 説明
            due_date：期限（YYYY-MM-DD）
            assignee_id：担当者ID
            priority: 優先順位 (low, medium, high)

        Returns:
            生成されたタスク情報
        """
        data = {
            'contactId': contact_id,
            'title': title,
            'priority': priority
        }

        if description:
            data['description'] = description
        if due_date:
            data['dueDate'] = due_date
        if assignee_id:
            data['assigneeId'] = assignee_id

        return self._request('POST', '/tasks', data=data)

    def list_tasks(
        self,
        contact_id: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        タスクリストの照会

        Args:
            contact_id：連絡先IDフィルタ
            status: ステータスフィルタ (pending, in_progress, completed)
            priority：優先順位フィルタ
            limit: 返す項目の数
            offset: オフセット

        Returns:
            タスクリスト
        """
        params = {'limit': limit, 'offset': offset}
        if contact_id:
            params['contactId'] = contact_id
        if status:
            params['status'] = status
        if priority:
            params['priority'] = priority

        response = self._request('GET', '/tasks', params=params)
        return response.get('tasks', [])

    def track_event(
        self,
        contact_id: str,
        event_name: str,
        properties: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        イベント追跡

        Args:
            contact_id：連絡先ID
            event_name：イベント名
            properties: イベント属性

        Returns:
            イベント追跡結果
        """
        data = {
            'contactId': contact_id,
            'eventName': event_name
        }

        if properties:
            data['properties'] = properties

        return self._request('POST', '/events/track', data=data)

    def get_contact_events(
        self,
        contact_id: str,
        event_type: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        連絡先イベント履歴の照会

        Args:
            contact_id：連絡先ID
            event_type：イベントタイプフィルタ
            limit: 返す項目の数
            offset: オフセット

        Returns:
            イベント一覧
        """
        params = {'limit': limit, 'offset': offset}
        if event_type:
            params['eventType'] = event_type

        response = self._request('GET', f'/contacts/{contact_id}/events', params=params)
        return response.get('events', [])

    def close(self):
        """セッション終了"""
        self.session.close()