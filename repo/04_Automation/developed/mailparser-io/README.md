#Mailparser.io APIクライアント

Mailparser.io用のPython APIクライアントです。

## 概要

このクライアントはMailparser.io APIにアクセスし、電子メール解析とデータ抽出操作をサポートします。

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

1. [Mailparser.io]（https://www.mailparser.io/)에서アカウントの作成
2. API キー発行
3. 発行された API キーの保存

##使用法

### 初期化

```python
from mailparser_io import Client

client = Client(
    api_key="YOUR_API_KEY",
    timeout=30
)
```

### サンプルコード

```python
# 이메일 파싱
try:
    result = client.parse_email(email_data)
    print("Parsed email:", result)
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