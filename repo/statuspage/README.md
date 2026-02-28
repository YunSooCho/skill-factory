# Statuspage

Statuspage is a platform for creating and managing status pages for your services.

## Installation

```bash
pip install -r requirements.txt
```

## API Key

To get your Statuspage API key:

1. Sign up at [Statuspage](https://statuspage.io)
2. Go to Settings > API Key
3. Copy your API key and Page ID

## Usage

```python
from statuspage import StatuspageClient

client = StatuspageClient(api_key='your-api-key', page_id='your-page-id')

# Create an incident
incident = client.create_incident({
    'name': 'Service Outage',
    'status': 'investigating',
    'body': 'We are investigating an issue with our API',
    'incident_updates': [{
        'status': 'investigating',
        'body': 'Investigation started'
    }]
})

# Update an incident
updated = client.update_incident(
    incident_id='incident-123',
    data={
        'status': 'identified',
        'body': 'We have identified the issue'
    }
)

# Create scheduled maintenance
maintenance = client.create_scheduled_maintenance({
    'name': 'System Maintenance',
    'start_time': '2024-03-01T02:00:00Z',
    'end_time': '2024-03-01T04:00:00Z',
    'description': 'Scheduled system maintenance'
})

# Search subscribers
subscribers = client.search_subscribers(query='john@example.com')

# Search incidents
incidents = client.search_incidents(query='API')
```

## API Methods

### Incidents
- `create_incident(incident_data)` - Create an incident
- `update_incident(incident_id, data)` - Update an incident
- `search_incidents(query)` - Search incidents

### Scheduled Maintenance
- `create_scheduled_maintenance(maintenance_data)` - Create scheduled maintenance

### Subscribers
- `search_subscribers(query)` - Search subscribers