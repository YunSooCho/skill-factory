# TeamSpirit HR Integration

TeamSpirit is a comprehensive Japanese HR management system that provides attendance tracking, leave management, and employee data management.

## Installation

```bash
pip install -e .
```

## API Key Setup

1. Log in to your TeamSpirit account
2. Navigate to Settings > API Management
3. Click "Generate API Key"
4. Copy your API key and company ID
5. Store them securely in your environment variables

## Usage

```python
from teamspirit import TeamSpiritClient

# Initialize client
client = TeamSpiritClient(
    api_key="your-api-key",
    company_id="your-company-id"
)

# Get employee information
employee = client.get_employee("EMP001")
print(employee)

# List employees
employees = client.list_employees(department="Engineering")
for emp in employees:
    print(f"{emp['name']} - {emp['position']}")

# Get attendance records
attendance = client.get_attendance(
    employee_id="EMP001",
    start_date="2024-01-01",
    end_date="2024-01-31"
)

# Clock in
client.clock_in(employee_id="EMP001")

# Clock out
client.clock_out(employee_id="EMP001")

# Request leave
leave = client.request_leave(
    employee_id="EMP001",
    leave_type="annual",
    start_date="2024-02-01",
    end_date="2024-02-03",
    reason="Personal trip"
)

# Approve leave request
client.approve_leave_request(
    request_id="LR12345",
    approver_id="MGR001"
)

# Get leave balance
balance = client.get_leave_balance(employee_id="EMP001")
print(balance)

# List departments
departments = client.get_departments()

# Get department employees
dept_employees = client.get_department_employees("DEPT001")
```

## API Methods

### Employee Management
- `get_employee(employee_id)` - Get employee details
- `list_employees()` - List all employees with filters
- `update_employee(employee_id, data)` - Update employee information

### Attendance Management
- `get_attendance(employee_id, start_date, end_date)` - Get attendance records
- `clock_in(employee_id, timestamp)` - Record clock-in
- `clock_out(employee_id, timestamp)` - Record clock-out
- `get_work_schedule(employee_id, start_date, end_date)` - Get work schedule

### Leave Management
- `request_leave(employee_id, leave_type, start_date, end_date, reason)` - Submit leave request
- `get_leave_balance(employee_id)` - Get remaining leave balance
- `list_leave_requests()` - List all leave requests
- `approve_leave_request(request_id, approver_id, comment)` - Approve leave
- `reject_leave_request(request_id, approver_id, reason)` - Reject leave

### Department Management
- `get_departments()` - List all departments
- `get_department_employees(department_id)` - Get employees in a department

## Error Handling

The client raises `requests.RequestException` for API errors. Always wrap API calls in try-except blocks:

```python
try:
    employee = client.get_employee("EMP001")
except requests.RequestException as e:
    print(f"Error fetching employee: {e}")
```

## Support

For API documentation and support, visit https://support.teamspirit.com/