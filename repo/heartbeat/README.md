# Heartbeat Employee Feedback Integration

Heartbeat enables employee surveys, pulse checks, and feedback collection.

## Installation
```bash
pip install -e .
```

## API Key Setup
1. Log in to Heartbeat account
2. Generate API key from settings

## Usage
```python
from heartbeat import HeartbeatClient

client = HeartbeatClient(api_key="your-key")

# Create survey
survey = client.create_survey({
    "title": "Weekly Check-in",
    "questions": ["How are you feeling?", "Blockers?"]
})

# Get surveys
surveys = client.get_surveys(status="active")

# Get responses
responses = client.get_responses("SURV123")

# Create response
client.create_response("SURV123", {"answers": ["Good", "None"]})

# Get employees
employees = client.get_employees()

# Get pulse score
pulse = client.get_pulse("2024-01-01", "2024-01-31")
```

## API Methods
- `create_survey(data)` - Create survey
- `get_surveys(status, limit)` - List surveys
- `get_survey(survey_id)` - Get survey
- `get_responses(survey_id, limit)` - Get responses
- `create_response(survey_id, data)` - Submit response
- `get_employees(limit)` - List employees
- `get_employee(employee_id)` - Get employee
- `get_pulse(start_date, end_date)` - Get engagement score