# ClickUp API Client

Python client for [ClickUp](https://clickup.com/) - Project management and collaboration platform.

## Features

- ✅ Create, read, update, delete tasks
- ✅ Search tasks by status and custom fields
- ✅ Add comments to tasks
- ✅ File attachments
- ✅ Custom field management
- ✅ Webhook support for triggers

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from clickup.client import ClickUpClient

client = ClickUpClient(api_key="your_api_key")

# Create a task
task = client.create_task(
    list_id="list_123",
    name="Complete project documentation",
    description="Write comprehensive docs",
    status="in progress"
)
print(task['id'])

# Get task
task = client.get_task("task_456")
print(task)

# Update task
client.update_task("task_456", status="completed")

# Search tasks
tasks = client.search_tasks_by_status("workspace_123", "in progress")

# Add custom field
client.add_label_custom_field("task_456", "priority", "High")

# Add comment
client.add_comment("task_456", "Task is completed successfully")

# Create webhooks
client.create_webhook("list_123", "https://your.webhook.com", ["task.created", "task.updated"])
```

## License

MIT License