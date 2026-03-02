# Cuttly API Client

Cuenote SMS用Pythonクライアント - URL短縮と分析API

## インストール

```bash
pip install -r requirements.txt
```

## API Keyを取得

1. [Cuttly アカウントの作成](https://cutt.ly/)
2. ログイン後のダッシュボードへのアクセス
3. Settings > API Keys メニューから API キーを生成
4. API キーのコピー

##使用法

###デフォルトクライアントの初期化

```python
from cuttly_client import create_cuttly_client

# API 키로 클라이언트 생성
client = create_cuttly_client(api_key='your-api-key')
```

### URLの短縮

```python
result = client.shorten_url(
    url='https://example.com/very-long-url',
    name='my-custom-link',  # 선택: 사용자 정의 이름
    tags=['marketing', 'social'],  # 선택: 태그
    public=False  # 선택: 공개 여부
)

short_link = result['url']['shortLink']
print(f"Short URL: {short_link}")
```

### 分析データの照会

```python
analytics = client.get_analytics(
    url='https://cutt.ly/my-custom-link',
    limit=100,  # 선택: 최대 결과 수
    date_from='2024-01-01',  # 선택: 시작 날짜
    date_to='2024-12-31'  # 선택: 종료 날짜
)

print(f"Total clicks: {analytics['url']['clicks']}")
```

##主な機能

1. **URLの短縮**: 長いURLを短いリンクに変換
2. **分析データ**: クリック数、リファラー、位置などの照会
3. **カスタム名**: 希望する短いURLを指定可能
4. **タグのサポート**: リンクをタグに分類

## エラー処理

```python
from cuttly_client import CuttlyError, RateLimitError

try:
    result = client.shorten_url('https://example.com')
except RateLimitError as e:
    print(f"Rate limit exceeded: {e}")
except CuttlyError as e:
    print(f"API error: {e}")
```

## APIの制限

- 基本制限：1秒あたり10リクエスト
- 無料プラン：月1,000短縮
- Rate limitを超えると429エラーを返す

## サポート

詳細なAPIドキュメント：[Cuttly API Documentation]（https://cutt.ly/api-documentation)