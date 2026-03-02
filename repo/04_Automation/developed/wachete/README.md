#Wachete APIクライアント

Wachete用のPython APIクライアントです。 Webページ監視機能を提供します。

## 概要

WacheteはWebページの変更を監視するサービスです。

## インストール

```bash
pip install requests
```

または：

```bash
pip install -r requirements.txt
```

## API キー発行

1. [Wachete]（https://wachete.com/)에서アカウントを作成
2. API キー発行
3. API キーを安全に保存

##使用法

### 初期化

```python
from wachete import WacheteClient, WacheteError

client = WacheteClient(
    api_key="YOUR_API_KEY",
    timeout=30
)
```

### Wachetの作成

```python
result = client.create_wachet(
    url="https://example.com",
    name="Monitor Homepage",
    check_interval=3600,
    email_notification=True
)
```

### Wachet ルックアップ

```python
wachet = client.get_wachet("wachet_id_here")
```

### Wachetを検索

```python
result = client.search_wachets(
    limit=20,
    status="active"
)

for wachet in result.get("wachets", []):
    print(f"- {wachet.get('name')}")
```

### Wachet アップデート

```python
result = client.update_wachet(
    wachet_id="wachet_id_here",
    check_interval=1800,
    name="Updated Name"
)
```

### Wachetを削除

```python
result = client.delete_wachet("wachet_id_here")
```

### 変更履歴の照会

```python
result = client.get_wachet_changes("wachet_id_here", limit=10)
```

## エラー処理

```python
try:
    result = client.create_wachet(url, name)
except WacheteAuthenticationError:
    print("API 키가 올바르지 않습니다")
except WacheteRateLimitError:
    print("속도 제한이 초과되었습니다")
except WacheteError as e:
    print(f"요청 실패: {str(e)}")
```

##ライセンス

MIT License

## サポート

- [Wachete公式サイト]（https://wachete.com/)
- [Wacheteドキュメント]（https://docs.wachete.com/)