# Delighted API Client

Delighted用Pyt​​honクライアント - 顧客満足度調査とフィードバック管理

## インストール

```bash
pip install -r requirements.txt
```

## API Keyを取得

1. [Delighted アカウントの作成](https://delighted.com/)
2. ログイン後の Settings > API Keys アクセス
3. プロジェクトごとにAPIキーを生成する
5. API キーのコピー

##使用法

### クライアントの初期化

```python
from delighted_client import create_delighted_client

client = create_delighted_client(api_key='your-api-key')
```

### NPSメトリック照会

```python
metrics = client.get_metrics(
    since='2024-01-01',  # 선택: 시작 날짜
    until='2024-12-31',  # 선택: 종료 날짜
    trend='30d'  # 선택: 트렌드 기간
)

print(f"NPS Score: {metrics['nps']}")
print(f"Total Responses: {metrics['total_responses']}")
```

###人の作成

```python
person = client.create_person(
    email='customer@example.com',
    name='John Doe',
    properties={'plan': 'premium', 'signup_date': '2024-01-15'},
    locale='en',  # 언어 설정
    send=True  # 즉시 설문조사 전송
)

print(f"Created person with ID: {person.get('id')}")
```

### 人の更新

```python
client.update_person(
    person_id='person-123',
    updates={
        'name': 'Jane Doe',
        'properties': {'plan': 'enterprise'}
    }
)
```

###人検索

```python
# 이메일로 검색
people = client.search_people(email='customer@example.com')
for person in people:
    print(f"{person['email']}: {person['name']}")
```

### アンケート回答の検索

```python
responses = client.search_survey_responses(
    per_page=20,
    since='2024-01-01',
    min_score=7,  # 점수 7 이상만
    max_score=10
)

for response in responses:
    print(f"Score: {response['score']}, Comment: {response.get('comment', 'N/A')}")
```

### 人の購読をキャンセル

```python
client.unsubscribe_people(email='customer@example.com')
# 또는
client.unsubscribe_people(person_id='person-123')
```

### 応答の追加(外部ソースから)

```python
client.add_survey_response(
    person_email='customer@example.com',
    score=9,
    comment='Great service!',
    properties={'source': 'phone'}
)
```

## Webhookハンドラ

Delightedで新しい応答または購読解除イベントを受信するには、Webフックサーバーを実行します。

```python
from delighted_client import DelightedWebhookHandler

# 핸들러 초기화
webhook = DelightedWebhookHandler(port=5000)

# 이벤트 핸들러 등록
@webhook.on_new_response
def handle_response(data):
    print(f"New response: {data}")

@webhook.on_new_unsubscribe
def handle_unsubscribe(data):
    print(f"Unsubscribe: {data}")

# 서버 시작
webhook.run(host='0.0.0.0')

# 또는 백그라운드에서 실행하려면:
import time
thread = webhook.run(host='0.0.0.0', debug=False)
# 메인 스레드 유지
while True:
    time.sleep(1)
```

DelightedダッシュボードでWebフックURLを設定します。
`https://your-server.com/webhook`

##主な機能

1. **NPSメトリック**：ネットプロモータースコアの計算
2. **人の管理**: 作成、更新、検索
3. **アンケートの回答**: 回答の照会とフィルタリング
4. **サブスクリプション管理**：サブスクリプションキャンセル処理
5. **ウェブフック**: リアルタイムイベント受信

## エラー処理

```python
from delighted_client import DelightedError, RateLimitError

try:
    metrics = client.get_metrics()
except RateLimitError as e:
    print(f"Rate limit exceeded. Retry after: {e}")
except DelightedError as e:
    print(f"API error: {e}")
```

## APIの制限

- 基本制限：1秒あたり10リクエスト
- Rate limitを超えると429応答
- 無料プラン：月250アンケート回答

## サポート

詳細なAPIドキュメント：[Delighted API Documentation]（https://delighted.com/docs/api)