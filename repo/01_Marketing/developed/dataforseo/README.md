# DataForSEO API Client

DataForSEO用Pythonクライアント - SEOデータと分析

## インストール

```bash
pip install -r requirements.txt
```

## API Credentialsを取得

1. [DataForSEOアカウントの作成]（https://dataforseo.com/)
2. DashboardでAPI LoginとAPI Passwordを取得
3. Settings > API API Credentials アクセス
4. LoginとPasswordのコピー

##使用法

### クライアントの初期化

```python
from dataforseo_client import create_dataforseo_client

client = create_dataforseo_client(
    api_login='your-api-login',
    api_password='your-api-password'
)
```

###検索量と競合データの検索

```python
result = client.get_search_volume(
    keywords=['python programming', 'machine learning', 'data science'],
    location_code=2840,  # Global (default)
    language_code='en'
)

for item in result['tasks'][0]['result']:
    kw = item['keyword']
    volume = item['search_volume']
    cpc = item['cpc']
    competition = item['competition']

    print(f"{kw}: Volume={volume}, CPC=${cpc:.2f}, Competition={competition:.2f}")
```

### SERPデータ検索

```python
serp = client.get_serp_data(
    keyword='python tutorial',
    location_code=2840,
    language_code='en',
    search_engine='google',
    depth=10
)

for result in serp['tasks'][0]['result'][0]['items']:
    print(f"{result['title']}: {result.get('url', 'N/A')}")
```

###ドメインランクの概要

```python
rank = client.get_domain_rank_overview(
    target='example.com',
    language_code='en'
)

domain_auth = rank['tasks'][0]['result'][0]['domain_authority']
page_auth = rank['tasks'][0]['result'][0]['page_authority']

print(f"DA: {domain_auth}, PA: {page_auth}")
```

### バックリンクデータの照会

```python
backlinks = client.get_backlink_data(
    target='example.com',
    limit=100,
    filters=[
        ["dofollow", "=", True],  # Dofollow 링크만
        ["type", "in", ["link", "redirect"]]
    ]
)

for bl in backlinks['tasks'][0]['result'][0]['backlinks']:
    print(f"{bl['domain_from']} -> PA={bl['page_authority']}")
```

### バックリンクサマリー

```python
summary = client.get_backlink_summary(target='example.com')

total = summary['tasks'][0]['result'][0]['total']
dofollow = summary['tasks'][0]['result'][0]['dofollow']

print(f"Total: {total}, Dofollow: {dofollow}")
```

###ビジネスリストの検索（Google Maps、etc.）

```python
businesses = client.search_business_listings(
    query='restaurants',
    location_name='New York',
    depth=10
)

for item in businesses['tasks'][0]['result'][0]['items']:
    print(f"{item['title']}")
    print(f"  Rating: {item.get('rating', 'N/A')}")
    print(f"  Phone: {item.get('phone', 'N/A')}")
    print(f"  Address: {item.get('address', 'N/A')}")
```

## 場所と言語コード

DataForSEOは標準の場所と言語コードを使用します。

- **Location Code**: [DataForSEO Location Codes](https://docs.dataforseo.com/v3/serp/google/locations/)
  - 2840: Global
  - 2840: USA
  - 2840: UK
  - 2840: Japan

- **Language Code**: ISO 639-1 (en, ja, ko, de, fr, etc.)

##主な機能

1. **検索量データ**: キーワード検索量、クリック単価、競争度
2. **SERPデータ**: 検索結果ページの分析
3. **ドメインランク**: DA、PA、バックリンク情報
4. **バックリンク分析**: バックリンクの要約と詳細
5. **ビジネスリスト**：Google Mapsビジネスデータ

## エラー処理

```python
from dataforseo_client import DataForSEOError, RateLimitError

try:
    result = client.get_search_volume(['python'])
except RateLimitError as e:
    print(f"Rate limit exceeded: {e}")
except DataForSEOError as e:
    print(f"API error: {e}")
```

## APIの制限

- 基本制限：毎秒50リクエスト
- 無料試用版：データ検索無料
- 有料プラン：従量制（API使用量ベース）

## 非同期操作

一部の操作は非同期として扱われます。ジョブIDを使用して結果を照会する：

```python
# 작업 제출
task_id = "your-task-id"

# 결과 조회
result = client.get_task_result(task_id)
```

## サポート

詳細なAPIドキュメント：[DataForSEO API Documentation]（https://docs.dataforseo.com/v3/)