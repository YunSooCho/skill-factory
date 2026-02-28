# King of Time

King of Time is a Japanese time and attendance management system that helps organizations track employee working hours, overtime, vacations, and leave requests.

## API Documentation

- **Base URL:** `https://api.ta.kingtime.jp/independent/api/v1`
- **Authentication:** Bearer Token + X-Company-Code header
- **Rate Limit:** Varies by plan

## Installation

```bash
pip install -r requirements.txt
```

## Example Usage

```python
from client import KingOfTimeClient

client = KingOfTimeClient(
    api_token="YOUR_API_TOKEN",
    company_code="YOUR_COMPANY_CODE"
)

# Get employees
employees = client.get_employees()
print(f"Employees: {employees}")

# Get employee details
employee = client.get_employee("12345")

# Get daily attendance
attendance = client.get_daily_attendance("12345", "2024-03-01")

# Update daily attendance
client.update_daily_attendance("12345", "2024-03-01", {
    "start_time": "09:00",
    "end_time": "18:00",
    "break_time": "01:00"
})

# Clock in
client.clock_in("12345")

# Clock out
client.clock_out("12345")

# Get monthly attendance
monthly = client.get_monthly_attendance("12345", 2024, 3)

# Get time off requests
requests = client.get_time_off_requests("12345")

# Create time off request
request_data = {
    "type": "annual_leave",
    "start_date": "2024-04-01",
    "end_date": "2024-04-05",
    "reason": "Personal vacation"
}
result = client.create_time_off_request("12345", request_data)

# Approve time off request
client.approve_time_off_request("req_123")

# Reject time off request
client.reject_time_off_request("req_456", "Insufficient coverage")

# Get overtime records
overtime = client.get_overtime_records("12345", "2024-01-01", "2024-01-31")

# Get schedule
schedule = client.get_schedule("12345", "2024-03-01", "2024-03-31")

# Update schedule
client.update_schedule("12345", {
    "date": "2024-03-01",
    "start_time": "09:00",
    "end_time": "18:00",
    "work_location_id": "loc_001"
})

# Get work locations
locations = client.get_work_locations()
```

## Error Handling

```python
from client import KingOfTimeClient, KingOfTimeError

try:
    client = KingOfTimeClient(api_token="...", company_code="...")
    employees = client.get_employees()
except KingOfTimeError as e:
    print(f"Error: {e}")
```

## License

This integration is provided as-is for use with the Yoom platform.