# Kasika

Kasika is a Japanese CRM platform for managing customer relationships and sales activities.

## Installation

```bash
pip install -r requirements.txt
```

## API Key

To get your Kasika API key:

1. Sign up at [Kasika](https://www.kasika.jp)
2. Go to Settings > API Settings
3. Generate and copy your API key

## Usage

```python
from kasika import KasikaClient

client = KasikaClient(api_key='your-api-key')

# Register a customer
customer = client.register_customer({
    'name': '株式会社ABC',
    'email': 'info@example.com',
    'phone': '03-1234-5678'
})

# Get customer details
customer = client.get_customer(customer_id='customer-123')

# Update customer
client.update_customer(customer_id='customer-123', data={'name': 'New Name'})

# Add customer agent
client.add_customer_agent(
    customer_id='customer-123',
    agent_id='agent-456',
    overwrite=False
)

# Create sales action
action = client.create_sales_action({
    'customer_id': 'customer-123',
    'type': 'phone_call',
    'note': 'Follow up call'
})

# List sales actions
actions = client.list_sales_actions(customer_id='customer-123')

# Invite employee
client.invite_employee(email='new@example.com', name='John Doe')

# Bulk add customer tags
client.bulk_add_customer_tags(
    customer_ids=['cust-1', 'cust-2'],
    tag='VIP'
)

# Export customer CSV
download_url = client.export_customer_csv()
```

## API Methods

### Customers
- `register_customer(customer_data)` - Register a new customer
- `get_customer(customer_id)` - Get customer details
- `update_customer(customer_id, data)` - Update customer
- `delete_customer(customer_id)` - Delete customer
- `add_customer_agent(customer_id, agent_id, **kwargs)` - Add or overwrite agent
- `remove_customer_agent(customer_id, agent_id)` - Remove agent
- `add_customer_external_activity(customer_id, activity)` - Add external activity
- `add_email_address(customer_id, email)` - Add email address
- `bulk_add_customer_tags(customer_ids, tag)` - Bulk add tags
- `bulk_delete_customer_tags(customer_ids, tag)` - Bulk delete tags
- `get_customer_id_change_history(customer_id)` - Get ID change history
- `export_customer_csv(**filter_params)` - Export to CSV
- `export_optout_customers_csv(**filter_params)` - Export opt-out customers
- `export_hot_customers_csv(**filter_params)` - Export hot customers

### Sales Actions
- `create_sales_action(action_data)` - Create sales action
- `update_sales_action(action_id, data)` - Update sales action
- `list_sales_actions(**filter_params)` - List sales actions
- `get_sales_action_types()` - Get action types
- `get_sales_action_types_list()` - Get action types list

### Inquiries
- `get_inquiry(inquiry_id)` - Get inquiry details
- `delete_inquiry(inquiry_id)` - Delete inquiry
- `send_inquiry_notification_email(data)` - Send notification email

### Employees
- `invite_employee(email, **kwargs)` - Invite employee
- `update_employee_status(employee_id, status)` - Update employee status

### Agent Assignment
- `assign_agent_by_postal_code(postal_code)` - Auto-assign by postal code