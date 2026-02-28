# MoneyForward Admina

MoneyForward Admina is a Japanese cloud-based HR and expense management system that helps organizations manage employees, payroll, approval workflows, time off, expenses, and invoices.

## API Documentation

- **Base URL:** `https://invoice.moneyforward.com/api/v2`
- **Authentication:** Bearer Token + X-Tenant-ID header
- **Rate Limit:** Varies by plan

## Installation

```bash
pip install -r requirements.txt
```

## Example Usage

```python
from client import MoneyForwardAdminaClient

client = MoneyForwardAdminaClient(
    api_key="YOUR_API_KEY",
    company_id="YOUR_COMPANY_ID"
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
    "department_id": "dept_123",
    "employment_type": "full_time"
}
result = client.create_employee(emp_data)

# Update employee
client.update_employee("12345", {"department_id": "dept_456"})

# Get departments
departments = client.get_departments()

# Create department
dept_data = {"name": "Engineering", "parent_id": "dept_001"}
client.create_department(dept_data)

# Get payroll
payroll = client.get_payroll(2024, 3)

# Get employee payroll
emp_payroll = client.get_employee_payroll("12345", 2024, 3)

# Get approval requests
requests = client.get_approval_requests()

# Approve request
client.approve_request("req_123")

# Approve with comment
client.approve_request("req_123", "Approved as requested")

# Reject request
client.reject_request("req_456", "Insufficient documentation")

# Get time off
time_off = client.get_time_off("12345")

# Request time off
time_off_data = {
    "type": "annual_leave",
    "start_date": "2024-04-01",
    "end_date": "2024-04-05",
    "reason": "Personal vacation"
}
client.request_time_off("12345", time_off_data)

# Get expenses
expenses = client.get_expenses()

# Create expense
expense_data = {
    "employee_id": "123",
    "amount": 5000,
    "category": "transportation",
    "date": "2024-03-01",
    "description": "Business trip"
}
client.create_expense(expense_data)

# Get employee expenses
emp_expenses = client.get_employee_expenses("12345")

# Get invoices
invoices = client.get_invoices()

# Create invoice
invoice_data = {
    "client_id": "client_001",
    "amount": 100000,
    "due_date": "2024-04-30",
    "items": [...]
}
client.create_invoice(invoice_data)

# Get payroll report
payroll_report = client.get_payroll_report(2024, 3)

# Get expense report
expense_report = client.get_expense_report("2024-01-01", "2024-03-31")
```

## Error Handling

```python
from client import MoneyForwardAdminaClient, MoneyForwardAdminaError

try:
    client = MoneyForwardAdminaClient(api_key="...", company_id="...")
    employees = client.get_employees()
except MoneyForwardAdminaError as e:
    print(f"Error: {e}")
```

## License

This integration is provided as-is for use with the Yoom platform.