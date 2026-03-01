# ZapSign

Electronic signature and digital document platform.

## API Key
1. Create account at [https://zapsign.com.br](https://zapsign.com.br)
2. Go to Account > Integrations > API
3. Generate API token

## Installation
```bash
pip install requests
```

## Example
```python
from zapsign.client import ZapSignClient

client = ZapSignClient(api_token='your_api_token')

# Upload document for signature
result = client.upload_pdf(
    pdf_path='contract.pdf',
    signers=[{'email': 'user@example.com', 'name': 'John Doe'}]
)
```