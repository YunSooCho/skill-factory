# Kaonavi

Kaonavi is a Japanese HR management system that helps organizations manage employee information, organizational structure, departments, positions, and employment status.

## API Documentation

- **Base URL:** `https://api.ta.kingtime.jp/independent/api/v1`
- **Authentication:** X-API-Key header
- **Rate Limit:** Varies by plan

## Installation

```bash
pip install -r requirements.txt
```

## Example Usage

```python
from client import KaonaviClient

client = KaonaviClient(
    api_key="YOUR_API_KEY",
    company_code="YOUR_COMPANY_CODE"
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
    "position_id": "pos_456"
}
result = client.create_employee(emp_data)

# Update employee
client.update_employee("12345", {"department_id": "dept_789"})

# Delete employee
client.delete_employee("12345")

# Get departments
departments = client.get_departments()

# Create department
dept_data = {"name": "Engineering", "parent_id": "dept_001"}
client.create_department(dept_data)

# Get positions
positions = client.get_positions()

# Get employment statuses
statuses = client.get_employment_statuses()

# Update employment status
client.update_employment_status("12345", {"status": "active", "effective_date": "2024-03-01"})

# Get custom fields
fields = client.get_custom_fields()

# Update custom field
client.update_custom_field("12345", "field_001", "Custom Value")

# Get attendance records
attendance = client.get_attendance("12345", "2024-01-01", "2024-01-31")

# Get reports
emp_report = client.get_employee_report()
org_report = client.get_organization_report()
```

## Error Handling

```python
from client import KaonaviClient, KaonaviError

try:
    client = KaonaviClient(api_key="...", company_code="...")
    employees = client.get_employees()
except KaonaviError as e:
    print(f"Error: {e}")
```

## License

This integration is provided as-is for use with the Yoom platform.