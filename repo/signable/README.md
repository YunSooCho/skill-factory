# Signable

 electronic signature and document management platform.

## API Key
1. Sign up at [https://signable.co.uk](https://signable.co.uk)
2. Navigate to Account > API Settings
3. Generate API key

## Installation
```bash
pip install requests
```

## Example
```python
from signable.client import SignableClient

client = SignableClient(api_key='your_api_key')

# List documents
docs = client.list_documents()

# Create document
result = client.create_document(
    title='Contract.pdf',
    file_path='/path/to/file.pdf'
)
```