# Superchat SDK

SuperchatはライブチャットとカスタマーサポートサービスのためのPython SDKです。

## インストール

```bash
pip install -r requirements.txt
```

## API キーの発行方法

1. [Superchatウェブサイト]（https://superchat.com)에にアクセスしてアカウントを作成します。
2. ダッシュボードで、Settings > API Keys メニューに移動します。
3. [Generate API Key]ボタンをクリックして新しいAPIキーを生成します。
4. 生成された API キーと Account ID を安全な場所に保存します。

##使用法

### クライアントの初期化

```python
from superchat import SuperchatClient

client = SuperchatClient(
    api_key="your_api_key_here",
    account_id="your_account_id",
    base_url="https://api.superchat.com/v1"
)
```

###チャット開始

```python
chat = client.start_chat(
    customer_name="김철수",
    customer_email="cheolsu@example.com",
    initial_message="안녕하세요, 상품 문의가 있습니다.",
    channel="web",
    metadata={
        "page": "/products",
        "referrer": "google.com"
    }
)

print(f"채팅 ID: {chat['id']}")
```

### メッセージ送信

```python
message = client.send_message(
    chat_id="chat_123",
    message안녕하세요! 어떤 상품에 대해 문의하시나요?",
    sender_type="agent",
    message_type="text"
)

print(f"메시지 ID: {message['id']}")
```

### メッセージ履歴の照会

```python
messages = client.get_messages(
    chat_id="chat_123",
    limit=50
)

for msg in messages:
    print(f"{msg['senderType']} ({msg['createdAt']}): {msg['message']}")
```

###チャットリストの閲覧

```python
chats = client.list_chats(
    status="active",
    assigned_to="agent_456",
    limit=20
)

for chat in chats:
    print(f"{chat['id']}: {chat['customerName']} - {chat['status']}")
```

###チャットの更新

```python
updated = client.update_chat(
    chat_id="chat_123",
    status="closed",
    tags=["해결완료", "제품문의"]
)
```

###チャット終了

```python
result = client.close_chat(chat_id="chat_123")
print(f"채팅 종료: {result['success']}")
```

###チャット担当者の指定

```python
result = client.assign_chat(
    chat_id="chat_123",
    agent_id="agent_456"
)

print(f"담당자 지정: {result['success']}")
```

### 顧客作成

```python
customer = client.create_customer(
    name="이영희",
    email="younghee@example.com",
    phone="010-9876-5432",
    company="XYZ Corp",
    custom_attributes={
        "tier": "VIP",
        "signup_date": "2024-01-15"
    }
)

print(f"고객 ID: {customer['id']}")
```

### 顧客情報の更新

```python
updated = client.update_customer(
    customer_id="customer_789",
    name="이영희 (수정)",
    custom_attributes={
        "tier": "premium"
    }
)
```

### AIチャットボットの作成

```python
bot = client.create_bot(
    name="고객지원 어시스턴트",
    welcome_message="안녕하세요! 무엇을 도와드릴까요?",
    handoff_message="잡시만 기다려 주시면 상담원이 연결됩니다.",
    ai_provider="openai",
    ai_model="gpt-4o-mini",
    knowledge_base="kb_123",
    is_active=True
)

print(f"봇 ID: {bot['id']}")
```

### ボットリストの照会

```python
bots = client.list_bots()

for bot in bots:
    print(f"{bot['name']} ({bot['aiModel']}) - {bot['status']}")
```

###ボットアップデート

```python
updated = client.update_bot(
    bot_id="bot_456",
    welcome_message="반갑습니다! 무엇을 도와드릴까요?",
    is_active=True
)
```

###テンプレート応答の生成

```python
canned = client.create_canned_response(
    title="영업시간 안내",
    content="저희 영업시간은 평일 09:00~18:00입니다. 문의하신 내용은 영업시간 내에 답변드리겠습니다.",
    shortcuts=["영업시간", "운영시간"],
    category="공통"
)

print(f"템플릿 ID: {canned['id']}")
```

###テンプレート応答リストの検索

```python
responses = client.list_canned_responses(
    category="공통",
    limit=20
)

for resp in responses:
    print(f"{resp['title']}: {resp['content']}")
```

### エージェントリストの照会

```python
agents = client.list_agents()

for agent in agents:
    print(f"{agent['name']} - {agent['status']} ({agent['role']})")
```

### 分析データの照会

```python
analytics = client.get_analytics(
    start_date="2024-01-01",
    end_date="2024-01-31",
    metric="all"
)

print(f"총 채팅: {analytics['totalChats']}")
print(f"총 메시지: {analytics['totalMessages']}")
print(f"평균 응답 시간: {analytics['avgResponseTime']}초")
print(f"고객 만족도: {analytics['satisfactionScore']}")
```

##チャットステータス

- **active**: アクティブ
- **closed**: 終了
- **archived**: アーカイブ

## 発信者タイプ

- **agent**: エージェント
- **customer**: 顧客
- **bot**: ボット
- **system**: システム

## メッセージタイプ

- **text**: テキスト
- **image**: イメージ
- **video**: ビデオ
- **file**: ファイル
- **location**: 場所

## 機能

- ✅ライブチャット管理
- ✅メッセージの送信と照会
- ✅顧客管理
- ✅ AIチャットボット統合
- ✅テンプレート応答
- ✅エージェント管理
- ✅担当者指定
- ✅分析とレポート

## サポートチャンネル

- ウェブサイトライブチャット
- WhatsApp
- Facebook Messenger
- Telegram
- Line
- SMS

##ライセンス

MIT License