# Rakuro

Rakuro is a Japanese HR management system that helps organizations manage employees, departments, attendance, time off, and payroll.

## API Documentation

- **Base URL:** `https://api.rakuro.jp/v1`
- **Authentication:** Bearer Token + X-Tenant-ID header
- **Rate Limit:** Varies by plan

## Installation

```bash
pip install -r requirements.txt
```

## Example Usage

```python
from client import RakuroClient

client = RakuroClient(
    api_key="YOUR_API_KEY",
    tenant_id="YOUR_TENANT_ID"
)

# Get employees
employees = client.get_employees()
print(f"Employees: {employees}")

# Get employee details
employee = client.get_employee("12345")

# Create employee
emp_data = {
    "name": "John Doe",
    "email": "john@example.com",
    "department_id": "dept_123"
}
result = client.create_employee(emp_data)

# Update employee
client.update_employee("12345", {"department_id": "dept_456"})

# Get departments
departments = client.get_departments()

# Get attendance
attendance = client.get_attendance("12345", "2024-01-01", "2024-01-31")

# Get time off requests
requests = client.get_time_off_requests("12345")

# Create time off request
request_data = {
    "type": "annual_leave",
    "start_date": "2024-04-01",
    "end_date": "2024-04-05"
}
client.create_time_off_request("12345", request_data)

# Get payroll
payroll = client.get_payroll(2024, 3)

# Get employee payroll
emp_payroll = client.get_employee_payroll("12345", 2024, 3)

# Get employee report
report = client.get_employee_report()
```

## Error Handling

```python
from client import RakuroClient, RakuroError

try:
    client = RakuroClient(api_key="...", tenant_id="...")
    employees = client.get_employees()
except RakuroError as e:
    print(f"Error: {e}")
```

## License

This integration is provided as-is for use with the Yoom platform.