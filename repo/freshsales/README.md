# Freshsales API Client

Python API client for Freshsales CRM API.

[API Documentation](https://developers.freshworks.com/crm/api/)

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

```python
from freshsales_client import FreshsalesClient

# Initialize client with your credentials
client = FreshsalesClient(
    api_key="your_api_key",
    domain="your_domain"  # e.g., mycompany (mycompany.freshsales.io)
)
```

Get API key from [Settings > API Settings](https://mydomain.freshsales.io/settings/api_key).

## Usage

### Create Contact (View)

```python
# Create a new contact
response = client.create_view_contact(
    first_name="John",
    last_name="Doe",
    email="john@example.com",
    phone="+1234567890",
    mobile="+0987654321",
    title="Sales Manager"
)
print(response)
```

### Update Contact

```python
# Update an existing contact
response = client.update_view_contact(
    contact_id=123456789,
    email="newemail@example.com",
    title="Senior Sales Manager"
)
print(response)
```

### Get Contact Details

```python
# Get contact by ID
response = client.get_view_contact(123456789)
print(response)
```

### Delete Contact

```python
# Delete a contact
response = client.delete_view_contact(123456789)
print(response)
```

### Create Account

```python
# Create a new account
response = client.create_account(
    name="Example Inc.",
    website="https://example.com",
    phone="+1234567890",
    address="123 Main St",
    city="New York",
    state="NY",
    zipcode="10001",
    country="USA"
)
print(response)
```

### Update Account

```python
# Update an existing account
response = client.update_account(
    account_id=987654321,
    website="https://newexample.com"
)
print(response)
```

### Get Account Details

```python
# Get account by ID
response = client.get_account(987654321)
print(response)
```

### Create Deal

```python
# Create a new deal
response = client.create_deal(
    deal_name="Sales Deal 2026",
    contact_id=123456789,
    account_id=987654321,
    deal_value=10000.00,
    currency="USD",
    closing_date="2026-12-31"
)
print(response)
```

### Update Deal

```python
# Update an existing deal
response = client.update_deal(
    deal_id=111222333,
    deal_value=12000.00,
    closing_date="2026-11-30"
)
print(response)
```

### Get Deal Details

```python
# Get deal by ID
response = client.get_deal(111222333)
print(response)
```

### Delete Deal

```python
# Delete a deal
response = client.delete_deal(111222333)
print(response)
```

### Create Task

```python
# Create a new task
from datetime import datetime, timedelta

response = client.create_task(
    title="Follow up with client",
    due_date=(datetime.now() + timedelta(days=3)).isoformat() + "Z",
    owner_id=123,
    targetable_id=123456789,
    targetable_type="Contact",
    description="Call the client to discuss proposal"
)
print(response)
```

### Update Task

```python
# Update an existing task
response = client.update_task(
    task_id=444555666,
    status="in_progress"
)
print(response)
```

### Get Task Details

```python
# Get task by ID
response = client.get_task(444555666)
print(response)
```

### Delete Task

```python
# Delete a task
response = client.delete_task(444555666)
print(response)
```

### Create Note

```python
# Create a note on a contact
response = client.create_note(
    description="Meeting notes from 2026-02-28 discussion",
    targetable_id=123456789,
    targetable_type="Contact"
)
print(response)
```

### Upload File

```python
# Upload a file to a contact
response = client.upload_file(
    file_path="/path/to/file.pdf",
    targetable_id=123456789,
    targetable_type="Contact"
)
print(response)
```

### Search

```python
# Search contacts
response = client.search(
    query="John",
    entity_type="contact",
    per_page=20
)
print(response)

# Search deals
response = client.search(
    query="Deal 2026",
    entity_type="deal",
    per_page=10
)
print(response)

# Search all entities
response = client.search(
    query="Example",
    entity_type="all",
    per_page=50
)
print(response)
```

## API Actions Implemented

| Action | Method | Description |
|--------|--------|-------------|
| 連絡先の作成 | `create_view_contact()` | Create contact |
| 連絡先情報の更新 | `update_view_contact()` | Update contact |
| 連絡先の詳細を取得 | `get_view_contact()` | Get contact details |
| 連絡先を削除 | `delete_view_contact()` | Delete contact |
| アカウントの作成 | `create_account()` | Create account |
| アカウント情報の更新 | `update_account()` | Update account |
| アカウントの詳細を取得 | `get_account()` | Get account details |
| 取引の作成 | `create_deal()` | Create deal |
| 取引情報の更新 | `update_deal()` | Update deal |
| 取引の詳細を取得 | `get_deal()` | Get deal details |
| 取引を削除 | `delete_deal()` | Delete deal |
| タスクの作成 | `create_task()` | Create task |
| タスク情報の更新 | `update_task()` | Update task |
| タスクの詳細を取得 | `get_task()` | Get task details |
| タスクを削除 | `delete_task()` | Delete task |
| ノートの新規作成 | `create_note()` | Create note |
| ファイルのアップロード | `upload_file()` | Upload file |
| 検索 | `search()` | Search all entities |

## Response Format

```python
{
    "status": "success",
    "data": {
        "contact": {
            "id": 123456789,
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            // ... other fields
        }
    },
    "status_code": 200
}
```

## Error Handling

```python
from freshsales_client import FreshsalesAPIError

try:
    response = client.create_view_contact(
        first_name="John",
        last_name="Doe",
        email="john@example.com"
    )
except FreshsalesAPIError as e:
    print(f"Freshsales API Error: {e}")
```

## Rate Limiting

Freshsales API has rate limits:
- Free tier: 100 requests/minute
- Paid tiers: Higher limits

The client implements basic rate limit handling. For high-volume operations, consider implementing additional rate limiting in your application.

## Testing

```bash
python test_freshsales.py
```

**Note:** Tests require valid Freshsales credentials.

## Yoom Integration

This client implements the following Yoom flow bot operations:
- **ノートの新規作成** - `create_note()`
- **連絡先情報の更新** - `update_view_contact()`
- **取引を削除** - `delete_deal()`
- **連絡先の作成** - `create_view_contact()`
- **連絡先を削除** - `delete_view_contact()`
- **タスクを削除** - `delete_task()`
- **連絡先の詳細を取得** - `get_view_contact()`
- **アカウントの作成** - `create_account()`
- **タスクの作成** - `create_task()`
- **アカウント情報の更新** - `update_account()`
- **取引の作成** - `create_deal()`
- **取引の詳細を取得** - `get_deal()`
- **タスクの詳細を取得** - `get_task()`
- **ファイルのアップロード** - `upload_file()`
- **ユーザー/リード/コンタクト/アカウント/取引を検索** - `search()`
- **タスク情報の更新** - `update_task()`
- **取引情報の更新** - `update_deal()`
- **アカウントの詳細を取得** - `get_account()`

## Triggers

The following Yoom triggers are available:
- **取引が更新されたら** (When deal updated)
- **コンタクトが更新されたら** (When contact updated)
- **コンタクトが作成されたら** (When contact created)
- **アカウントが更新されたら** (When account updated)
- **アカウントが作成されたら** (When account created)
- **取引が作成されたら** (When deal created)

Triggers require webhook endpoint setup.