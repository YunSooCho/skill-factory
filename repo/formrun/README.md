# Formrun API

Formrun API integration for form management (Japanese service).

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from formrun import FormrunClient

client = FormrunClient(api_key="your_key")
forms = client.list_forms()
submissions = client.get_submissions("form_id")
client.update_submission_status("form_id", "sub_id", "done")
```

## Features

- List forms
- Get form details
- Get submissions
- Update submission status

## Authentication

Requires Formrun API Key.
