# Sleekflow SDK

Sleekflowはチャットとカスタマーサポートのワークフロー管理のためのPython SDKです。

## インストール

```bash
pip install -r requirements.txt
```

## API キーの発行方法

1. [Sleekflowウェブサイト]（https://sleekflow.io)에にアクセスしてアカウントを作成します。
2. ダッシュボードで、Settings > API Keys メニューに移動します。
3. [Create API Key]ボタンをクリックして新しいAPIキーを生成します。
4.生成されたAPIキーとWorkspace IDを安全な場所に保存します。

##使用法

### クライアントの初期化

```python
from sleekflow import SleekflowClient

client = SleekflowClient(
    api_key="your_api_key_here",
    workspace_id="your_workspace_id",
    base_url="https://api.sleekflow.io/v1"
)
```

###チャットセッションの作成

```python
session = client.create_chat_session(
    customer_id="customer_123",
    channel="web",
    metadata={
        "source": "homepage",
        "referrer": "google.com"
    }
)

print(f"세션 ID: {session['id']}")
```

### メッセージ送信

```python
message = client.send_message(
    session_id="session_123",
    text="안녕하세요! 무엇을 도와드릴까요?",
    sender_type="agent",
    message_type="text"
)

print(f"메시지 ID: {message['id']}")
```

### メッセージ履歴の照会

```python
messages = client.get_messages(
    session_id="session_123",
    limit=50
)

for msg in messages:
    print(f"{msg['senderType']}: {msg['text']}")
```

### ワークフローの作成

```python
workflow = client.create_workflow(
    name="신규 고객 온보딩",
    description="신규 가입 고객에게 환영 메시지와 가이드 전송",
    steps=[
        {
            "type": "send_message",
            "delay": 0,
            "templateId": "welcome_template"
        },
        {
            "type": "wait",
            "delay": 3600,
            "duration": "1h"
        },
        {
            "type": "send_message",
            "delay": 0,
            "templateId": "guide_template"
        }
    ],
    trigger_type="event",
    is_active=True
)

print(f"워크플로우 ID: {workflow['id']}")
```

### ワークフロートリガー

```python
result = client.trigger_workflow(
    workflow_id="workflow_123",
    customer_id="customer_456",
    parameters={
        "name": "김철수",
        "product": "Premium"
    }
)

print(f"워크플로우 실행: {result['success']}")
```

###テンプレートの作成

```python
template = client.create_template(
    name="환영 메시지",
    category="greeting",
    content="안녕하세요, {name}님! 서비스에 오신 것을 환영합니다.",
    variables=["name"],
    language="ko"
)

print(f"템플릿 ID: {template['id']}")
```

### AIチャットボットの作成

```python
bot = client.create_bot(
    name="고객지원 봇",
    description="기본적인 고객 질문에 응답하는 AI 봇",
    greeting_message="안녕하세요! 저는 AI 어시스턴트입니다. 무엇을 도와드릴까요?",
    ai_model="gpt-4",
    knowledge_base="kb_123"
)

print(f"봇 ID: {bot['id']}")
```

### ボットリストの照会

```python
bots = client.list_bots()

for bot in bots:
    print(f"{bot['name']} ({bot['aiModel']}) - {bot['status']}")
```

###チャットセッションリストの検索

```python
sessions = client.list_chat_sessions(
    customer_id="customer_123",
    status="active",
    limit=20
)

for session in sessions:
    print(f"{session['id']}: {session['channel']} - {session['status']}")
```

### 分析データの照会

```python
analytics = client.get_analytics(
    start_date="2024-01-01",
    end_date="2024-01-31",
    metric="messages",
    channel="web"
)

print(f"총 메시지: {analytics['totalMessages']}")
print(f"평균 응답 시간: {analytics['avgResponseTime']}초")
```

### 顧客イベントの追跡

```python
client.track_customer_event(
    customer_id="customer_123",
    event_name="product_purchased",
    properties={
        "product_id": "prod_456",
        "price": 99900,
        "category": "electronics"
    }
)
```

## 機能

- ✅チャットセッション管理
- ✅メッセージの送信と照会
- ✅ワークフロー自動化
- ✅メッセージテンプレート
- ✅ AIチャットボット統合
- ✅顧客イベント追跡
- ✅分析とレポート
- ✅マルチチャンネルサポート

## サポートチャンネル

- ウェブサイトチャット
- WhatsApp
- Facebook Messenger
- Telegram
- Line

##ライセンス

MIT License