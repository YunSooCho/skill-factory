# HRmos Kintai API

HRmos Kintai API provides attendance management functionality including clock in/out tracking, working hour calculation, and leave management.

## API Documentation

- **Base URL:** `https://api.hrmos.co/kintai/v1`
- **Authentication:** OAuth Access Token
- **Rate Limit:** Varies by plan

## Installation

```bash
pip install -r requirements.txt
```

## Example Usage

```python
from client import HRmosKintaiClient

client = HRmosKintaiClient(
    access_token="YOUR_ACCESS_TOKEN",
    company_id="YOUR_COMPANY_ID"
)

# Get employees
employees = client.get_employees()
print(f"Employees: {employees}")

# Get employee
employee = client.get_employee("12345")

# Get attendance for date
attendance = client.get_attendance("12345", "2024-02-28")

# Get attendance records
records = client.get_attendance_records("12345", "2024-02-01", "2024-02-28")

# Clock in
client.clock_in("12345", timestamp="2024-02-28T09:00:00Z", note="Ready to work")

# Clock out
client.clock_out("12345", timestamp="2024-02-28T18:00:00Z", note="Done for the day")

# Get work records
work_records = client.get_work_records("12345", "2024-02-01", "2024-02-28")

# Get leave requests
requests = client.get_leave_requests()

# Create leave request
request_data = {
    "employee_id": "123",
    "start_date": "2024-03-01",
    "end_date": "2024-03-05",
    "reason": "Family vacation"
}
result = client.create_leave_request(request_data)

# Approve leave request
client.approve_leave_request("67890")

# Get overtime requests
overtime = client.get_overtime_requests()
```

## Error Handling

```python
from client import HRmosKintaiClient, HRmosKintaiError

try:
    client = HRmosKintaiClient(access_token="...", company_id="...")
    employees = client.get_employees()
except HRmosKintaiError as e:
    print(f"Error: {e}")
```

## License

This integration is provided as-is for use with the Yoom platform.