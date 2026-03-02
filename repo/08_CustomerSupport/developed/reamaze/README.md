# Reamaze SDK

Reamazeは、顧客関係管理およびサポートチケット管理のためのPython SDKです。

## インストール

```bash
pip install -r requirements.txt
```

## API キーの発行方法

1. [Reamaze Webサイト]（https://www.reamaze.com)에にアクセスしてアカウントを作成します。
2. Settings > API & Webhooks メニューに移動します。
3. [Generate API Key]ボタンをクリックして新しいAPIキーを生成します。
4. 生成された API キーとアカウントのブランド名を安全な場所に保存します。

##使用法

### クライアントの初期化

```python
from reamaze import ReamazeClient

client = ReamazeClient(
    api_key="your_api_key_here",
    account="your_brand_name",
    base_url="https://api.reamaze.com"
)
```

###会話（チケット）の作成

```python
conversation = client.create_conversation(
    subject="주문 관련 문의",
    message주문 번호 #12345의 배송 상태를 확인하고 싶습니다.",
    customer_email="customer@example.com",
    customer_name="홍길동",
    channel="email",
    tags=["주문", "배송"],
    user_assignee="support@example.com"
)

print(f"대화 ID: {conversation['conversation']['slug']}")
```

### 会話リストの照会

```python
conversations = client.list_conversations(
    status="open",
    channel="email",
    limit=20,
    page=1
)

for conv in conversations:
    print(f"{conv['slug']}: {conv['subject']} ({conv['status']})")
```

###会話の更新

```python
updated = client.update_conversation(
    conversation_id="conversation-slug",
    status="resolved",
    user_assignee="agent@example.com"
)
```

### メッセージの追加

```python
message = client.add_message(
    conversation_id="conversation-slug",
    body고객님, 배송이 도착했습니다. 확인 부탁드립니다.",
    internal=False
)

print(f"메시지 ID: {message['message']['id']}")
```

### 顧客作成

```python
customer = client.create_customer(
    email="newcustomer@example.com",
    name="김철수",
    phone="010-1234-5678",
    company="ABC Corp",
    location="서울",
    metadata={
        "tier": "gold",
        "signup_date": "2024-01-01"
    }
)

print(f"고객 ID: {customer['customer']['id']}")
```

### 顧客リストの照会

```python
customers = client.list_customers(
    search="ABC Corp",
    limit=50,
    page=1
)

for customer in customers:
    print(f"{customer['email']}: {customer['name']}")
```

###従業員リストの照会

```python
users = client.list_users()

for user in users:
    print(f"{user['name']}: {user['email']}")
```

###統計照会

```python
stats = client.get_statistics(
    start_date="2024-01-01",
    end_date="2024-01-31"
)

print(f"총 대화: {stats['totalConversations']}")
print(f"해결된 대화: {stats['resolvedConversations']}")
print(f"평균 응답 시간: {stats['avgResponseTime']}분")
```

### ヘルプ文書の生成

```python
article = client.create_article(
    title="주문 취소 방법",
    content="<h1>주문 취소 방법</h1><p>다음 단계를 따르세요...</p>",
    category_id="category_123",
    published=True
)

print(f"문서 ID: {article['article']['id']}")
```

###チャンネルリストの閲覧

```python
channels = client.list_channels()

for channel in channels:
    print(f"{channel['name']}: {channel['type']}")
```

## 機能

- ✅会話（チケット）管理
- ✅メッセージ管理
- ✅顧客管理
- ✅従業員管理
- ✅統計と分析
- ✅ヘルプ文書の管理
- ✅マルチチャンネルサポート（Eメール、チャット、ソーシャル）

##ライセンス

MIT License