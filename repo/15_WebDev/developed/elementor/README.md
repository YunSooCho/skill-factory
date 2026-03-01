# Elementor API Integration

## Overview
Complete Elementor WordPress website builder API client for Yoom automation. Supports templates, kits, settings, and design system management.

## Supported Features
- ✅ Kit management (global design tokens)
- ✅ Template CRUD operations
- ✅ Library access
- ✅ Template import/export
- ✅ Site settings
- ✅ Typography settings
- ✅ Color palette management
- ✅ Document management

## Setup

### 1. Get API Key
1. Install Elementor on WordPress
2. Configure API in Elementor settings
3. Or use WordPress Application Passwords for REST API

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure
```bash
export ELEMENTOR_API_KEY="your_api_key"  # optional
export ELEMENTOR_BASE_URL="https://your-site.com"
```

## Usage

### Kit Management
```python
import os
from elementor_client import ElementorAPIClient

os.environ['ELEMENTOR_BASE_URL'] = 'https://your-site.com'
os.environ['ELEMENTOR_API_KEY'] = 'your_api_key'

client = ElementorAPIClient()

# List kits
kits = client.list_kits()

# Create kit
kit = client.create_kit(
    title='Main Kit',
    meta={
        'primary_color': '#336699',
        'secondary_color': '#FF5733',
        'font_primary': 'Roboto',
        'font_secondary': 'Open Sans'
    }
)

# Update kit
client.update_kit(kit['id'], title='Updated Kit')

client.close()
```

### Template Management
```python
# List templates (page, section, block)
templates = client.list_templates(template_type='page')

# Get template details
template = client.get_template(123)

# Create template
new_template = client.create_template(
    title='Home Page',
    content='<div class="elementor-widget-wrap">...</div>',
    template_type='page',
    post_status='draft'
)

# Update template
client.update_template(
    new_template['id'],
    content='<div class="elementor-widget-wrap">Updated...</div>'
)
```

### Import/Export
```python
# Export template
exported = client.export_template(template_id=123)

# Import template
imported = client.import_template(
    file_data=exported['data']
)
```

### Settings Management
```python
# Get site settings
settings = client.get_site_settings()

# Update site settings
client.update_site_settings({
    'default_font': 'Roboto',
    'container_width': 1200
})
```

### Typography and Colors
```python
# Get typography settings
typography = client.get_typography_settings()

# Get color palette
colors = client.get_color_settings()
```

### Library Access
```python
# Get library items (blocks, pages)
blocks = client.get_library_details(type='block')
pages = client.get_library_details(type='page')
```

## Template Types
- `page`: Full page template
- `section`: Section block
- `block`: Widget block
- `popup`: Popup template
- `header`: Header template
- `footer`: Footer template

## Integration Type
- **Type:** REST API
- **Authentication:** Bearer token (optional) or WordPress auth
- **Protocol:** HTTPS REST API
- **Platform:** WordPress + Elementor

## Notes
- Requires Elementor plugin installed on WordPress
- Kits provide global design tokens for consistency
- Templates can be saved and reused
- Import/export for template sharing
- Works with Elementor Pro features
- Design tokens (kits) ensure consistency across site

## Kit Meta Properties
Common kit meta properties:
- `primary_color`: Main brand color
- `secondary_color`: Secondary brand color
- `font_primary`: Primary font family
- `font_secondary`: Secondary font family
- `h1` through `h6`: Typography settings
- `button`: Button design settings
- `form`: Form styling settings