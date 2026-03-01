# ImgBB API Client

A Python client for interacting with the ImgBB API.

## About

ImgBB is a free image hosting and sharing service that allows you to upload, store, and share images. This client provides easy integration with ImgBB's REST API for uploading images from files, URLs, or base64 strings.

## Installation

```bash
pip install requests
```

## API Key Setup

1. Visit [imgbb.com](https://imgbb.com/) and create an account
2. Go to [API Settings](https://api.imgbb.com/)
3. Get your API key from the dashboard
4. Keep your API key secure - do not share it publicly

## Usage

```python
from imgbb import ImgBBClient

# Initialize the client
client = ImgBBClient(api_key="your_api_key_here")

# Upload an image from a local file
result = client.upload_image(
    image_path="/path/to/image.png",
    name="My Image"
)
print(f"Image URL: {result['data']['url']}")
print(f"Thumbnail URL: {result['data']['thumb']['url']}")

# Upload from URL
result = client.upload_image_from_url(
    image_url="https://example.com/image.jpg",
    name="Uploaded from URL"
)

# Upload from base64
import base64
with open("image.png", "rb") as f:
    base64_string = base64.b64encode(f.read()).decode('utf-8')

result = client.upload_image_from_base64(
    base64_string=base64_string,
    name="Base64 Upload"
)

# Upload with expiration (300 seconds = 5 minutes)
result = client.upload_image(
    image_path="temp_image.jpg",
    expiration=300
)

# Upload with resize
result = client.upload_image(
    image_path="large_image.jpg",
    resize_width=800,
    resize_height=600
)

# Close the session
client.close()
```

## API Methods

### Upload Methods

- `upload_image()` - Upload an image from a local file path
- `upload_image_from_url()` - Upload an image from a URL
- `upload_image_from_base64()` - Upload an image from a base64 string

### Upload Options

- `name` - Custom name for the image
- `expiration` - Expiration time in seconds (default: never expires)
- `resize_width` - Resize image to this width (in pixels)
- `resize_height` - Resize image to this height (in pixels)

### Common Expiration Times

- `60` - 1 minute
- `300` - 5 minutes
- `3600` - 1 hour
- `86400` - 1 day
- `604800` - 1 week

## Response Format

All upload methods return a dictionary with the following structure:

```python
{
    "status": 200,
    "success": True,
    "data": {
        "id": "image_id",
        "title": "image_title",
        "url_viewer": "https://ibb.co/image_id",
        "url": "https://i.ibb.co/...",
        "display_url": "https://i.ibb.co/...",
        "size": 12345,
        "time": "1234567890",
        "expiration": "1234567890",
        "delete_url": "https://ibb.co/...",
        "thumb": {
            "url": "https://i.ibb.co/...",
            "width": 160,
            "height": 160
        },
        "medium": {
            "url": "https://i.ibb.co/...",
            "width": 320,
            "height": 320
        }
    }
}
```

## Supported Image Formats

ImgBB supports the following image formats:
- JPEG/JPG
- PNG
- GIF
- BMP
- TIFF
- WEBP

Maximum file size: 32MB

## Error Handling

```python
try:
    result = client.upload_image(image_path="invalid.jpg")
except requests.exceptions.RequestException as e:
    print(f"Upload failed: {e}")
except FileNotFoundError as e:
    print(f"File not found: {e}")
```

## Rate Limits

TheImgBB API has rate limits. Check your account plan for specific limits. Implement proper error handling and retry logic when encountering rate limits.

## Best Practices

1. **Validate images** before uploading to ensure they meet size requirements
2. **Use compression** for large images to optimize upload times
3. **Set expiration** for temporary content
4. **Handle errors** gracefully in production code
5. **Close sessions** when done to free resources

## API Documentation

Official ImgBB API documentation: https://api.imgbb.com/

## License

This client is provided as-is for integration with the ImgBB API.