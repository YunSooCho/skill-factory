# Giriton

Giriton is a cloud attendance management platform that helps track employee working hours, manage clock in/out, and handle leave requests.

## API Documentation

- **Base URL:** `https://api.giriton.com/v1`
- **Authentication:** Bearer Token
- **Rate Limit:** Varies by plan

## Installation

```bash
pip install -r requirements.txt
```

## Example Usage

```python
from client import GiritonClient

client = GiritonClient(api_key="YOUR_API_KEY")

# Get employees
employees = client.get_employees()
print(f"Employees: {employees}")

# Get employee
employee = client.get_employee("12345")

# Create employee
employee_data = {"name": "John Doe", "email": "john@example.com"}
result = client.create_employee(employee_data)

# Get attendance for date
attendance = client.get_attendance("12345", "2024-02-28")

# Get attendance records
records = client.get_attendance_records("12345", "2024-02-01", "2024-02-28")

# Clock in
client.clock_in("12345", timestamp="2024-02-28T09:00:00Z")

# Clock out
client.clock_out("12345", timestamp="2024-02-28T18:00:00Z")

# Get leave requests
requests = client.get_leave_requests()

# Create leave request
request_data = {
    "employee_id": "123",
    "start_date": "2024-03-01",
    "end_date": "2024-03-05"
}
result = client.create_leave_request(request_data)
```

## Error Handling

```python
from client import GiritonClient, GiritonError

try:
    client = GiritonClient(api_key="...")
    employees = client.get_employees()
except GiritonError as e:
    print(f"Error: {e}")
```

## License

This integration is provided as-is for use with the Yoom platform.