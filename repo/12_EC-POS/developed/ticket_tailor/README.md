# Ticket Tailor Client

A Python client for the Ticket Tailor REST API, providing complete access to event management, ticket sales, orders, and attendee check-in.

## Features

- **Events**: Create and manage events
- **Tickets**: Configure ticket types and pricing
- **Orders**: Complete order management and processing
- **Attendees**: Manage attendee information and check-ins
- **Venues**: Create and manage event venues
- **Discounts**: Create promo codes and discounts
- **Webhooks**: Subscribe to event and order notifications
- **Analytics**: Sales summaries and attendee statistics

## Installation

```bash
pip install -r requirements.txt
```

## API Key Setup

### Getting API Credentials

1. Log into your [Ticket Tailor Dashboard](https://app.tickettailor.com/manage)
2. Go to **Settings → API**
3. Click **Generate API Key**
4. Copy the generated API key

### Environment Variables

Set the following environment variable:

```bash
export TICKETTAILOR_API_KEY="your_api_key_from_dashboard"
```

## Usage Example

```python
from ticket_tailor import TicketTailorClient

# Initialize client
client = TicketTailorClient(api_key="xxxxx")

# List events
events = client.list_events(status="upcoming")
print(f"Upcoming events: {events['data']}")

# Get specific event
event = client.get_event("event123")
print(f"Event: {event['name']}")

# Create a new event
new_event = client.create_event({
    "name": "Music Festival 2024",
    "start_date": "2024-07-15T18:00:00Z",
    "end_date": "2024-07-15T23:00:00Z",
    "venue": {
        "name": "Grand Arena",
        "address": {
            "line1": "123 Main St",
            "city": "New York",
            "state": "NY",
            "postcode": "10001",
            "country": "US"
        }
    },
    "description": "<p>Amazing music event</p>",
    "is_virtual": False
})
print(f"Created event: {new_event['id']}")

# Update event
updated = client.update_event(event_id="event123", {
    "name": "Updated Event Name"
})

# List tickets for event
tickets = client.list_event_tickets(event_id="event123")

# Create ticket type
new_ticket = client.create_ticket(event_id="event123", {
    "name": "General Admission",
    "price": 5000,  # $50.00 in cents
    "max_per_order": 10,
    "total_quantity": 500,
    "description": "General admission ticket",
    "display_order": 1
})

# Update ticket
updated_ticket = client.update_ticket(ticket_id="ticket123", {
    "price": 4500,  # Change to $45.00
    "total_quantity": 600
})

# List orders
orders = client.list_orders(event_id="event123", status="paid")

# Get specific order
order = client.get_order("order456")

# Create order
new_order = client.create_order({
    "event_id": "event123",
    "currency": "USD",
    "status": "paid",
    "billing_address": {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "address_line1": "456 Oak Ave",
        "city": "Los Angeles",
        "state": "CA",
        "postcode": "90001",
        "country": "US"
    },
    "tickets": [{
        "ticket_id": "ticket123",
        "quantity": 2,
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com"
    }]
})

# Refund order
refunded = client.refund_order(order_id="order456", reason="Customer request")

# Cancel order
cancelled = client.cancel_order(order_id="order456")

# List attendees
attendees = client.list_attendees(
    event_id="event123",
    status="active",
    page=1,
    per_page=50
)

# Get specific attendee
attendee = client.get_attendee("attendee789")

# Update attendee
updated_attendee = client.update_attendee(attendee_id="attendee789", {
    "first_name": "Jane",
    "last_name": "Smith",
    "email": "jane@example.com"
})

# Check in attendee
checked_in = client.check_in_attendee("attendee789")

# Undo check-in
undone = client.undo_check_in("attendee789")

# Bulk check-in multiple attendees
bulk_checked = client.bulk_check_in([
    "attendee001",
    "attendee002",
    "attendee003"
])

# Venues
venues = client.list_venues()
venue = client.get_venue("venue123")

# Create venue
new_venue = client.create_venue({
    "name": "Music Hall",
    "address": {
        "line1": "789 Concert Blvd",
        "city": "Chicago",
        "state": "IL",
        "postcode": "60601",
        "country": "US"
    },
    "latitude": 41.8827,
    "longitude": -87.6233,
    "website": "https://musichall.com",
    "description": "World-class concert venue"
})

# Update venue
updated_venue = client.update_venue(venue_id="venue123", {
    "name": "Updated Venue Name"
})

# Organisation details
org = client.get_organisation()

# Update organisation
updated_org = client.update_organisation({
    "name": "My Event Company",
    "email": "contact@myevents.com",
    "phone": "+1234567890",
    "website": "https://myevents.com",
    "currency": "USD"
})

# Discounts/Promo codes
discounts = client.list_discounts(event_id="event123")

# Create discount
new_discount = client.create_discount({
    "code": "SUMMER20",
    "discount_type": "percentage",
    "discount_amount": 20,
    "event_id": "event123",
    "max_uses": 100,
    "expiry_date": "2024-12-31T23:59:59Z",
    "minimum_spend": 5000,  # $50 minimum
    "description": "20% off summer sale"
})

# Update discount
updated_discount = client.update_discount(discount_id="discount123", {
    "discount_amount": 25  # Change to 25%
})

# Delete discount
client.delete_discount(discount_id="discount123")

# Webhooks
webhooks = client.list_webhooks()

# Create webhook
new_webhook = client.create_webhook(
    url="https://your-server.com/webhooks/ticket-tailor",
    events=[
        "order.created",
        "order.refunded",
        "attendee.checked_in",
        "event.published"
    ],
    secret="your_webhook_secret",
    description="Event notifications"
)

# Update webhook
client.update_webhook(webhook_id="webhook123", {
    "url": "https://new-url.com/webhooks"
})

# Test webhook
test_result = client.test_webhook(webhook_id="webhook123")

# Delete webhook
client.delete_webhook(webhook_id="webhook123")

# Event series
series_list = client.list_series()
series = client.get_series(series_id="series456")
series_events = client.list_series_events(series_id="series456")

# Analytics
sales_summary = client.get_event_sales_summary(event_id="event123")
print(f"Total sales: {sales_summary['total_sales']}")

attendee_stats = client.get_attendee_statistics(event_id="event123")
print(f"Total attendees: {attendee_stats['total_attendees']}")

# Sales summary with date range
sales_with_date = client.get_event_sales_summary(
    event_id="event123",
    from_date="2024-01-01T00:00:00Z",
    to_date="2024-12-31T23:59:59Z"
)

# Use context manager
with TicketTailorClient(api_key="xxxxx") as client:
    events = client.list_events()
    orders = client.list_orders()
    attendees = client.list_attendees()
```

## Webhook Events

Available webhook event types:

### Orders
- `order.created` - New order created
- `order.updated` - Order updated
- `order.refunded` - Order refunded
- `order.cancelled` - Order cancelled

### Attendees
- `attendee.checked_in` - Attendee checked in
- `attendee.check_in_undo` - Check-in undone

### Events
- `event.published` - Event published
- `event.unpublished` - Event unpublished

### Discounts
- `discount.created` - Discount created
- `discount.updated` - Discount updated
- `discount.deleted` - Discount deleted

## Discount Types

- **percentage**: Percentage-based discount
- **fixed**: Fixed amount discount

## Order Status Flow

The order lifecycle:

1. **pending**: Order created, payment pending
2. **paid**: Payment successful
3. **refunded**: Order refunded
4. **cancelled**: Order cancelled

## API Documentation

For complete API reference, see: https://developers.tickettailor.com/

### Key Endpoints

| Resource | Methods |
|----------|---------|
| Events | list_events, get_event, create_event, update_event |
| Tickets | list_tickets, get_ticket, create_ticket, update_ticket, delete_ticket |
| Orders | list_orders, get_order, create_order, update_order, refund_order, cancel_order |
| Attendees | list_attendees, get_attendee, update_attendee, check_in_attendee, undo_check_in, bulk_check_in |
| Venues | list_venues, get_venue, create_venue, update_venue |
| Discounts | list_discounts, get_discount, create_discount, update_discount, delete_discount |
| Webhooks | list_webhooks, get_webhook, create_webhook, update_webhook, delete_webhook, test_webhook |
| Series | list_series, get_series, list_series_events |
| Organisation | get_organisation, update_organisation |
| Analytics | get_event_sales_summary, get_attendee_statistics |

## Notes

- Maximum items per page is 100
- Prices are in cents (e.g., $50.00 = 5000)
- All dates should be in ISO 8601 format
- Currency codes should follow ISO 4217 (e.g., USD, EUR, GBP)
- Check-ins can be done individually or in bulk
- Webhook secrets can be used to verify event authenticity
- Tickets can have quantity limits per order

## Check-in Workflow

```python
# Get all unchecked-in attendees for an event
attendees = client.list_attendees(
    event_id="event123",
    check_in=False,
    status="active"
)

# Check in individual attendee
client.check_in_attendee(attendee_id)

# Or bulk check-in
ids = [a['id'] for a in attendees['data'][:100]]
client.bulk_check_in(ids)
```

## Requirements

- Python 3.7+
- requests>=2.31.0

## License

MIT License