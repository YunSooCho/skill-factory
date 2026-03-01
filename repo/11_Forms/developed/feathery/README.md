# Feathery API

Feathery API integration for form management.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from feathery import FeatheryClient

client = FeatheryClient(api_key="your_key")

# List forms
forms = client.list_forms()

# Get form details
form = client.get_form("form_id")

# Create submission
submission = client.create_submission(
    form_id="form_id",
    submission_data={"name": "John", "email": "john@example.com"}
)

# Get submissions
submissions = client.get_submissions("form_id", limit=10)

# Update submission
updated = client.update_submission("form_id", "submission_id", {"status": "reviewed"})
```

## Features

- List all forms
- Get form details
- Create submissions
- Get submissions
- Update submissions

## API Reference

- `list_forms()` - List all forms
- `get_form(form_id)` - Get form details
- `create_submission(form_id, submission_data)` - Create submission
- `get_submissions(form_id, limit, offset)` - Get submissions
- `get_submission(form_id, submission_id)` - Get submission
- `update_submission(form_id, submission_id, update_data)` - Update submission

## Authentication

Requires Feathery API Key.