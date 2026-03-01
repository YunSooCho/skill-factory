# Cohere API Client

Python async client for Cohere's NLP API.

## Features

- ✅ Rerank documents by relevance
- ✅ Generate text embeddings
- ✅ Chat with language models
- ✅ Async/await support
- ✅ Type hints and dataclasses
- ✅ Comprehensive error handling

## Installation

```bash
pip install -r requirements.txt
```

## API Key

Get your API key from: https://dashboard.cohere.com/

## Usage

### Rerank Documents

```python
import asyncio
from cohere_client import CohereAPIClient

async def main():
    api_key = "your-api-key-here"

    async with CohereAPIClient(api_key) as client:
        query = "What is machine learning?"

        documents = [
            "Machine learning is a subset of artificial intelligence.",
            "Python is a popular programming language.",
            "The sky is blue on a clear day."
        ]

        result = await client.rerank(
            query=query,
            documents=documents,
            model="rerank-english-v2.0",
            top_n=2
        )

        for r in result.results:
            print(f"Doc #{r.index}: Score={r.relevance_score:.4f}")

asyncio.run(main())
```

### Generate Embeddings

```python
async with CohereAPIClient(api_key) as client:
    texts = ["Hello world", "How are you?"]

    result = await client.embed(
        texts=texts,
        model="embed-english-v3.0",
        input_type="search_document"
    )

    print(f"Generated {len(result.embeddings)} embeddings")
```

### Chat

```python
async with CohereAPIClient(api_key) as client:
    response = await client.chat(
        message="Explain quantum computing in simple terms.",
        model="command-r",
        temperature=0.7,
        preamble="You are a helpful and knowledgeable assistant."
    )

    print(f"Response: {response.text}")
```

## API Actions

### Rerank

Rerank documents based on their relevance to a query.

**Parameters:**
- `query` (str): Query string
- `documents` (List[str]): List of document strings
- `model` (str): Rerank model name (default: "rerank-english-v2.0")
- `top_n` (Optional[int]): Number of top results

**Returns:** `RerankResponse`

### Embed

Get embeddings for texts.

**Parameters:**
- `texts` (List[str]): List of text strings
- `model` (str): Embedding model name (default: "embed-english-v3.0")
- `input_type` (str): Input type ('search_document', 'search_query', etc.)
- `truncate` (str): Truncation mode ('NONE', 'START', 'END')

**Returns:** `EmbedResponse`

### Chat

Send a chat message and get a response.

**Parameters:**
- `message` (str): User message
- `chat_history` (Optional[List[Dict]]): Conversation history
- `model` (str): Chat model name (default: "command-r")
- `temperature` (float): Sampling temperature (0.0-5.0)
- `preamble` (Optional[str]): System prompt
- `max_tokens` (Optional[int]): Max tokens to generate

**Returns:** `ChatResponse`

## API Reference

Official documentation: https://docs.cohere.com/reference/

## Models

### Embedding Models
- `embed-english-v3.0`: Latest English embedding model
- `embed-multilingual-v3.0`: Multilingual embedding model

### Rerank Models
- `rerank-english-v2.0`: English reranker
- `rerank-multilingual-v2.0`: Multilingual reranker

### Chat Models
- `command-r`: Powerful chat model
- `command-r-plus`: Advanced chat model

## Rate Limits

Check your account dashboard for rate limit information.

## Support

For issues, visit: https://docs.cohere.com/