# Moxie API Integration

## Overview
Implementation of Moxie client and project management API for Yoom automation.

## Supported Features
- ✅ Client: Create, Search
- ✅ Contact: Create, Search
- ✅ Project: Create, Search
- ✅ Task: Create
- ✅ Ticket: Create, Add Comment
- ✅ Expense: Create
- ✅ Invoice: Create
- ✅ Calendar Event: Create/Update
- ✅ Form Submission: Create
- ✅ File Upload
- ✅ Deliverable: Approve
- ✅ Client Invoices: Search

## Setup

### Get API Key
Visit https://www.moxie.com/settings/api and obtain your API key.

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Configure
```python
from moxie_client import MoxieClient, Client, Project

api_key = "your_moxie_api_key"

async with MoxieClient(api_key=api_key) as client:
    pass
```

## Usage

```python
# Create client
client = Client(name="Example Corp", email="info@example.com")
await client.create_client(client)

# Create project
project = Project(name="Website Redesign", client_id=client_id)
await client.create_project(project)

# Create task
task = Task(title="Design homepage", project_id=project_id)
await client.create_task(task)
```

## Notes
- Async operations with rate limiting
- Client and project management
- Comprehensive feature set