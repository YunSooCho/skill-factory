# Dash API Client

Dash DAM (Digital Asset Management) 用 Python クライアント

## インストール

```bash
pip install -r requirements.txt
```

## API Keyを取得

1. [Dashアカウントの作成]（https://www.dashhq.com/)
2. Workspace設定でAPIキーを生成する
3. ログイン後の Settings > API & Integrations アクセス
4. Generate API Key ボタンをクリック
5. API キーのコピー

##使用法

### クライアントの初期化

```python
from dash_client import DashClient

client = DashClient(api_key='your-api-key')
```

### アセット検索

```python
result = client.search_assets(
    query='logo',  # 검색 쿼리
    tags=['branding'],
    asset_type='image',  # image, video, document, audio
    limit=10
)

for asset in result['assets']:
    print(f"{asset['name']}: {asset['url']}")
```

### アセットをアップロード

```python
result = client.upload_asset(
    file_path='/path/to/image.png',
    name='Branding Logo',
    folder_id='folder-123',  # 선택
    tags=['logo', 'brand'],
    metadata={'campaign': 'spring-2024'}
)

asset_id = result['id']
print(f"Uploaded asset with ID: {asset_id}")
```

### アセット詳細検索

```python
asset = client.get_asset(asset_id='asset-123')
print(f"Name: {asset['name']}")
print(f"Type: {asset['type']}")
print(f"Size: {asset['size']} bytes")
```

### アセットのダウンロード

```python
# 파일 경로로 저장
saved_path = client.download_asset(
    asset_id='asset-123',
    output_path='/tmp/logo.png'
)
print(f"Saved to: {saved_path}")

# 바이너리로 직접 받기
binary_data = client.download_asset(asset_id='asset-123')
```

### Signed URLを取得

```python
signed_url = client.get_asset_file_url(
    asset_id='asset-123',
    expires_in=3600  # 1시간 유효
)
print(f"Signed URL: {signed_url}")
```

### アセットの更新

```python
client.update_asset(
    asset_id='asset-123',
    name='New Name',
    tags=['updated', 'new-tag'],
    metadata={'status': 'approved'}
)
```

### アセットの削除

```python
result = client.delete_asset(asset_id='asset-123')
print(f"Deleted: {result['success']}")
```

##主な機能

1. **アセット検索**: 名前、タグ、タイプ、日付で検索
2. **アセットアップロード**: ローカルファイルサーバーにアップロード
3. **アセットのダウンロード**: サーバーからローカルにダウンロード
4. **Signed URL**: 安全に共有可能な URL を作成
5. **メタデータ管理**: カスタム属性の保存

## エラー処理

```python
from dash_client import DashError, RateLimitError

try:
    asset = client.get_asset('asset-123')
except RateLimitError as e:
    print(f"Rate limit exceeded: {e}")
except DashError as e:
    print(f"API error: {e}")
```

## APIの制限

- 基本制限：毎秒20リクエスト
- 無料プラン：10GBストレージ
- 有料プラン：無制限のアップロード

## サポート

詳細なAPIドキュメント：[Dash Documentation]（https://www.dashhq.com/developers/)