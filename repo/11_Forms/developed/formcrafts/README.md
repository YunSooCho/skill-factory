# Formcrafts API

Formcrafts API integration for form management.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from formcrafts import FormcraftsClient

client = FormcraftsClient(api_key="your_key")
forms = client.list_forms()
submissions = client.get_submissions("form_id")
analytics = client.get_analytics("form_id")
```

## Features

- List forms
- Get form details
- Get submissions
- Get analytics
- Export submissions

## Authentication

Requires Formcrafts API Key.
