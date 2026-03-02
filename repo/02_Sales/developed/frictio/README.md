#Frictio APIクライアント

Frictio用のPython APIクライアント。

## 概要

このクライアントはFrictio APIにアクセスし、さまざまなCRUD操作とイベント処理をサポートします。

## インストール

依存パッケージ：

```bash
pip install requests
```

または：

```bash
pip install -r requirements.txt
```

## API キー発行

1. Frictio開発者ポータルでアプリを作成する
2. APIキー/トークン発行
3. 発行された API キー/トークンの保存

##使用法

### 初期化

```python
from frictio.client import FrictioClient

client = FrictioClient(
    api_key="YOUR_API_KEY",
    timeout=30
)
```

### サンプルコード

```python
# CRUD 작업
try:
    result = client.create_item({"name": "test"})
    print("Created:", result)
except Exception as e:
    print("Error:", str(e))

# 리스트 조회
items = client.list_items()
for item in items:
    print(item['id'], item['name'])
```

## APIアクション

- `__init__` - Initialize Frictio webhook client Args: webhook_secret: Secret key for webhook s...
- `register_event_handler` - Register a handler for a specific event type Args: event_type: Event type to han...
- `unregister_event_handler` - Unregister an event handler
- `on_meeting_ended` - Register handler for meeting ended events Event data structure example: { "event...
- `on_playbook_result_updated` - Register handler for playbook result updated events Event data structure example...
- `on_playbook_generated` - Register handler for playbook generated events Event data structure example: { "...

## Webhookトリガー

- **Register Event Handler** - Register a handler for a specific event type Args: event_typ...
- **Unregister Event Handler** - Unregister an event handler

## エラー処理

```python
try:
    result = client.your_method()
except Exception as e:
    print("Error:", str(e))
```

## Rate Limiting

APIリクエスト間の最小0.1秒遅延が適用されます。要求が多すぎると、Rate Limitエラーが発生する可能性があります。

##ライセンス

MIT License