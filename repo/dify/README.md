# Dify API Client

Python async client for Dify's AI workflow platform.

## Features

- ✅ Create documents from text
- ✅ Update knowledge bases
- ✅ Execute workflows
- ✅ Get dataset details
- ✅ Send chat messages
- ✅ Get knowledge base tags
- ✅ List datasets
- ✅ Upload files for workflows
- ✅ Async/await support
- ✅ Type hints and dataclasses

## Installation

```bash
pip install -r requirements.txt
```

## API Key

Get your API key from: https://cloud.dify.ai/

## Usage

### Initialize Client

```python
import asyncio
from dify_client import DifyAPIClient

async def main():
    api_key = "your-api-key-here"

    async with DifyAPIClient(api_key) as client:
        # Use the client
        pass

asyncio.run(main())
```

### Create Document from Text

Add text content to a knowledge base.

```python
async with DifyAPIClient(api_key) as client:
    result = await client.create_document_from_text(
        knowledge_base_id="kb-123",
        text="This is a sample document about AI and machine learning.",
        name="AI Introduction",
        metadata={
            "source": "internal",
            "category": "technology"
        }
    )

    if result.success:
        print(f"Document created: {result.document.id}")
        print(f"Name: {result.document.name}")
```

### Update Knowledge Base

Update knowledge base metadata.

```python
async with DifyAPIClient(api_key) as client:
    result = await client.update_knowledge_base(
        knowledge_base_id="kb-123",
        name="Updated KB Name",
        description="Updated description"
    )

    if result.success:
        print(f"Knowledge base updated: {result.knowledge_base.name}")
        print(f"Document count: {result.knowledge_base.document_count}")
```

### Execute Workflow

Run a workflow with inputs.

```python
async with DifyAPIClient(api_key) as client:
    result = await client.execute_workflow(
        workflow_id="workflow-123",
        inputs={
            "query": "What is machine learning?",
            "context": "Beginner level"
        },
        user="test-user"
    )

    print(f"Execution ID: {result.execution.execution_id}")
    print(f"Status: {result.execution.status}")
    print(f"Result: {result.execution.result}")
```

### Get Dataset Details

Retrieve detailed dataset information.

```python
async with DifyAPIClient(api_key) as client:
    result = await client.get_dataset_details(dataset_id="dataset-123")

    print(f"Dataset: {result.dataset.name}")
    print(f"Description: {result.dataset.description}")
    print(f"Documents: {result.total}")

    for doc in result.documents[:5]:
        print(f"  - {doc.name} ({doc.id})")
```

### Send Chat Message

Chat with an AI assistant.

```python
async with DifyAPIClient(api_key) as client:
    result = await client.send_chat_message(
        chat_id="chat-123",
        message="Explain quantum computing in simple terms.",
        user="john-doe",
        conversation_id="conv-123"  # Optional: for conversation context
    )

    print(f"Response: {result.message.content}")
    print(f"Conversation ID: {result.conversation_id}")
```

### Get Knowledge Base Tags

Retrieve all tags from a knowledge base.

```python
async with DifyAPIClient(api_key) as client:
    result = await client.get_knowledge_base_tags(
        knowledge_base_id="kb-123"
    )

    print(f"Tags: {result.total}")
    for tag in result.tags:
        print(f"  - {tag.name} (ID: {tag.id})")
```

### List Datasets

List all available datasets.

```python
async with DifyAPIClient(api_key) as client:
    result = await client.list_datasets(page=1, page_size=20)

    print(f"Total datasets: {result.total}")
    for dataset in result.datasets:
        print(f"  - {dataset.name}: {dataset.document_count} docs")
```

### Upload File for Workflow

Upload a file for workflow processing.

```python
async with DifyAPIClient(api_key) as client:
    result = await client.upload_file_for_workflow(
        file_path="document.pdf",
        workflow_id="workflow-123"
    )

    if result.success:
        print(f"File uploaded: {result.file.name}")
        print(f"File ID: {result.file.id}")
        print(f"URL: {result.file.url}")
```

## API Actions

### Create Document from Text

Add a text document to a knowledge base.

**Parameters:**
- `knowledge_base_id` (str): Knowledge base ID
- `text` (str): Document content
- `name` (str): Document name
- `metadata` (Optional[Dict]): Additional metadata

**Returns:** `CreateDocumentResponse`

### Update Knowledge Base

Update knowledge base information.

**Parameters:**
- `knowledge_base_id` (str): Knowledge base ID
- `name` (Optional[str]): New name
- `description` (Optional[str]): New description

**Returns:** `UpdateKnowledgeBaseResponse`

### Execute Workflow

Run a workflow with provided inputs.

**Parameters:**
- `workflow_id` (str): Workflow ID
- `inputs` (Dict[str, Any]): Workflow inputs
- `user` (str): User identifier (default: "default")

**Returns:** `ExecuteWorkflowResponse`

### Get Dataset Details

Get detailed information about a dataset.

**Parameters:**
- `dataset_id` (str): Dataset ID

**Returns:** `DatasetDetailsResponse`

### Send Chat Message

Send a message to a chat bot.

**Parameters:**
- `chat_id` (str): Chat bot ID
- `message` (str): User message
- `user` (str): User identifier (default: "default")
- `conversation_id` (Optional[str]): Conversation ID for context

**Returns:** `ChatResponse`

### Get Knowledge Base Tags

Get all tags for a knowledge base.

**Parameters:**
- `knowledge_base_id` (str): Knowledge base ID

**Returns:** `GetTagsResponse`

### List Datasets

List all datasets with pagination.

**Parameters:**
- `page` (int): Page number (default: 1)
- `page_size` (int): Items per page (default: 20)

**Returns:** `ListDatasetsResponse`

### Upload File for Workflow

Upload a file for workflow use.

**Parameters:**
- `file_path` (str): Path to file
- `workflow_id` (str): Workflow ID

**Returns:** `UploadFileResponse`

## API Reference

Official documentation: https://docs.dify.ai/

## Common Use Cases

### Knowledge Base Management

```python
# Create documents
await client.create_document_from_text(kb_id, text, name)

# Update KB info
await client.update_knowledge_base(kb_id, name, description)

# Get tags
await client.get_knowledge_base_tags(kb_id)
```

### Workflow Automation

```python
# Execute workflow
result = await client.execute_workflow(
    workflow_id="workflow-id",
    inputs={"data": {...}},
    user="user-id"
)

# Check status and result
print(result.execution.status)
print(result.execution.result)
```

### Chat Integration

```python
# Simple chat
response = await client.send_chat_message(
    chat_id="bot-id",
    message="Hello!",
    user="user-id"
)

# Conversation with context
response = await client.send_chat_message(
    chat_id="bot-id",
    message="Tell me more about that.",
    user="user-id",
    conversation_id="conv-id"
)
```

## Error Handling

All methods raise exceptions on errors:

```python
try:
    result = await client.execute_workflow(
        workflow_id="invalid-id",
        inputs={}
    )
except Exception as e:
    print(f"Error: {e}")
```

## Rate Limits

Check your account dashboard for rate limit information.

## Support

For issues, visit: https://docs.dify.ai/