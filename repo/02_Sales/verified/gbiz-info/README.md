# Gbiz-info API Client

Python API client for Gbiz-info (Japanese Corporate Information Database).

[API Documentation](https://info.gbiz.go.jp/) | [API Reference](https://info.gbiz.go.jp/)

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

```python
from gbiz_info_client import GbizInfoClient

# Initialize client (API key is optional for some endpoints)
client = GbizInfoClient(
    api_key="your_api_key",  # Optional
    base_url="https://info.gbiz.go.jp/api"
)
```

Get API key from [Gbiz-info Developer Portal](https://info.gbiz.go.jp/).

## Usage

### Search by Corporate Number

```python
# Search by 13-digit corporate number
response = client.search_by_corporate_number("1234567890123")
print(response)
```

### Search by Company Name

```python
# Search by company name
response = client.search_by_name(
    name="株式会社ABC",
    page=1,
    limit=10
)
print(response)

# Advanced search with status filter
response = client.search_by_name_advanced(
    name="株式会社ABC",
    status="01",  # 01: active
    exact_match=True,
    limit=20
)
print(response)
```

### Get Detailed Information

```python
# Get detailed corporation information
response = client.get_detailed_info("1234567890123")
print(response)

# Get corporation status
status = client.get_corporation_status("1234567890123")
print(status)
```

### Corporate Status Codes

| Status | Description |
|--------|-------------|
| 01 | Active (存続) |
| 02 | Dissolved (解散) |
| 03 | Liquidated (清算中) |
| 04 | Others (その他) |

## API Actions Implemented

| Action | Method | Description |
|--------|--------|-------------|
| 法人番号から法人情報を検索 | `search_by_corporate_number()` | Search by corporate number |
| 法人名から法人情報を検索 | `search_by_name()` | Search by company name |
| 法人情報を取得 | `get_detailed_info()` | Get detailed information |
| 法人名から法人情報を検索（詳細） | `search_by_name_advanced()` | Advanced name search |
| 【非推奨】法人番号から法人情報を検索 | `search_by_corporate_number_simple()` | Deprecated search |
| 【非推奨】法人名から法人情報を検索 | `search_by_name_simple()` | Deprecated search |
| 【非推奨】法人情報を取得 | `search_by_corporate_number_old()` | Old deprecated endpoint |

## Response Format

```python
{
    "status": "success",
    "data": {
        "corporateNumber": "1234567890123",
        "name": "株式会社ABC",
        "nameEnglish": "ABC Corporation",
        "postalCode": "1000001",
        "prefectureName": "東京都",
        "cityName": "千代田区",
        "streetNumber": "1-1-1",
        "address": "千代田区1-1-1",
        "status": "01",
        "capitalStock": "10000000",
        "establishmentDate": "2000-01-01",
        // ... more fields
    },
    "status_code": 200
}
```

## Error Handling

```python
from gbiz_info_client import GbizInfoAPIError

try:
    response = client.search_by_corporate_number("invalid_number")
except GbizInfoAPIError as e:
    print(f"Gbiz-info API Error: {e}")
```

## Usage Notes

### Corporate Number Format
- Must be a 13-digit number
- Example: "1234567890123"
- Validated by the Gbiz-info API

### Search Results Pagination
- Default: 10 results per page
- Maximum: 100 results per page
- Use `page` parameter for pagination

### Rate Limiting
- Free tier: Limited requests per day
- Paid tier: Higher limits available
- Implement backoff on rate limit errors

## Testing

```bash
python test_gbiz_info.py
```

**Note:** Tests require valid Gbiz-info corporate numbers for data verification.

## Yoom Integration

This client implements the following Yoom flow bot operations:
- **法人番号から法人情報を検索** - `search_by_corporate_number()`
- **法人名から法人情報を検索** - `search_by_name()`
- **法人情報を取得** - `get_detailed_info()`

**Note:** Some deprecated methods are also implemented for backward compatibility.

## Support

For API issues, visit:
- [Gbiz-info Official Site](https://info.gbiz.go.jp/)
- [API Documentation](https://info.gbiz.go.jp/)
- [Developer Support](https://info.gbiz.go.jp/contact/)