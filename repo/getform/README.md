# Getform API

Getform API integration for form backend.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from getform import GetformClient

client = GetformClient(api_token="your_token")
forms = client.list_forms()
submissions = client.get_submissions("form_id")
export = client.export_submissions("form_id", format="csv")
```

## Features

- List forms
- Get submissions
- Delete submissions
- Export submissions

## Authentication

Requires Getform API Token.
