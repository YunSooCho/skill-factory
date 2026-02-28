# BambooHR

BambooHR is a comprehensive HR management platform that helps businesses manage employee data, time off, benefits, payroll, and more in one centralized system.

## API Documentation

- **Official API Doc:** https://developers.bamboohr.com/
- **Base URL:** `https://api.bamboohr.com/api/gateway.php/{subdomain}`
- **Authentication:** Basic Auth with API Key
- **Rate Limit:** Varies by plan (typically 1000 requests per day)

## API Keys & Authentication

### Getting API Key

1. Login to your BambooHR account
2. Go to your name in the top right corner
3. Select "API Keys" from the dropdown
4. Click "Add New API Key"
5. Generate and copy the key

### Finding Your Subdomain

Your subdomain is part of your BambooHR URL:
- If your BambooHR URL is `https://company.bamboohr.com`, your subdomain is `company`

## Installation

```bash
pip install -r requirements.txt
```

## Example Usage

```python
from client import BambooHRClient

# Initialize client
client = BambooHRClient(
    subdomain="your-company",
    api_key="YOUR_API_KEY",
    timeout=30
)

# Get all employees (basic directory)
employees = client.get_company_directory()
print(f"Employees: {employees}")

# Get detailed employee list with specific fields
employees = client.get_employees(fields=['id', 'firstName', 'lastName', 'hireDate', 'department'])
print(f"Employees: {employees}")

# Get specific employee details
employee = client.get_employee("12345", fields=['id', 'firstName', 'lastName', 'email', 'jobTitle'])
print(f"Employee: {employee}")

# Add a new employee
new_employee_data = {
    "firstName": "John",
    "lastName": "Doe",
    "email": "john.doe@example.com",
    "hireDate": "2024-02-28",
    "jobTitle": "Software Engineer",
    "department": "Engineering"
}
result = client.add_employee(new_employee_data)
print(f"Added employee: {result}")

# Update employee information
update_data = {
    "jobTitle": "Senior Software Engineer",
    "department": "Engineering"
}
result = client.update_employee("12345", update_data)
print(f"Updated employee: {result}")

# Get employees updated since a date
updated = client.get_updated_employees("2024-02-01")
print(f"Updated employees: {updated}")

# Get time off requests
requests = client.get_time_off_requests()
print(f"Time off requests: {requests}")

# Get time off requests for a specific employee
requests = client.get_time_off_requests(employee_id="12345", status="approved")
print(f"Employee time off: {requests}")

# Add a time off request
time_off_data = {
    "employeeId": "12345",
    "start": "2024-03-01",
    "end": "2024-03-05",
    "type": "PTO",
    "notes": "Vacation"
}
result = client.add_time_off_request(time_off_data)
print(f"Time off request: {result}")

# Approve a time off request
result = client.change_time_off_status("67890", "approved")
print(f"Approved request: {result}")

# Get who's out (employees on time off)
whos_out = client.get_whos_out(start_date="2024-03-01", end_date="2024-03-31")
print(f"Who's out: {whos_out}")

# Get employee files
files = client.get_employee_files("12345")
print(f"Employee files: {files}")

# Get file categories
categories = client.get_employee_files_categories("12345")
print(f"File categories: {categories}")

# Upload a file
with open('document.pdf', 'rb') as f:
    result = client.upload_employee_file(
        employee_id="12345",
        category_id="1",
        file=f,
        file_name="document.pdf",
        share=True
    )
    print(f"Uploaded file: {result}")

# Get list of available reports
reports = client.get_reports_list()
print(f"Available reports: {reports}")

# Run a report
report_data = client.run_report("12345", format="JSON")
print(f"Report data: {report_data}")

# Get metadata (fields, lists, options)
meta = client.get_meta_data()
print(f"Metadata: {meta}")

# Get custom tabs
tabs = client.get_tabs()
print(f"Custom tabs: {tabs}")

# Get time off balance
balance = client.get_time_off_balance("12345")
print(f"Time off balance: {balance}")
```

## Common Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /v1/employees/directory` | Get employee directory |
| `GET /v1/employees` | Get all employees |
| `GET /v1/employees/{id}` | Get specific employee |
| `POST /v1/employees` | Add new employee |
| `POST /v1/employees/{id}` | Update employee |
| `GET /v1/employees/updated` | Get updated employees |
| `GET /v1/time_off/requests` | List time off requests |
| `GET /v1/time_off/requests/{id}` | Get specific time off request |
| `POST /v1/time_off/requests` | Add time off request |
| `PUT /v1/time_off/requests/{id}` | Change request status |
| `GET /v1/time_off/whos_out` | Get who's out |
| `GET /v1/employees/{id}/files` | Get employee files |
| `GET /v1/employees/{id}/files/categories` | Get file categories |
| `POST /v1/employees/{id}/files` | Upload employee file |
| `GET /v1/reports` | List reports |
| `GET /v1/reports/{id}` | Run report |
| `GET /v1/meta/fields` | Get metadata |
| `GET /v1/employees/{id}/time_off/balance` | Get time off balance |

## Error Handling

```python
from client import BambooHRClient, BambooHRError, BambooHRRateLimitError, BambooHRAuthenticationError

try:
    client = BambooHRClient(subdomain="your-company", api_key="YOUR_API_KEY")
    employees = client.get_employees()
except BambooHRRateLimitError:
    print("Rate limit exceeded - try again later")
except BambooHRAuthenticationError:
    print("Invalid API key or credentials")
except BambooHRError as e:
    print(f"Error: {e}")
```

## License

This integration is provided as-is for use with the Yoom platform.