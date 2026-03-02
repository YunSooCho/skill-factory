#Plumsail Documents APIクライアント

Plumsail Documents用のPython APIクライアント。

## 概要

このクライアントはPlumsail Documents APIにアクセスし、さまざまなCRUD操作とイベント処理をサポートします。

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

1. Plumsail Documents開発者ポータルでアプリを作成する
2. APIキー/トークン発行
3. 発行された API キー/トークンの保存

##使用法

### 初期化

```python
from plumsail_documents.client import PlumsailDocumentsClient

client = PlumsailDocumentsClient(
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

- `__init__` - Initialize Plumsail Documents client. Args: api_key: Plumsail API key

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