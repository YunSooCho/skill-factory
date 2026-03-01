# Smaregi Timecard

Smaregi Timecard is a Japan-based time attendance system that helps manage employee clock-in/out records, daily work records, monthly attendance summaries, and leave requests.

## API Documentation

- **Base URL:** `https://api.smaregi.jp/timecard/v1`
- **Authentication:** Bearer Token
- **Rate Limit:** Based on contract plan

## Installation

```bash
pip install -r requirements.txt
```

## Example Usage

```python
from client import SmaregiTimecardClient

client = SmaregiTimecardClient(
    access_token="YOUR_ACCESS_TOKEN",
    contract_id="YOUR_CONTRACT_ID"
)

# Get punch records
records = client.get_punch_records()
print(f"Records: {records}")

# Clock in employee
result = client.clock_in(employee_id="12345")

# Clock out employee
result = client.clock_out(employee_id="12345", clock_in_record_id="rec_123")

# Get daily records
daily = client.get_daily_records(employee_id="12345", date="2024-02-28")

# Get monthly records
monthly = client.get_monthly_records(year=2024, month=2)

# Get leave requests
requests = client.get_leave_requests(status="pending")

# Create leave request
leave_data = {
    "employee_id": "12345",
    "leave_type": "annual",
    "start_date": "2024-03-01",
    "end_date": "2024-03-05"
}
client.create_leave_request(leave_data)

# Approve request
client.approve_request("req_123", comment="Approved by manager")
```

## Key Features

- **Clock-in/Clock-out:** Track employee attendance
- **Daily Records:** View daily work summaries
- **Monthly Reports:** Generate monthly attendance summaries
- **Leave Management:** Create and manage leave requests
- **Approval Workflow:** Approve or reject leave requests

## Error Handling

```python
from client import SmaregiTimecardClient, SmaregiTimecardError

try:
    client = SmaregiTimecardClient(access_token="...", contract_id="...")
    records = client.get_punch_records()
except SmaregiTimecardError as e:
    print(f"Error: {e}")
```

## License

This integration is provided as-is for use with the Yoom platform.