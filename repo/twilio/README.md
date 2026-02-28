# Twilio API Client

Python API client for Twilio SMS and Voice services.

[API Documentation](https://www.twilio.com/docs/)

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

```python
from twilio_client import TwilioClient

# Initialize with your Twilio credentials
client = TwilioClient(
    account_sid="ACxxxxx",
    auth_token="your_auth_token"
)
```

Get your credentials from [Twilio Console](https://console.twilio.com/).

## Usage

### Send SMS

```python
# Send a simple SMS
response = client.send_sms(
    to="+819012345678",
    from_="+818012345678",
    body="Hello from Twilio!"
)
print(response)
```

### Make Phone Call

```python
# Make a call with TwiML URL
response = client.make_call(
    to="+819012345678",
    from_="+818012345678",
    url="https://handler.twilio.com/twiml/EHxxxxxxxxx"
)
print(response)

# Make a call with inline TwiML
response = client.make_call(
    to="+819012345678",
    from_="+818012345678",
    twiml='<Response><Say>Hello from Twilio!</Say></Response>'
)
print(response)
```

### Get Message Details

```python
# Get message by SID
message = client.get_message("SMxxxxxxxxx")
print(message)
```

### Get Call Details

```python
# Get call by SID
call = client.get_call("CAXxxxxxxx")
print(call)
```

### List Messages

```python
# List all messages
messages = client.list_messages(limit=50)
print(messages)

# Filter messages
messages = client.list_messages(
    to="+819012345678",
    date_sent_after=datetime(2026, 2, 1),
    limit=100
)
```

### List Calls

```python
# List all calls
calls = client.list_calls(limit=50)
print(calls)

# Filter calls by status
calls = client.list_calls(
    status="completed",
    limit=100
)
```

### Call Recording

```python
# Get recording details
recording = client.get_call_recording("RExxxxxxxxx")
print(recording)

# Delete recording
client.delete_call_recording("RExxxxxxxxx")
```

## API Actions Implemented

| Action | Method | Description |
|--------|--------|-------------|
| Send SMS | `send_sms()` | Send SMS message |
| Make Call | `make_call()` | Make phone call |
| Get Message | `get_message()` | Retrieve message details |
| Get Call | `get_call()` | Retrieve call details |
| List Messages | `list_messages()` | List sent messages |
| List Calls | `list_calls()` | List calls |
| Get Recording | `get_call_recording()` | Get call recording details |
| Delete Recording | `delete_call_recording()` | Delete call recording |

## Error Handling

```python
from twilio_client import TwilioAPIError

try:
    response = client.send_sms(
        to=invalid_number,
        from_="+818012345678",
        body="Test"
    )
except TwilioAPIError as e:
    print(f"Twilio API Error: {e}")
```

## Rate Limiting

Twilio has rate limits based on your account tier. The client does not implement rate limiting - your application should handle rate limit errors (HTTP 429) and implement appropriate backoff strategies.

## Testing

```bash
python test_twilio.py
```

**Note:** Tests require valid Twilio credentials and will make actual API calls. Use a test account number in the `from_` field to avoid charges.

## Yoom Integration

This client implements the following Yoom flow bot operations:
- **電話を発信** (Make Phone Call) - `make_call()`
- **SMSを送信** (Send SMS) - `send_sms()`

For webhook triggers:
- **SMSを受信したら** (When SMS Received) - Requires webhook endpoint setup