# VideoAsk API

VideoAsk API integration for video form management.

## Usage

```python
from videoask import VideoAskClient
client = VideoAskClient(api_key="your_key")
videoasks = client.list_videoasks()
interactions = client.get_interactions("videoask_id")
contacts = client.list_contacts()
```

## Features
- List videoasks
- Get interactions (responses)
- List/get contacts

## Authentication
Requires VideoAsk API Key.
