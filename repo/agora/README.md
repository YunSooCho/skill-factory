# Agora API Integration

## Overview
Complete Agora real-time communication API client for Yoom automation. Supports RTC (voice/video), RTM (messaging), cloud recording, and user management.

## Supported Features
- ✅ RTC channel user management
- ✅ RTM messaging
- ✅ Cloud recording (acquire, start, stop)
- ✅ Recording status tracking
- ✅ Storage configuration
- ✅ Usage statistics
- ✅ Project management
- ✅ Token generation support

## Setup

### 1. Get Credentials
Visit https://console.agora.io/ to get:
- App ID and Certificate (for local token generation)
- Customer ID and Secret (for REST API)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure
```bash
export AGORA_APP_ID="your_app_id"
export AGORA_APP_CERTIFICATE="your_app_certificate"
export AGORA_CUSTOMER_ID="your_customer_id"
export AGORA_CUSTOMER_SECRET="your_customer_secret"
```

## Usage

```python
import os
from agora_client import AgoraAPIClient
from agora_token import RtcTokenBuilder

os.environ['AGORA_CUSTOMER_ID'] = 'your_customer_id'
os.environ['AGORA_CUSTOMER_SECRET'] = 'your_customer_secret'

client = AgoraAPIClient()

# Get RTC channel users
users = client.get_rtc_users(channel_name='test_channel')

# Start cloud recording
resource = client.create_acquisition(resource_id='res_123', recorder_id='rec_456')
recording = client.start_recording(
    resource_id=resource['resourceId'],
    recorder_id='rec_456',
    start_config={'channelName': 'test_channel'}
)

# Stop recording
stopped = client.stop_recording(
    resource_id=resource['resourceId'],
    recorder_id='rec_456',
    sid=recording['sid']
)

client.close()
```

## Token Generation
```python
# For token generation (server-side)
from agora_token import RtcTokenBuilder
import os

app_id = os.getenv('AGORA_APP_ID')
app_certificate = os.getenv('AGORA_APP_CERTIFICATE')

token = RtcTokenBuilder.buildTokenWithUid(
    app_id,
    app_certificate,
    'test_channel',
    'user_123',
    1,  # Role publisher
    1640995200  # Expiry timestamp
)
```

## Integration Type
- **Type:** Customer Credentials + App ID
- **Authentication:** Basic Auth (Customer ID/Secret)
- **Protocol:** HTTPS REST API
- **Focus:** Real-time communication

## Notes
- Supports voice, video, and real-time messaging
- Cloud recording available
- Token generation requires agora_token library
- Sub-millisecond latency global network
- Up to 1M+ concurrent users per stream