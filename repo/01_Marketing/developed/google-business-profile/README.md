#Google Business Profile API クライアント

Google Business Profile用のPython APIクライアント。

## 概要

このクライアントは Google Business Profile API にアクセスし、ビジネス位置情報を管理します。

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

1. [Google Cloud Console]（https://console.cloud.google.com/)에서プロジェクトの作成
2. Google My Business API を有効にする
3. OAuth 2.0 または Service Account 認証トークンの発行
4. 発行された Access Token を保存

##使用法

### 初期化

```python
from google_business_profile.google_business_profile_client import GoogleBusinessProfileClient

client = GoogleBusinessProfileClient(
    access_token="YOUR_ACCESS_TOKEN",
    timeout=30
)
```

### サンプルコード

```python
# 계정의 모든 위치 조회
locations = client.get_locations(
    account_id="accounts/123456789",
    page_size=100
)
print("Locations:", locations)

# 특정 위치 상세 조회
location_detail = client.get_location(
    location_id="locations/987654321"
)
print("Location detail:", location_detail)
```

## APIアクション

- `get_locations` - アカウントのビジネスロケーションリストの検索
- `get_location` - 特定のビジネスロケーションの詳細検索

## エラー処理

```python
try:
    result = client.get_locations("accounts/123456789")
except Exception as e:
    print("Error:", str(e))
```

## Rate Limiting

APIリクエスト間の最小0.1秒遅延が適用されます。要求が多すぎると、Rate Limitエラーが発生する可能性があります。

##ライセンス

MIT License