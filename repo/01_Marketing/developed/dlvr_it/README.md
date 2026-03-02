#Dlvr It APIクライアント

Dlvr It用のPython APIクライアント。

## 概要

このクライアントはDlvr It APIにアクセスし、さまざまなCRUD操作とイベント処理をサポートします。

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

1. Dlvr It開発者ポータルでアプリを作成する
2. APIキー/トークン発行
3. 発行された API キー/トークンの保存

##使用法

### 初期化

```python
from dlvr_it import Client

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

- `close` - Close the session.

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