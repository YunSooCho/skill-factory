# EmailOctopus API Integration

## Overview
Implementation of EmailOctopus email marketing API for Yoom automation.

## Supported Features

### API Actions (9 operations)
- ✅ Contact: Create, Get, Search, Update, Delete
- ✅ Tag: Create, Get all, Delete
- ✅ Automation: Start for contact
- ✅ Campaign: Get summary report, Get link report

### Triggers (8 events)
- ✅ Created Contact
- ✅ Updated Contact
- ✅ Deleted Contact
- ✅ Opened Email
- ✅ Clicked Email
- ✅ Bounced Email
- ✅ Unsubscribed Email
- ✅ Complained Email

## Setup

### 1. Get API Credentials
1. Visit https://emailoctopus.com/ and sign up
2. Go to Settings > API Keys
3. Generate a new API Key
4. Copy your API key
5. Get your list ID from List settings

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure
```python
api_key = "your_api_key"
list_id = "your_list_id"
```

## Usage

### Basic Example
```python
import asyncio
from emailoctopus_client import EmailOctopusClient

async def main():
    api_key = "your_api_key"
    list_id = "your_list_id"

    async with EmailOctopusClient(api_key=api_key) as client:
        # Create contact
        contact = await client.create_contact(
            list_id=list_id,
            email="john@example.com"
        )
        print(f"Contact: {contact.email}")
```

### Contact Management
```python
# Create contact with details
contact = await client.create_contact(
    list_id=list_id,
    email="jane@example.com",
    first_name="Jane",
    last_name="Doe",
    tags=["new-signup", "newsletter"],
    fields={"Source": "Website", "Country": "US"},
    subscribe=True
)

# Get contact
contact = await client.get_contact(
    list_id=list_id,
    contact_id=contact.id
)

# Search contact by email
contact = await client.search_contact(
    list_id=list_id,
    email="john@example.com"
)

# Update contact
contact = await client.update_contact(
    list_id=list_id,
    contact_id=contact.id,
    first_name="Janet",
    tags=["updated", "vip"],
    fields={"LastPurchase": "2024-02-27"}
)

# Delete contact
await client.delete_contact(
    list_id=list_id,
    contact_id=contact.id
)
```

### Tag Management
```python
# Create tag
tag = await client.create_tag(
    list_id=list_id,
    name="vip-customer"
)
print(f"Tag: {tag.name} (ID: {tag.id})")

# Get all tags
tags = await client.get_tags(list_id)
for tag in tags:
    print(f"{tag.name}")

# Delete tag
await client.delete_tag(
    list_id=list_id,
    tag_id=tag.id
)
```

### Automation Triggers
```python
# Start automation for a contact
result = await client.start_automation_for_contact(
    automation_id="automation_123",
    contact_id="contact_456",
    list_id=list_id  # Optional
)
```

### Campaign Reports
```python
# Get campaign summary report
summary = await client.get_campaign_summary_report(
    campaign_id="campaign_123"
)

if summary:
    print(f"Campaign: {summary.name}")
    print(f"Status: {summary.status}")
    print(f"Recipients: {summary.recipients}")
    print(f"Opens: {summary.opens}")
    print(f"Clicks: {summary.clicks}")
    print(f"Bounces: {summary.bounces}")
    print(f"Unsubscribes: {summary.unsubscribes}")
    print(f"Complaints: {summary.complaints}")

    # Calculate rates
    if summary.recipients > 0:
        open_rate = (summary.opens / summary.recipients) * 100
        click_rate = (summary.clicks / summary.recipients) * 100
        print(f"Open Rate: {open_rate:.2f}%")
        print(f"Click Rate: {click_rate:.2f}%")
```

### Campaign Link Reports
```python
# Get Link click report
links = await client.get_campaign_link_report(
    campaign_id="campaign_123"
)

print(f"Links tracked: {len(links)}")
for link in links:
    print(f"{link.url}:")
    print(f"  Total Clicks: {link.clicks}")
    print(f"  Unique Clicks: {link.unique_clicks}")
```

## Integration Type
- **Type:** API Key (Basic Authentication)
- **Authentication:** Basic Auth with API key as username
- **Protocol:** HTTPS REST API v1.6

## Testability
- ✅ All API actions testable with valid credentials
- ⚠️ Webhook triggers require public endpoint

## Webhook Setup

To receive triggers:
1. Go to Settings > Webhooks in EmailOctopus
2. Add your webhook endpoint URL
3. Select events to track:
   - `contact.created` - Contact created
   - `contact.updated` - Contact updated
   - `contact.deleted` - Contact deleted
   - `email.opened` - Email opened
   - `email.clicked` - Link clicked in email
   - `email.bounced` - Email bounced
   - `email.unsubscribed` - Contact unsubscribed
   - `email.complained` - Email marked as spam
4. EmailOctopus will POST event data to your endpoint

Example webhook payload:
```json
{
  "event": "contact.created",
  "data": {
    "contact": {
      "id": "123",
      "email": "john@example.com",
      "first_name": "John",
      "last_name": "Doe"
    }
  },
  "timestamp": "2024-02-27T10:00:00Z"
}
```

## List Management

### Finding Your List ID
```python
# Get your list ID from EmailOctopus dashboard
# Go to Lists > Select your list > List settings
# The list ID is shown in the URL or list details

list_id = "your-list-id-here"
```

### Custom Fields
```python
# EmailOctopus supports custom fields
contact = await client.create_contact(
    list_id=list_id,
    email="user@example.com",
    fields={
        "Company": "Acme Corp",
        "Phone": "+1234567890",
        "City": "San Francisco",
        "CustomField1": "Value"
    }
)
```

## Best Practices

### Contact Organization
```python
# Use tags to segment contacts
await client.create_contact(
    list_id=list_id,
    email="customer@example.com",
    tags=["customer", "premium", "newsletter"]
)

# Create tags for segmentation
tags = ["newsletter", "customers", "leads", "inactive"]
for tag in tags:
    await client.create_tag(list_id, tag)
```

### Bulk Contact Import
```python
# Import multiple contacts efficiently
contacts = [
    {"email": "user1@ex.com", "first_name": "John"},
    {"email": "user2@ex.com", "first_name": "Jane"},
    {"email": "user3@ex.com", "first_name": "Bob"},
]

tasks = [
    client.create_contact(
        list_id=list_id,
        email=c["email"],
        first_name=c["first_name"]
    )
    for c in contacts
]

results = await asyncio.gather(*tasks)
print(f"Created {len(results)} contacts")
```

### Campaign Analysis
```python
# Analyze campaign performance
summary = await client.get_campaign_summary_report(campaign_id)

if summary:
    # Health check
    bounce_rate = (summary.bounces / summary.recipients) * 100
    complaint_rate = (summary.complaints / summary.recipients) * 100

    if bounce_rate > 5:
        print("Warning: High bounce rate")
    if complaint_rate > 0.1:
        print("Warning: High complaint rate")

    # Engagement metrics
    open_rate = (summary.opens / summary.recipients) * 100
    click_rate = (summary.clicks / summary.recipients) * 100

    print(f"Engagement Score: {(open_rate + click_rate) / 2:.2f}%")
```

### Link Performance Analysis
```python
# Analyze which links perform best
links = await client.get_campaign_link_report(campaign_id)

# Sort by clicks
links_sorted = sorted(links, key=lambda l: l.clicks, reverse=True)

print("Top Performing Links:")
for link in links_sorted[:5]:
    click_rate = link.unique_clicks / link.clicks * 100 if link.clicks > 0 else 0
    print(f"{link.url}: {link.clicks} clicks ({click_rate:.1f}% unique)")
```

### Automation Workflows
```python
# Trigger automation based on contact segmentation
async def trigger_onboarding(contact_id: str):
    """Trigger onboarding automation for new customers"""
    result = await client.start_automation_for_contact(
        automation_id="automation_onboarding",
        contact_id=contact_id,
        list_id=list_id
    )
    return result

# Use after contact creation
contact = await client.create_contact(
    list_id=list_id,
    email="new@example.com",
    tags=["new-customer"]
)

await trigger_onboarding(contact.id)
```

### Contact Maintenance
```python
# Clean up unsubscribed or bounced contacts
async def clean_inactive_contacts():
    """Remove contacts with invalid emails"""
    # Get all contacts in chunks
    offset = 0
    limit = 100
    deleted_count = 0

    while True:
        # Query contacts (you'd need a list method here)
        # For simplicity, assuming you have contact IDs
        contact_ids = await get_contact_ids(list_id, offset, limit)

        if not contact_ids:
            break

        for contact_id in contact_ids:
            contact = await client.get_contact(list_id, contact_id)

            if contact.status in ("unsubscribed", "bounced"):
                await client.delete_contact(list_id, contact_id)
                deleted_count += 1

        offset += limit

    return deleted_count
```

### Data Enrichment
```python
# Enrich existing contacts with additional data
async def enrich_contacts(contact_ids: List[str], fields: Dict[str, str]):
    """Add custom fields to multiple contacts"""
    tasks = [
        client.update_contact(
            list_id=list_id,
            contact_id=contact_id,
            fields=fields
        )
        for contact_id in contact_ids
    ]

    results = await asyncio.gather(*tasks)
    return results

results = await enrich_contacts(
    contact_ids=["c1", "c2", "c3"],
    fields={"Segment": "VIP", "Region": "North America"}
)
```

## Error Handling

```python
# Always handle API errors gracefully
try:
    contact = await client.create_contact(
        list_id=list_id,
        email="user@example.com"
    )
except Exception as e:
    print(f"Failed to create contact: {e}")
    # Handle error appropriately
```

## Notes

- All operations are async and require `async/await` syntax
- Contact IDs and List IDs are returned as strings
- Tags help with segmentation and targeting
- Campaign reports provide valuable engagement metrics
- Implement proper error handling for production use
- Rate limits apply, implement appropriate pacing for bulk operations
- Double opt-in is handled by the `subscribe` parameter
- Fields can store custom data as key-value pairs