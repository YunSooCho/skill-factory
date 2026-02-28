# Apollo API Client

Python client for Apollo API - B2B sales intelligence and engagement platform.

## Features

- **Account Management**: Create, update, search accounts
- **Contact Management**: Create, update, search contacts
- **Enrichment**: Enrich person and organization data
- **Webhooks**: Register for contact and account events

## API Actions (9)

1. アカウントを更新 (Update account)
2. コンタクトを検索 (Search contacts)
3. 人物情報のエンリッチメント (Enrich person data)
4. 組織情報のエンリッチメント (Enrich organization data)
5. 人物情報を検索 (Search people)
6. アカウントを検索 (Search accounts)
7. コンタクトを作成 (Create contact)
8. コンタクトを更新 (Update contact)
9. アカウントを作成 (Create account)

## Triggers (3)

1. コンタクトが作成されたら (Contact created)
2. コンタクトが更新されたら (Contact updated)
3. アカウントが作成されたら (Account created)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from apollo_client import ApolloClient

# Initialize client
client = ApolloClient(api_key="your_api_key")

# Create account
account = client.create_account(
    name="Example Corp",
    website="https://example.com",
    industry="Technology",
    size="51-200"
)
print(f"Created account: {account.name}")

# Create contact
contact = client.create_contact(
    first_name="John",
    last_name="Doe",
    email="john.doe@example.com",
    title="Sales Manager",
    organization_id=account.id
)
print(f"Created contact: {contact.first_name} {contact.last_name}")

# Search contacts
contacts = client.search_contacts(organization_id=account.id)
print(f"Found {len(contacts)} contacts")

# Enrich person data
enriched = client.enrich_person(email="john.doe@example.com")
print(f"Enriched: {enriched.title} at {enriched.organization_name}")

# Search people
people = client.search_people(organization_name="Example Corp")
print(f"Found {len(people)} people")

# Enrich organization
org_data = client.enrich_organization(website="https://example.com")
print(f"Organization: {org_data.name}, Size: {org_data.size}")

# Register webhook
webhook = client.register_webhook(
    callback_url="https://your-server.com/webhook",
    events=["contact.created", "contact.updated", "account.created"]
)
print(f"Webhook registered: {webhook['id']}")

client.close()
```

## Authentication

Apollo uses API key authentication. Set your API key in the constructor.

Get your API key from: https://app.apollo.io/settings/api

## Enrichment

The enrichment endpoints allow you to enrich contacts and organizations using various input methods:

**Enrich Person:**
- By email address
- By LinkedIn URL
- By name and organization

**Enrich Organization:**
- By website
- By LinkedIn URL
- By name

## Webhook Events

Available webhook events:
- `contact.created` - Contact created trigger
- `contact.updated` - Contact updated trigger
- `account.created` - Account created trigger

## Testing

To test with your API key:

```bash
python apollo_client.py
```

Edit the `if __name__ == "__main__"` section with your actual API key.

## License

MIT License