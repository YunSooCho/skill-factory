# Maintainx API Integration

## Overview
Complete Maintainx facilities maintenance API client for Yoom automation. Supports work orders, tasks, users, vendors, and locations.

## Supported Features
- ✅ Create and manage work orders
- ✅ Task management within work orders
- ✅ Location and facility management
- ✅ User management with roles
- ✅ Vendor management
- ✅ Comments and notes
- ✅ File attachments
- ✅ Webhook notifications

## Setup

### 1. Get API Key
Visit https://app.maintainx.com/settings/api to get your API key.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure
```bash
export MAINTAINX_API_KEY="your_api_key_here"
```

## Usage

```python
import os
from maintainx_client import MaintainxAPIClient

os.environ['MAINTAINX_API_KEY'] = 'your_api_key'

client = MaintainxAPIClient()

# Create work order
wo = client.create_work_order(
    title='Fix HVAC System',
    description='HVAC not cooling properly',
    location_id='loc_123',
    priority='high',
    assigned_to_ids=['user_456']
)

# Add comment
client.add_comment(
    work_order_id=wo['id'],
    comment='Vendor scheduled for tomorrow'
)

# Close work order
client.close_work_order(wo['id'], notes='Issue resolved')

client.close()
```