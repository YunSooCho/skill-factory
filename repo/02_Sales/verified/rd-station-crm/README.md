# RD Station CRM API Client

Python API client for RD Station CRM API.

[Official Site](https://www.rdstation.com/) | [API Documentation](https://developers.rdstation.com/)

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

```python
from rd_station_crm_client import RdStationCrmClient

# Initialize client with your API token
client = RdStationCrmClient(
    api_token="your_api_token"
)
```

Get API token from RD Station CRM settings.

## Usage

### Create Deal

```python
# Create a new deal
response = client.create_deal(
    name="Sales Deal 2026",
    deal_stage_id="658f722b-1234-5678-1234-567812345678",
    user_id="658f722b-1234-5678-1234-567812345679",
    value=10000.00,
    currency="BRL",
    expected_close_date="2026-12-31"
)
print(response)
```

### Get Deal

```python
# Get deal details
response = client.get_deal(deal_id=123456)
print(response)
```

### Update Deal

```python
# Update an existing deal
response = client.update_deal(
    deal_id=123456,
    deal_stage_id="new_stage_id",
    value=12000.00,
    expected_close_date="2026-11-30"
)
print(response)
```

### Delete Deal

```python
# Delete a deal
response = client.delete_deal(deal_id=123456)
print(response)
```

### Search Deals

```python
# Search deals
response = client.search_deals(
    user_id="user_id",
    deal_stage_id="stage_id",
    per_page=50
)
print(response)

# List all deals
response = client.search_deals(per_page=100, page=2)
print(response)
```

### Create Lead

```python
# Create a new lead
response = client.create_lead(
    name="John Doe",
    email="john@example.com",
    organization_id=123
)
print(response)
```

### Get Lead

```python
# Get lead details
response = client.get_lead(lead_id=789)
print(response)
```

### Update Lead

```python
# Update a lead
response = client.update_lead(
    lead_id=789,
    name="John Updated",
    email="john.updated@example.com"
)
print(response)
```

### Delete Lead

```python
# Delete a lead
response = client.delete_lead(lead_id=789)
print(response)
```

### Search Leads

```python
# Search leads
response = client.search_leads(q="John", per_page=50)
print(response)

# List all leads
response = client.search_leads(per_page=100)
print(response)
```

### Create Organization

```python
# Create a new organization
response = client.create_organization(
    name="Example Inc.",
    website="https://example.com",
    phone="+1234567890"
)
print(response)
```

### Get Organization

```python
# Get organization details
response = client.get_organization(organization_id=456)
print(response)
```

### Update Organization

```python
# Update an organization
response = client.update_organization(
    organization_id=456,
    name="Example Updated Inc.",
    website="https://newexample.com"
)
print(response)
```

### Search Organizations

```python
# Search organizations
response = client.search_organizations(q="Example", per_page=50)
print(response)

# List all organizations
response = client.search_organizations(per_page=100)
print(response)
```

### Create Task

```python
# Create a new task
from datetime import datetime, timedelta

deadline = (datetime.now() + timedelta(days=3)).isoformat() + "Z"

response = client.create_task(
    description="Follow up with client",
    type="call",
    deadline=deadline
)
print(response)
```

### Update Task

```python
# Update a task
response = client.update_task(
    task_id=999,
    status="completed"
)
print(response)
```

## API Actions Implemented

| Action | Method | Description |
|--------|--------|-------------|
| Create Deal | `create_deal()` | Create deal |
| Get Deal | `get_deal()` | Get deal details |
| Update Deal | `update_deal()` | Update deal |
| Delete Deal | `delete_deal()` | Delete deal |
| Search Deal | `search_deals()` | Search/list deals |
| Create Lead | `create_lead()` | Create lead |
| Get Lead | `get_lead()` | Get lead details |
| Update Lead | `update_lead()` | Update lead |
| Delete Lead | `delete_lead()` | Delete lead |
| Search Lead | `search_leads()` | Search/list leads |
| Create Organization | `create_organization()` | Create organization |
| Get Organization | `get_organization()` | Get organization details |
| Update Organization | `update_organization()` | Update organization |
| Search Organization | `search_organizations()` | Search/list organizations |
| Create Task | `create_task()` | Create task |
| Update Task | `update_task()` | Update task |

## Response Format

```python
{
    "status": "success",
    "data": {
        "id": 123456,
        "name": "Sales Deal 2026",
        "deal_stage_id": "658f722b-...",
        "amount": 10000.00,
        // ... other fields
    },
    "status_code": 200
}
```

## Error Handling

```python
from rd_station_crm_client import RdStationCrmAPIError

try:
    response = client.create_deal(
        name="Test Deal",
        deal_stage_id="stage_id",
        user_id="user_id"
    )
except RdStationCrmAPIError as e:
    print(f"RD Station CRM API Error: {e}")
```

## Rate Limiting

RD Station CRM API has rate limits. The client does not implement rate limiting - your application should handle rate limit errors (HTTP 429) with appropriate backoff.

## Testing

```bash
python test_rd_station_crm.py
```

**Note:** Tests require valid RD Station CRM credentials.

## Yoom Integration

This client implements the following Yoom flow bot operations:
- **Get Deal** - `get_deal()`
- **Update Deal** - `update_deal()`
- **Create Deal** - `create_deal()`
- **Get Lead** - `get_lead()`
- **Update Lead** - `update_lead()`
- **Delete Deal** - `delete_deal()`
- **Create Lead** - `create_lead()`
- **Search Deal** - `search_deals()`
- **Create Task** - `create_task()`
- **Update Task** - `update_task()`
- **Create Organization** - `create_organization()`
- **Delete Lead** - `delete_lead()`
- **Search Lead** - `search_leads()`
- **Search Organization** - `search_organizations()`
- **Get Organization** - `get_organization()`
- **Update Organization** - `update_organization()`

## Triggers

The following Yoom triggers are available:
- **Lead Deleted**, **Lead Updated**, **Lead Created**, **Organization Created**, **Organization Updated**, **Organization Deleted**, **Deal Updated**, **Deal Deleted**, **Deal Created**

Triggers require webhook endpoint setup.