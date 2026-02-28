# Employment Hero

Employment Hero is an HR and payroll platform that helps businesses manage employees, benefits, leave, and pay runs.

## API Documentation

- **Base URL:** `https://api.employmenthero.com/v1`
- **Authentication:** Bearer Token
- **Rate Limit:** Varies by plan

## Installation

```bash
pip install -r requirements.txt
```

## Example Usage

```python
from client import EmploymentHeroClient

client = EmploymentHeroClient(
    api_key="YOUR_API_KEY",
    business_id="YOUR_BUSINESS_ID"
)

# Get employees
employees = client.get_employees()
print(f"Employees: {employees}")

# Create employee
employee_data = {"first_name": "John", "last_name": "Doe"}
result = client.create_employee(employee_data)

# Get pay items
pay_items = client.get_pay_items()

# Get leave requests
requests = client.get_leave_requests()

# Create leave request
request_data = {
    "employee_id": "123",
    "start_date": "2024-03-01",
    "end_date": "2024-03-05"
}
result = client.create_leave_request(request_data)

# Get pay slips
pay_slips = client.get_pay_slips()

# Get payroll
payroll = client.get_payroll()
```

## Error Handling

```python
from client import EmploymentHeroClient, EmploymentHeroError

try:
    client = EmploymentHeroClient(api_key="...", business_id="...")
    employees = client.get_employees()
except EmploymentHeroError as e:
    print(f"Error: {e}")
```

## License

This integration is provided as-is for use with the Yoom platform.