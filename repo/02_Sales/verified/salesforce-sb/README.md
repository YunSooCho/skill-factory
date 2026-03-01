# Salesforce Sb API Client

Python API client for Salesforce S&B (Sales & Business integration) API.

[Salesforce Developer Docs](https://developer.salesforce.com/docs/api/rest/) | [REST API Guide](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/)

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

```python
from salesforce_sb_client import SalesforceSbClient

# Initialize client with OAuth credentials
client = SalesforceSbClient(
    instance_url="https://yourcompany.my.salesforce.com",
    access_token="your_oauth_access_token",
    api_version="56.0"
)
```

Get access token via [OAuth 2.0](https://help.salesforce.com/s/articleView?id=sf.remoteaccess_oauth_flow_examples.htm).

## Usage

### SOQL Query

```python
# Execute SOQL query
response = client.query("SELECT Id, Name, Type FROM Account LIMIT 10")
print(response)

# Query with filters
response = client.query(
    "SELECT Id, Name, AnnualRevenue FROM Account WHERE Type = 'Customer' ORDER BY Name"
)
print(response)
```

### Create Account

```python
# Create a new account
response = client.create_account(
    name="Example Corporation",
    type="Customer",
    billing_city="Tokyo",
    billing_country="Japan",
    billing_postal_code="100-0001",
    billing_street="1-1-1 Marunouchi, Chiyoda-ku",
    phone="+81-3-1234-5678",
    website="https://example.com",
    industry="Technology",
    annual_revenue=1000000000,
    number_of_employees=500
)
print(response)
```

### Create Contact

```python
# Create a new contact
response = client.create_contact(
    first_name="John",
    last_name="Doe",
    account_id="0012800000XXXXX",  # Associated account ID
    email="john.doe@example.com",
    phone="+81-90-1234-5678",
    title="Sales Manager",
    department="Sales",
    lead_source="Web"
)
print(response)
```

### Create Opportunity

```python
# Create a new opportunity
response = client.create_opportunity(
    name="Large Deal 2026",
    stage_name="Prospecting",
    account_id="0012800000XXXXX",
    close_date="2026-12-31",
    amount=1000000.00,
    type="New Customer",
    probability=20
)
print(response)
```

### Create Lead

```python
# Create a new lead
response = client.create_lead(
    first_name="Jane",
    last_name="Smith",
    company="Acme Inc.",
    email="jane.smith@acme.com",
    phone="+81-80-9876-5432",
    title="CEO",
    industry="Technology",
    status="Open",
    lead_source="Website",
    description="Interested in our enterprise solution"
)
print(response)
```

### Convert Lead

```python
# Convert a lead to account/contact/opportunity
response = client.convert_lead(
    lead_id="00Q2800000XXXXX",
    account_id="0012800000XXXXX",
    opportunity_name="Conversion Opportunity",
    converted_status="Converted"
)
print(response)
```

### Create Task

```python
# Create a new task
response = client.create_task(
    subject="Follow up with customer",
    owner_id="0052800000XXXXX",
    what_id="0012800000XXXXX",  # Related account
    who_id="0032800000XXXXX",    # Related contact
    status="Not Started",
    priority="High",
    activity_date="2026-03-05",
    description="Call to discuss proposal"
)
print(response)
```

### Create Event

```python
# Create a new event
from datetime import datetime, timedelta

start_time = (datetime.now() + timedelta(days=7)).isoformat() + "+09:00"
end_time = (datetime.now() + timedelta(days=7, hours=1)).isoformat() + "+09:00"

response = client.create_event(
    subject="Customer Meeting",
    start_datetime=start_time,
    end_datetime=end_time,
    what_id="0012800000XXXXX",
    who_id="0032800000XXXXX",
    location="Tokyo Office",
    description="Quarterly review meeting"
)
print(response)
```

### Create Case

```python
# Create a new case
response = client.create_case(
    subject="Technical Support Request",
    account_id="0012800000XXXXX",
    contact_id="0032800000XXXXX",
    priority="High",
    status="New",
    origin="Email",
    description="Customer is experiencing login issues"
)
print(response)
```

### Get Object

```python
# Get account by ID
response = client.get_object("Account", "0012800000XXXXX")
print(response)

# Get contact by ID
response = client.get_object("Contact", "0032800000XXXXX")
print(response)
```

### Update Object

```python
# Update account
response = client.update_object(
    object_type="Account",
    record_id="0012800000XXXXX",
    data={"AnnualRevenue": 1500000000, "NumberOfEmployees": 600}
)
print(response)

# Update contact
response = client.update_object(
    object_type="Contact",
    record_id="0032800000XXXXX",
    data={"Phone": "+81-90-5555-4444", "Title": "Senior Sales Manager"}
)
print(response)
```

### Delete Object

```python
# Delete account
response = client.delete_object("Account", "0012800000XXXXX")
print(response)

#Delete contact
response = client.delete_object("Contact", "0032800000XXXXX")
print(response)
```

### Upsert Object

```python
# Upsert using external ID
response = client.upsert_object(
    object_type="Contact",
    external_id_field="External_ID__c",
    external_id="EXT12345",
    data={
        "FirstName": "John",
        "LastName": "Doe",
        "Email": "john.doe@example.com"
    }
)
print(response)
```

### SOSL Search

```python
# Search across multiple objects
response = client.search("FIND {John} IN NAME FIELDS RETURNING Account(Id, Name), Contact(Id, Name)")
print(response)
```

### Describe Object

```python
# Get object metadata
response = client.describe_object("Account")
print(response)
```

### Get Limits

```python
# Get organization limits
response = client.get_limits()
print(response)
```

### Bulk Insert

```python
# Bulk insert accounts
records = [
    {"Name": "Corp A", "Type": "Customer"},
    {"Name": "Corp B", "Type": "Customer"},
    {"Name": "Corp C", "Type": "Prospect"}
]

response = client.bulk_insert("Account", records)
print(response)
```

### Chatter Post

```python
# Post to Chatter feed
response = client.chatter_post(
    user_id="0052800000XXXXX",
    text="Just closed a big deal! 🎉"
)
print(response)
```

## API Actions Implemented

This client provides comprehensive Salesforce API access including:

- **Query Operations**: `query()`, `query_all()`, `search()`
- **Object CRUD**: `create_object()`, `get_object()`, `update_object()`, `delete_object()`, `upsert_object()`
- **Domain Objects**:
  - **Account**: Full CRUD with all standard fields
  - **Contact**: Full CRUD with all standard fields
  - **Opportunity**: Full CRUD with sales tracking
  - **Lead**: Full CRUD with conversion support
  - **Task**: Task management
  - **Event**: Calendar event management
  - **Case**: Customer support case management
- **Advanced Operations**:
  - Lead Conversion: `convert_lead()`
  - Bulk API: `bulk_insert()`
  - Chatter: `chatter_post()`
  - Metadata: `describe_object()`
  - Limits: `get_limits()`

## Response Format

```python
{
    "status": "success",
    "data": {
        "id": "0012800000XXXXX",
        "success": true,
        "errors": []
    },
    "status_code": 200
}
```

For Query results:
```python
{
    "status": "success",
    "data": {
        "totalSize": 10,
        "done": true,
        "records": [
            {
                "Id": "0012800000XXXXX",
                "Name": "Account Name",
                // ... other fields
            }
        ]
    },
    "status_code": 200
}
```

## Error Handling

```python
from salesforce_sb_client import SalesforceSbAPIError

try:
    response = client.create_account(name="Test Account")
except SalesforceSbAPIError as e:
    print(f"Salesforce API Error: {e}")
```

## Rate Limiting

Salesforce has detailed rate limits. Check limits with `client.get_limits()`.

The client does not implement rate limiting - your application should handle rate limit errors (HTTP 429, HTTP 403) with appropriate backoff.

## Testing

```bash
python test_salesforce_sb.py
```

**Note:** Tests require valid Salesforce credentials.

## Yoom Integration

This client implements comprehensive Salesforce CRM operations for:

- **Account Management**: Create, read, update, delete accounts
- **Contact Management**: Full contact lifecycle
- **Opportunity Tracking**: Sales pipeline management
- **Lead Management**: Lead capture and conversion
- **Activity Management**: Tasks and events
- **Case Management**: Customer service cases
- **Advanced Operations**: Bulk operations, search, Chatter

## Salesforce Object Reference

### Common Object Types
- **Account**: Companies/organizations
- **Contact**: People associated with accounts
- **Opportunity**: Sales opportunities
- **Lead**: Potential customers
- **Task**: Action items
- **Event**: Calendar events
- **Case**: Customer service cases
- **User**: Salesforce users

### Common Fields
Field names in Salesforce use PascalCase (e.g., `FirstName`, `LastName`, `AnnualRevenue`).

## Notes

- All dates should be in ISO 8601 format for datetime fields
- All currency values should be numbers (not strings)
- Use `describe_object()` to check available fields for any object
- External ID fields end with `__c` (custom fields)
- Record IDs are 15-18 character alphanumeric strings

## Support

For API documentation and support:
- [Salesforce Developer Docs](https://developer.salesforce.com/docs/api/rest/)
- [REST API Reference](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/)
- [SOQL Reference](https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/)

## Authentication

This client uses OAuth 2.0 access tokens. To obtain a token:

1. Create a Connected App in Salesforce Setup
2. Configure OAuth settings with redirect URI
3. Use OAuth 2.0 authorization code flow to get access token
4. Refresh tokens as needed

The access token is valid for a limited time (typically 1 hour for session tokens).