# Exa AI API Client

Python client for [Exa AI](https://exa.ai/) - AI-powered web search and content retrieval platform.

## Features

- ✅ Intelligent web search with neural and keyword search
- ✅ Content retrieval from URLs
- ✅ Highlight-based search results
- ✅ Similar page finding
- ✅ Query autocomplete
- ✅ Answer generation from web sources
- ✅ Category and domain filtering
- ✅ Comprehensive error handling

## Installation

```bash
pip install -r requirements.txt
```

## Getting Started

### 1. Get API Credentials

1. Visit [Exa AI Dashboard](https://dashboard.exa.ai/api-keys)
2. Sign up or log in
3. Create an API key

### 2. Initialize the Client

```python
from exa_ai.client import ExaAIClient

# Initialize with your API key
client = ExaAIClient(api_key="your_api_key_here")
```

## Usage Examples

### Search for URLs

```python
# Basic URL search
results = client.search_url(
    query="blog post about artificial intelligence",
    num_results=10
)
print(results)

# Neural search (AI-powered)
results = client.search_url(
    query="latest developments in quantum computing",
    query_type="neural",
    num_results=5
)
```

### Search with Content

```python
# Search with full text content
results = client.search_contents(
    query="machine learning tutorials",
    num_results=5,
    max_characters=2000
)

for result in results.get("results", []):
    print(f"Title: {result['title']}")
    print(f"URL: {result['url']}")
    print(f"Content: {result.get('contents', {}).get('text', '')[:200]}...")
    print()
```

### Search with Highlights

```python
# Search with highlighted passages
results = client.search_highlights(
    query="climate change impacts",
    num_results=3,
    max_characters=4000
)

for result in results.get("results", []):
    print(f"Title: {result['title']}")
    highlights = result.get('contents', {}).get('highlights', [])
    for highlight in highlights:
        print(f"  • {highlight}")
    print()
```

### Get Page Contents

```python
# Fetch contents of specific URLs
urls = [
    "https://example.com/article1",
    "https://example.com/article2"
]
contents = client.get_page_contents(
    urls=urls,
    max_characters=3000
)
print(contents)
```

### Find Similar Pages

```python
# Find pages similar to a URL
similar = client.find_similar(
    url="https://example.com/interesting-article",
    num_results=5
)
print(similar)
```

### Get Answers

```python
# Get an answer to a question
answer = client.get_answer(
    question="What are the benefits of renewable energy?",
    num_results=5
)
print(f"Answer: {answer['answer']}")
print(f"Citations: {len(answer['citations'])}")
```

### Advanced Search

```python
# Search with category filter
results = client.search_with_category(
    query="latest AI research papers",
    category="researchPaper",
    num_results=10
)

# Search within specific domain
results = client.search_with_domain(
    query="python tutorials",
    domain="realpython.com",
    num_results=5
)

# Autocomplete suggestions
suggestions = client.autocomplete_query(
    query="artificial intell",
    num_results=5
)
print(suggestions)
```

### Create Tasks

```python
# Create a search task
task_result = client.create_task(
    task_type="search",
    query="blockchain technology explained",
    num_results=5,
    query_type="neural"
)
print(task_result)

# Create a content retrieval task
task_result = client.create_task(
    task_type="contents",
    urls=["https://example.com/article1", "https://example.com/article2"],
    max_characters=4000
)
print(task_result)
```

## API Reference

### Search Methods

- `search_url(query, query_type="auto", num_results=10, **kwargs)` - Search for URLs
- `search_contents(query, query_type="auto", num_results=10, max_characters=None, **kwargs)` - Search with full content
- `search_highlights(query, query_type="auto", num_results=10, max_characters=4000, **kwargs)` - Search with highlights
- `search_with_category(query, category, query_type="auto", num_results=10, **kwargs)` - Search with category filter
- `search_with_domain(query, domain, query_type="auto", num_results=10, **kwargs)` - Search within specific domain

### Content Methods

- `get_page_contents(urls, max_characters=None)` - Get contents of specific URLs

### Similarity Methods

- `find_similar(url, num_results=10, **kwargs)` - Find pages similar to a URL

### Autocomplete Methods

- `autocomplete_query(query, num_results=5, **kwargs)` - Get query suggestions

### Task Methods

- `create_task(task_type, query=None, urls=None, **kwargs)` - Create a search/retrieval task

### Answer Methods

- `get_answer(question, search_context=None, **kwargs)` - Get answer from web sources

## Search Types

- `auto` - Automatically choose best search type (recommended)
- `neural` - AI-powered semantic search
- `keyword` - Traditional keyword search
- `magic` - Hybrid approach

## Categories

Available categories for `search_with_category`:

- `company` - Company pages
- `researchPaper` - Research papers
- `news` - News articles
- `github` - GitHub repositories
- `tweet` - Tweets
- `pdf` - PDF documents

## Advanced Parameters

```python
results = client.search_url(
    query="artificial intelligence",
    
    # Search parameters
    query_type="neural",
    num_results=10,
    
    # Content parameters
    useAutoprompt=True,
    text=True,
    livecrawl="always",
    
    # Filter parameters
    includeDomains=["example.com", "another.com"],
    excludeDomains=["spam.com"],
    startPublishedDate="2024-01-01",  # ISO format
    endPublishedDate="2024-12-31"
)
```

## Error Handling

```python
from exa_ai.client import ExaAIClient, ExaAIError

client = ExaAIClient(api_key="your_key")

try:
    results = client.search_url(
        query="artificial intelligence",
        num_results=10
    )
    print(results)
except ExaAIError as e:
    print(f"Error: {e}")
finally:
    client.close()
```

## Response Format

Search responses follow this structure:

```json
{
  "results": [
    {
      "title": "Article Title",
      "url": "https://example.com/article",
      "score": 0.95,
      "publishedDate": "2024-02-15",
      "contents": {
        "text": "Full article text...",
        "highlights": ["Highlight 1", "Highlight 2"]
      },
      "author": "John Doe"
    }
  ]
}
```

## Best Practices

1. **Always close the client**: Use `client.close()` or a context manager
2. **Choose appropriate search type**: Use `auto` for most cases, `neural` for semantic understanding
3. **Control result size**: Set `num_results` and `max_characters` to manage costs
4. **Use highlights**: Better than full content for most applications
5. **Filter by date**: Use `startPublishedDate` and `endPublishedDate` for temporal queries
6. **Handle rate limits**: The client includes automatic rate limit detection
7. **Validate URLs**: Ensure URLs are valid before content retrieval

## Use Cases

- **Research**: Find relevant papers and articles
- **Content Discovery**: Discover related content for marketing
- **Competitive Analysis**: Monitor competitor websites
- **Market Research**: Study trends and news
- **Answer Generation**: Build QA systems powered by web search
- **Similar Content**: Find similar articles to recommend

## License

MIT License

## Support

- Documentation: https://exa.ai/docs
- Dashboard: https://dashboard.exa.ai
- API Keys: https://dashboard.exa.ai/api-keys