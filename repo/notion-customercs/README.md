# Notion Customer Support Integration

Integration for using Notion as a customer support knowledge base and ticket system.

## Installation
```bash
pip install -e .
```

## API Key Setup
1. Log in to Notion
2. Create an integration at https://www.notion.so/my-integrations
3. Generate integration token
4. Share your customer support database with the integration
5. Copy the database ID from URL

## Usage
```python
from notion_customercs import NotionCustomercsClient

client = NotionCustomercsClient(
    integration_token="your-token",
    database_id="your-database-id"
)

# Query tickets
tickets = client.query_database({
    "property": "Status",
    "select": {"equals": "Open"}
})

# Get ticket page
ticket = client.get_page("page_123")

# Create ticket
new_ticket = client.create_page({
    "properties": {
        "Title": {"title": [{"text": {"content": "Support request"}}]},
        "Status": {"select": {"name": "Open"}},
        "Email": {"email": "customer@example.com"}
    }
})

# Update ticket
client.update_page("page_123", {
    "properties": {
        "Status": {"select": {"name": "Resolved"}}
    }
})

# Add comment/content
client.append_block("page_123", [{
    "object": "block",
    "type": "paragraph",
    "paragraph": {"text": [{"type": "text", "text": {"content": "Follow up scheduled"}}]}
}])

# Search
results = client.search({
    "query": "urgent",
    "filter": {"value": "page", "property": "object"}
})

# Get user info
user = client.get_user("user_456")
```

## API Methods
- `query_database(filter_data)` - Query database with filters
- `get_page(page_id)` - Get page content
- `create_page(data)` - Create new page (ticket)
- `update_page(page_id, data)` - Update page
- `append_block(block_id, children)` - Add content to page
- `get_page_children(page_id)` - Get page contents
- `search(query_data)` - Search across workspace
- `get_user(user_id)` - Get user details

## Database Setup
Create a Notion database with these recommended properties:
- Title (title property)
- Status (select: Open, In Progress, Resolved, Closed)
- Email (email)
- Priority (select: Low, Medium, High, Urgent)
- Created (date)
- Assigned To (people)

## Error Handling
```python
try:
    ticket = client.get_page("page_123")
except requests.RequestException as e:
    print(f"Error: {e}")
```