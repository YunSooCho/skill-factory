# Contentful API Integration

## Overview
Complete Contentful headless CMS API client for Yoom automation. Supports both Management API (CUD) and Delivery API (read) for comprehensive content operations.

## Supported Features
- ✅ Content type management
- ✅ Entry CRUD operations
- ✅ Asset management (images, files)
- ✅ Publishing and unpublishing
- ✅ Multi-environment support
- ✅ Multi-locale support
- ✅ Query and filtering
- ✅ Space and environment management

## Setup

### 1. Get Credentials
Visit https://app.contentful.com/account/apikeys to get:
- Space ID
- Management Access Token (for write operations)
- Delivery Access Token (for read operations)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure
```bash
export CONTENTFUL_SPACE_ID="your_space_id"
export CONTENTFUL_ACCESS_TOKEN="your_management_token"
export CONTENTFUL_DELIVERY_TOKEN="your_delivery_token"
```

## Usage

### Working with Content Types
```python
import os
from contentful_client import ContentfulAPIClient

os.environ['CONTENTFUL_SPACE_ID'] = 'your_space_id'
os.environ['CONTENTFUL_ACCESS_TOKEN'] = 'your_management_token'

client = ContentfulAPIClient()

# List content types
content_types = client.list_content_types()

# Create content type
content_type = client.create_content_type(
    name='Blog Post',
    fields=[
        {
            'id': 'title',
            'name': 'Title',
            'type': 'Text',
            'localized': False,
            'required': True
        },
        {
            'id': 'body',
            'name': 'Body',
            'type': 'RichText',
            'localized': False,
            'required': False
        }
    ]
)

# Publish content type
client.publish_content_type(content_type['sys']['id'], content_type['sys']['version'])

client.close()
```

### Working with Entries
```python
# Create entry
entry_data = {
    'fields': {
        'title': {'en-US': 'My First Post'},
        'body': {'en-US': 'This is the content'}
    }
}

entry = client.create_entry('blogPost', entry_data)

# Publish entry
client.publish_entry(entry['sys']['id'], entry['sys']['version'])

# Query entries (Delivery API)
entries = client.list_entries(
    content_type='blogPost',
    limit=10
)

# Get single entry
single_entry = client.get_entry(entry['sys']['id'])
```

### Working with Assets
```python
# Create asset
asset = client.create_asset(
    file_data={
        'contentType': 'image/jpeg',
        'fileName': 'photo.jpg',
        'upload': 'https://example.com/photo.jpg'
    },
    title='My Photo'
)

# Process asset
client.process_asset(asset['sys']['id'], asset['sys']['version'])

# Publish asset
client.publish_asset(asset['sys']['id'], asset['sys']['version'])

# List assets
assets = client.list_assets(limit=20)
```

### Query with Filters
```python
# Complex query
entries = client.list_entries(
    content_type='blogPost',
    query={
        'query': 'search term',
        'order': '-sys.createdAt',
        'limit': 100
    }
)
```

### Environment Management
```python
# List environments
environments = client.get_environments()

# Get space info
space = client.get_space()
```

## API Types

### Management API
- **Purpose:** Create, update, delete content
- **Authentication:** Management Access Token
- **Use cases:** CMS operations, content admin

### Delivery API
- **Purpose:** Read-only content delivery
- **Authentication:** Delivery Access Token
- **Use cases:** Frontend apps, displaying content
- **Performance:** CDN-optimized

## Integration Type
- **Type:** Bearer Token
- **Authentication:** Separate tokens for Management and Delivery APIs
- **Protocol:** HTTPS REST API
- **Focus:** Headless CMS

## Notes
- Content types must be published before creating entries
- Assets must be processed before publishing
- Version numbers required for updates
- Multi-environment support (master, staging, etc.)
- Strong typing with content types
- Rich text fields supported
- Image optimization included

## Field Types
- Text (single line, multi line)
- Number
- Date
- Boolean
- Location
- Rich Text
- Object
- Array
- Link (single reference)
- Links (multiple references)
- User