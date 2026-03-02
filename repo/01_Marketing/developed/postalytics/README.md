# Postalytics API クライアント

Postalytics用のPython APIクライアント。

## 概要

このクライアントは Postalytics API にアクセスし、さまざまな CRUD 操作とイベント処理をサポートします。

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

1. Postalytics開発者ポータルでアプリを作成する
2. APIキー/トークン発行
3. 発行された API キー/トークンの保存

##使用法

### 初期化

```python
from postalytics.client import PostalyticsClient

client = PostalyticsClient(
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

- `__init__` - Initialize # Postalytics API client Args: api_key: API key for authentication ba...
- `_wait_for_rate_limit` - Wait if necessary to respect rate limits

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