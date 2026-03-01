# Figma API Client

A Python client for interacting with the Figma REST API.

## About

Figma is a collaborative interface design tool that allows designers to create and prototype digital experiences together in real-time. This client provides access to design files, components, comments, users, webhooks, and more through the Figma REST API.

## Installation

```bash
pip install requests
```

## API Key Setup

1. Log in to your [Figma account](https://www.figma.com/)
2. Go to Settings > Account > Personal Access Tokens
3. Click "Create new token"
4. Give your token a name and copy it
5. Keep this token secure - do not share it publicly

For OAuth2 apps:
1. Visit [My apps](https://www.figma.com/developers/apps)
2. Register your app to get client ID and secret
3. Implement OAuth2 flow to get access tokens

## Usage

```python
from figma import FigmaClient

# Initialize the client
client = FigmaClient(access_token="your_access_token_here")

# Get file details
file_data = client.get_file(file_key="abc123")
print(file_data)

# Get specific nodes
node_data = client.get_file_nodes(
    file_key="abc123",
    ids=["node1", "node2"]
)

# Get image URLs
images = client.get_image(
    file_key="abc123",
    ids=["frame1", "frame2"],
    format="png",
    scale=2.0
)
print(images)

# Post a comment
comment = client.post_comment(
    file_key="abc123",
    message="Great design!",
    client_meta={"x": 100, "y": 200}
)

# Get user info
me = client.get_me()
print(me)

# Get team projects
projects = client.get_team_projects(team_id="team123")

# Get all comments
comments = client.get_comments(file_key="abc123")

# Close the session
client.close()
```

## API Endpoints Supported

### File Endpoints
- `get_file()` - Get file details
- `get_file_nodes()` - Get specific nodes from a file
- `get_image()` - Get image URLs for nodes

### Comment Endpoints
- `get_comments()` - Get all comments
- `post_comment()` - Post a new comment
- `delete_comment()` - Delete a comment

### User Endpoints
- `get_me()` - Get authenticated user info
- `get_users()` - Get user info by IDs

### Project Endpoints
- `get_team_projects()` - Get all projects for a team
- `get_project_files()` - Get all files in a project

### Component Endpoints
- `get_components()` - Get all components
- `get_component_sets()` - Get component sets
- `get_styles()` - Get all styles

### Variables Endpoints
- `get_variable_consumers()` - Get variable consumers
- `get_local_variable_modes()` - Get local variable modes
- `get_library_variable_modes()` - Get library variable modes

### Webhooks Endpoints
- `create_webhook()` - Create a webhook
- `get_webhooks()` - Get all webhooks
- `delete_webhook()` - Delete a webhook

### Activity Logs & Discovery
- `get_activity_logs()` - Get team activity logs
- `get_text_events()` - Get text editing events

## API Documentation

Full API documentation: https://developers.figma.com/docs/rest-api/

## Rate Limits

The Figma API has rate limits. Requests exceeding the limit will return 429 status code. Implement exponential backoff when handling rate limits.

## License

This client is provided as-is for integration with the Figma API.