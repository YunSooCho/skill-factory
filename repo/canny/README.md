# Canny Feature Request Platform Integration

Canny is a platform for collecting and organizing feature requests, bug reports, and feedback from customers and teams.

## Features

- Feature request collection
- User voting system
- Status tracking (Planning, In Progress, Implemented)
- Board organization
- Comment discussions
- User management
- Tag management
- Changelog updates
- Activity tracking

## Installation

```bash
pip install -e .
```

## API Key Setup

1. Log in to your Canny account
2. Go to Settings > API Keys
3. Generate an API key
4. Store credentials securely

## Usage

```python
from canny import CannyClient

# Initialize client
client = CannyClient(api_key="your-api-key")

# List posts
posts = client.list_posts(limit=50)
for post in posts.get('posts', []):
    print(f"{post['title']} - {post['status']}: {post['score']} votes")

# Get post details
post = client.get_post("POST123")

# Create a post
new_post = client.create_post({
    "authorID": "USER123",
    "boardID": "BOARD456",
    "title": "Add dark mode support",
    "details": "It would be great if the app supported dark mode...",
    "status": "open"
})

# Update post
client.update_post("POST123", {
    "title": "Add dark mode and theme customizer"
})

# Change post status
client.change_post_status(
    post_id="POST123",
    status="in_progress"
)

# Delete post
client.delete_post("POST123")

# List comments
comments = client.list_comments(post_id="POST123")

# Create comment
comment = client.create_comment({
    "authorID": "USER123",
    "postID": "POST123",
    "value": "This would be very useful!"
})

# Delete comment
client.delete_comment("COMMENT123")

# List voters
voters = client.list_voters(post_id="POST123")

# Vote for a post
client.create_vote({
    "userID": "USER123",
    "postID": "POST123",
    "score": 1
})

# Delete vote
client.delete_vote(user_id="USER123", post_id="POST123")

# List boards
boards = client.list_boards()

# Get board
board = client.get_board("BOARD456")

# Create board
new_board = client.create_board({
    "name": "Feature Requests"
})

# List users
users = client.list_users(limit=100)

# Get user
user = client.get_user("USER123")

# Create user
new_user = client.create_user({
    "name": "John Doe",
    "email": "john@example.com"
})

# Get user by email
user = client.get_user_by_email("john@example.com")

# List tags
tags = client.list_tags()

# Create tag
tag = client.create_tag({
    "name": "Enhancement",
    "color": "#3498db"
})

# Attach tag to post
client.attach_tag(post_id="POST123", tag_id="TAG456")

# Detach tag from post
client.detach_tag(post_id="POST123", tag_id="TAG456")

# List changelogs
changelogs = client.list_changelogs()

# Create changelog
changelog = client.create_changelog({
    "label": "New Feature",
    "value": "We've added dark mode support!",
    "type": "post",
    "postID": "POST789"
})

# Delete changelog
client.delete_changelog("CHANGELOG123")

# List activities
activities = client.list_activities(object_id="POST123")
```

## API Methods

### Posts
- `list_posts(board_id, limit, skip, status)` - List posts
- `get_post(post_id)` - Get post details
- `create_post(data)` - Create post
- `update_post(post_id, data)` - Update post
- `change_post_status(post_id, status)` - Change status
- `delete_post(post_id)` - Delete post

### Comments
- `list_comments(post_id, limit, skip)` - List comments
- `create_comment(data)` - Create comment
- `delete_comment(comment_id)` - Delete comment

### Votes
- `list_voters(post_id, limit, skip)` - List voters
- `create_vote(data)` - Vote for post
- `delete_vote(user_id, post_id)` - Delete vote

### Boards
- `list_boards(limit, skip)` - List boards
- `get_board(board_id)` - Get board details
- `create_board(data)` - Create board
- `update_board(board_id, data)` - Update board

### Users
- `list_users(limit, skip, search)` - List users
- `get_user(user_id)` - Get user details
- `create_user(data)` - Create user
- `get_user_by_email(email)` - Get user by email

### Tags
- `list_tags(post_id, limit, skip)` - List tags
- `create_tag(data)` - Create tag
- `attach_tag(post_id, tag_id)` - Attach tag
- `detach_tag(post_id, tag_id)` - Detach tag

### Changelogs
- `list_changelogs(limit, skip)` - List changelogs
- `create_changelog(data)` - Create changelog
- `delete_changelog(changelog_id)` - Delete changelog

### Activities
- `list_activities(object_id, limit, skip)` - List activities

## Post Status

- `open` - Open for voting
- `planning` - Planned for future
- `in_progress` - Currently being worked on
- `implemented` - Feature shipped
- `closed` - Closed without implementing
- `duplicate` - Duplicate of another post

## Error Handling

```python
try:
    post = client.create_post({
        "authorID": "USER123",
        "boardID": "BOARD456",
        "title": "New Feature",
        "details": "Description..."
    })
except requests.RequestException as e:
    print(f"Error creating post: {e}")
```

## Webhooks

Canny supports webhooks for real-time notifications:
- Post created/updated/deleted
- Comments created
- Votes added
- Status changes

Configure webhooks in your Canny settings.

## Support

For API documentation, visit https://developers.canny.io/