# Fillout API

Fillout API integration for form management.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from fillout import FilloutClient

client = FilloutClient(api_key="your_key")
forms = client.list_forms()
submissions = client.get_submissions("form_id")
webhook = client.create_webhook("form_id", "https://yoururl.com")
```

## Features

- List forms
- Get form details
- Get form submissions with pagination
- Webhook management

## Authentication

Requires Fillout API Key.
