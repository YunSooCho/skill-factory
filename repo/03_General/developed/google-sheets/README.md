# Google Sheets API Client

A comprehensive Python client for Google Sheets API v4, providing access to 21 API actions and webhook trigger support.

## Features

- ✅ **21 API Actions**: Full coverage of Google Sheets operations
- 🔄 **2 Webhook Triggers**: Integration with row-added and row-updated events
- 🛡️ **Error Handling**: Comprehensive HTTP error handling with contextual logging
- 🚦 **Rate Limiting**: Built-in rate limiter to respect API quotas
- 🔐 **OAuth 2.0 Authentication**: Secure credential management
- 📝 **Type Hints**: Complete type annotations for better IDE support

## Installation

```bash
pip install -r requirements.txt
```

## Authentication

Google Sheets requires OAuth 2.0 authentication. Choose one of three methods:

### Method 1: Dictionary Credentials

```python
from google_sheets_client import GoogleSheetsClient

client = GoogleSheetsClient(
    credentials={
        'access_token': 'ya29.a0Af...',
        'refresh_token': '1//0g...',
        'client_id': 'your-client-id.apps.googleusercontent.com',
        'client_secret': 'your-client-secret'
    }
)
```

### Method 2: Token File

```python
client = GoogleSheetsClient(token_file='token.pickle')
```

### Method 3: OAuth 2.0 Flow (Interactive)

```python
client = GoogleSheetsClient(
    credentials_file='client_secret.json'
)
# This will open a browser for OAuth consent
```

### Setting up Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable the Google Sheets API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download `client_secret.json`

## API Actions

### Spreadsheet Management

#### 1. Create Spreadsheet
```python
response = client.create_spreadsheet(
    title="My New Sheet",
    sheets=[
        {"title": "Data", "rowCount": 1000, "colCount": 26}
    ]
)
print(response['spreadsheetId'])
```

#### 2. Get Spreadsheet Info
```python
info = client.get_spreadsheet_info(spreadsheet_id)
print(info['title'])
print([s['title'] for s in info['sheets']])
```

### Sheet Operations

#### 3. Add Sheet
```python
client.add_sheet(
    spreadsheet_id=spreadsheet_id,
    title="New Tab",
    rows=500,
    columns=20
)
```

#### 4. Delete Sheet
```python
client.delete_sheet(
    spreadsheet_id=spreadsheet_id,
    sheet_name="Old Sheet"
)
```

#### 5. Copy Sheet
```python
client.copy_sheet(
    spreadsheet_id=spreadsheet_id,
    sheet_name="Template",
    new_title="Copy of Template"
)
```

#### 6. Rename Sheet
```python
client.rename_sheet(
    spreadsheet_id=spreadsheet_id,
    sheet_name="Old Name",
    new_title="New Name"
)
```

#### 7. Get Sheet Names
```python
sheets = client.get_sheet_names(spreadsheet_id)
for sheet in sheets:
    print(f"{sheet['sheetId']}: {sheet['title']}")
```

#### 8. Hide Sheet
```python
client.hide_sheet(
    spreadsheet_id=spreadsheet_id,
    sheet_name="Hidden Data"
)
```

### Cell Operations

#### 9. Get Values
```python
values = client.get_values(
    spreadsheet_id=spreadsheet_id,
    range_a1='Sheet1!A1:C10'
)
print(values['values'])
```

#### 10. Set Single Value
```python
client.set_value(
    spreadsheet_id=spreadsheet_id,
    range_a1='Sheet1!A1',
    value="Hello World"
)
```

#### 11. Set Values in Range
```python
client.set_values_in_range(
    spreadsheet_id=spreadsheet_id,
    range_a1='Sheet1!A1:D3',
    values=[
        ['Name', 'Age', 'City'],
        ['Alice', 30, 'Tokyo'],
        ['Bob', 25, 'New York']
    ]
)
```

#### 12. Set Values in Multiple Columns
```python
client.set_values_in_columns(
    spreadsheet_id=spreadsheet_id,
    start_column='A',
    column_values={
        'A': ['Item1', 'Item2', 'Item3'],
        'B': [100, 200, 300],
        'C': ['Desc1', 'Desc2', 'Desc3']
    }
)
```

#### 13. Delete Values
```python
client.delete_values(
    spreadsheet_id=spreadsheet_id,
    range_a1='Sheet1!A1:D10'
)
```

#### 14. Replace Values
```python
client.replace_values(
    spreadsheet_id=spreadsheet_id,
    range_a1='Sheet1!A1:Z1000',
    find_value="Old Text",
    replace_value="New Text",
    match_case=False
)
```

#### 15. Add Note
```python
client.add_note(
    spreadsheet_id=spreadsheet_id,
    cell='B5',
    note='Important: Check this value'
)
```

#### 16. Embed Image
```python
client.embed_image(
    spreadsheet_id=spreadsheet_id,
    url='https://example.com/logo.png',
    position={'rowIndex': 0, 'columnIndex': 0},
    size={'height': 100, 'width': 100}
)
```

### Row & Column Operations

#### 17. Add Rows
```python
client.add_rows(
    spreadsheet_id=spreadsheet_id,
    sheet_name="Data",
    insert_at=5,  # Insert at row 6 (0-indexed)
    number_of_rows=10
)
```

#### 18. Delete Rows
```python
client.delete_rows(
    spreadsheet_id=spreadsheet_id,
    sheet_name="Data",
    start_index=5,  # Start at row 6 (0-indexed)
    number_of_rows=3
)
```

#### 19. Add Columns
```python
client.add_columns(
    spreadsheet_id=spreadsheet_id,
    sheet_name="Data",
    insert_at=2,  # Insert after column C
    number_of_columns=2
)
```

#### 20. Delete Columns
```python
client.delete_columns(
    spreadsheet_id=spreadsheet_id,
    sheet_name="Data",
    start_index=2,  # Start at column C
    number_of_columns=1
)
```

#### 21. Sort by Column
```python
client.sort_by_column(
    spreadsheet_id=spreadsheet_id,
    range_a1='Sheet1!A2:Z1000',
    sort_column=0,  # Sort by first column (A)
    ascending=True
)
```

## Webhook Triggers

Google Sheets doesn't provide native webhooks. Two options:

### Option 1: Google Apps Script

```python
from google_sheets_client import GoogleSheetsWebhooks

config = GoogleSheetsWebhooks.setup_webhook_handler(
    spreadsheet_id=spreadsheet_id,
    trigger_config={'webhook_url': 'https://your-server.com/webhook'}
)

print(config['sample_code'])
```

Deploy this in Google Apps Script Editor:

```javascript
function onEdit(e) {
  var webhook_url = "YOUR_WEBHOOK_URL";
  var data = {
    spreadsheet_id: e.range.getSheet().getParent().getId(),
    sheetName: e.range.getSheet().getName(),
    editedRange: e.range.getA1Notation(),
    old_value: e.oldValue || "",
    new_value: e.value,
    timestamp: new Date().toISOString()
  };
  
  UrlFetchApp.fetch(webhook_url, {
    method: "post",
    contentType: "application/json",
    payload: JSON.stringify(data)
  });
}
```

### Option 2: Polling

```python
# Periodically check for changes
import time

last_values = None
while True:
    current = client.get_values(spreadsheet_id, 'Sheet1!A1:Z1000')
    if last_values and current['values'] != last_values:
        # Detect changes
        pass
    last_values = current['values']
    time.sleep(60)  # Check every minute
```

## Rate Limiting

The client includes automatic rate limiting:

- **Default**: 100 calls per 100 seconds
- Adjust via: `GoogleSheetsClient().rate_limiter.max_calls = 200`

The rate limiter automatically:
- Tracks API call timestamps
- Sleeps when approaching limits
- Resets counters after the period

## Error Handling

The client provides detailed error logging:

```python
try:
    client.set_value(spreadsheet_id, 'Sheet1!A1', 'value')
except Exception as e:
    # Errors are already logged with context
    # Check logs for detailed information
    pass
```

Common errors:
- `401`: Authentication failed → Refresh credentials
- `403`: Permission denied → Check sharing settings
- `404`: Not found → Verify spreadsheet_id
- `429`: Rate limit exceeded → Reduce call frequency

## Advanced Usage

### Batch Operations

For multiple writes, use `set_values_in_range` instead of multiple `set_value` calls:

```python
# ❌ Slow - multiple API calls
client.set_value(spreadsheet_id, 'A1', 'v1')
client.set_value(spreadsheet_id, 'A2', 'v2')
client.set_value(spreadsheet_id, 'A3', 'v3')

# ✅ Fast - single API call
client.set_values_in_range(
    spreadsheet_id,
    'A1:A3',
    [['v1'], ['v2'], ['v3']]
)
```

### Using Array Formulas

For `repeat_formula` operation, use array formulas:

```python
client.set_value(
    spreadsheet_id,
    'B1',
    '=ArrayFormula(A1:A100*2)'
)
```

This automatically fills down the column.

## Testing

```python
# Test connection
client = GoogleSheetsClient(token_file='token.pickle')
info = client.get_spreadsheet_info('your-spreadsheet-id')
print(f"Connected to: {info['title']}")
```

## Limitations

- **Webhooks**: Google Sheets doesn't support native webhooks. Use Google Apps Script or polling.
- **Formulas**: Complex formulas may require manual testing in the Sheets UI.
- **Batch Size**: Maximum 10,000 cells per request for `update` operations.

## License

MIT License

## Support

For issues or questions:
- Check Google Sheets API documentation: https://developers.google.com/sheets/api
- Review error logs in your application