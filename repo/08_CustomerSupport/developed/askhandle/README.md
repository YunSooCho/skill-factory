# AskHandle SDK

AskHandleは、顧客の問い合わせと要求を管理するためのPython SDKです。

## インストール

```bash
pip install -r requirements.txt
```

## API キーの発行方法

1. [AskHandleウェブサイト]（https://askhandle.com)에にアクセスしてアカウントを作成します。
2. ダッシュボードで、Settings > API Keys メニューに移動します。
3. [Create API Key]ボタンをクリックして新しいAPIキーを生成します。
4. 生成された API キーを安全な場所に保存します。

##使用法

### クライアントの初期化

```python
from askhandle import AskHandleClient

client = AskHandleClient(
    api_key="your_api_key_here",
    base_url="https://api.askhandle.com/v1"
)
```

### チケットの作成

```python
ticket = client.create_ticket(
    title="로그인 문제",
    description="사용자가 로그인할 수 없음",
    requester_name="홍길동",
    requester_email="hong@example.com",
    priority="high",
    category="로그인",
    tags=["긴급", "버그"]
)

print(f"티켓 ID: {ticket['id']}")
```

### チケットリストの照会

```python
tickets = client.list_tickets(
    status="open",
    priority="high",
    limit=20
)

for ticket in tickets:
    print(f"{ticket['id']}: {ticket['title']} ({ticket['status']})")
```

### チケットの更新

```python
updated_ticket = client.update_ticket(
    ticket_id="ticket_123",
    status="in_progress",
    assignee_id="agent_456"
)
```

###コメントを追加

```python
comment = client.add_comment(
    ticket_id="ticket_123",
    comment="문제를 조사 중입니다. 잠시만 기다려 주세요.",
    author_name="담당자",
    author_email="support@example.com"
)
```

### 顧客作成

```python
customer = client.create_customer(
    name="김철수",
    email="cheolsu@example.com",
    phone="010-1234-5678",
    company="ABC Corp"
)
```

###統計照会

```python
stats = client.get_statistics(
    start_date="2024-01-01",
    end_date="2024-01-31"
)

print(f"총 티켓: {stats['total_tickets']}")
print(f"해결된 티켓: {stats['resolved_tickets']}")
```

## 機能

- ✅チケットの作成、照会、更新
- ✅コメントの追加と閲覧
- ✅顧客管理
- ✅統計とレポート
- ✅優先順位と状態管理

##ライセンス

MIT License