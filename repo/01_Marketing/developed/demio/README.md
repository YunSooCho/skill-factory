# Demio API Client

Demio用Pythonクライアント - ウェビナープラットフォームの自動化

## インストール

```bash
pip install -r requirements.txt
```

## API Credentialsを取得

1. [Demio アカウントの作成](https://demio.com/)
2. ログイン後の Settings > Integrations > API アクセス
3. API KeyとAPI Secretの生成
4. 資格情報のコピー

##使用法

### クライアントの初期化

```python
from demio_client import DemioClient

client = DemioClient(
    api_key='your-api-key',
    api_secret='your-api-secret'
)
```

### イベントリストの照会

```python
events = client.list_events(
    status='scheduled',  # scheduled, completed, active, cancelled
    limit=10
)

for event in events['events']:
    print(f"{event['name']}: {event['start_date']}")
```

### イベント詳細検索

```python
event = client.get_event(event_id=12345)
print(f"Event: {event['name']}")
print(f"Status: {event['status']}")
print(f"Duration: {event['duration']} minutes")
```

### イベント参加者リスト

```python
participants = client.list_event_participants(
    event_id=12345,
    limit=20
)

for p in participants['participants']:
    print(f"{p['name']} ({p['email']}): Attended {p['is_attended']}")
```

### イベント登録者リスト

```python
registrants = client.get_event_registrants(event_id=12345)

for r in registrants['registrants']:
    print(f"{r['email']}: {r['join_link']}")
```

###参加者登録

```python
result = client.register_event_participant(
    event_id=12345,
    email='new@example.com',
    name='New Participant',
    first_name='New',
    last_name='Participant',
    custom_fields={'company': 'Acme Corp'}
)

print(f"Join link: {result['join_link']}")
print(f"UUID: {result['uuid']}")
```

###登録解除

```python
client.cancel_registration(
    event_id=12345,
    email='new@example.com'
)
```

### 今後のイベント検索

```python
upcoming = client.get_upcoming_events(limit=5)
```

### 完了したイベントの検索

```python
completed = client.get_completed_events(limit=10)
```

##主な機能

1. **イベント管理**: ウェビナーイベントの照会
2. **参加者管理**: 登録、参加照会
3. **自動化**: ウェビナー登録の自動化
4. **分析**: 参加者データの抽出

## エラー処理

```python
from demio_client import DemioError, RateLimitError

try:
    event = client.get_event(12345)
except RateLimitError as e:
    print(f"Rate limit exceeded: {e}")
except DemioError as e:
    print(f"API error: {e}")
```

## APIの制限

- 基本制限：1秒あたり10リクエスト
- 無料プラン：月50参加者
- 有料プラン：無制限

## サポート

詳細なAPIドキュメント：[Demio API Documentation]（https://demio.com/docs/developers/)