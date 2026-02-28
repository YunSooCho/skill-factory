# HRmos

HRmos is a Japanese HR platform that provides comprehensive HR management including employees, departments, positions, and organizational structure.

## API Documentation

- **Base URL:** `https://api.hrmos.co/v1`
- **Authentication:** OAuth Access Token
- **Rate Limit:** Varies by plan

## Installation

```bash
pip install -r requirements.txt
```

## Example Usage

```python
from client import HRmosClient

client = HRmosClient(
    access_token="YOUR_ACCESS_TOKEN",
    company_id="YOUR_COMPANY_ID"
)

# Get employees
employees = client.get_employees()
print(f"Employees: {employees}")

# Get employee
employee = client.get_employee("12345")

# Create employee
employee_data = {"name": "John Doe", "email": "john@example.com"}
result = client.create_employee(employee_data)

# Update employee
client.update_employee("12345", {"department_id": "789"})

# Get organizations
organizations = client.get_organizations()

# Get departments
departments = client.get_departments()

# Get positions
positions = client.get_positions()
```

## Error Handling

```python
from client import HRmosClient, HRmosError

try:
    client = HRmosClient(access_token="...", company_id="...")
    employees = client.get_employees()
except HRmosError as e:
    print(f"Error: {e}")
```

## License

This integration is provided as-is for use with the Yoom platform.