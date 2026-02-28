# Cloudflare API Integration

## Overview
Complete Cloudflare infrastructure API client for Yoom automation. Supports DNS, CDN, SSL, firewall, Workers, and analytics management.

## Supported Features
- ✅ Zone management (domains)
- ✅ DNS record CRUD operations
- ✅ SSL/TLS configuration
- ✅ Firewall rules
- ✅ Cloudflare Workers (serverless functions)
- ✅ Analytics and metrics
- ✅ Page rules
- ✅ Account management

## Setup

### 1. Get API Token
Visit https://dash.cloudflare.com/profile/api-tokens to create an API token with appropriate permissions.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure
```bash
export CLOUDFLARE_API_KEY="your_api_token"
export CLOUDFLARE_ACCOUNT_ID="your_account_id"  # optional
```

## Usage

### DNS Management
```python
import os
from cloudflare_client import CloudflareAPIClient

os.environ['CLOUDFLARE_API_KEY'] = 'your_api_token'

client = CloudflareAPIClient()

# List zones
zones = client.list_zones()

# Create DNS record
record = client.create_dns_record(
    zone_id='zone_123',
    record_type='A',
    name='www.example.com',
    content='192.0.2.1',
    proxied=True
)

# Update DNS record
updated = client.update_dns_record(
    zone_id='zone_123',
    record_id=record['result']['id'],
    content='192.0.2.2'
)

client.close()
```

### SSL Configuration
```python
# Get SSL settings
ssl_settings = client.get_ssl_settings(zone_id='zone_123')

# Update SSL to Full
client.update_ssl_settings(zone_id='zone_123', value='full')
```

### Workers
```python
# Create a worker
worker_code = """
addEventListener('fetch', event => {
    event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
    return new Response('Hello from Cloudflare Worker!')
})
"""

worker = client.create_worker(
    script_name='my-worker',
    script_content=worker_code
)
```

### Analytics
```python
# Get zone analytics
analytics = client.get_zone_analytics(
    zone_id='zone_123',
    metrics=['requests', 'bandwidth', 'uniques'],
    since='2024-01-01',
    until='2024-01-31'
)
```

### Page Rules
```python
# Create page rule
rule = client.create_page_rule(
    zone_id='zone_123',
    targets=[
        {'target': 'url', 'constraint': {'operator': 'matches', 'value': 'example.com/*'}}
    ],
    actions=[
        {'id': 'cache_level', 'value': 'cache_everything'}
    ]
)
```

## Integration Type
- **Type:** Bearer Token
- **Authentication:** Bearer token header
- **Protocol:** HTTPS REST API
- **Focus:** DNS, CDN, Security, Serverless

## Notes
- API token must have appropriate permissions
- Resource-based access control available
- Rate limits apply based on plan
- Supports all Cloudflare products

## Common Record Types
- A: IPv4 address
- AAAA: IPv6 address
- CNAME: Canonical name
- TXT: Text records
- MX: Mail exchange
- NS: Name server
- SRV: Service records

## SSL Modes
- off: No SSL
- flexible: Cloudflare to visitor only
- full: Full SSL
- strict: Full SSL (strict validation)