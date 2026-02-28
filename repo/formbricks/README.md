# Formbricks API

Formbricks API integration for survey management.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from formbricks import FormbricksClient

client = FormbricksClient(api_key="your_key")
surveys = client.list_surveys()
responses = client.get_responses("survey_id")
new_survey = client.create_survey({"name": "My Survey"})
```

## Features

- List surveys
- Get survey details
- Get survey responses
- Create surveys
- Delete surveys

## Authentication

Requires Formbricks API Key.
