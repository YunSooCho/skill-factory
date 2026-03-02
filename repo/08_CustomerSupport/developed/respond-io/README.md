# Respond.io SDK

Respond.ioはマルチチャンネルカスタマーサポートのためのPython SDKです。

## インストール

```bash
pip install -r requirements.txt
```

## API キーの発行方法

1. [Respond.io Webサイト]（https://respond.io)에にアクセスしてアカウントを作成します。
2. Settings > APIs & Webhooks メニューに移動します。
3. [Generate API Token]ボタンをクリックして新しいAPIキーを生成します。
4. 生成された API キーを安全な場所に保存します。

##使用法

### クライアントの初期化

```python
from respond_io import RespondIOClient

client = RespondIOClient(
    api_key="your_api_key_here",
    base_url="https://api.respond.io/v1"
)
```

### メッセージ送信

```python
message = client.create_message(
    channel_id="channel_123",
    text="안녕하세요! 무엇을 도와드릴까요?",
    customer_id="customer_456"
)

print(f"메시지 ID: {message['id']}")
```

### 会話の作成

```python
conversation = client.create_conversation(
    customer_id="customer_456",
    channel_id="channel_123",
    initial_message="제품 관련 문의입니다.",
    tags=["문의", "제품"]
)

print(f"대화 ID: {conversation['id']}")
```

### 会話リストの照会

```python
conversations = client.list_conversations(
    status="open",
    assigned_to="user_789",
    limit=20
)

for conv in conversations:
    print(f"{conv['id']}: {conv['status']} (할당: {conv['assignedTo']})")
```

###会話の更新

```python
updated = client.update_conversation(
    conversation_id="conv_123",
    status="closed",
    assigned_to="user_789"
)
```

### 会話終了

```python
result = client.close_conversation(conversation_id="conv_123")
print(f"대화 종료 완료: {result['success']}")
```

### 顧客作成

```python
customer = client.create_customer(
    external_id="user_999",
    name="김철수",
    email="cheolsu@example.com",
    phone="010-1234-5678",
    avatar_url="https://example.com/avatar.jpg",
    custom_attributes={
        "tier": "VIP",
        "signup_date": "2024-01-01"
    }
)

print(f"고객 ID: {customer['id']}")
```

### 顧客情報の更新

```python
updated = client.update_customer(
    customer_id="customer_456",
    name="김철수 (수정)",
    custom_attributes={
        "tier": "premium"
    }
)
```

###チャンネルリストの閲覧

```python
channels = client.list_channels()

for channel in channels:
    print(f"{channel['name']}: {channel['type']}")
```

### ユーザーリストの照会

```python
users = client.list_users()

for user in users:
    print(f"{user['name']}: {user['role']}")
```

### 会話担当者の指定

```python
result = client.assign_conversation(
    conversation_id="conv_123",
    user_id="user_789"
)

print(f"담당자 지정 완료: {result['success']}")
```

### ノートを追加

```python
note = client.add_note(
    conversation_id="conv_123",
    content고객이 제품 교환을 요청함 - 배송비는 우리가 부담하기로 확정",
    author_id="user_789"
)

print(f"노트 ID: {note['id']}")
```

### メッセージ履歴の照会

```python
messages = client.list_messages(
    conversation_id="conv_123",
    limit=50
)

for msg in messages:
    print(f"{msg['author']} ( {msg['createdAt']}): {msg['text']}")
```

###統計照会

```python
stats = client.get_statistics(
    start_date="2024-01-01",
    end_date="2024-01-31"
)

print(f"총 대화: {stats['totalConversations']}")
print(f"평균 응답 시간: {stats['avgResponseTime']}초")
print(f"해결된 대화: {stats['resolvedConversations']}")
```

## 機能

- ✅マルチチャンネルメッセージ管理
- ✅会話の作成、照会、更新、終了
- ✅顧客管理
- ✅担当者指定
- ✅ノートを追加
- ✅チャンネルとユーザー管理
- ✅統計と分析

## サポートチャンネル

- ウェブサイトライブチャット
- WhatsApp
- Facebook Messenger
- Telegram
- Email
- SMS
- Line
- Viber

##ライセンス

MIT License