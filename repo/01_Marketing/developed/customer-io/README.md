# Customer.io API Client

Customer.io用Pythonクライアント - 顧客エンゲージメントと自動化プラットフォーム

## インストール

```bash
pip install -r requirements.txt
```

## API Credentialsを取得

1. [Customer.io アカウントの作成](https://customer.io/)
2. ログイン後の Settings > Integrations > API Credentials アクセス
3. Site IDとAPI Keyを取得
4.リージョンの確認（USまたはEU）

##使用法

### クライアントの初期化

```python
from customer_io_client import create_customerio_client

client = create_customerio_client(
    site_id='your-site-id',
    api_key='your-api-key',
    region='us'  # 'us' 또는 'eu'
)
```

### 顧客作成

```python
customer = client.create_customer(
    id='customer_123',
    email='user@example.com',
    name='John Doe',
    attributes={
        'plan': 'premium',
        'signup_date': '2024-01-15',
        'country': 'Japan'
    },
    created_at='1705276800'  # Unix timestamp (선택)
)

print(f"Customer ID: {customer.get('id')}")
```

###カスタマーアップデート

```python
client.update_customer(
    id='customer_123',
    email='new-email@example.com',
    attributes={'plan': 'enterprise', 'last_login': '2024-02-28'}
)
```

### 顧客の削除

```python
client.delete_customer(id='customer_123')
```

### 顧客イベントの追跡

```python
client.track_customer_event(
    customer_id='customer_123',
    name='purchase_completed',
    data={
        'amount': 99.99,
        'product': 'Premium Plan',
        'transaction_id': 'TXN-12345'
    },
    timestamp=1709164800  # Unix timestamp (선택)
)
```

### 匿名イベントの追跡

```python
client.track_anonymous_event(
    name='page_viewed',
    data={
        'page': '/pricing',
        'referrer': 'google.com',
        'duration': 45
    }
)
```

### 手動セグメントに顧客を追加

```python
client.add_customer_to_segment(
    customer_id='customer_123',
    segment_id=1
)
```

### 手動セグメントから顧客を削除する

```python
client.remove_customer_from_segment(
    customer_id='customer_123',
    segment_id=1
)
```

### 顧客リストの照会

```python
customers = client.list_customers(
    limit=50,
    start='customer_100',
    email='user@example.com'  # 선택: 이메일로 필터링
)

for customer in customers:
    print(f"{customer['email']}: {customer['name']}")
```

### 顧客活動履歴の照会

```python
activities = client.get_customer_activities(
    customer_id='customer_123',
    limit=20,
    type='email_click'  # email_actioned, email_opened, email_clicked, etc.
)

for activity in activities:
    print(f"{activity['type']}: {activity['timestamp']}")
```

###フォーム提出

```python
client.submit_form(
    form_id=1,
    customer_id='customer_123',
    data={
        'name': 'John Doe',
        'message': 'I love your product!',
        'rating': 5
    }
)
```

## Track API vs Management API

Customer.ioには2つのAPIがあります。

1. **Management API** (`/v1`): 顧客データの管理
2. **Track API** (`/track/v1`): イベントと匿名アクティビティの追跡

このクライアントは両方のAPIを自動的に処理します。

##リージョンの設定

- **USリージョン**：デフォルト、 `https://api.customer.io`と `https://track.customer.io`
- **EUリージョン**： `https://api-eu.customer.io`と `https://track-eu.customer.io`

```python
client = create_customerio_client(
    site_id='your-site-id',
    api_key='your-api-key',
    region='eu'  # EU 리전 사용
)
```

##主な機能

1. **顧客管理**: 作成、更新、削除、照会
2. **イベント追跡**：顧客と匿名イベント
3. **セグメント管理**: 手動セグメント操作
4. **活動履歴**: 顧客活動記録の照会
5. **フォーム提出**: Webフォームデータの収集

## エラー処理

```python
from customer_io_client import CustomerIOError, RateLimitError

try:
    customer = client.create_customer(
        id='customer_123',
        email='user@example.com'
    )
except RateLimitError as e:
    print(f"Rate limit exceeded. Retry: {e}")
except CustomerIOError as e:
    print(f"API error: {e}")
```

## APIの制限

- 基本制限：毎秒60リクエスト
- Rate limitを超えると `Retry-After`ヘッダを返す
- 無料プラン：月400のお客様
- 有料プラン：無制限

## ベストプラクティス

1. **Eメール必須**：Eメールは識別子として使用されます
2. **属性の正規化**: カスタム属性に underscore を使う (`last_login`)
3. **一貫したイベント名**：イベント名にsnake_caseを使用する
4. **Rate Limiting**: クライアントが自動処理するので心配なし

## サポート

詳細なAPIドキュメント：[Customer.io API Documentation]（https://customer.io/docs/api/)