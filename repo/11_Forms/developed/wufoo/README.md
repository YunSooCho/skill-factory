# Wufoo API

Wufoo API integration for form management.

## Usage

```python
from wufoo import WufooClient
client = WufooClient(api_key="your_key", subdomain="yoursubdomain")
forms = client.list_forms()
entries = client.get_entries("form_hash")
fields = client.get_fields("form_hash")
count = client.get_entry_count("form_hash")
```

## Features
- List forms
- Get entries with pagination and sorting
- Get form fields
- Submit entries
- Get comments

## Authentication
Requires Wufoo API Key and account subdomain.
