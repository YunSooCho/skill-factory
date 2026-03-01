# Google Forms API

Google Forms API integration.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from google_form import GoogleFormClient

client = GoogleFormClient(access_token="your_oauth_token")
form = client.get_form("form_id")
responses = client.get_responses("form_id")
new_form = client.create_form("My Form")
```

## Features

- Get form details
- Get responses with pagination
- Create forms
- Batch update forms
- Create watches for push notifications

## Authentication

Requires Google OAuth2 Access Token.
