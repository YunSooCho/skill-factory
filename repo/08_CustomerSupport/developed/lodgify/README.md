# Lodgify Reservation Management Integration

Lodgify provides vacation rental reservation and property management.

## Installation
```bash
pip install -e .
```

## API Key Setup
1. Log in to Lodgify account
2. Generate API key from settings

## Usage
```python
from lodgify import LodgifyClient

client = LodgifyClient(api_key="your-key")

# Get reservations
reservations = client.get_reservations(property_id="PROP123")

# Get reservation
res = client.get_reservation("RES456")

# Create reservation
client.create_reservation({
    "property_id": "PROP123",
    "guest_id": "GUEST789",
    "arrival": "2024-06-01",
    "departure": "2024-06-07"
})

# Update reservation
client.update_reservation("RES456", {"status": "confirmed"})

# Get properties
properties = client.get_properties()

# Get availability
availability = client.get_availability("PROP123", "2024-06-01", "2024-06-30")

# Get guests
guests = client.get_guests()
```

## API Methods
- `get_reservations(property_id, limit)` - List reservations
- `get_reservation(reservation_id)` - Get reservation
- `create_reservation(data)` - Create reservation
- `update_reservation(reservation_id, data)` - Update reservation
- `get_properties()` - List properties
- `get_property(property_id)` - Get property
- `get_guests(limit)` - List guests
- `get_guest(guest_id)` - Get guest
- `get_availability(property_id, start_date, end_date)` - Check availability