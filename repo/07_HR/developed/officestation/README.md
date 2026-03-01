# OfficeStation

OfficeStation is a Japanese cloud-based document workflow and approval management system that helps organizations manage documents, forms, workflows, and approval requests.

## API Documentation

- **Base URL:** `https://api.officestation.com/v1`
- **Authentication:** Bearer Token + X-Workspace-ID header
- **Rate Limit:** Varies by plan

## Installation

```bash
pip install -r requirements.txt
```

## Example Usage

```python
from client import OfficeStationClient

client = OfficeStationClient(
    api_key="YOUR_API_KEY",
    workspace_id="YOUR_WORKSPACE_ID"
)

# Get documents
documents = client.get_documents()
print(f"Documents: {documents}")

# Get document details
document = client.get_document("doc_123")

# Create document
doc_data = {
    "name": "Leave Request",
    "category": "HR",
    "content": "...",
    "author_id": "user_123"
}
result = client.create_document(doc_data)

# Update document
client.update_document("doc_123", {"content": "Updated content"})

# Delete document
client.delete_document("doc_123")

# Get workflows
workflows = client.get_workflows()

# Get workflow details
workflow = client.get_workflow("wf_123")

# Create workflow
wf_data = {
    "name": "Expense Approval",
    "steps": [...],
    "assignees": ["user_123", "user_456"]
}
client.create_workflow(wf_data)

# Start workflow
client.start_workflow("wf_123", {"employee_id": "emp_001", "amount": 5000})

# Get form templates
templates = client.get_form_templates()

# Get form template
template = client.get_form_template("tpl_123")

# Create form template
tpl_data = {
    "name": "Time Off Request",
    "fields": [...]
}
client.create_form_template(tpl_data)

# Get requests
requests = client.get_requests()

# Get request details
request = client.get_request("req_123")

# Create request
req_data = {
    "form_template_id": "tpl_001",
    "data": {"type": "annual_leave", "days": 5}
}
client.create_request(req_data)

# Approve request
client.approve_request("req_123")

# Approve with comment
client.approve_request("req_123", "Approved as requested")

# Reject request
client.reject_request("req_456", "Insufficient information")

# Get users
users = client.get_users()

# Get departments
departments = client.get_departments()

# Get notifications
notifications = client.get_notifications()

# Mark notification as read
client.mark_notification_read("notif_123")
```

## Error Handling

```python
from client import OfficeStationClient, OfficeStationError

try:
    client = OfficeStationClient(api_key="...", workspace_id="...")
    documents = client.get_documents()
except OfficeStationError as e:
    print(f"Error: {e}")
```

## License

This integration is provided as-is for use with the Yoom platform.