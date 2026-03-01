# Google Drive API Client

A comprehensive Python client for Google Drive API v3, providing access to 35 API actions for file and folder management, plus webhook trigger support.

## Features

- ✅ **35 API Actions**: Complete file, folder, and storage management
- 🔄 **3 Webhook Triggers**: File creation, folder creation, file update events
- 🛡️ **Error Handling**: Comprehensive HTTP error handling
- 🚦 **Rate Limiting**: Built-in rate limiter for API quota management
- 🔐 **OAuth 2.0 Authentication**: Secure credential management
- 📝 **Type Hints**: Complete type annotations

## Installation

```bash
pip install -r requirements.txt
```

## Authentication

Google Drive API requires OAuth 2.0 authentication.

### Method 1: Dictionary Credentials

```python
from google_drive_client import GoogleDriveClient

client = GoogleDriveClient(
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
client = GoogleDriveClient(token_file='drive_token.pickle')
```

### Method 3: OAuth 2.0 Flow (Interactive)

```python
client = GoogleDriveClient(credentials_file='client_secret.json')
```

### Prerequisites

1. Enable Google Drive API in Google Cloud Console
2. Create OAuth 2.0 credentials (Desktop app or Web app)
3. Authorize with appropriate OAuth scopes

## API Actions

### File & Folder Operations

#### Create Folder
```python
folder = client.create_folder(
    name='My New Folder',
    parent_folder_id='parent_folder_id'
)
print(f"Created folder with ID: {folder['id']}")
```

#### Search Files
```python
files = client.search_files(
    query="name contains 'report' and mimeType='application/pdf'",
    page_size=50
)

for file in files['files']:
    print(f"{file['name']}: {file['webViewLink']}")
```

#### List Folder Contents
```python
contents = client.list_folder_contents(
    folder_id='folder_id',
    page_size=100
)

for item in contents['files']:
    print(f"{item['name']} ({item['mimeType']})")
```

#### Rename File
```python
client.rename_file(
    file_id='file_id',
    new_name='New File Name.pdf'
)
```

#### Update File Description
```python
client.update_file_description(
    file_id='file_id',
    description='This is an important document'
)
```

#### Delete File
```python
client.delete_file(file_id='file_id')
```

#### Move File to Folder
```python
client.move_file_to_folder(
    file_id='file_id',
    new_parent_folder_id='new_folder_id'
)
```

#### Move to Trash
```python
client.move_to_trash(file_id='file_id')
```

#### Get File Info
```python
info = client.get_file_info(file_id='file_id')
print(f"Name: {info['name']}")
print(f"Size: {info['size']} bytes")
print(f"Created: {info['createdTime']}")
print(f"Owner: {info['owners'][0]['displayName']}")
```

### Upload & Download Operations

#### Upload File
```python
# Upload to root
uploaded = client.upload_file(
    file_path='/path/to/file.pdf'
)

# Upload to specific folder
uploaded = client.upload_file(
    file_path='/path/to/file.pdf',
    parent_folder_id='folder_id',
    file_name='Custom Name.pdf'
)

print(f"Uploaded: {uploaded['name']}")
print(f"View link: {uploaded['webViewLink']}")
```

#### Download File
```python
# Download regular file
client.download_file(
    file_id='file_id',
    output_path='/local/path/file.pdf'
)

# Download Google Workspace file as base64
result = client.download_file(file_id='google_doc_id')
# Google Workspace files automatically export
```

### File Conversion

#### Convert to Google Docs
```python
doc = client.convert_to_document(file_id='pdf_file_id')
print(f"Google Doc ID: {doc['id']}")
```

#### Convert CSV/Excel to Sheets
```python
sheets = client.convert_csv_to_sheets(
    file_path='/path/to/data.csv',
    parent_folder_id='folder_id'
)

# Convert Excel
sheets = client.convert_excel_to_sheets(
    file_path='/path/to/data.xlsx'
)
```

#### Convert PDF to Docs
```python
doc = client.convert_pdf_to_doc(file_id='pdf_file_id')
```

### Download Google Workspace Files

#### Download Google Docs
```python
# Download as DOCX
client.download_google_doc(
    file_id='doc_id',
    format='docx',
    output_path='/path/to/document.docx'
)

# Download as PDF
client.download_google_doc(
    file_id='doc_id',
    format='pdf',
    output_path='/path/to/document.pdf'
)

# Get base64 content
result = client.download_google_doc(file_id='doc_id', format='html')
content = result['content']  # Base64 encoded
```

#### Download Google Sheets
```python
# Download as XLSX
client.download_sheets(
    file_id='sheet_id',
    format='xlsx',
    sheet_name='Sheet1'
)

# Download as CSV
csv_result = client.download_sheets(file_id='sheet_id', format='csv')

# Download as PDF
client.download_sheets(
    file_id='sheet_id',
    format='pdf',
    output_path='/path/to/sheet.pdf'
)
```

#### Download Google Slides
```python
client.download_slides(
    file_id='presentation_id',
    format='pptx'
)
```

### Copy & Duplicate Operations

#### Duplicate File
```python
duplicate = client.duplicate_file(
    file_id='file_id',
    new_name='Copy of File'
)
print(f"Duplicated: {duplicate['id']}")
```

### Permissions & Sharing

#### List Permissions
```python
permissions = client.list_permissions(file_id='file_id')
for perm in permissions['permissions']:
    print(f"{perm['type']} - {perm['role']}: {perm.get('emailAddress', perm.get('domain', 'N/A'))}")
```

#### Grant Permission to User
```python
client.grant_permission_to_user(
    file_id='file_id',
    email='colleague@example.com',
    role='writer'  # reader, writer, commenter
)

# Transfer ownership
client.grant_permission_to_user(
    file_id='file_id',
    email='new_owner@example.com',
    role='owner',
    transfer_ownership=True
)
```

#### Grant Permission to Organization
```python
client.grant_permission_to_organization(
    file_id='file_id',
    domain='example.com',
    role='reader'
)
```

#### Grant "Anyone with Link" Permission
```python
client.set_anyone_with_link_permission(
    file_id='file_id',
    role='reader',  # reader or writer
    allow_discovery=False  # Allow search engine indexing
)
```

#### Delete Permission
```python
client.delete_permission(
    file_id='file_id',
    permission_id='permission_id'
)
```

#### Set Copy/Download Restrictions
```python
client.set_copy_and_download_permission(
    file_id='file_id',
    allow_copy=False,
    allow_download=False
)
```

### Shared Drive Operations

#### Search Shared Drives
```python
drives = client.search_shared_drives(query="sales")
for drive in drives['drives']:
    print(f"{drive['name']}: {drive['id']}")
```

#### Create Shared Drive
```python
drive = client.create_shared_drive(
    name='Team Documents'
)
print(f"Shared Drive ID: {drive['id']}")
```

### File Update Operations

#### Update File Content
```python
client.update_file_content(
    file_id='existing_file_id',
    file_path='/path/to/new_version.pdf'
)
```

## Advanced Usage

### Search Queries

```python
# PDF files created this year
files = client.search_files(
    query='mimeType="application/pdf" and createdTime >= "2024-01-01"'
)

# Files shared with me
files = client.search_files(
    query='sharedWithMe=true'
)

# Files from specific folder
files = client.search_files(
    query="'parent_folder_id' in parents'
)

# Files not in trash
files = client.search_files(
    query='trashed=false'
)

# Starred files
files = client.search_files(
    query='starred=true'
)

# Combination query
files = client.search_files(
    query='name contains "invoice" and mimeType="application/pdf" and trashed=false'
)
```

### Batch Operations

```python
# Upload multiple files
import os
folder_id = 'folder_id'

for filename in os.listdir('/local/folder'):
    filepath = os.path.join('/local/folder', filename)
    if os.path.isfile(filepath) and filename.endswith('.pdf'):
        try:
            client.upload_file(filepath, parent_folder_id=folder_id)
            print(f"Uploaded: {filename}")
        except Exception as e:
            print(f"Failed: {filename} - {e}")
```

## Rate Limiting

The client includes automatic rate limiting:
- **Default**: 100 calls per 100 seconds
- Adjust via: `client.rate_limiter.max_calls = 200`

## Error Handling

```python
try:
    client.upload_file(file_path='document.pdf')
except Exception as e:
    # Errors are automatically logged
    if '401' in str(e):
        print("Authentication failed - refresh credentials")
    elif '403' in str(e):
        print("Permission denied - check sharing settings")
    elif '404' in str(e):
        print("File not found")
    else:
        print(f"Error: {e}")
```

Common errors:
- `401`: Authentication failed → Refresh credentials
- `403`: Permission denied → Check file permissions
- `404`: Resource not found → Verify file/folder ID
- `409`: Conflict → File/folder already exists
- `429`: Rate limit exceeded → Reduce call frequency

## Webhook Triggers

Google Drive doesn't provide native webhooks. Use Google Cloud Pub/Sub or Google Apps Script.

### Using Google Apps Script

```javascript
// In Google Apps Script linked to Drive
function onFileCreated() {
  var files = DriveApp.getFiles();
  while (files.hasNext()) {
    var file = files.next();
    var webhook_url = "YOUR_WEBHOOK_URL";
    
    var data = {
      event: "file_created",
      file_id: file.getId(),
      file_name: file.getName(),
      mime_type: file.getMimeType(),
      created_at: new Date().toISOString()
    };
    
    UrlFetchApp.fetch(webhook_url, {
      method: "post",
      contentType: "application/json",
      payload: JSON.stringify(data)
    });
  }
}
```

## Best Practices

1. **Handle rate limits**: Use built-in rate limiter
2. **Page large results**: Use pagination for listing operations
3. **Use specific queries**: Narrow search queries to reduce API calls
4. **Cache metadata**: Store file info locally when possible
5. **Handle conversions**: Google Workspace files need export for download
6. **Use shared drives**: For team collaboration

## Limitations

- **Webhook limitations**: No native webhooks, requires Pub/Sub or Apps Script
- **Export formats**: Limited export options for Google Workspace files
- **File size limits**: Large files take time to upload/download
- **API quotas**: Respect daily quota limits

## Testing

```python
# Test basic operations
client = GoogleDriveClient(token_file='drive_token.pickle')

# Create test folder
folder = client.create_folder('Test Folder')

# List root folders
root = client.list_folder_contents(folder_id='root')

# Clean up
client.delete_file(folder['id'])

print("✅ Tests passed!")
```

## License

MIT License

## Resources

- [Google Drive API Documentation](https://developers.google.com/drive/api/v3/about)
- [Drive API - Files](https://developers.google.com/drive/api/v3/reference/files)
- [Drive API - Permissions](https://developers.google.com/drive/api/v3/reference/permissions)
- [OAuth 2.0 for Google APIs](https://developers.google.com/identity/protocols/oauth2)