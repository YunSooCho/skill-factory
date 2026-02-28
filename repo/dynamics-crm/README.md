# Dynamics CRM API Client

Complete API client for Microsoft Dynamics CRM - Microsoft's customer relationship management platform.

## Features

- Full API coverage for 23 endpoints
- Lead management with custom fields
- Opportunity (案件) management with custom fields
- Company (取引先企業) management with custom fields
- Contact (取引先担当者) management with custom fields
- Search and filtering capabilities
- Complete error handling
- Rate limiting support

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
import asyncio
from dynamics_crm_client import DynamicsCRMClient

async def main():
    client = DynamicsCRMClient(
        api_key="your_api_key",
        organization_url="https://yourorg.api.crm.dynamics.com"
    )

    # Create a lead
    lead = await client.create_lead({
        "name": "John Smith",
        "email": "john@example.com",
        "company": "Acme Corp"
    })

    # Create an opportunity
    opportunity = await client.create_opportunity({
        "name": "Enterprise Deal",
        "value": 100000.0,
        "currency": "USD"
    })

    await client.close()

asyncio.run(main())
```

## API Endpoints

### Leads (リード)
- `create_lead()`, `update_lead()`, `get_lead()`, `delete_lead()`, `search_leads()`
- `update_lead_custom_field()`

### Opportunities (案件)
- `create_opportunity()`, `update_opportunity()`, `get_opportunity()`, `delete_opportunity()`, `search_opportunities()`
- `update_opportunity_custom_field()`

### Companies (取引先企業)
- `create_company()`, `update_company()`, `get_company()`, `delete_company()`, `search_companies()`
- `update_company_custom_field()`

### Contacts (取引先担当者)
- `create_contact()`, `update_contact()`, `get_contact()`, `delete_contact()`, `search_contacts()`

## Error Handling

All methods raise `DynamicsCrmAPIError` on API errors.

## Rate Limiting

Automatic rate limiting included.

## Webhooks

Supports 8 webhook triggers for leads, contacts, companies, and opportunities creation/updates.