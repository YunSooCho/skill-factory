# Zoho Forms API

Zoho Forms API integration for form management.

## Usage

```python
from zoho_forms import ZohoFormsClient
client = ZohoFormsClient(oauth_token="your_token")
forms = client.list_forms()
entries = client.get_entries("form_link_name")
fields = client.get_fields("form_link_name")
```

## Features
- List forms
- Get entries with sorting and pagination
- Get form fields
- Create entries

## Authentication
Requires Zoho OAuth Token.
