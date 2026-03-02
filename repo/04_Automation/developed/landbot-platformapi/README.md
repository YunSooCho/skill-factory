#Landbot Platformapi APIクライアント

Landbot Platformapi用のPython APIクライアント。

## 概要

このクライアントはLandbot Platformapi APIにアクセスし、さまざまなCRUD操作とイベント処理をサポートします。

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

1. Landbot Platformapi開発者ポータルでアプリを作成する
2. APIキー/トークン発行
3. 発行された API キー/トークンの保存

##使用法

### 初期化

```python
from landbot_platformapi import Client

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

- `list_items` - アイテムリストの照会
- `get_item` - アイテムの詳細検索
- `create_item` - 新しいエントリの作成

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