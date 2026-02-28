# Alooma API Client (Deprecated)

⚠️ **DEPRECATED** - Alooma was acquired by Google Cloud and is now part of Google Cloud Data Fusion.

This implementation is maintained only for historical reference and migration purposes.

## Migration Options

For new projects, consider these modern alternatives:

- **Google Cloud Data Fusion**: https://cloud.google.com/data-fusion
- **Apache Airflow**: https://airflow.apache.org
- **dbt**: https://www.getdbt.com
- **Fivetran**: https://fivetran.com
- **Airbyte**: https://airbyte.com

## Features (Legacy)

- Pipeline management (create, get, update, list)
- Pipeline control (start, stop)
- Pipeline status monitoring
- Transformations
- Metrics

## Usage (For Migration Reference Only)

```python
import asyncio
from looma_client import AloomaClient

async def main():
    # This service is deprecated - for migration reference only
    api_token = "legacy_token"

    async with AloomaClient(api_token) as client:
        # Get migration suggestions
        suggestions = client.get_migration_suggestions()

asyncio.run(main())
```

## Legacy API Actions

- Pipeline Management (create, get, update, list, start, stop)
- Pipeline Status
- Transformations
- Pipeline Metrics

## Documentation

- [Google Cloud Data Fusion](https://cloud.google.com/data-fusion/docs)