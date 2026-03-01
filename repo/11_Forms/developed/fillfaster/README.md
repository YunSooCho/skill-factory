# FillFaster API

FillFaster API integration for form autofill and submission management.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from fillfaster import FillFasterClient

client = FillFasterClient(api_key="your_key")
forms = client.list_forms()
submissions = client.get_submissions("form_id")
detail = client.get_submission("form_id", "sub_id")
```

## Features

- List forms
- Get form details
- Get submissions
- Export submissions

## Authentication

Requires FillFaster API Key.
