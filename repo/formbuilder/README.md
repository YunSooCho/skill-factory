# FormBuilder API

FormBuilder API integration for form management.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from formbuilder import FormBuilderClient

client = FormBuilderClient(api_key="your_key")
forms = client.list_forms()
new_form = client.create_form({"name": "My Form"})
submissions = client.get_submissions("form_id")
```

## Features

- List forms
- Get form details
- Create forms
- Delete forms
- Get submissions

## Authentication

Requires FormBuilder API Key.
