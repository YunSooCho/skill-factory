#Geniee Sfa APIクライアント

Geniee Sfa用のPython APIクライアント。

## 概要

このクライアントはGeniee Sfa APIにアクセスし、さまざまなCRUD操作とイベント処理をサポートします。

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

1. Geniee Sfa開発者ポータルでアプリを作成する
2. APIキー/トークン発行
3. 発行された API キー/トークンの保存

##使用法

### 初期化

```python
from geniee_sfa.client import GenieeSfaClient

client = GenieeSfaClient(
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

- `__init__` - Initialize Geniee SFA webhook client Args: webhook_secret: Secret key for webhoo...
- `register_event_handler` - Register a handler for a specific trigger type Args: trigger_type: Trigger type ...
- `unregister_event_handler` - Unregister an event handler
- `add_middleware` - Add middleware function to process event data before handlers Args: middleware: ...
- `on_prospect_created` - Register handler for prospect created events Event data example: { "trigger_type...
- `on_deal_created` - Register handler for deal created events Event data example: { "trigger_type": "...
- `on_prospect_created_updated` - Register handler for prospect created and updated events Event data includes bot...
- `on_deal_created_updated` - Register handler for deal created and updated events Event data includes both cr...
- `on_company_created` - Register handler for company created events Event data example: { "trigger_type"...
- `on_company_created_updated` - Register handler for company created and updated events Event data includes both...

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