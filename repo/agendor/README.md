# Agendor API Client

Python client for Agendor CRM/PaaS API.

## Features

- **Organizations**: Create, get, update, search organizations
- **People**: Create, get, update, search people (contacts)
- **Deals**: Create, get, update, search deals for people and organizations
- **Tasks**: Create and search tasks for people, organizations, and deals
- **Products**: Create, get, update, search products

## API Actions (27)

1. Create Organization
2. Search Deal
3. Search Organization
4. Get Organization
5. Search Tasks of Person
6. Get Product
7. Update Deal
8. Create Task For Person
9. Update Deal Stage
10. Search Tasks of Deals
11. Update Product
12. Create Task For Organization
13. Create Person
14. Create Product
15. Update Organization
16. Create Task For Deal
17. Get Deal Of Person
18. Create Deal For Organization
19. Get Person
20. Update Person
21. Get Deal For Organization
22. Search Product
23. Search Tasks of Organization
24. Get Deal
25. Update Deal Status
26. Create Deal For Person
27. Search Person

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from agendor_client import AgendorClient

# Initialize client
client = AgendorClient(api_token="your_api_token")

# Create organization
org = client.create_organization(
    name="Example Company",
    email="contact@example.com"
)

# Create person
person = client.create_person(
    name="John Doe",
    email="john@example.com",
    organization_id=org.id
)

# Create deal
deal = client.create_deal_for_organization(
    organization_id=org.id,
    title="Software License",
    value=10000.0
)

# Create task
task = client.create_task_for_deal(
    deal_id=deal.id,
    title="Send proposal"
)

# Search organizations
orgs = client.search_organizations(name="Example")

# Search deals
deals = client.search_deals(organization_id=org.id, status="open")

client.close()
```

## Authentication

Agendor uses API token authentication. Get your token from: https://app.agendor.com.br/settings/api

## API Reference

Official documentation: https://api.agendor.com.br/docs/

## Testing

To test with your API token:

```bash
python agendor_client.py
```

Edit the `if __name__ == "__main__"` section with your actual API token.

## License

MIT License