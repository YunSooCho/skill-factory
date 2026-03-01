# Next SFA API Client

Python client library for Next SFA API - Sales Force Automation system for Japanese market.

## Installation

```bash
pip install -r requirements.txt
```

## Authentication

You need an API key from Next SFA. Initialize the client with your API key:

```python
from next_sfa_client import NextSFAClient

client = NextSFAClient(api_key="your_api_key_here")
```

## Usage Examples

### Company Management

```python
# Register Company
result = client.register_company(
    company_name="株式会社サンプル",
    company_code="SAMPLE001",
    industry="IT・通信",
    address="東京都渋谷区",
    phone="03-1234-5678",
    email="info@sample.co.jp"
)

# Get Company
company = client.get_company(company_id="company_123")

# Update Company
result = client.update_company(
    company_id="company_123",
    phone="03-8765-4321"
)

# Search Companies
companies = client.search_companies(
    company_name="サンプル",
    limit=50
)
```

### Person/Contact Management

```python
# Get Person Details
person = client.get_person(person_id="person_123")

# Search Persons
persons = client.search_persons(
    company_id="company_123",
    person_name="田中",
    limit=50
)
```

### Deal/Opportunity Management

```python
# Register Deal
result = client.register_deal(
    company_id="company_123",
    deal_name="大型案件 A",
    deal_amount=5000000.0,
    deal_stage="negotiating",
    expected_close_date="2024-03-31",
    probability=75
)

# Get Deal Details
deal = client.get_deal(deal_id="deal_123")

# Update Deal
result = client.update_deal(
    deal_id="deal_123",
    deal_stage="won",
    probability=100
)

# Search Deals
deals = client.search_deals(
    company_id="company_123",
    deal_stage="in_progress",
    limit=50
)
```

### Order/Contract Management

```python
# Register Order
result = client.register_order(
    deal_id="deal_123",
    order_number="ORD-2024-001",
    order_amount=5000000.0,
    order_date="2024-01-15",
    delivery_date="2024-02-28"
)

# Get Order Details
order = client.get_order(order_id="order_123")

# Update Order
result = client.update_order(
    order_id="order_123",
    delivery_date="2024-03-15"
)

# Search Orders
orders = client.search_orders(
    order_number="ORD-2024",
    limit=50
)

# Add Product to Order
result = client.add_product_to_order(
    order_id="order_123",
    product_id="product_456",
    quantity=10,
    unit_price=500000.0
)
```

### Sales/Revenue Management

```python
# Register Sales
result = client.register_sales(
    order_id="order_123",
    sales_amount=5000000.0,
    sales_date="2024-01-15"
)

# Get Sales Details
sales = client.get_sales(sales_id="sales_123")

# Update Sales
result = client.update_sales(
    sales_id="sales_123",
    sales_amount=5200000.0
)

# Search Sales
sales_list = client.search_sales(
    company_id="company_123",
    limit=50
)

# Delete Sales
result = client.delete_sales(sales_id="sales_123")
```

### Activity/Interaction Management

```python
# Register Activity
result = client.register_activity(
    company_id="company_123",
    activity_type="meeting",
    description="商談ミーティング実施",
    activity_date="2024-01-15T14:00:00",
    person_id="person_123"
)

# Get Activity Details
activity = client.get_activity(activity_id="activity_123")

# Update Activity
result = client.update_activity(
    activity_id="activity_123",
    description="商談ミーティング完了、次回予定を設定"
)

# Get Activities List
activities = client.get_activities(
    company_id="company_123",
    limit=50
)

# Search Activities
activities = client.search_activities(
    company_id="company_123",
    activity_type="call",
    limit=50
)
```

### User Management

```python
# Get Staff List
staff = client.get_staff_list(limit=50)
```

## Webhook Handling

```python
# Verify webhook signature
is_valid = client.verify_webhook_signature(
    payload=request_body,
    signature=request.headers.get("X-Webhook-Signature"),
    webhook_secret="your_webhook_secret"
)

# Handle webhook event
data = client.handle_webhook(payload)
```

## API Actions

### Company Management (6 actions)
- Register Company (会社登録)
- Update Company (会社更新)
- Get Companies (会社一覧)
- Get Company (会社情報取得)
- Search Companies (会社情報検索)
- Get Company Information (企業情報取得)

### Person Management (2 actions)
- Get Person (企業担当者情報を取得)
- Search Persons (企業担当者情報を検索)

### Deal Management (4 actions)
- Register Deal (案件登録)
- Update Deal (案件更新)
- Get Deal (案件情報を取得)
- Search Deals (案件情報を検索)

### Order Management (6 actions)
- Register Order (受注情報登録)
- Update Order (受注情報更新)
- Get Order (受注情報を取得)
- Get Orders (受注情報)
- Search Orders (受注情報検索)
- Add Product to Order (受注に商品を紐づける)

### Sales Management (5 actions)
- Register Sales (売上情報登録)
- Update Sales (売上情報更新)
- Delete Sales (売上情報削除)
- Get Sales (売上情報を取得)
- Search Sales (売上情報検索)

### Activity Management (5 actions)
- Register Activity (対応履歴登録)
- Update Activity (対応履歴更新)
- Get Activity (対応履歴情報を取得)
- Get Activities (対応履歴一覧)
- Search Activities (対応履歴情報検索)

### User Management (1 action)
- Get Staff List (担当者一覧)

## Triggers

- Activity Registered (対応履歴が登録されたら)
- Activity Updated (対応履歴が更新されたら)
- Deal Registered (案件が登録されたら)
- Deal Updated (案件が更新されたら)
- Order Registered (受注情報が登録されたら)
- Order Updated (受注情報が更新されたら)
- Company Registered (企業が登録されたら)
- Sales Registered (売上情報が登録されたら)
- Sales Updated (売上情報が更新されたら)

## Error Handling

```python
from next_sfa_client import NextSFAClient, NextSFAAPIError

try:
    company = client.get_company(company_id="invalid_id")
except NextSFAAPIError as e:
    print(f"Error: {e}")
```

## Notes

- API designed for Japanese market (interface in Japanese)
- All dates should be in ISO 8601 format
- Currency values should be in Japanese Yen (JPY)
- Deal stages: new, negotiating, won, lost, standby
- Webhook signature verification uses HMAC-SHA256
- Comprehensive sales pipeline management from lead to revenue
- Japanese company culture-specific features included