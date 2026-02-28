# Pappers API Integration

## Overview
Implementation of Pappers API for French company information and documentation for Yoom automation.

## Supported Features
- ✅ Search Company
- ✅ Get Company (by SIRET)
- ✅ Download Document (statuts, kbis, etc.)

## Setup

### Get API Key
Visit https://www.pappers.fr/ to create an account and obtain your API key.

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Configure
```python
from pappers_client import PappersClient

api_key = "your_pappers_api_key"

async with PappersClient(api_key=api_key) as client:
    pass
```

## Usage

```python
# Search companies
results = await client.search_company("Google France")
for company in results.results:
    print(f"{company.nom_entreprise} (SIRET: {company.siret})")

# Get company details
company = await client.get_company("44306184100030")

# Download document
document = await client.download_document(siret, "statuts")
with open("document.pdf", "wb") as f:
    f.write(document)
```

## Notes
- Async operations with rate limiting
- French company registry (SIRET/SIREN)
- Document downloads available
- Comprehensive company information

## API Documentation
Official Pappers API: https://www.pappers.fr/api/