# Canva API Client

Python async client for Canva's design platform API.

## Features

- ✅ List folders and folder items
- ✅ Search designs
- ✅ Get design download links
- ✅ Create folders
- ✅ Move folder items
- ✅ Rename folders
- ✅ Create export jobs
- ✅ Get export job status
- ✅ Webhook verification (Design Updated)
- ✅ Async/await support
- ✅ Type hints and dataclasses

## Installation

```bash
pip install -r requirements.txt
```

## API Key

Get your API key from: https://www.canva.com/developers/

## Usage

### Initialize Client

```python
import asyncio
from canva_client import CanvaAPIClient

async def main():
    api_key = "your-api-key-here"

    async with CanvaAPIClient(api_key) as client:
        # Use the client
        pass

asyncio.run(main())
```

### List Folders

List all folders in your Canva workspace.

```python
async with CanvaAPIClient(api_key) as client:
    result = await client.list_folders(limit=50)

    print(f"Found {result['total']} folders:")
    for folder in result['folders']:
        print(f"  - {folder.name} ({folder.id})")
```

### List Folder Items

List designs and subfolders in a folder.

```python
async with CanvaAPIClient(api_key) as client:
    result = await client.list_folder_items(
        folder_id="folder-123",
        item_type="design",  # Optional: 'design' or 'folder'
        limit=50
    )

    print(f"Items: {result['total']}")
    for item in result['items']:
        print(f"  [{item.type}] {item.name}")
```

### Search Design

Search for designs by name or content.

```python
async with CanvaAPIClient(api_key) as client:
    result = await client.search_design(
        query="marketing",
        folder_id="folder-123",  # Optional: search within folder
        limit=20
    )

    print(f"Found {result.total} designs:")
    for design in result.designs:
        print(f"  - {design.name}")
        print(f"    Type: {design.design_type}")
        print(f"    URL: {design.design_url}")
```

### Get Design Download Link

Get a download link for a design.

```python
async with CanvaAPIClient(api_key) as client:
    link = await client.get_design_download_link(
        design_id="design-123",
        format="pdf",  # 'pdf', 'png', 'jpg'
        quality="standard"  # 'standard' or 'high'
    )

    print(f"Download URL: {link.url}")
    print(f"Expires at: {link.expires_at}")
    print(f"Format: {link.format}")

    # Download the file
    import aiohttp
    async with aiohttp.ClientSession() as session:
        async with session.get(link.url) as response:
            with open("design.pdf", "wb") as f:
                f.write(await response.read())
```

### Create Folder

Create a new folder.

```python
async with CanvaAPIClient(api_key) as client:
    folder = await client.create_folder(
        name="Marketing Assets",
        parent_id="folder-456"  # Optional: parent folder
    )

    print(f"Folder created: {folder.id}")
    print(f"Name: {folder.name}")
```

### Move Folder Item

Move a design or folder to another folder.

```python
async with CanvaAPIClient(api_key) as client:
    success = await client.move_folder_item(
        folder_id="folder-123",
        item_id="design-456",
        item_type="design",
        target_folder_id="folder-789"  # None to move to root
    )

    if success:
        print("Item moved successfully")
```

### Rename Folder

Rename an existing folder.

```python
async with CanvaAPIClient(api_key) as client:
    folder = await client.rename_folder(
        folder_id="folder-123",
        new_name="New Folder Name"
    )

    print(f"Renamed: {folder.name}")
```

### Create Export Job

Create an export job for a design.

```python
async with CanvaAPIClient(api_key) as client:
    job = await client.create_export_job(
        design_id="design-123",
        format="pdf",  # 'pdf', 'png', 'jpg'
        quality="high",  # 'standard' or 'high'
        pages=[1, 2, 3]  # Optional: specific pages
    )

    print(f"Export job created: {job.job_id}")
    print(f"Status: {job.status}")
```

### Get Export Job Status

Check the status of an export job.

```python
async with CanvaAPIClient(api_key) as client:
    job = await client.get_export_job_status(job_id="job-123")

    print(f"Status: {job.status}")
    print(f"Progress: {job.progress * 100:.1f}%")

    if job.status == "completed":
        print(f"Download URL: {job.download_url}")
```

### Wait for Export Completion

```python
async def wait_for_export(client, job_id, timeout=300):
    """Wait for export job to complete."""
    import asyncio

    start_time = asyncio.get_event_loop().time()

    while True:
        if asyncio.get_event_loop().time() - start_time > timeout:
            raise TimeoutError("Export timed out")

        job = await client.get_export_job_status(job_id)

        if job.status == "completed":
            return job.download_url
        elif job.status == "failed":
            raise Exception("Export failed")

        await asyncio.sleep(2)

# Usage
download_url = await wait_for_export(client, "job-123")
print(f"Export complete: {download_url}")
```

### Webhook Handler

Handle webhooks for design updates.

```python
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

@app.post("/webhook/canva")
async def canva_webhook(request: Request):
    payload = await request.json()
    signature = request.headers.get("X-Canva-Signature", "")
    secret = "your-webhook-secret"

    # Verify signature
    if not client.verify_webhook(payload, signature, secret):
        raise HTTPException(status_code=401, detail="Invalid signature")

    # Parse event
    event = client.parse_webhook_event(payload)

    if event["event_type"] == "design.updated":
        print(f"Design updated: {event['design_id']}")
        print(f"Changes: {event['changes']}")
        # Process design update

    return {"status": "ok"}
```

## API Actions

### List Folders

List all folders.

**Parameters:**
- `team_id` (Optional[str]): Team ID
- `limit` (int): Maximum results (default: 50)

**Returns:** Dict with folders list

### List Folder Items

List items in a folder.

**Parameters:**
- `folder_id` (str): Folder ID
- `item_type` (Optional[str]): Filter by type ('design' or 'folder')
- `limit` (int): Maximum results (default: 50)

**Returns:** Dict with folder items

### Get Design Download Link

Get download URL for a design.

**Parameters:**
- `design_id` (str): Design ID
- `format` (str): Export format ('pdf', 'png', 'jpg')
- `quality` (str): Quality ('standard', 'high')

**Returns:** `DownloadLink`

### Search Design

Search for designs.

**Parameters:**
- `query` (str): Search query
- `folder_id` (Optional[str]): Optional folder to search
- `limit` (int): Maximum results (default: 50)

**Returns:** `DesignResult`

### Create Folder

Create a new folder.

**Parameters:**
- `name` (str): Folder name
- `parent_id` (Optional[str]): Parent folder ID

**Returns:** `Folder`

### Move Folder Item

Move an item to another folder.

**Parameters:**
- `folder_id` (str): Source folder ID
- `item_id` (str): Item ID
- `item_type` (str): 'design' or 'folder'
- `target_folder_id` (Optional[str]): Target folder (None for root)

**Returns:** bool

### Rename Folder

Rename a folder.

**Parameters:**
- `folder_id` (str): Folder ID
- `new_name` (str): New name

**Returns:** `Folder`

### Create Export Job

Create export job.

**Parameters:**
- `design_id` (str): Design ID
- `format` (str): Export format
- `quality` (str): Export quality
- `pages` (Optional[List[int]]): Specific pages

**Returns:** `ExportJob`

## Webhook Events

### Design Updated

Triggered when a design is modified.

**Event Type:** `design.updated`

**Payload:**
```json
{
  "type": "design.updated",
  "id": "evt-123",
  "timestamp": "2026-02-28T12:00:00Z",
  "data": {
    "design_id": "design-123",
    "changes": {
      "name": "New Name",
      "thumbnail_url": "..."
    }
  }
}
```

## Export Formats

| Format | Description | Multiple Pages |
|--------|-------------|----------------|
| `pdf` | PDF document | ✅ |
| `png` | PNG image | ❌ (first page only) |
| `jpg` | JPEG image | ❌ (first page only) |

## API Reference

Official documentation: https://www.canva.com/developers/api-docs/

## Best Practices

1. **Handle export jobs asynchronously** - Use job IDs and check status
2. **Cache folder lists** - Reduce API calls for frequently accessed folders
3. **Use pagination** - For large workspaces, use pagination properly
4. **Webhook security** - Always verify webhook signatures
5. **Export limits** - Monitor export job quotas and limits

## Support

For issues, visit: https://www.canva.com/developers/