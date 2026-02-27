# Salesforce Test Guide

## Environment
```bash
YOOM_SALESFORCE_USERNAME=username
YOOM_SALESFORCE_PASSWORD=password
YOOM_SALESFORCE_AUTH_TOKEN=security_token
```

## Test Connection
```python
from integration import SalesforceClient
client = SalesforceClient()
```