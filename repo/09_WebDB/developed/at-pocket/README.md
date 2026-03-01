# Airtable Pocket Integration

Airtable Pocket is the mobile app companion for Airtable that enables quick data capture, offline access, QR code scanning, rich media capture, and geolocation features.

## Installation
```bash
pip install -e .
```

## API Token Setup

1. Sign up at [airtable.com](https://airtable.com)
2. Generate an API token from Account Settings
3. Install Airtable Pocket mobile app and sign in
4. Use the same API token for programmatic access

## Usage

### Initialize Client

```python
from at_pocket import PocketClient

client = PocketClient(api_token="your-api-token")
```

### Quick Capture

```python
BASE_ID = "appXXX"
TABLE_ID = "tblXXX"

# Quick capture a record from Pocket
record = client.quick_capture(
    BASE_ID,
    TABLE_ID,
    data={
        "Title": "Task from mobile",
        "Status": "Pending",
        "Priority": "High"
    },
    source="pocket"
)
```

### Notes and Attachments

```python
# Add a text note
client.add_note(
    BASE_ID,
    TABLE_ID,
    "recXXX",
    note="Important follow-up needed",
    note_type="text"
)

# Add a photo
client.add_photo(
    BASE_ID,
    TABLE_ID,
    "recXXX",
    photo_url="https://example.com/photo.jpg",
    caption="Site inspection photo"
)

# Add a voice note with transcription
client.add_voice_note(
    BASE_ID,
    TABLE_ID,
    "recXXX",
    audio_url="https://example.com/audio.mp3",
    transcription="Meeting summary notes"
)
```

### QR Code Scanning

```python
# Scan QR code to find matching record
result = client.scan_qr_code(
    BASE_ID,
    TABLE_ID,
    qr_data="QRCODE123",
    lookup_field="QR Code"
)
```

### Offline Access

```python
# Get records for offline use
offline_records = client.get_offline_records(BASE_ID, TABLE_ID)

# Sync offline changes
client.sync_offline_changes(
    BASE_ID,
    TABLE_ID,
    changes=[
        {
            "id": "recXXX",
            "fields": {"Status": "Complete"},
            "type": "update"
        }
    ]
)

# Check sync status
status = client.get_sync_status(BASE_ID, TABLE_ID)
print(f"Last synced: {status['lastSync']}")
```

### Form Submissions

```python
# Submit form from Pocket with location
client.create_form_submission(
    BASE_ID,
    "frmXXX",
    submission_data={
        "Name": "John Doe",
        "Email": "john@example.com",
        "Feedback": "Great service!"
    },
    location={
        "lat": 37.7749,
        "lng": -122.4194,
        "accuracy": 10
    }
)
```

### Geolocation

```python
# Find nearby records
nearby = client.get_nearby_records(
    BASE_ID,
    TABLE_ID,
    location={"lat": 37.7749, "lng": -122.4194},
    radius=1000,  # 1000 meters
    location_field="Location"
)
```

### Background Sync

```python
# Configure background sync
client.set_background_sync(
    BASE_ID,
    TABLE_ID,
    enabled=True,
    interval=300  # 5 minutes
)
```

### Pocket Templates

```python
# Get capture templates
templates = client.get_pocket_templates(BASE_ID, TABLE_ID)

# Create a new template
client.create_pocket_template(
    BASE_ID,
    TABLE_ID,
    name="Site Inspection",
    fields=[
        {"id": "fld1", "name": "Site Name", "type": "text", "required": True},
        {"id": "fld2", "name": "Inspection Type", "type": "select", "options": ["Monthly", "Quarterly"]},
        {"id": "fld3", "name": "Photo Required", "type": "photo"},
        {"id": "fld4", "name": "Notes", "type": "textarea"}
    ]
)
```

### Activity Tracking

```python
# Get recent Pocket activity
activity = client.get_recent_activity(BASE_ID, TABLE_ID, limit=20)
for item in activity:
    print(f"{item['action']} by {item['user']} at {item['timestamp']}")
```

## API Methods

### Data Capture
- `quick_capture(base_id, table_id, data, source)` - Quick create record
- `scan_qr_code(base_id, table_id, qr_data, lookup_field)` - QR code lookup

### Notes & Media
- `add_note(base_id, table_id, record_id, note, note_type)` - Add text note
- `add_photo(base_id, table_id, record_id, photo_url, caption)` - Add photo
- `add_voice_note(base_id, table_id, record_id, audio_url, transcription)` - Add voice note

### Offline Sync
- `get_offline_records(base_id, table_id, last_sync)` - Get records for offline
- `sync_offline_changes(base_id, table_id, changes)` - Sync offline changes
- `get_sync_status(base_id, table_id)` - Check sync status
- `set_background_sync(base_id, table_id, enabled, interval)` - Configure sync

### Forms
- `create_form_submission(base_id, form_id, submission_data, location)` - Submit form

### Geolocation
- `get_nearby_records(base_id, table_id, location, radius, location_field)` - Find nearby records

### Templates
- `get_pocket_templates(base_id, table_id)` - List capture templates
- `create_pocket_template(base_id, table_id, name, fields)` - Create template

### Activity
- `get_recent_activity(base_id, table_id, limit)` - Get recent activity

## Pocket Features

### Rich Media Capture
- Photos with captions
- Voice notes with automatic transcription
- Text notes
- Document attachments

### Geolocation Features
- GPS coordinates capture
- Nearby record lookup
- Location-based form submissions
- Distance calculations

### Offline Capabilities
- Download data for offline use
- Capture data while offline
- Auto-sync when connected
- Conflict resolution

### QR Code Operations
- Scan QR codes to find records
- Generate QR codes from records
- Batch QR code operations

## Best Practices

1. **GPS accuracy**: Check GPS accuracy before relying on location data
2. **Offline sync**: Sync regularly to avoid data loss
3. **Media sizes**: Compress large photos/audio before uploading
4. **Template design**: Design templates for optimal mobile input
5. **Background sync**: Configure sensible intervals to balance battery and freshness
6. **Error handling**: Handle network failures gracefully for offline scenarios