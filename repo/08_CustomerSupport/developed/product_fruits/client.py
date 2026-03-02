"""
Product Fruits Client
製品オンボーディングおよびユーザーガイドAPIクライアント
"""

import requests
from typing import Optional, Dict, List, Any


class ProductFruitsClient:
    """
    Product Fruits API クライアント

    製品オンボーディング、ユーザーガイド、ツアー、ツールチップ管理のためのクライアント
    """

    def __init__(
        self,
        api_key: str,
        workspace_id: str,
        base_url: str = "https://api.productfruits.com",
        timeout: int = 30
    ):
        """
        Product Fruits クライアントの初期化

        Args:
            api_key: Product Fruits API キー
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

    def create_tour(
        self,
        name: str,
        description: str,
        steps: List[Dict[str, Any]],
        target_url_pattern: str,
        trigger_type: str = "manual",
        is_active: bool = False
    ) -> Dict[str, Any]:
        """
        新しいツアーを作成

        Args:
            name: ツアー名
            description: ツアーの説明
            steps: ツアーステップ一覧
            target_url_pattern：ターゲットURLパターン
            trigger_type：トリガータイプ（manual、auto、onboarding）
            is_active: 有効かどうか

        Returns:
            生成されたツアー情報
        """
        data = {
            'name': name,
            'description': description,
            'steps': steps,
            'targetUrlPattern': target_url_pattern,
            'triggerType': trigger_type,
            'isActive': is_active
        }

        return self._request('POST', '/tours', data=data)

    def get_tour(self, tour_id: str) -> Dict[str, Any]:
        """
        ツアービュー

        Args:
            tour_id：ツアーID

        Returns:
            ツアー詳細
        """
        return self._request('GET', f'/tours/{tour_id}')

    def list_tours(
        self,
        is_active: Optional[bool] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        ツアーリストを見る

        Args:
            is_active: アクティブ状態フィルタ
            limit: 返す項目の数
            offset: オフセット

        Returns:
            ツアー一覧
        """
        params = {'limit': limit, 'offset': offset}
        if is_active is not None:
            params['isActive'] = is_active

        response = self._request('GET', '/tours', params=params)
        return response.get('tours', [])

    def update_tour(
        self,
        tour_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        steps: Optional[List[Dict[str, Any]]] = None,
        is_active: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        ツアーアップデート

        Args:
            tour_id：ツアーID
            name: 新しい名前
            description: 新しい説明
            steps: 新しいステップのリスト
            is_active: 有効かどうか

        Returns:
            更新されたツアー情報
        """
        data = {}
        if name:
            data['name'] = name
        if description:
            data['description'] = description
        if steps:
            data['steps'] = steps
        if is_active is not None:
            data['isActive'] = is_active

        return self._request('PUT', f'/tours/{tour_id}', data=data)

    def create_tooltip(
        self,
        name: str,
        selector: str,
        content: str,
        position: str = "top",
        trigger_type: str = "hover",
        is_active: bool = False
    ) -> Dict[str, Any]:
        """
        新しいツールチップの作成

        Args:
            name: ツールチップ名
            セレクタ：CSSセレクタ
            content: ツールチップの内容
            position: 位置 (top, right, bottom, left)
            trigger_type：トリガータイプ（hover、click）
            is_active: 有効かどうか

        Returns:
            生成されたツールチップ情報
        """
        data = {
            'name': name,
            'selector': selector,
            'content': content,
            'position': position,
            'triggerType': trigger_type,
            'isActive': is_active
        }

        return self._request('POST', '/tooltips', data=data)

    def get_tooltip(self, tooltip_id: str) -> Dict[str, Any]:
        """
        ツールチップの検索

        Args:
            tooltip_id：ツールチップID

        Returns:
            ツールチップの詳細
        """
        return self._request('GET', f'/tooltips/{tooltip_id}')

    def list_tooltips(
        self,
        is_active: Optional[bool] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        ツールチップリストの照会

        Args:
            is_active: アクティブ状態フィルタ
            limit: 返す項目の数
            offset: オフセット

        Returns:
            ツールチップリスト
        """
        params = {'limit': limit, 'offset': offset}
        if is_active is not None:
            params['isActive'] = is_active

        response = self._request('GET', '/tooltips', params=params)
        return response.get('tooltips', [])

    def update_tooltip(
        self,
        tooltip_id: str,
        name: Optional[str] = None,
        selector: Optional[str] = None,
        content: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        ツールチップの更新

        Args:
            tooltip_id：ツールチップID
            name: 新しい名前
            セレクタ：新しいCSSセレクタ
            content: 新しいコンテンツ
            is_active: 有効かどうか

        Returns:
            更新されたツールチップ情報
        """
        data = {}
        if name:
            data['name'] = name
        if selector:
            data['selector'] = selector
        if content:
            data['content'] = content
        if is_active is not None:
            data['isActive'] = is_active

        return self._request('PUT', f'/tooltips/{tooltip_id}', data=data)

    def create_checklist(
        self,
        name: str,
        description: str,
        items: List[Dict[str, Any]],
        target_url_pattern: str,
        is_active: bool = False
    ) -> Dict[str, Any]:
        """
        新しいチェックリストの作成

        Args:
            name: チェックリスト名
            description: チェックリストの説明
            items: チェックリスト項目リスト
            target_url_pattern：ターゲットURLパターン
            is_active: 有効かどうか

        Returns:
            生成されたチェックリスト情報
        """
        data = {
            'name': name,
            'description': description,
            'items': items,
            'targetUrlPattern': target_url_pattern,
            'isActive': is_active
        }

        return self._request('POST', '/checklists', data=data)

    def get_checklist(self, checklist_id: str) -> Dict[str, Any]:
        """
        チェックリストの照会

        Args:
            checklist_id: チェックリスト ID

        Returns:
            チェックリスト詳細
        """
        return self._request('GET', f'/checklists/{checklist_id}')

    def get_user_progress(
        self,
        user_id: str,
        checklist_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        ユーザーの進捗状況の表示

        Args:
            user_id：ユーザーID
            checklist_id：チェックリストID（オプション）

        Returns:
            進行状況情報
        """
        params = {'userId': user_id}
        if checklist_id:
            params['checklistId'] = checklist_id

        return self._request('GET', '/user-progress', params=params)

    def track_event(
        self,
        user_id: str,
        event_name: str,
        properties: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        ユーザーイベントの追跡

        Args:
            user_id：ユーザーID
            event_name：イベント名
            properties: イベント属性

        Returns:
            イベント追跡結果
        """
        data = {
            'userId': user_id,
            'eventName': event_name
        }

        if properties:
            data['properties'] = properties

        return self._request('POST', '/events/track', data=data)

    def create_announcement(
        self,
        name: str,
        content: str,
        target_url_pattern: str,
        display_type: str = "modal",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        is_active: bool = False
    ) -> Dict[str, Any]:
        """
        新しいお知らせの作成

        Args:
            name: お知らせ名
            content: お知らせ内容
            target_url_pattern：ターゲットURLパターン
            display_type：表示タイプ（modal、banner、tooltip）
            start_date：開始日（YYYY-MM-DD）
            end_date: 終了日 (YYYY-MM-DD)
            is_active: 有効かどうか

        Returns:
            生成されたお知らせ情報
        """
        data = {
            'name': name,
            'content': content,
            'targetUrlPattern': target_url_pattern,
            'displayType': display_type,
            'isActive': is_active
        }

        if start_date:
            data['startDate'] = start_date
        if end_date:
            data['endDate'] = end_date

        return self._request('POST', '/announcements', data=data)

    def get_announcements(
        self,
        is_active: Optional[bool] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        お知らせリストの照会

        Args:
            is_active: アクティブ状態フィルタ
            limit: 返す項目の数
            offset: オフセット

        Returns:
            お知らせ一覧
        """
        params = {'limit': limit, 'offset': offset}
        if is_active is not None:
            params['isActive'] = is_active

        response = self._request('GET', '/announcements', params=params)
        return response.get('announcements', [])

    def get_analytics(
        self,
        start_date: str,
        end_date: str,
        content_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        分析データの照会

        Args:
            start_date：開始日（YYYY-MM-DD）
            end_date: 終了日 (YYYY-MM-DD)
            content_type：コンテンツタイプフィルタ（tour、tooltip、checklist）

        Returns:
            分析データ
        """
        params = {
            'startDate': start_date,
            'endDate': end_date
        }
        if content_type:
            params['contentType'] = content_type

        return self._request('GET', '/analytics', params=params)

    def close(self):
        """セッション終了"""
        self.session.close()