# Promptitude API Client

Python client for [Promptitude](https://promptitude.io/) - Prompt management and text generation platform.

## Features

- ✅ Generate text from custom prompts
- ✅ Create and manage prompt templates
- ✅ Rate and collect feedback on outputs
- ✅ Organize content with folders
- ✅ Analytics and statistics
- ✅ Support for multiple AI models

## Installation

```bash
pip install -r requirements.txt
```

## Getting Started

### Initialize Client

```python
from promptitude_io.client import PromptitudeClient

client = PromptitudeClient(api_key="your_api_key_here")
```

## Usage Examples

### Generate Text

```python
# Basic text generation
result = client.generate_text(
    prompt="Write a professional email template for a meeting invitation",
    max_tokens=200,
    temperature=0.7
)
print(result['text'])
```

### Create and Use Templates

```python
# Create a template
template = client.create_prompt_template(
    name="Meeting Invitation",
    template="Hi {{name}},\n\nI'd like to invite you to a meeting on {{date}} at {{time}}.\n\n{{message}}",
    variables=["name", "date", "time", "message"],
    tags=["meetings", "templates"]
)
print(template['template_id'])

# Generate from template
result = client.generate_text_from_template(
    template_id=template['template_id'],
    variables={
        "name": "John",
        "date": "2024-03-15",
        "time": "2:00 PM",
        "message": "We'll discuss the project roadmap."
    }
)
print(result['text'])
```

### Rate Outputs

```python
# Rate a generated output
rating = client.rate_prompt_output(
    prompt_id="output-123",
    rating=4.5,
    feedback="Great content, but could be more concise"
)
print(rating)

# Get ratings for a prompt
ratings = client.get_ratings(prompt_id="template-456")
print(ratings)
```

### Manage Content

```python
# Create folders
folder = client.create_folder(name="Marketing Templates")
print(folder)

# Get all templates
templates = client.get_prompt_templates(tags=["meetings"])
print(templates)

# Update a template
updated = client.update_prompt_template(
    template_id="template-123",
    description="Updated template description",
    template="New template content..."
)
print(updated)
```

### Analytics

```python
# Get generation stats
stats = client.get_generation_stats(
    template_id="template-123",
    start_date="2024-01-01",
    end_date="2024-12-31"
)
print(stats)
```

## API Reference

### Generation Methods

- `generate_text(prompt, model=None, max_tokens=None, temperature=None, **kwargs)` - Generate text
- `generate_text_from_template(template_id, variables=None, **kwargs)` - Generate from template

### Rating Methods

- `rate_prompt_output(prompt_id, rating, feedback=None, metadata=None)` - Rate output
- `get_ratings(prompt_id=None, limit=None)` - Get ratings

### Template Management

- `create_prompt_template(name, template, description=None, tags=None, variables=None, **kwargs)` - Create template
- `update_prompt_template(template_id, **kwargs)` - Update template
- `get_prompt_templates(tags=None, limit=None)` - List templates
- `get_prompt_template(template_id)` - Get template
- `delete_prompt_template(template_id)` - Delete template

### Organization

- `create_folder(name, parent_id=None)` - Create folder
- `get_folders(parent_id=None)` - List folders
- `move_content(content_id, content_type, target_folder_id=None)` - Move content

### Analytics

- `get_generation_stats(template_id=None, start_date=None, end_date=None)` - Get stats
- `get_available_models()` - List available models

## Error Handling

```python
from promptitude_io.client import PromptitudeClient, PromptitudeError

client = PromptitudeClient(api_key="your_key")

try:
    result = client.generate_text(prompt="Hello")
    print(result)
except PromptitudeError as e:
    print(f"Error: {e}")
finally:
    client.close()
```

## License

MIT License