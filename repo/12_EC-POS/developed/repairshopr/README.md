# RepairShopr Client

A Python client for the RepairShopr REST API, providing complete access to repair shop management including tickets, customers, inventory, invoicing, and more.

## Features

- **Tickets**: create and manage repair tickets
- **Customers**: Customer management
- **Products**: Inventory and product management
- **Services**: Service catalog management
- **Invoices**: Create and send invoices
- **Estimates**: Generate and convert to invoices
- **Lead Sources**: Track customer sources
- **Search**: Global search across resources

## Installation

```bash
pip install -r requirements.txt
```

## API Key Setup

### Getting API Credentials

1. Log into your [RepairShopr Dashboard](https://app.repairshopr.com/)
2. Go to **Settings → API Keys**
3. Click **Generate New API Key**
4. Copy the generated API token

### Environment Variables

```bash
export REPAIRSHOPR_API_KEY="your_api_token"
export REPAIRSHOPR_BASE_URL="https://app.repairshopr.com/api"  # Optional, default already set
```

## Usage Example

```python
from repairshopr import RepairShoprClient

# Initialize client
client = RepairShoprClient(api_key="xxxxx")

# List tickets
tickets = client.list_tickets(status_id="status123")
print(f"Found {len(tickets['tickets'])} tickets")

# Get specific ticket
ticket = client.get_ticket("ticket456")

# Create ticket
new_ticket = client.create_ticket({
    "customer_id": "cust123",
    "status_id": "status456",
    "subject": "iPhone Screen Repair",
    "description": "Customer needs screen replacement",
    "device_brand_id": "apple",
    "device_model_id": "iphone11",
    "device_serial": "DNLXKXXXXX"
})

# Update ticket status
updated = client.update_ticket_status(ticket_id="ticket456", status_id="status789")

# Ticket items
items = client.list_ticket_items(ticket_id="ticket456")

# Add line item
new_item = client.create_ticket_item(ticket_id="ticket456", {
    "service_id": "service123",
    "quantity": 1,
    "price": 89.99,
    "name": "Screen Replacement Service"
})

# Customers
customers = client.list_customers(search="John Doe")
customer = client.get_customer("cust123")

# Create customer
new_customer = client.create_customer({
    "first_name": "Jane",
    "last_name": "Smith",
    "email": "jane@example.com",
    "phone": "+1234567890",
    "address": "456 Oak Ave",
    "city": "Los Angeles",
    "state": "CA",
    "zip": "90001",
    "business_name": "Jane Services",
    "notes": "Preferred customer"
})

# Products
products = client.list_products(category_id="cat123")
product = client.get_product("prod456")

# Create product
new_product = client.create_product({
    "name": "iPhone Screen",
    "sku": "SCREEN-IP11",
    "category_id": "cat123",
    "cost": 45.00,
    "price": 89.99,
    "quantity": 50,
    "description": "Replacement screen for iPhone 11"
})

# Adjust inventory
adjusted = client.adjust_product_inventory(
    product_id="prod456",
    quantity=-5,
    note="Repairs completed"
)

# Services
services = client.list_services()
service = client.get_service("svc123")

# Create service
new_service = client.create_service({
    "name": "Screen Replacement",
    "price": 89.99,
    "duration": 45,
    "taxable": True,
    "description": "Professional screen replacement service"
})

# Invoices
invoices = client.list_invoices(customer_id="cust123")
invoice = client.get_invoice("inv789")

# Convert ticket to invoice
created_invoice = client.convert_ticket_to_invoice(ticket_id="ticket456")

# Email invoice
client.email_invoice(invoice_id="inv789")

# Estimates
estimates = client.list_estimates()
estimate = client.get_estimate("est456")

# Convert estimate to invoice
client.convert_estimate_to_invoice(estimate_id="est456")

# Lead sources
lead_sources = client.list_lead_sources()

# Statuses
statuses = client.list_statuses()
status = client.get_status("status123")

# Brands
brands = client.list_brands()

# Locations
locations = client.list_locations()

# Staff
staff = client.list_staff()

# Search
results = client.search("John Doe")
results = client.search("iPhone", resource="tickets")

# Account info
account = client.get_account_info()

# Use context manager
with RepairShoprClient(api_key="xxxxx") as client:
    tickets = client.list_tickets()
    customers = client.list_customers()
    products = client.list_products()
```

## API Documentation

For complete API reference, see: https://www.repairshopr.com/api/

### Key Endpoints

| Resource | Methods |
|----------|---------|
| Tickets | list_tickets, get_ticket, create_ticket, update_ticket, delete_ticket |
| Ticket Items | list_ticket_items, create_ticket_item, update_ticket_item, delete_ticket_item |
| Customers | list_customers, get_customer, create_customer, update_customer, delete_customer |
| Products | list_products, get_product, create_product, update_product, adjust_product_inventory |
| Services | list_services, get_service, create_service, update_service |
| Invoices | list_invoices, get_invoice, convert_ticket_to_invoice, email_invoice |
| Estimates | list_estimates, get_estimate, convert_estimate_to_invoice |
| Lead Sources | list_lead_sources |
| Statuses | list_statuses, get_status |
| Brands | list_brands |
| Locations | list_locations |
| Staff | list_staff |

## Requirements

- Python 3.7+
- requests>=2.31.0

## License

MIT License