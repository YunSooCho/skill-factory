# Keap API Integration

## Overview
Implementation of Keap (formerly Infusionsoft) marketing and sales automation API for Yoom automation.

## Supported Features
- ✅ Update Sales Opportunity
- ✅ Create Product
- ✅ Delete Note
- ✅ Get Notes
- ✅ Search Contacts
- ✅ Create Task
- ✅ Delete Contact
- ✅ Update Note
- ✅ Delete Task
- ✅ Update Product
- ✅ Create Note
- ✅ Create Contact
- ✅ Create Sales Opportunity
- ✅ Get Product
- ✅ Search Products
- ✅ Get Task
- ✅ Search Opportunities
- ✅ Remove Tag from Contacts
- ✅ Delete Product
- ✅ Apply Tag to Contacts
- ✅ Update Contact
- ✅ Search Tasks
- ✅ Update Task
- ✅ Get Sales Opportunity
- ✅ Get Contact

## Setup

### 1. Get OAuth Access Token
Keap uses OAuth 2.0 for authentication. Visit https://developer.keap.com/ to:
1. Create an application in the developer portal
2. Obtain client ID and secret
3. Set up OAuth redirect_uri
4. Get access token from the authorization flow

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure
```python
from keap_client import KeapClient, Contact, Task, SalesOpportunity

access_token = "your_keap_oauth_access_token"

async with KeapClient(access_token=access_token) as client:
    # Use the client
    pass
```

## Usage

### Create Contact and Task
```python
import asyncio
from keap_client import KeapClient, Contact, Task

async def main():
    access_token = "your_keap_oauth_access_token"

    async with KeapClient(access_token=access_token) as client:
        # Create contact
        contact = Contact(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="+1-555-1234",
            company="Example Corp",
            job_title="CEO"
        )
        created_contact = await client.create_contact(contact)

        # Create task
        task = Task(
            title="Follow up call",
            description="Schedule follow-up call with John",
            contact_id=created_contact.id,
            priority="high"
        )
        created_task = await client.create_task(task)

asyncio.run(main())
```

### Sales Opportunity
```python
# Create a sales opportunity
opportunity = SalesOpportunity(
    opportunity_title="Enterprise Deal",
    estimated_value=50000.0,
    probability=50,
    contact_id=contact_id,
    projected_close_date="2024-06-30"
)
created_opportunity = await client.create_sales_opportunity(opportunity)
```

### Products
```python
from keap_client import Product

# Create a product
product = Product(
    product_name="Premium Plan",
    sku="PREM-001",
    price=99.99,
    description="Premium subscription plan",
    taxable=True
)
created_product = await client.create_product(product)
```

### Tag Management
```python
# Apply tag to contacts
await client.apply_tag_to_contacts(
    contact_ids=["contact_1", "contact_2"],
    tag_id="tag_123"
)

# Remove tag from contacts
await client.remove_tag_from_contacts(
    contact_ids=["contact_1", "contact_2"],
    tag_id="tag_123"
)
```

### Notes
```python
from keap_client import Note

# Create a note
note = Note(
    title="Meeting notes",
    description="Discussed new project requirements",
    contact_id=contact_id
)
created_note = await client.create_note(note)

# Get all notes for a contact
notes = await client.get_notes(contact_id=contact_id)
```

## Integration Type
- **Type:** OAuth 2.0 (Bearer token)
- **Authentication:** OAuth access token via Authorization header
- **Protocol:** HTTPS REST API
- **Rate Limiting:** Built-in with 0.5s delay between requests
- **Retries:** Up to 3 retries with exponential backoff

## Error Handling
The client includes comprehensive error handling:
- **401 Unauthorized:** Invalid access token
- **403 Forbidden:** Insufficient permissions
- **404 Not Found:** Resource doesn't exist
- **429 Rate Limited:** Automatic retry with exponential backoff
- **5xx Server Errors:** Automatic retry with exponential backoff

## Data Models

### Contact
- `id`: Unique identifier
- `first_name`: Contact's first name
- `last_name`: Contact's last name
- `email`: Primary email address
- `phone`: Primary phone number
- `website`: Website URL
- `company`: Company name
- `job_title`: Job title
- `street1`, `street2`: Address lines
- `city`, `state`, `postal_code`, `country`: Address fields
- `tags`: List of tag IDs
- `custom_fields`: Dictionary for custom fields
- `date_created`: Creation timestamp
- `last_updated`: Last update timestamp

### Task
- `id`: Unique identifier
- `title`: Task title
- `description`: Task description
- `status`: Status (open, completed)
- `priority`: Priority (low, medium, high)
- `due_date`: Due date (ISO 8601)
- `contact_id`: Associated contact ID
- `assigned_user_id`: Assigned user ID
- `completed_date`: Completion timestamp
- `date_created`: Creation timestamp
- `last_updated`: Last update timestamp

### Note
- `id`: Unique identifier
- `title`: Note title
- `description`: Note content
- `contact_id`: Associated contact ID
- `user_id`: Creator user ID
- `date_created`: Creation timestamp
- `last_updated`: Last update timestamp

### Product
- `id`: Unique identifier
- `product_name`: Product name
- `sku`: Product SKU/code
- `price`: Product price
- `description`: Full description
- `short_description`: Short description
- `taxable`: Whether taxable
- `weight`: Product weight
- `is_active`: Active status
- `date_created`: Creation timestamp
- `last_updated`: Last update timestamp

### SalesOpportunity
- `id`: Unique identifier
- `opportunity_title`: Opportunity name
- `estimated_value`: Estimated deal value
- `probability`: Win probability (0-100)
- `stage_id`: Opportunity stage ID
- `stage_name`: Stage name
- `contact_id`: Associated contact ID
- `user_id`: Assigned user ID
- `projected_close_date`: Expected close date (ISO 8601)
- `notes`: Additional notes
- `date_created`: Creation timestamp
- `last_updated`: Last update timestamp

## Notes
- All operations are async for better performance
- Built-in rate limiting prevents hitting API limits
- Automatic retry logic for transient errors
- Complete CRUD operations for contacts, tasks, notes, products, and opportunities
- Tag management for contacts
- OAuth 2.0 authentication for secure access
- Data model mapping handles API differences

## API Documentation
Official Keap API documentation: https://developer.keap.com/