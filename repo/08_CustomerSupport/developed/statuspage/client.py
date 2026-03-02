"""
Statuspage Client
サービス状態監視APIクライアント
"""

import requests
from typing import Optional, Dict, List, Any


class StatuspageClient:
    """
    Statuspage API クライアント

    サービス状態監視、インシデント管理、メンテナンス予約のためのクライアント
    """

    def __init__(
        self,
        api_key: str,
        page_id: str,
        base_url: str = "https://api.statuspage.io/v1",
        timeout: int = 30
    ):
        """
        Statuspage クライアントの初期化

        Args:
            api_key: Statuspage API キー
            page_id：ステータスページID
            base_url：APIベースURL
            timeout：リクエストタイムアウト（秒）
        """
        self.api_key = api_key
        self.page_id = page_id
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'OAuth {api_key}',
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

    def get_page_summary(self) -> Dict[str, Any]:
        """
        ステータスページの要約検索

        Returns:
            ページ概要情報
        """
        return self._request('GET', f'/pages/{self.page_id}')

    def list_components(
        self,
        page_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        コンポーネントリストの照会

        Args:
            page_id：ページID（選択 - デフォルトは初期化時に設定）

        Returns:
            コンポーネントリスト
        """
        pid = page_id if page_id else self.page_id
        response = self._request('GET', f'/pages/{pid}/components')
        return response.get('components', [])

    def create_component(
        self,
        name: str,
        status: str = "operational",
        description: Optional[str] = None,
        only_show_if_degraded: bool = False,
        showcase: bool = False,
        group_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        コンポーネントの作成

        Args:
            name: コンポーネント名
            status: 初期状態 (operational, degraded, partial_outage, major_outage, under_maintenance)
            description: 説明
            only_show_if_degraded：問題が発生した場合にのみ表示
            showcase: メインコンポーネントとして表示
            group_id：グループID

        Returns:
            生成されたコンポーネント情報
        """
        data = {
            'component': {
                'name': name,
                'status': status,
                'only_show_if_degraded': only_show_if_degraded,
                'showcase': showcase
            }
        }

        if description:
            data['component']['description'] = description
        if group_id:
            data['component']['group_id'] = group_id

        return self._request('POST', f'/pages/{self.page_id}/components', data=data)

    def get_component(self, component_id: str) -> Dict[str, Any]:
        """
        コンポーネントの照会

        Args:
            component_id: コンポーネントID

        Returns:
            コンポーネント情報
        """
        return self._request('GET', f'/pages/{self.page_id}/components/{component_id}')

    def update_component(
        self,
        component_id: str,
        status: Optional[str] = None,
        description: Optional[str] = None,
        only_show_if_degraded: Optional[bool] = None,
        showcase: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        コンポーネントの更新

        Args:
            component_id: コンポーネントID
            status: 新しい状態
            description: 新しい説明
            only_show_if_degraded: 表示オプション
            showcase: ショーケースオプション

        Returns:
            更新されたコンポーネント情報
        """
        data = {'component': {}}

        if status:
            data['component']['status'] = status
        if description:
            data['component']['description'] = description
        if only_show_if_degraded is not None:
            data['component']['only_show_if_degraded'] = only_show_if_degraded
        if showcase is not None:
            data['component']['showcase'] = showcase

        return self._request('PATCH', f'/pages/{self.page_id}/components/{component_id}', data=data)

    def delete_component(self, component_id: str) -> Dict[str, Any]:
        """
        コンポーネントの削除

        Args:
            component_id: コンポーネントID

        Returns:
            削除結果
        """
        return self._request('DELETE', f'/pages/{self.page_id}/components/{component_id}')

    def create_incident(
        self,
        name: str,
        status: str = "investigating",
        body: Optional[str] = None,
        incident_updates: Optional[List[Dict[str, Any]]] = None,
        component_ids: Optional[List[str]] = None,
        components: Optional[Dict[str, str]] = None,
        deliver_notifications: bool = True,
        impact_override: Optional[str] = None,
        scheduled_for: Optional[str] = None,
        auto_transition_to_maintenance: bool = False,
        auto_transition_to_operational: bool = False
    ) -> Dict[str, Any]:
        """
        インシデントの生成

        Args:
            name: インシデント名
            status: 状態 (investigating, identified, monitoring, resolved, scheduled, in_progress, verifying, completed)
            body：説明
            incident_updates：アップデートリスト
            component_ids：影響を受けるコンポーネントIDのリスト
            components: コンポーネント状態マップ {id: status}
            deliver_notifications: 通知を送信するかどうか
            impact_override: 影響度 (critical, major, minor, none)
            scheduled_for: 予約時間 (YYYY-MM-DDTHH:MM:SS)
            auto_transition_to_maintenance: メンテナンスに自動切り替え
            auto_transition_to_operational：定常状態に自動切り替え

        Returns:
            生成されたインシデント情報
        """
        data = {
            'incident': {
                'name': name,
                'status': status,
                'deliver_notifications': deliver_notifications
            }
        }

        if body:
            data['incident']['body'] = body
        if incident_updates:
            data['incident']['incident_updates'] = incident_updates
        if component_ids:
            data['incident']['component_ids'] = component_ids
        if components:
            data['incident']['components'] = components
        if impact_override:
            data['incident']['impact_override'] = impact_override
        if scheduled_for:
            data['incident']['scheduled_for'] = scheduled_for
        if auto_transition_to_maintenance:
            data['incident']['auto_transition_to_maintenance'] = auto_transition_to_maintenance
        if auto_transition_to_operational:
            data['incident']['auto_transition_to_operational'] = auto_transition_to_operational

        return self._request('POST', f'/pages/{self.page_id}/incidents', data=data)

    def get_incident(self, incident_id: str) -> Dict[str, Any]:
        """
        インシデント照会

        Args:
            incident_id：インシデントID

        Returns:
            インシデント情報
        """
        return self._request('GET', f'/pages/{self.page_id}/incidents/{incident_id}')

    def list_incidents(
        self,
        status: Optional[str] = None,
        impact: Optional[str] = None,
        limit: int = 50,
        page: int = 1
    ) -> List[Dict[str, Any]]:
        """
        インシデントリストの照会

        Args:
            status: ステータスフィルタ
            impact: 影響度フィルタ
            limit: 返す項目の数
            page: ページ番号

        Returns:
            インシデントリスト
        """
        params = {'limit': limit, 'page': page}
        if status:
            params['status'] = status
        if impact:
            params['impact'] = impact

        response = self._request('GET', f'/pages/{self.page_id}/incidents', params=params)
        return response.get('incidents', [])

    def update_incident(
        self,
        incident_id: str,
        status: Optional[str] = None,
        name: Optional[str] = None,
        body: Optional[str] = None,
        component_ids: Optional[List[str]] = None,
        components: Optional[Dict[str, str]] = None,
        deliver_notifications: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        インシデントの更新

        Args:
            incident_id：インシデントID
            status: 新しい状態
            name: 新しい名前
            body：新しい説明
            component_ids：影響を受けるコンポーネントIDのリスト
            components: コンポーネント状態マップ
            deliver_notifications: 通知を送信するかどうか

        Returns:
            更新されたインシデント情報
        """
        data = {'incident': {}}

        if status:
            data['incident']['status'] = status
        if name:
            data['incident']['name'] = name
        if body:
            data['incident']['body'] = body
        if component_ids:
            data['incident']['component_ids'] = component_ids
        if components:
            data['incident']['components'] = components
        if deliver_notifications is not None:
            data['incident']['deliver_notifications'] = deliver_notifications

        return self._request('PATCH', f'/pages/{self.page_id}/incidents/{incident_id}', data=data)

    def delete_incident(self, incident_id: str) -> Dict[str, Any]:
        """
        インシデントの削除

        Args:
            incident_id：インシデントID

        Returns:
            削除結果
        """
        return self._request('DELETE', f'/pages/{self.page_id}/incidents/{incident_id}')

    def create_incident_update(
        self,
        incident_id: str,
        body: str,
        status: Optional[str] = None,
        deliver_notifications: bool = True
    ) -> Dict[str, Any]:
        """
        インシデント更新の追加

        Args:
            incident_id：インシデントID
            body：アップデート内容
            status: 新しい状態
            deliver_notifications: 通知を送信するかどうか

        Returns:
            追加された更新情報
        """
        data = {
            'incident_update': {
                'body': body,
                'deliver_notifications': deliver_notifications
            }
        }

        if status:
            data['incident_update']['status'] = status

        return self._request('POST', f'/pages/{self.page_id}/incidents/{incident_id}/incident_updates', data=data)

    def list_incident_updates(
        self,
        incident_id: str
    ) -> List[Dict[str, Any]]:
        """
        インシデント更新リストの照会

        Args:
            incident_id：インシデントID

        Returns:
            アップデートリスト
        """
        response = self._request('GET', f'/pages/{self.page_id}/incidents/{incident_id}/incident_updates')
        return response.get('incident_updates', [])

    def create_maintenance(
        self,
        name: str,
        scheduled_for: str,
        scheduled_until: str,
        status: str = "scheduled",
        body: Optional[str] = None,
        component_ids: Optional[List[str]] = None,
        components: Optional[Dict[str, str]] = None,
        auto_transition_to_operational: bool = False,
        auto_transition_to_in_progress: bool = False
    ) -> Dict[str, Any]:
        """
        メンテナンスの作成

        Args:
            name: メンテナンス名
            scheduled_for: 開始時間 (YYYY-MM-DDTHH:MM:SS)
            scheduled_until: 終了時間 (YYYY-MM-DDTHH:MM:SS)
            status: 状態 (scheduled, in_progress, verifying, completed)
            body：説明
            component_ids：影響を受けるコンポーネントIDのリスト
            components: コンポーネント状態マップ
            auto_transition_to_operational：定常状態に自動切り替え
            auto_transition_to_in_progress：進行中の状態に自動切り替え

        Returns:
            生成されたメンテナンス情報
        """
        data = {
            'scheduled_maintenance': {
                'name': name,
                'scheduled_for': scheduled_for,
                'scheduled_until': scheduled_until,
                'status': status,
                'auto_transition_to_operational': auto_transition_to_operational,
                'auto_transition_to_in_progress': auto_transition_to_in_progress
            }
        }

        if body:
            data['scheduled_maintenance']['body'] = body
        if component_ids:
            data['scheduled_maintenance']['component_ids'] = component_ids
        if components:
            data['scheduled_maintenance']['components'] = components

        return self._request('POST', f'/pages/{self.page_id}/scheduled-maintenances', data=data)

    def list_maintenances(
        self,
        status: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        メンテナンスリストの照会

        Args:
            status: ステータスフィルタ
            limit: 返す項目の数

        Returns:
            メンテナンスリスト
        """
        params = {'limit': limit}
        if status:
            params['status'] = status

        response = self._request('GET', f'/pages/{self.page_id}/scheduled-maintenances', params=params)
        return response.get('scheduled_maintenances', [])

    def update_maintenance(
        self,
        maintenance_id: str,
        name: Optional[str] = None,
        status: Optional[str] = None,
        body: Optional[str] = None,
        scheduled_for: Optional[str] = None,
        scheduled_until: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        メンテナンスアップデート

        Args:
            maintenance_id：メンテナンスID
            name: 新しい名前
            status: 新しい状態
            body：新しい説明
            scheduled_for: 新しい開始時間
            scheduled_until: 新しい終了時間

        Returns:
            更新されたメンテナンス情報
        """
        data = {'scheduled_maintenance': {}}

        if name:
            data['scheduled_maintenance']['name'] = name
        if status:
            data['scheduled_maintenance']['status'] = status
        if body:
            data['scheduled_maintenance']['body'] = body
        if scheduled_for:
            data['scheduled_maintenance']['scheduled_for'] = scheduled_for
        if scheduled_until:
            data['scheduled_maintenance']['scheduled_until'] = scheduled_until

        return self._request('PATCH', f'/pages/{self.page_id}/scheduled-maintenances/{maintenance_id}', data=data)

    def delete_maintenance(self, maintenance_id: str) -> Dict[str, Any]:
        """
        メンテナンスの削除

        Args:
            maintenance_id：メンテナンスID

        Returns:
            削除結果
        """
        return self._request('DELETE', f'/pages/{self.page_id}/scheduled-maintenances/{maintenance_id}')

    def get_subscribers(
        self,
        limit: int = 50,
        page: int = 1
    ) -> List[Dict[str, Any]]:
        """
        購読者リストの閲覧

        Args:
            limit: 返す項目の数
            page: ページ番号

        Returns:
            加入者リスト
        """
        params = {'limit': limit, 'page': page}
        response = self._request('GET', f'/pages/{self.page_id}/subscribers', params=params)
        return response.get('subscribers', [])

    def close(self):
        """セッション終了"""
        self.session.close()