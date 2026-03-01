# Zoho People HR Management Integration

Zoho People is a cloud-based HR management system that provides employee onboarding, leave management, attendance tracking, and HR automation capabilities.

## Features

- Employee records management
- Leave request and approval
- Attendance tracking with geolocation
- Time tracking and project logging
- Performance management
- Document management
- Department hierarchy

## Installation

```bash
pip install -e .
```

## API Key Setup

1. Log in to your Zoho People account
2. Go to Setup > Developer Space > API
3. Generate an authentication token
4. Find your organization ID in setup
5. Store credentials securely

## Usage

```python
from zoho_people import ZohoPeopleClient

# Initialize client
client = ZohoPeopleClient(
    auth_token="your-auth-token",
    organization_id="your-org-id"
)

# Get employees
employees = client.get_employees(limit=100)
for employee in employees:
    print(f"{employee['firstName']} {employee['lastName']} - {employee['department']}")

# Get specific employee
employee = client.get_employee("EMP123")

# Create employee
new_employee = client.create_employee({
    "firstName": "John",
    "lastName": "Doe",
    "email": "john.doe@example.com",
    "department": "Engineering",
    "joiningDate": "2024-03-01"
})

# Update employee
client.update_employee("EMP123", {
    "designation": "Senior Engineer",
    "department": "Engineering"
})

# Get attendance
attendance = client.get_attendance(
    employee_id="EMP123",
    start_date="2024-01-01",
    end_date="2024-01-31"
)

# Clock in
client.clock_in(
    employee_id="EMP123",
    location="Office HQ"
)

# Clock out
client.clock_out(employee_id="EMP123")

# Get leave balance
balance = client.get_leave_balance(employee_id="EMP123")
print(f"Annual leave: {balance['annual']}")
print(f"Sick leave: {balance['sick']}")

# Request leave
leave = client.request_leave(
    employee_id="EMP123",
    leave_type="annual",
    from_date="2024-04-01",
    to_date="2024-04-03",
    days=3.0,
    reason="Personal vacation"
)

# Get leave requests
requests = client.get_leave_requests(status="pending")

# Approve leave
client.approve_leave(
    request_id="LR12345",
    comment="Approved"
)

# Reject leave
client.reject_leave(
    request_id="LR12346",
    reason="Staffing shortage"
)

# Time logs
timelogs = client.get_time_logs(
    employee_id="EMP123",
    start_date="2024-01-01",
    end_date="2024-01-31"
)

# Create time log
client.create_time_log(
    employee_id="EMP123",
    project_id="PROJ001",
    date="2024-01-15",
    hours=8.0,
    description="Developed new feature"
)

# Get departments
departments = client.get_departments()

# Get department employees
dept_employees = client.get_department_employees("DEPT001")

# Get holidays
holidays = client.get_holidays(2024)
for holiday in holidays:
    print(f"{holiday['date']}: {holiday['name']}")

# Get leave types
leave_types = client.get_leave_types()

# Get employee documents
documents = client.get_employee_documents("EMP123")

# Upload document
client.upload_document(
    employee_id="EMP123",
    document_type="contract",
    file_url="https://example.com/contract.pdf"
)
```

## API Methods

### Employee Management
- `get_employees(department, status, limit, offset)` - List employees
- `get_employee(employee_id)` - Get employee details
- `create_employee(data)` - Create new employee
- `update_employee(employee_id, data)` - Update employee
- `get_employee_documents(employee_id)` - Get documents
- `upload_document(employee_id, document_type, file_url)` - Upload document

### Attendance Management
- `get_attendance(employee_id, start_date, end_date)` - Get attendance records
- `clock_in(employee_id, timestamp, location)` - Clock in
- `clock_out(employee_id, timestamp)` - Clock out

### Leave Management
- `get_leave_balance(employee_id)` - Get leave balance
- `request_leave(employee_id, leave_type, from_date, to_date, days, reason)` - Request leave
- `get_leave_requests(employee_id, status, limit)` - Get leave requests
- `approve_leave(request_id, comment)` - Approve leave
- `reject_leave(request_id, reason)` - Reject leave

### Time Tracking
- `get_time_logs(employee_id, start_date, end_date)` - Get time logs
- `create_time_log(employee_id, project_id, date, hours, description)` - Create time log

### Department Management
- `get_departments()` - List departments
- `get_department_employees(department_id)` - Get department employees

### Settings
- `get_holidays(year)` - Get company holidays
- `get_leave_types()` - Get configured leave types

## Common Leave Types

- `annual` - Annual/vacation leave
- `sick` - Sick leave
- `casual` - Casual leave
- `maternity` - Maternity leave
- `paternity` - Paternity leave
- `unpaid` - Unpaid leave

## Error Handling

```python
try:
    employee = client.get_employee("EMP123")
except requests.RequestException as e:
    print(f"Error fetching employee: {e}")
```

## Rate Limits

Zoho People has API rate limits. The SDK handles basic retry logic, but implement exponential backoff for high-volume operations.

## Support

For API documentation, visit https://www.zoho.com/people/api/