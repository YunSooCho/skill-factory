# YukyuNote Vacation Management System Integration

YukyuNote is a Japanese vacation management system that helps companies manage paid leave, holidays, and time-off requests efficiently.

## Features

- Paid leave tracking and calculation
- Vacation request submission and approval
- Leave balance management
- Department-level leave overview
- Calendar integration
- Public holiday management
- Yearly leave summaries

## Installation

```bash
pip install -e .
```

## API Key Setup

1. Log in to your YukyuNote account
2. Navigate to Settings > API Settings
3. Generate an API key
4. Note your company ID
5. Store credentials securely

## Usage

```python
from yukyu_note import YukyuNoteClient

# Initialize client
client = YukyuNoteClient(
    api_key="your-api-key",
    company_id="your-company-id"
)

# Get leave balance
balance = client.get_leave_balance(employee_id="EMP001")
print(f"Paid leave remaining: {balance['paid_leave']['remaining']} days")

# Check leave history
history = client.get_leave_history(employee_id="EMP001", year=2024)
for record in history:
    print(f"{record['date']}: {record['type']} - {record['days']} days")

# Submit a leave request
request = client.request_leave(
    employee_id="EMP001",
    leave_type="paid",
    start_date="2024-04-01",
    end_date="2024-04-03",
    reason="Personal trip"
)
request_id = request['id']

# Get request details
details = client.get_leave_request(request_id)
print(details)

# List all pending requests
pending = client.list_leave_requests(status="pending")
for req in pending:
    print(f"{req['employee_name']}: {req['start_date']} to {req['end_date']}")

# Approve a request
client.approve_leave_request(
    request_id=request_id,
    approver_id="MGR001",
    comment="Approved"
)

# Reject a request
client.reject_leave_request(
    request_id="REQ123",
    approver_id="MGR001",
    reason="Staffing shortage on those dates"
)

# Cancel a request
client.cancel_leave_request(
    request_id="REQ456",
    employee_id="EMP001",
    reason="Plans changed"
)

# Get leave calendar
calendar = client.get_calendar(
    start_date="2024-04-01",
    end_date="2024-04-30",
    department="Engineering"
)

# Get employee yearly summary
summary = client.get_employee_summary(employee_id="EMP001", year=2024)
print(f"Total taken: {summary['total_taken']} days")
print(f"Remaining: {summary['remaining']} days")

# Get available leave types
types = client.get_leave_types()
for leave_type in types:
    print(f"{leave_type['name']}: {leave_type['description']}")

# Get public holidays
holidays = client.get_public_holidays(2024)
for holiday in holidays:
    print(f"{holiday['date']}: {holiday['name']}")

# Get department summary
dept_summary = client.get_department_summary(department_id="DEPT001", year=2024)

# Adjust leave balance (admin)
client.update_leave_balance(
    employee_id="EMP001",
    adjustment=1.5,
    reason="Carry over from previous year"
)

# List all employees
employees = client.get_employees()
```

## API Methods

### Leave Balance & History
- `get_leave_balance(employee_id)` - Get current leave balance
- `get_leave_history(employee_id, year, limit)` - Get leave history
- `get_employee_summary(employee_id, year)` - Get yearly summary

### Leave Requests
- `request_leave(employee_id, leave_type, start_date, end_date, reason, hours)` - Submit request
- `get_leave_request(request_id)` - Get request details
- `list_leave_requests(employee_id, status, start_date, end_date, limit, offset)` - List requests
- `approve_leave_request(request_id, approver_id, comment)` - Approve request
- `reject_leave_request(request_id, approver_id, reason)` - Reject request
- `cancel_leave_request(request_id, employee_id, reason)` - Cancel request

### Leave Types & Holidays
- `get_leave_types()` - Get available leave types
- `get_public_holidays(year)` - Get public holidays

### Calendar & Overviews
- `get_calendar(start_date, end_date, department)` - Get leave calendar
- `get_department_summary(department_id, year)` - Get department statistics

### Employee Management
- `get_employees()` - List all employees
- `get_employee(employee_id)` - Get employee details

### Admin Functions
- `update_leave_balance(employee_id, adjustment, reason)` - Adjust balance

## Leave Types

Common leave types in YukyuNote:
- `paid` - Paid annual leave (有給休暇)
- `sick` - Sick leave (病欠)
- `personal` - Personal leave (忌引き)
- `special` - Special leave (特別休暇)
- `parental` - Parental leave (育児休業)
- `nursing` - Nursing care leave (介護休業)

## Request Statuses

- `pending` - Waiting for approval
- `approved` - Approved
- `rejected` - Rejected
- `cancelled` - Cancelled

## Error Handling

```python
try:
    request = client.request_leave(
        employee_id="EMP001",
        leave_type="paid",
        start_date="2024-04-01",
        end_date="2024-04-03"
    )
except requests.RequestException as e:
    print(f"Error submitting leave request: {e}")
```

## Compliance

YukyuNote complies with Japanese Labor Standards Act and manages:
- 5-day work week
- Annual paid leave (minimum 10 days after 6 months)
- Sick leave provisions
- Family care leave
- Bereavement leave

## Support

For API documentation and support, visit https://yukyu-note.jp/api/