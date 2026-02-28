# CodeGPT API Client

Python async client for CodeGPT's AI coding assistant API.

## Features

- ✅ AI-powered code completion and suggestions
- ✅ Upload and manage code documents
- ✅ Update existing documents
- ✅ Search your codebase
- ✅ Support for multiple programming languages
- ✅ Async/await support
- ✅ Type hints and dataclasses

## Installation

```bash
pip install -r requirements.txt
```

## API Key

Get your API key from: https://codegpt.co/api-keys

## Usage

### Chat Completion

Get AI coding assistance and suggestions.

```python
import asyncio
from codegpt_client import CodeGPTAPIClient

async def main():
    api_key = "your-api-key-here"

    async with CodeGPTAPIClient(api_key) as client:
        messages = [
            {"role": "system", "content": "You are a helpful coding assistant."},
            {"role": "user", "content": "Write a Python function to calculate factorial."}
        ]

        response = await client.chat_completion(
            messages=messages,
            model="codegpt-4",
            temperature=0.7
        )

        print(f"Response: {response.content}")
        print(f"Tokens used: {response.usage}")

asyncio.run(main())
```

### Upload Document

Upload code to your CodeGPT workspace.

```python
async with CodeGPTAPIClient(api_key) as client:
    result = await client.upload_document(
        content='''def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
''',
        name="fibonacci.py",
        language="python",
        file_type="code"
    )

    if result.success and result.document:
        print(f"Uploaded document ID: {result.document.id}")
        print(f"Document name: {result.document.name}")
```

### Update Document

Update an existing document.

```python
async with CodeGPTAPIClient(api_key) as client:
    result = await client.update_document(
        document_id="doc-123",
        content='''def fibonacci(n):
    """Calculate fibonacci number iteratively."""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
''',
        name="fibonacci_iterative.py"
    )

    if result.success:
        print("Document updated successfully!")
```

### Search Documents

Search your codebase for relevant code.

```python
async with CodeGPTAPIClient(api_key) as client:
    result = await client.search_documents(
        query="fibonacci",
        language="python",
        limit=5
    )

    print(f"Found {result.total} results:")
    for hit in result.results:
        print(f"\n  Document: {hit.document_name}")
        print(f"  Score: {hit.score:.2f}")
        print(f"  Snippet: {hit.snippet}")
```

### Chat with Context

Get code suggestions with context from your codebase.

```python
async with CodeGPTAPIClient(api_key) as client:
    # Search first
    search_result = await client.search_documents(query="api client", limit=5)

    # Build context from search results
    context = "\n\n".join([f"File: {hit.document_name}\n{hit.snippet}"
                           for hit in search_result.results[:3]])

    messages = [
        {"role": "user", "content": "How can I improve error handling in this code?"}
    ]

    response = await client.chat_completion(
        messages=messages,
        context=context
    )

    print(f"Suggestions: {response.content}")
```

## API Actions

### Chat Completion

Get AI code completion/suggestions.

**Parameters:**
- `messages` (List[Dict]): List of message objects with 'role' and 'content'
- `model` (str): Model name (default: "codegpt-4")
- `temperature` (float): Sampling temperature (0.0-2.0)
- `max_tokens` (Optional[int]): Maximum tokens to generate
- `context` (Optional[str]): Additional context from your codebase

**Returns:** `ChatCompletionResponse`

### Upload Document

Upload a new document to your workspace.

**Parameters:**
- `content` (str): Document content (code/text)
- `name` (str): Document name
- `language` (Optional[str]): Programming language (e.g., 'python', 'javascript')
- `file_type` (str): Type of document ('code', 'text', 'markdown')

**Returns:** `DocumentResponse`

### Update Document

Update an existing document.

**Parameters:**
- `document_id` (str): ID of the document to update
- `content` (str): New document content
- `name` (Optional[str]): Optional new name for the document

**Returns:** `DocumentResponse`

### Search Documents

Search your codebase for relevant documents.

**Parameters:**
- `query` (str): Search query string
- `limit` (int): Maximum number of results (default: 10)
- `language` (Optional[str]): Filter by programming language
- `file_type` (Optional[str]): Filter by file type

**Returns:** `SearchResponse`

## Supported Languages

- Python
- JavaScript / TypeScript
- Java
- C# / .NET
- Go
- Rust
- Ruby
- PHP
- Swift
- Kotlin
- And many more...

## Models

- `codegpt-4`: Latest code generation model
- `codegpt-3.5`: Faster, lighter model
- `codegpt-fine-tuned`: Model fine-tuned on your codebase

## API Reference

Official documentation: https://codegpt.co/api-docs

## Rate Limits

Check your account dashboard for rate limit information.

## Tips

1. **Use context**: Provide relevant code snippets as context for better suggestions
2. **Be specific**: Clear, detailed prompts get better results
3. **Iterate**: Use conversation history to refine suggestions
4. **Organize documents**: Structure your codebase for better search results

## Support

For issues, visit: https://codegpt.co/support