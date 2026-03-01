# Kairos Sales API Integration

## Overview
Implementation of Kairos Sales CRM API for Yoom automation.

## Supported Features
- ✅ Add sales log to deal (案件に営業ログを追加)
- ✅ Add tag to company (会社にタグを追加)
- ✅ Create deal (案件を作成)
- ✅ Create company (会社を作成)
- ✅ Delete customer (顧客を削除)
- ✅ Update deal (案件を更新)
- ✅ Search company (会社を検索)
- ✅ Update customer (顧客を更新)
- ✅ Add tag to customer (顧客にタグを追加)
- ✅ Add todo to deal (案件にToDoを追加)
- ✅ Delete company tag (会社のタグを削除)
- ✅ Get customer (顧客を取得)
- ✅ Delete customer tag (顧客のタグを削除)
- ✅ Delete company (会社を削除)
- ✅ Add todo to customer (顧客にToDoを追加)
- ✅ Get company (会社を取得)
- ✅ Delete deal (案件を削除)
- ✅ Search deal (案件を検索)
- ✅ Create customer (顧客を作成)
- ✅ Add sales log to customer (顧客に営業ログを追加)
- ✅ Search customer (顧客を検索)
- ✅ Get deal (案件を取得)
- ✅ Update company (会社を更新)

## Setup

### 1. Get API Key
Visit https://lp.yoom.fun/apps/kairos-sales and obtain your API key from the account settings.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure
```python
from kairos_sales_client import KairosSalesClient, Deal, Company, Customer

api_key = "your_kairos_sales_api_key"

async with KairosSalesClient(api_key=api_key) as client:
    # Use the client
    pass
```

## Usage

### Create Company, Customer, and Deal
```python
import asyncio
from kairos_sales_client import KairosSalesClient, Deal, Company, Customer

async def main():
    api_key = "your_kairos_sales_api_key"

    async with KairosSalesClient(api_key=api_key) as client:
        # Create company
        company = Company(
            name="Example Corp",
            website="https://example.com",
            industry="Technology",
            phone="+1-555-1234"
        )
        created_company = await client.create_company(company)

        # Create customer
        customer = Customer(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            company_id=created_company.id
        )
        created_customer = await client.create_customer(customer)

        # Create deal
        deal = Deal(
            name="Software License",
            value=50000.0,
            currency="USD",
            stage="Proposal",
            customer_id=created_customer.id,
            company_id=created_company.id
        )
        created_deal = await client.create_deal(deal)

asyncio.run(main())
```

### Search and Filter
```python
# Search deals by customer
deals = await client.search_deals(customer_id="customer_123")

# Search companies by industry
companies = await client.search_companies(industry="Technology")

# Search customers by email
customers = await client.search_customers(email="john@example.com")
```

### Tags and Todos
```python
# Add tag to company
tags = await client.add_company_tag(company_id, "Enterprise")

# Add sales log to deal
from kairos_sales_client import SalesLog
log = await client.add_deal_sales_log(
    deal_id,
    SalesLog(content="Discovery call completed")
)

# Add todo to deal
from kairos_sales_client import Todo
todo = await client.add_deal_todo(
    deal_id,
    Todo(
        subject="Send proposal",
        due_date="2024-03-01",
        priority="high"
    )
)
```

## Integration Type
- **Type:** API Key (Bearer token)
- **Authentication:** Authorization header with Bearer token
- **Protocol:** HTTPS REST API
- **Rate Limiting:** Built-in with 0.5s delay between requests
- **Retries:** Up to 3 retries with exponential backoff

## Error Handling
The client includes comprehensive error handling:
- **401 Unauthorized:** Invalid API key
- **403 Forbidden:** Insufficient permissions
- **404 Not Found:** Resource doesn't exist
- **429 Rate Limited:** Automatic retry with exponential backoff
- **5xx Server Errors:** Automatic retry with exponential backoff

## Data Models

### Deal
- `id`: Unique identifier
- `name`: Deal name
- `value`: Deal value in specified currency
- `currency`: Currency code (default: USD)
- `stage`: Current sales stage
- `probability`: Win probability (0-100)
- `expected_close_date`: Expected close date (ISO 8601)
- `customer_id`: Associated customer ID
- `company_id`: Associated company ID
- `description`: Deal description
- `custom_fields`: Dictionary for custom fields

### Company
- `id`: Unique identifier
- `name`: Company name
- `website`: Company website URL
- `industry`: Industry sector
- `size`: Company size
- `address`: Dictionary with address fields
- `phone`: Phone number
- `description`: Company description
- `tags`: List of tags
- `custom_fields`: Dictionary for custom fields

### Customer
- `id`: Unique identifier
- `first_name`: First name
- `last_name`: Last name
- `email`: Email address
- `phone`: Phone number
- `company_id`: Associated company ID
- `title`: Job title
- `description`: Customer description
- `tags`: List of tags
- `custom_fields`: Dictionary for custom fields

### Todo
- `id`: Unique identifier
- `subject`: Task subject
- `due_date`: Due date (ISO 8601)
- `priority`: Priority (low/medium/high)
- `status`: Task status (open/completed)
- `assignee_id`: Assigned user ID
- `description`: Task description

### SalesLog
- `id`: Unique identifier
- `content`: Log content
- `author_id`: Author user ID
- `created_at`: Creation timestamp

## Notes
- All operations are async for better performance
- Built-in rate limiting prevents hitting API limits
- Automatic retry logic for transient errors
- Complete CRUD operations for deals, companies, and customers
- Tag and todo management for all entities