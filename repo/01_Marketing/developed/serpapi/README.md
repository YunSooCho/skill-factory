# SerpApi Client

Python client for SerpApi - real-time search API for Google, Bing, YouTube, and more.

## Installation

```bash
pip install -r requirements.txt
```

## Authentication

```python
from client import SerpApiClient

client = SerpApiClient(api_key="your-api-key")
```

## API Actions

### Google Search

```python
result = client.google_search("Python tutorial", num=10)
for item in result['organic_results']:
    print(item['title'])
```

### Bing Search

```python
result = client.bing_search("Python tutorial", count=10)
```

### YouTube Search

```python
result = client.youtube_search("Python tutorial")
for video in result['video_results']:
    print(video['title'])
```

### Google Maps Search

```python
result = client.google_maps_search("restaurants near Times Square")
```

### Google Local Search

```python
result = client.google_local_search("coffee shop Brooklyn")
```

### Google Images Search

```python
result = client.google_images_search("Python logo")
for img in result['images_results']:
    print(img['original'])
```

### Google News Search

```python
result = client.google_news_search("technology news")
```

### Google Finance Search

```python
result = client.google_finance_search("AAPL stock")
```

### Google Autocomplete

```python
result = client.google_autocomplete("Python")
for suggestion in result['suggestions']:
    print(suggestion['value'])
```

### Baidu Search

```python
result = client.baidu_search("Python教程")
```

### Yelp Search

```python
result = client.yelp_search(
    find_desc="pizza",
    find_loc="New York"
)
```

## License

MIT License
