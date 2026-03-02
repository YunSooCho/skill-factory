# Statuspage SDK

Statuspageは、サービス状態の監視とインシデント管理のためのPython SDKです。

## インストール

```bash
pip install -r requirements.txt
```

## API キーの発行方法

1. [Statuspage.ioウェブサイト]（https://statuspage.io)에にアクセスしてアカウントを作成します。
2.新しいステータスページを作成するか、既存のページの設定メニューに移動します。
3. API> API Tokensで新しいAPIトークンを作成します。
4.ページID（URLで確認可能）とAPIトークンを安全な場所に保存します。

##使用法

### クライアントの初期化

```python
from statuspage import StatuspageClient

client = StatuspageClient(
    api_key="your_api_key_here",
    page_id="your_page_id",
    base_url="https://api.statuspage.io/v1"
)
```

###ステータスページサマリーの検索

```python
summary = client.get_page_summary()

print(f"페이지 이름: {summary['name']}")
print(f"URL: {summary['url']}")
print(f"전체 상태: {summary['status_indicator']}")
```

### コンポーネントの作成

```python
component = client.create_component(
    name="API 서버",
    status="operational",
    description="메인 API 서비스",
    showcase=True
)

print(f"컴포넌트 ID: {component['id']}")
```

### コンポーネント状態の更新

```python
updated = client.update_component(
    component_id="component_123",
    status="degraded"
)
```

### コンポーネントリストの照会

```python
components = client.list_components()

for component in components:
    print(f"{component['name']}: {component['status']}")
```

### インシデントの生成

```python
incident = client.create_incident(
    name="API 서버 응답 지연",
    status="investigating",
    body="현재 API 서버의 응답 시간이 평소보다 느립니다. 원인을 조사 중입니다.",
    component_ids=["component_123"],
    components={"component_123": "degraded"},
    impact_override="major",
    deliver_notifications=True
)

print(f"인시던트 ID: {incident['id']}")
```

### インシデントの更新

```python
updated = client.update_incident(
    incident_id="incident_456",
    status="identified",
    body="데이터베이스 쿼리 성능 문제로 확인되었습니다."
)
```

### インシデントの解決

```python
updated = client.update_incident(
    incident_id="incident_456",
    status="resolved",
    body="인덱스 최적화를 완료하여 서비스가 정상화되었습니다.",
    components={"component_123": "operational"}
)
```

### インシデントリストの照会

```python
incidents = client.list_incidents(
    status="open",
    impact="major",
    limit=20
)

for incident in incidents:
    print(f"{incident['name']} - {incident['status']} ({incident['impact']})")
```

### インシデント更新の追加

```python
update = client.create_incident_update(
    incident_id="incident_456",
    body="문제가 해결되어 정상 상태로 복귀했습니다.",
    status="resolved"
)

print(f"업데이트 ID: {update['id']}")
```

### メンテナンスの作成

```python
maintenance = client.create_maintenance(
    name="데이터베이스 서버 업그레이드",
    scheduled_for="2024-02-15T02:00:00Z",
    scheduled_until="2024-02-15T04:00:00Z",
    status="scheduled",
    body="데이터베이스 서버 버전 업그레이드 예정입니다.",
    component_ids=["component_123"],
    components={"component_123": "under_maintenance"},
    auto_transition_to_in_progress=True,
    auto_transition_to_operational=True
)

print(f"메인테넌스 ID: {maintenance['id']}")
```

### メンテナンスリストの照会

```python
maintenances = client.list_maintenances(
    status="scheduled",
    limit=10
)

for maintenance in maintenances:
    print(f"{maintenance['name']}: {maintenance['scheduled_for']}")
```

### メンテナンスアップデート

```python
updated = client.update_maintenance(
    maintenance_id="maintenance_789",
    status="completed"
)
```

### 購読者リストの検索

```python
subscribers = client.get_subscribers(limit=50)

for sub in subscribers:
    print(f"{sub['email']} - {sub['mode']}")
```

## コンポーネントの状態

- **operational**: 正常
- **degraded**: パフォーマンスの低下
- **partial_outage**: 部分障害
- **major_outage**：主な障害
- **under_maintenance**: メンテナンス中

## インシデント状態

- **investigating**: 調査中
- **identified**: 原因の特定
- **monitoring**: 監視中
- **resolved**: 解決済み
- **postmortem**: 事後分析

##影響度

- **critical**: 致命的
- **major**: メイン
- **minor**: 些細
- **none**: なし

## 機能

- ✅コンポーネント管理（作成、照会、更新、削除）
- ✅インシデント管理
- ✅インシデントアップデートを追加
- ✅メンテナンスの予約と管理
- ✅ 加入者管理
- ✅ステータスページ要約照会

##ライセンス

MIT License