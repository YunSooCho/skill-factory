# Apollo API Client

Python client for Apollo sales intelligence API.

## Features

- Accounts: Create, update, search accounts
- Contacts: Create, update, search contacts
- Enrichment: AI-powered enrichment for people and organizations
- Search: Advanced search for people and accounts
- Error Handling: Comprehensive error handling
- Rate Limiting: Built-in rate limiter

## Installation

```bash
pip install aiohttp
```

## API Actions (9)

1. アカウントを更新 (Update Account)
2. コンタクトを検索 (Search Contacts)
3. 人物情報のエンリッチメント (Enrich Person)
4. 組織情報のエンリッチメント (Enrich Organization)
5. 人物情報を検索 (Search People)
6. アカウントを検索 (Search Accounts)
7. コンタクトを作成 (Create Contact)
8. コンタクトを更新 (Update Contact)
9. アカウントを作成 (Create Account)

## Triggers (3)

- コンタクトが作成されたら (When contact is created)
- コンタクトが更新されたら (When contact is updated)
- アカウントが作成されたら (When account is created)

## Usage

```python
import asyncio
from apollo import ApolloClient

async def main():
    client = ApolloClient(api_key="your_api_key")

    # Create account
    account = await client.create_account({
        "name": "Acme Corp",
        "website": "https://acme.com"
    })
    print(f"Created account: {account.name}")

    # Search contacts
    contacts = await client.search_contacts(first_name="John", last_name="Doe")
    print(f"Found {len(contacts)} contacts")

    # Enrich person data
    result = await client.enrich_person(email="john@acme.com")
    print(f"Enriched data: {result.data}")

    # Enrich organization
    org_result = await client.enrich_organization(website="https://acme.com")
    print(f"Organization data: {org_result.data}")

asyncio.run(main())
```

## Testing

Requires API key (test with existing data):
```python
# Search contacts
# Enrich existing email/website
# Create test account
```

## Authentication

Get API key from Apollo dashboard.

## Error Handling

```python
from apollo.apollo_client import ApolloError

try:
    contact = await client.search_contacts(email="test@example.com")
except ApolloError as e:
    print(f"Error: {e.message}")
```

## License

MIT