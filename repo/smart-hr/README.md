# SmartHR

SmartHR is a Japan-based HR management system that helps manage employees, employment information, attendance, leaves, documents, and workflow approvals.

## API Documentation

- **Base URL:** `https://api.smarkthr.jp/v1`
- **Authentication:** Bearer Token

## Installation

```bash
pip install -r requirements.txt
```

## Example Usage

```python
from client import SmartHRClient

client = SmartHRClient(
    api_key="YOUR_API_KEY",
    company_id="YOUR_COMPANY_ID"
)

# Get employees
employees = client.get_employees()

# Get employee details
employee = client.get_employee("12345")

# Create employee
employee_data = {
    "name": "John Doe",
    "email": "john@example.com",
    "department": "Engineering"
}
result = client.create_employee(employee_data)

# Get leave balances
balances = client.get_leave_balances("12345")

# Create leave request
leave_data = {
    "employee_id": "12345",
    "leave_type": "annual",
    "start_date": "2024-03-01",
    "end_date": "2024-03-05"
}
client.create_leave_request(leave_data)

# Get workflows
workflows = client.get_workflows(status="pending")
```

## Key Features

- **Employee Management:** Full CRUD operations
- **Employment Info:** Track employment details and contracts
- **Attendance:** View and manage attendance records
- **Leave Management:** Balances and requests
- **Documents:** Upload and manage HR documents
- **Workflow:** Approval workflows

## License

This integration is provided as-is for use with the Yoom platform.
