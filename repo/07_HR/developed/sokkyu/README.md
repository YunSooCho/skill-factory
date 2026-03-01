# Sokkyu

Sokkyu is a Japan-based rapid HR system that helps manage employees, attendance, leaves, and payroll.

## API Documentation

- **Base URL:** `https://api.sokkyu.jp/v1`
- **Authentication:** Bearer Token

## Installation

```bash
pip install -r requirements.txt
```

## Example Usage

```python
from client import SokkyuClient

client = SokkyuClient(
    api_key="YOUR_API_KEY",
    organization_id="YOUR_ORGANIZATION_ID"
)

# Get employees
employees = client.get_employees()

# Clock in
client.clock_in("12345")

# Get leave balances
balances = client.get_leave_balances("12345")

# Get payroll summary
payroll = client.get_payroll_summary(year=2024, month=2)
```

## License

This integration is provided as-is for use with the Yoom platform.
