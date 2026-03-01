# Convenia

Convenia is a Brazilian HR management platform that helps companies manage employees, payroll, benefits, and time off.

## API Documentation

- **Base URL:** `https://api.convenia.com.br/v1`
- **Authentication:** Bearer Token
- **Rate Limit:** Varies by plan

## Installation

```bash
pip install -r requirements.txt
```

## Example Usage

```python
from client import ConveniaClient

client = ConveniaClient(api_key="YOUR_API_KEY")

# Get employees
employees = client.get_employees()
print(f"Employees: {employees}")

# Create employee
employee_data = {"name": "John Doe", "email": "john@example.com"}
result = client.create_employee(employee_data)

# Get payroll
payroll = client.get_payroll(start_date="2024-02-01", end_date="2024-02-28")

# Get benefits
benefits = client.get_benefits()

# Get time off requests
requests = client.get_time_off_requests()
```

## Error Handling

```python
from client import ConveniaClient, ConveniaError

try:
    client = ConveniaClient(api_key="...")
    employees = client.get_employees()
except ConveniaError as e:
    print(f"Error: {e}")
```

## License

This integration is provided as-is for use with the Yoom platform.