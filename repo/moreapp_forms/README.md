# MoreApp Forms API

MoreApp Forms API integration for mobile form management.

## Usage

```python
from moreapp_forms import MoreAppFormsClient
client = MoreAppFormsClient(api_key="key", customer_id="cid")
forms = client.list_forms()
submissions = client.get_submissions("form_id")
```

## Features
- List forms
- Get submissions
- Export submissions

## Authentication
Requires MoreApp API Key and Customer ID.
