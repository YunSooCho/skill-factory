# Amptalk API Client

Python client for Amptalk conversation analysis API.

## Features

- Call Summaries: Get AI-powered call summaries
- Analytics: Retrieve conversation analytics and insights
- User Management: List and manage users
- Call Search: Search and retrieve calls
- Error Handling: Comprehensive error handling
- Rate Limiting: Built-in rate limiter

## Installation

```bash
pip install aiohttp
```

## API Actions (5)

1. 通話の要約を取得 (Get Call Summary)
2. 分析情報を取得 (Get Analytics Info)
3. ユーザーの一覧を取得 (List Users)
4. 通話を検索 (Search Calls)
5. 通話を取得 (Get Call)

## Triggers (1)

- 通話が完了したら (When call is completed)

## Usage

```python
import asyncio
from amptalk import AmptalkClient

async def main():
    client = AmptalkClient(api_key="your_api_key")

    # List users
    users = await client.list_users()
    print(f"Found {len(users)} users")

    # Search calls
    calls = await client.search_calls(user_id="user_123")
    print(f"Found {len(calls)} calls")

    # Get call details
    if calls:
        call = calls[0]
        print(f"Call: {call.title} ({call.duration}s)")

        # Get call summary
        summary = await client.get_call_summary(call.id)
        print(f"Summary: {summary.summary}")
        print(f"Key points: {summary.key_points}")

    # Get analytics
    analytics = await client.get_analytics(start_date="2024-01-01")
    print(f"Total calls: {analytics.total_calls}")

asyncio.run(main())
```

## Testing

Requires API key (test with existing calls):
```python
# Get existing call ID
# Get call summary
# Search calls
# Get analytics
```

## Authentication

Get API key from Amptalk dashboard.

## Error Handling

```python
from amptalk.amptalk_client import AmptalkError

try:
    summary = await client.get_call_summary(call_id)
except AmptalkError as e:
    print(f"Error: {e.message}")
```

## License

MIT