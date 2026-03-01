# Formsite API

Formsite API integration for form management.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from formsite import FormsiteClient

client = FormsiteClient(api_token="your_token", server="fs1", user_dir="your_dir")
forms = client.list_forms()
results = client.get_results("form_id")
items = client.get_form_items("form_id")
```

## Features

- List forms
- Get form details
- Get results with pagination and date filters
- Get form items/fields

## Authentication

Requires Formsite API Token, server ID, and user directory.
