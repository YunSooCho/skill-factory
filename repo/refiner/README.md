# Refiner

Refiner is a user survey platform for collecting feedback and understanding user behavior.

## Installation

```bash
pip install -r requirements.txt
```

## API Key

To get your Refiner API key:

1. Sign up at [Refiner](https://refiner.io)
2. Go to Settings > API Keys
3. Generate and copy your API key

## Usage

```python
from refiner import RefinerClient

client = RefinerClient(api_key='your-api-key')

# Create or update a user
user = client.create_or_update_user({
    'id': 'user-123',
    'email': 'john@example.com',
    'name': 'John Doe'
})

# Track an event
client.track_event(
    event_name='signup_completed',
    user_id='user-123',
    properties={'plan': 'premium'}
)

# Search survey responses
responses = client.search_survey_responses(
    survey_id='survey-123',
    date_from='2024-01-01'
)

# Store survey responses
client.store_survey_responses(
    survey_id='survey-123',
    responses=[{'question_1': 'Yes', 'question_2': '5'}]
)

# Search contacts
contacts = client.search_contacts(query='john@example.com')

# Set form publication status
client.set_form_publication_status(form_id='form-123', published=True)

# Archive a form
client.archive_form(form_id='form-123')
```

## API Methods

### Users & Contacts
- `create_or_update_user(user_data)` - Create or update a user
- `search_contacts(query)` - Search contacts

### Surveys
- `search_survey_responses(survey_id, **filters)` - Search survey responses
- `store_survey_responses(survey_id, responses)` - Store survey responses

### Events
- `track_event(event_name, user_id, **kwargs)` - Track an event

### Forms
- `set_form_publication_status(form_id, published)` - Set publication status
- `archive_form(form_id)` - Archive a form

## Triggers

Refiner provides trigger-based webhooks for:
- Survey Completed
- User Enters Segment

Configure webhooks in your Refiner dashboard.