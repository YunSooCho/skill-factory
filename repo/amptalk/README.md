# Amptalk API Client

Python client for Amptalk API - call analysis and phone call analytics platform.

## Features

- **Call Operations**: Get call details, search calls
- **Call Summary**: Retrieve AI-generated call summaries
- **Call Analysis**: Get detailed analysis including sentiment, keywords, topics
- **User Management**: List users in the account
- **Webhooks**: Register for call completion notifications

## API Actions (5)

1. 通話の要約を取得 (Get call summary)
2. 分析情報を取得 (Get analysis information)
3. ユーザーの一覧を取得 (Get user list)
4. 通話を検索 (Search calls)
5. 通話を取得 (Get call details)

## Triggers (1)

1. 通話が完了したら (Call completed)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from amptalk_client import AmptalkClient

# Initialize client
client = AmptalkClient(api_key="your_api_key")

# Get user list
users = client.get_users()
print(f"Found {len(users)} users")

# Search calls
calls = client.search_calls(
    status="completed",
    limit=10
)
print(f"Found {len(calls)} calls")

# Get call summary
if calls:
    call_summary = client.get_call_summary(calls[0].id)
    print(f"Summary: {call_summary.summary}")

    # Get call analysis
    call_analysis = client.get_call_analysis(calls[0].id)
    print(f"Sentiment: {call_analysis.sentiment_label}")
    print(f"Keywords: {call_analysis.keywords}")

# Register webhook
webhook = client.register_webhook(
    callback_url="https://your-server.com/webhook",
    events=["call.completed"]
)
print(f"Webhook registered: {webhook['id']}")

client.close()
```

## Authentication

Amptalk uses API key authentication. Set your API key in the constructor.

## Webhook Setup

To receive notifications when calls are completed:

1. Create a public HTTPS endpoint on your server
2. Register the webhook URL with the client
3. Configure your server to handle POST requests

Example webhook payload:
```json
{
  "event": "call.completed",
  "call_id": "12345",
  "timestamp": "2026-02-28T09:00:00Z",
  "data": {
    "phone_number": "+819012345678",
    "duration": 300,
    "status": "completed"
  }
}
```

## Testing

To test with your API key:

```bash
python amptalk_client.py
```

Edit the `if __name__ == "__main__"` section with your actual API key.

## License

MIT License