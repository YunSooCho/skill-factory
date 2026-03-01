# Paperform API

Paperform API integration for form management.

## Usage

```python
from paperform import PaperformClient
client = PaperformClient(api_key="your_key")
forms = client.list_forms()
submissions = client.get_submissions("form_slug")
partial = client.get_partial_submissions("form_slug")
```

## Features
- List forms
- Get submissions
- Get partial submissions

## Authentication
Requires Paperform API Key.
