# Akashi

Akashi is a Japanese attendance and HR management platform that helps companies track employee working hours, manage leave requests, and ensure labor compliance.

## API Documentation

- **Base URL:** `https://api.akashi.co.jp/v1`
- **Authentication:** Bearer Token
- **Rate Limit:** Varies by plan

## API Keys & Authentication

### Getting API Key

1. Login to your Akashi admin console
2. Go to Settings > API Settings
3. Generate and copy your API key
4. Note your Company ID from the settings page

## Installation

```bash
pip install -r requirements.txt
```

## Example Usage

```python
from client import AkashiClient

# Initialize client
client = AkashiClient(
    api_key="YOUR_API_KEY",
    company_id="YOUR_COMPANY_ID",
    timeout=30
)

# Get all employees
employees = client.get_employees()
print(f"Employees: {employees}")

# Get specific employee details
employee = client.get_employee("12345")
print(f"Employee: {employee}")

# Add a new employee
new_employee = {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "department": "Engineering",
    "join_date": "2024-02-28"
}
result = client.add_employee(new_employee)
print(f"Added employee: {result}")

# Update employee information
update_data = {
    "department": "Senior Engineering"
}
result = client.update_employee("12345", update_data)
print(f"Updated employee: {result}")

# Get attendance for a specific date
attendance = client.get_attendance("12345", "2024-02-28")
print(f"Attendance: {attendance}")

# Get attendance records for a date range
records = client.get_attendance_records("12345", "2024-02-01", "2024-02-28")
print(f"Attendance records: {records}")

# Clock in an employee
result = client.clock_in("12345", note="Regular work day")
print(f"Clocked in: {result}")

# Clock out an employee
result = client.clock_out("12345", note="Completed tasks")
print(f"Clocked out: {result}")

# Get work records
work_records = client.get_work_records("12345", "2024-02-01", "2024-02-28")
print(f"Work records: {work_records}")

# Get leave requests
requests = client.get_leave_requests()
print(f"Leave requests: {requests}")

# Get leave requests for a specific employee
requests = client.get_leave_requests(employee_id="12345", status="pending")
print(f"Employee leave requests: {requests}")

# Create a leave request
leave_data = {
    "employee_id": "12345",
    "type": "annual",
    "start_date": "2024-03-01",
    "end_date": "2024-03-05",
    "reason": "Family vacation"
}
result = client.create_leave_request(leave_data)
print(f"Created leave request: {result}")

# Approve a leave request
result = client.approve_leave_request("67890")
print(f"Approved leave request: {result}")

# Reject a leave request
result = client.reject_leave_request("67890", reason="Insufficient notice")
print(f"Rejected leave request: {result}")

# Get overtime requests
overtime = client.get_overtime_requests()
print(f"Overtime requests: {overtime}")

# Get departments
departments = client.get_departments()
print(f"Departments: {departments}")
```

## Error Handling

```python
from client import AkashiClient, AkashiError, AkashiRateLimitError, AkashiAuthenticationError

try:
    client = AkashiClient(api_key="...", company_id="...")
    employees = client.get_employees()
except AkashiRateLimitError:
    print("Rate limit exceeded - try again later")
except AkashiAuthenticationError:
    print("Invalid API key or credentials")
except AkashiError as e:
    print(f"Error: {e}")
```

## License

This integration is provided as-is for use with the Yoom platform.