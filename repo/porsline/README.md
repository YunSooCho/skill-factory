# Porsline API

Porsline API integration for survey management.

## Usage

```python
from porsline import PorslineClient
client = PorslineClient(api_key="your_key")
surveys = client.list_surveys()
responses = client.get_responses("survey_id")
count = client.get_response_count("survey_id")
```

## Features
- List surveys
- Get responses
- Get response count

## Authentication
Requires Porsline API Key.
