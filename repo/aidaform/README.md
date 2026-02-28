# AidaForm API

AidaForm API integration for form management.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from aidaform import AidaFormClient

client = AidaFormClient(api_token="your_token")

# List forms
forms = client.list_forms()

# Get form details
form = client.get_form_details("form_id")

# Get submissions
submissions = client.get_submissions("form_id", limit=10)

# Get submission detail
detail = client.get_submission_detail("form_id", "submission_id")
```

## Features

- List all forms
- Get form details
- Get form submissions
- Get submission details
- Get submission count

## API Reference

- `list_forms()` - List all forms
- `get_form_details(form_id)` - Get form details
- `get_submissions(form_id, limit, offset, status)` - Get submissions
- `get_submission_detail(form_id, submission_id)` - Get submission detail
- `get_submission_count(form_id)` - Get submission count

## Authentication

Requires AidaForm API Token.