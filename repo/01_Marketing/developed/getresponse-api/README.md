#Getresponse Api APIクライアント

Getresponse Api用のPython APIクライアント。

## 概要

このクライアントはGetresponse Api APIにアクセスし、さまざまなCRUD操作とイベント処理をサポートします。

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

1. Getresponse Api開発者ポータルでアプリを作成する
2. APIキー/トークン発行
3. 発行された API キー/トークンの保存

##使用法

### 初期化

```python
from getresponse_api import Client

client = Client(
    api_key="YOUR_API_KEY",
    timeout=30
)
```

### サンプルコード

```python
# CRUD 작업
try:
    result = client.list_items()
    print("Items:", result)
except Exception as e:
    print("Error:", str(e))
```

## APIアクション

- `register_handler` - Register webhook handler.
- `from_dict` - API method
- `close` - API method
- `close` - Close the session.

## Webhookトリガー

- **Webhook** - このサービスはWebhookトリガーをサポートします
- **Getresponseapitrigger** - トリガー

## エラー処理

```python
try:
    result = client.your_method()
except Exception as e:
    print("Error:", str(e))
```

## Rate Limiting

APIリクエスト間の最小0.1秒遅延が適用されます。

##ライセンス

MIT License