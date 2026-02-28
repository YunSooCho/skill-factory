# Bubble API Integration

## Overview
Complete Bubble no-code platform API client for Yoom automation. Provides full access to Bubble app data, workflows, and external API capabilities.

## Supported Features
- ✅ Generic CRUD operations on all data types
- ✅ Constraint-based filtering
- ✅ Batch operations
- ✅ API workflow execution
- ✅ External API calls
- ✅ File uploads
- ✅ Query parameters support

## Setup

### 1. Get API Key
1. Open your Bubble app editor
2. Go to Settings > API
3. Configure API options and generate API key
4. Note your app URL

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure
```bash
export BUBBLE_API_KEY="your_api_key"
export BUBBLE_APP_URL="https://your-app.bubbleapps.io/version-test"
```

## Usage

### Data Operations
```python
import os
from bubble_client import BubbleAPIClient

os.environ['BUBBLE_API_KEY'] = 'your_api_key'
os.environ['BUBBLE_APP_URL'] = 'https://your-app.bubbleapps.io/version-test'

client = BubbleAPIClient()

# Get all objects of a type
users = client.get_objects('User', limit=50)

# Get with constraints
filtered = client.get_objects(
    'Product',
    constraints=[
        {'key': 'category', 'constraint_type': 'equals', 'value': 'Electronics'}
    ]
)

# Create object
product = client.create_object('Product', {
    'name': 'iPhone 15',
    'price': 999,
    'category': 'Electronics'
})

# Update object
updated = client.update_object('Product', product['_id'], {
    'price': 899
})

# Delete object
client.delete_object('Product', product['_id'])

client.close()
```

### Workflow Calls
```python
# Call an API workflow
result = client.call_api_workflow(
    'create_order',
    params={
        'customer_id': 'cust_123',
        'items': ['item_456'],
        'total': 100
    }
)
```

### Batch Operations
```python
# Bulk create objects
batch_result = client.batch_create_objects('Order', [
    {'customer_id': 'cust_1', 'total': 50},
    {'customer_id': 'cust_2', 'total': 75}
])
```

### File Uploads
```python
# Upload file
file_result = client.upload_file('document.pdf')
```

## Integration Type
- **Type:** Bearer Token
- **Authentication:** Bearer token header
- **Protocol:** HTTPS REST API
- **Focus:** No-code app backend

## Notes
- Object types must exist in your Bubble app
- Constraints follow Bubble API format
- Supports all Bubble data types dynamically
- Can trigger workflows and external APIs
- File upload support included
- Query parameters for complex filters

## Data Types
Work with any Bubble data type:
- User (built-in)
- Custom types you create
- Connected data types from plugins

## Constraint Types
Common constraint types:
- `equals`
- `contains`
- `greater than`
- `less than`
- `not_contains`
- `is_empty` / `is_not_empty`