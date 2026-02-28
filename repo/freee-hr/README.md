# freee HR

freee HR is a Japanese cloud HR platform that helps manage employees, working hours, leave requests, and organizational structure.

## API Documentation

- **Base URL:** `https://api.freee.co.jp/hr/api/v1`
- **Authentication:** OAuth Access Token
- **Rate Limit:** Varies by plan

## Installation

```bash
pip install -r requirements.txt
```

## Example Usage

```python
from client import FreeeHRClient

client = FreeeHRClient(
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

# Get work types
work_types = client.get_work_types()

# Get departments
departments = client.get_departments()

# Get leave types
leave_types = client.get_leave_types()

# Get time off requests
requests = client.get_time_off_requests()

# Create time off request
request_data = {
    "employee_id": "123",
    "leave_type_id": "1",
    "start_date": "2024-03-01"
}
result = client.create_time_off_request(request_data)

# Approve request
client.approve_time_off_request("67890")
```

## Error Handling

```python
from client import FreeeHRClient, FreeeHRError

try:
    client = FreeeHRClient(access_token="...", company_id="...")
    employees = client.get_employees()
except FreeeHRError as e:
    print(f"Error: {e}")
```

## License

This integration is provided as-is for use with the Yoom platform.