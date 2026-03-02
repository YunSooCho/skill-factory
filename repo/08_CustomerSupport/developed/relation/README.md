# Relation SDK

Relationは、顧客関係管理（CRM）用のPython SDKです。

## インストール

```bash
pip install -r requirements.txt
```

## API キーの発行方法

1. [Relation ウェブサイト](https://relation.io)에 にアクセスしてアカウントを作成します。
2. ダッシュボードで、Settings > API Keys メニューに移動します。
3. [Generate API Key]ボタンをクリックして新しいAPIキーを生成します。
4. 生成された API キーを安全な場所に保存します。

##使用法

### クライアントの初期化

```python
from relation import RelationClient

client = RelationClient(
    api_key="your_api_key_here",
    base_url="https://api.relation.io/v1"
)
```

###連絡先の作成

```python
contact = client.create_contact(
    email="customer@example.com",
    first_name="철수",
    last_name="김",
    phone="010-1234-5678",
    company="ABC Corp",
    title="마케팅 매니저",
    tags=["VIP", "대기업"],
    attributes={
        "tier": "gold",
        "signup_date": "2024-01-01"
    }
)

print(f"연락처 ID: {contact['id']}")
```

###連絡先の検索

```python
contact = client.get_contact(contact_id="contact_123")

print(f"{contact['firstName']} {contact['lastName']}")
print(f"회사: {contact['company']}")
print(f"태그: {contact['tags']}")
```

###連絡先リストの検索

```python
contacts = client.list_contacts(
    tags=["VIP"],
    created_after="2024-01-01",
    limit=20
)

for contact in contacts:
    print(f"{contact['email']}: {contact['firstName']} {contact['lastName']}")
```

###連絡先の更新

```python
updated = client.update_contact(
    contact_id="contact_123",
    title="시니어 마케팅 매니저",
    add_tags=["중요고객"],
    remove_tags=["신규"]
)
```

### セグメントの作成

```python
segment = client.create_segment(
    name="VIP 고객",
    description="연간 매출 1억 이상 고객",
    criteria={
        "tags": ["VIP"],
        "attributes": {
            "tier": "gold"
        }
    }
)

print(f"세그먼트 ID: {segment['id']}")
```

###セグメント連絡先の検索

```python
contacts = client.get_segment_contacts(
    segment_id="segment_456",
    limit=50
)

print(f"VIP 고객 수: {len(contacts)}")
```

### ノートの生成

```python
note = client.create_note(
    contact_id="contact_123",
    content고객과의 통화 결과 - 제품 데모 일정 조율 완료",
    author_id="user_456",
    note_type="call"
)

print(f"노트 ID: {note['id']}")
```

### タスクの作成

```python
task = client.create_task(
    contact_id="contact_123",
    title="제품 데모 일정 확인",
    description="고객과 협의한 날짜에 데모 진행 예정",
    due_date="2024-02-15",
    assignee_id="user_456",
    priority="high"
)

print(f"태스크 ID: {task['id']}")
```

### タスクリストの照会

```python
tasks = client.list_tasks(
    contact_id="contact_123",
    status="pending",
    priority="high",
    limit=10
)

for task in tasks:
    print(f"{task['title']} - {task['dueDate']}")
```

### イベント追跡

```python
client.track_event(
    contact_id="contact_123",
    event_name="product_viewed",
    properties={
        "product_id": "prod_789",
        "price": 99900,
        "category": "electronics"
    }
)
```

###連絡先イベント履歴の照会

```python
events = client.get_contact_events(
    contact_id="contact_123",
    event_type="product_viewed",
    limit=20
)

for event in events:
    print(f"{event['eventName']}: {event['properties']}")
    print(f"시간: {event['createdAt']}")
```

###連絡先の削除

```python
result = client.delete_contact(contact_id="contact_123")
print(f"삭제 완료: {result['success']}")
```

## 機能

- ✅連絡先管理（作成、照会、更新、削除）
- ✅セグメントベースの顧客分類
- ✅ノートと活動記録
- ✅タスク管理
- ✅イベント追跡
- ✅統合検索

##ライセンス

MIT License