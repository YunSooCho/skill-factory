# Adalo API Integration

## Overview
Complete Adalo mobile and web app development API client for Yoom automation. Supports database operations, collections, records, and user management.

## Supported Features
- ✅ Collection management
- ✅ Create/read/update/delete records
- ✅ User management
- ✅ File uploads
- ✅ App information and settings
- ✅ Analytics data

## Setup

### 1. Get API Credentials
Visit https://help.adalo.com/how-to/api to get your API key and App ID.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure
```bash
export ADALO_API_KEY="your_api_key"
export ADALO_APP_ID="your_app_id"
```

## Usage

```python
import os
from adalo_client import AdaloAPIClient

os.environ['ADALO_API_KEY'] = 'your_api_key'
os.environ['ADALO_APP_ID'] = 'your_app_id'

client = AdaloAPIClient()

# List collections
collections = client.list_collections()

# Get records
records = client.get_records(collection_id='col_123')

# Create record
record = client.create_record(
    collection_id='col_123',
    record_data={'name': 'John', 'email': 'john@example.com'}
)

# Create user
user = client.create_user({
    'email': 'user@example.com',
    'name': 'User Name',
    'password': 'secure_password'
})

client.close()
```

## Integration Type
- **Type:** API Token
- **Authentication:** Token header + App ID
- **Protocol:** HTTPS REST API
- **Focus:** No-code app development

## Notes
- Requires App ID for API access
- Supports any collection in your app
- File uploads supported
- Real-time database operations