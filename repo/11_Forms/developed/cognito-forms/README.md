# Cognito Forms API

Cognito Forms API integration for form management.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from cognito_forms import CognitoFormsClient

client = CognitoFormsClient(api_key="your_key")

# List forms
forms = client.list_forms()

# Get form details
form = client.get_form("form_id")

# Get entries
entries = client.get_entries("form_id", limit=10)

# Create entry
entry = client.create_entry("form_id", {"Name": "John", "Email": "john@example.com"})
```

## Features

- List all forms
- Get form information
- Get entries with filtering
- Create, update, delete entries
- Query with OData filters

## API Reference

- `list_forms()` - List all forms
- `get_form(form_id)` - Get form details
- `get_entries(form_id, limit, offset, filter_query)` - Get entries
- `get_entry(form_id, entry_id)` - Get specific entry
- `create_entry(form_id, entry_data)` - Create entry
- `update_entry(form_id, entry_id, entry_data)` - Update entry
- `delete_entry(form_id, entry_id)` - Delete entry

## Authentication

Requires Cognito Forms API Key.