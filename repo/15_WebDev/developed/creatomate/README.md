# Creatomate API Integration

## Overview
Complete Creatomate automated video generation API client for Yoom automation. Supports template-based video creation with customizable content.

## Supported Features
- ✅ Template management
- ✅ Video rendering creation
- ✅ Status tracking
- ✅ Download completed videos
- ✅ Format options (MP4, GIF, PNG)
- ✅ Quality settings
- ✅ Webhook notifications
- ✅ Account usage tracking

## Setup

### 1. Get API Key
Visit https://creatomate.com/dashboard/api to get your API key.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure
```bash
export CREATOMATE_API_KEY="your_api_key"
```

## Usage

### Basic Video Rendering
```python
import os
from creatomate_client import CreatomateAPIClient

os.environ['CREATOMATE_API_KEY'] = 'your_api_key'

client = CreatomateAPIClient()

# List templates
templates = client.list_templates()

# Create rendering
render = client.create_render(
    template_id='tmpl_abc123',
    modifications={
        'background_color': '#FF5733',
        'text': {
            'text': 'Hello World!',
            'font': 'roboto'
        },
        'images': [
            {'source': 'https://example.com/image.jpg'}
        ]
    },
    format='mp4',
    quality='high'
)

# Check status
status = client.get_render(render['id'])
print(f"Status: {status['status']}")

# Download when ready
if status['status'] == 'succeeded':
    video_data = client.download_render(render['id'])
    with open('video.mp4', 'wb') as f:
        f.write(video_data)

client.close()
```

### Webhook Setup
```python
# Create webhook for completion notifications
webhook = client.create_webhook(
    url='https://your-app.com/webhooks/creatomate',
    events=['rendering.succeeded', 'rendering.failed']
)
```

### Usage Monitoring
```python
# Check usage stats
usage = client.get_usage()
print(f"Used: {usage['renders_used']}/{usage['renders_limit']}")
```

## Rendering Status
- `succeeded`: Video ready for download
- `pending`: Waiting to start
- `processing`: Currently rendering
- `failed`: Rendering failed

## Output Formats
- `mp4`: Video file
- `gif`: Animated GIF
- `png`: PNG sequence

## Quality Levels
- `standard`: Standard quality
- `high`: High quality
- `pro`: Professional quality

## Integration Type
- **Type:** Bearer Token
- **Authentication:** Bearer token header
- **Protocol:** HTTPS REST API
- **Focus:** Automated video generation

## Notes
- Rendering takes time (async operation)
- Use webhooks for notifications
- Templates define structure and animations
- Modifications customize content
- Multiple formats and qualities available
- Rate limits apply based on plan