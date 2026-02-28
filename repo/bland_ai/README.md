# Bland AI API Client

Python client for [Bland AI](https://bland.ai/) - AI-powered phone call automation platform.

## Features

- ✅ Send AI phone calls with custom objectives
- ✅ Manage calls (get, search, stop)
- ✅ Retrieve transcripts and audio recordings
- ✅ Create and manage knowledge bases
- ✅ Call analysis and citations
- ✅ Webhook support for call events
- ✅ Comprehensive error handling
- ✅ Rate limiting support

## Installation

```bash
pip install -r requirements.txt
```

## Getting Started

### 1. Get API Credentials

1. Visit [Bland AI Dashboard](https://app.bland.ai/dashboard/settings)
2. Sign up or log in
3. Navigate to Settings → API Keys
4. Generate your API key

### 2. Initialize the Client

```python
from bland_ai.client import BlandAIClient

# Initialize with your API key
client = BlandAIClient(api_key="your_api_key_here")
```

## Usage Examples

### Send an AI Phone Call

```python
# Send a call with a task
call = client.send_call(
    phone_number="+1234567890",
    task="Call John to follow up on his purchase. Ask if he's satisfied with the product.",
    voice="maya",
    record=True
)
print(call)
# Output: {'status': 'success', 'call_id': '...', 'message': 'Call successfully queued.'}
```

```python
# Send call using a pathway
call = client.send_call(
    phone_number="+1234567890",
    pathway_id="your-pathway-id",
    voice="josh",
    language="en-US"
)
print(call)
```

### Call Management

```python
# Get call details
call_details = client.get_call(call_id="your-call-id")
print(call_details)

# Search calls
calls = client.search_calls(
    phone_number="+1234567890",
    completed=True
)
print(calls)

# Stop an active call
result = client.stop_call(call_id="active-call-id")
print(result)
```

### Transcripts

```python
# Get corrected transcripts
transcripts = client.get_corrected_transcripts(call_id="call-id")
print(transcripts)

# Get raw transcripts
raw_transcripts = client.get_transcripts(call_id="call-id")
print(raw_transcripts)
```

### Audio Recording

```python
# Get audio information
audio_info = client.get_audio_recording(call_id="call-id")
print(f"Recording URL: {audio_info.get('recording_url')}")

# Download recording
client.download_recording(
    call_id="call-id",
    output_path="recording.mp3"
)
print("Recording downloaded")
```

### Knowledge Base

```python
# Create knowledge base from text
kb = client.create_knowledge_base_from_text(
    name="Product Information",
    text_content="Our product X is a revolutionary solution for..."
)
print(kb)

# Create knowledge base from URLs
kb = client.create_knowledge_base_from_url(
    name="Company Knowledge",
    urls=["https://example.com/about", "https://example.com/faq"]
)
print(kb)

# List all knowledge bases
kbs = client.get_knowledge_bases()
print(kbs)

# Delete knowledge base
result = client.delete_knowledge_base(knowledge_base_id="kb-id")
print(result)
```

### Call Analysis

```python
# Get call analysis
analysis = client.get_call_analysis(call_id="call-id")
print(analysis)

# Get citations
citations = client.get_citations(call_id="call-id")
print(citations)
```

### Webhooks (Triggers)

```python
# Register webhook for call events
webhook = client.register_webhook(
    webhook_url="https://your-domain.com/webhook",
    events=["end_call", "call_ended"]
)
print(webhook)
```

## API Reference

### Call Methods

- `send_call(phone_number, task=None, pathway_id=None, **kwargs)` - Send an AI phone call
- `get_call(call_id)` - Get call details
- `search_calls(phone_number=None, completed=None, **kwargs)` - Search for calls
- `stop_call(call_id)` - Stop an active call

### Transcript Methods

- `get_corrected_transcripts(call_id)` - Get corrected transcripts
- `get_transcripts(call_id)` - Get raw transcripts

### Audio Methods

- `get_audio_recording(call_id)` - Get audio recording information
- `download_recording(call_id, output_path=None)` - Download recording file

### Knowledge Base Methods

- `create_knowledge_base(name, knowledge_base_type, data, **kwargs)` - Create knowledge base
- `create_knowledge_base_from_text(name, text_content, **kwargs)` - Create from text
- `create_knowledge_base_from_url(name, urls, **kwargs)` - Create from URLs
- `get_knowledge_bases()` - Get all knowledge bases
- `delete_knowledge_base(knowledge_base_id)` - Delete knowledge base

### Analysis Methods

- `get_call_analysis(call_id)` - Get call analysis
- `get_citations(call_id)` - Get citation data

### Webhook Methods

- `register_webhook(webhook_url, events=None)` - Register for call events

## Call Parameters

When sending a call, you can specify many options:

```python
call = client.send_call(
    phone_number="+1234567890",
    task="Your task instructions here",
    
    # Voice settings
    voice="maya",  # josh, florian, derek, june, nat, paige
    language="en-US",
    
    # Model settings
    model="base",  # "base" or "turbo"
    temperature=0.7,
    
    # Call settings
    max_duration=30,
    record=True,
    wait_for_greeting=False,
    
    # Voicemail settings
    voicemail={
        "action": "leave_message",
        "message": "Hi, this is a test message."
    },
    
    # Transfer settings
    transfer_phone_number="+1098765432",
    
    # Knowledge base
    tools=["KB-..."],  # Knowledge base IDs
    
    # Webhook
    webhook="https://your-domain.com/webhook",
    webhook_events=["call", "webhook"]
)
```

## Common Voice Options

- `maya` - Female voice
- `josh` - Male voice
- `florian` - Male voice
- `derek` - Male voice
- `june` - Female voice
- `nat` - Male voice
- `paige` - Female voice

## Language Codes

Full list includes: `en`, `es`, `fr`, `de`, `ja`, `ko`, `zh`, `pt`, `it`, `nl`, `ru`, etc.

Use:
- `babel-XX` for multilingual support
- `XX-YY` for specific regions (e.g., `en-US`, `es-419`)

## Error Handling

```python
from bland_ai.client import BlandAIClient, BlandAIError

client = BlandAIClient(api_key="your_key")

try:
    call = client.send_call(
        phone_number="+1234567890",
        task="Your task"
    )
    print(call)
except BlandAIError as e:
    print(f"Error: {e}")
finally:
    client.close()
```

## Webhook Format

When you register a webhook, you'll receive payloads for events:

```json
{
  "call_id": "...",
  "event_type": "end_call",
  "status": "completed",
  "duration": 125,
  "summary": "...",
  "disposition_tag": "INTERESTED"
}
```

## Best Practices

1. **Always close the client**: Use `client.close()` or a context manager
2. **Handle rate limits**: The client includes automatic rate limit detection
3. **Use meaningful tasks**: Be specific in your agent instructions
4. **Enable recording**: Set `record=true` for post-call analysis
5. **Validate phone numbers**: Ensure E.164 format with country code
6. **Use knowledge bases**: Improve agent responses with relevant data
7. **Set webhooks**: Track call completion and results

## License

MIT License

## Support

- Documentation: https://docs.bland.ai
- Dashboard: https://app.bland.ai
- Discord Support: https://discord.gg/QvxDz8zcKe