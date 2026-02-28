# JotForm API

JotForm API integration for form management.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from jotform import JotFormClient

client = JotFormClient(api_key="your_key")
forms = client.list_forms()
submissions = client.get_submissions("form_id")
questions = client.get_questions("form_id")
```

## Features

- List forms
- Get submissions with pagination
- Get form questions
- Create / delete submissions
- Get form properties

## Authentication

Requires JotForm API Key. Supports EU endpoint with `use_eu=True`.
