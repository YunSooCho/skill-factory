# Pipedrive Test Guide

## Environment
```bash
YOOM_PIPEDRIVE_BASE_URL=https://api.pipedrive.com
YOOM_PIPEDRIVE_AUTH_TOKEN=your_token
```

## Test Connection
```python
from integration import PipedriveClient
client = PipedriveClient()