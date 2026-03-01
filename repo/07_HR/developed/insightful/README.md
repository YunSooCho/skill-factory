# Insightful

Insightful is an employee productivity and analytics platform that helps organizations track productivity, app usage, website activity, and generate actionable insights.

## API Documentation

- **Base URL:** `https://api.insightful.io/v1`
- **Authentication:** Bearer Token
- **Rate Limit:** Varies by plan

## Installation

```bash
pip install -r requirements.txt
```

## Example Usage

```python
from client import InsightfulClient

client = InsightfulClient(
    api_key="YOUR_API_KEY",
    workspace_id="YOUR_WORKSPACE_ID"
)

# Get employees
employees = client.get_employees()
print(f"Employees: {employees}")

# Get employee
employee = client.get_employee("12345")

# Get productivity data
productivity = client.get_productivity_data(
    start_date="2024-02-01",
    end_date="2024-02-28"
)

# Get employee productivity
emp_productivity = client.get_employee_productivity(
    employee_id="12345",
    start_date="2024-02-01",
    end_date="2024-02-28"
)

# Get activity logs
activity = client.get_activity_logs(
    start_date="2024-02-01",
    end_date="2024-02-28"
)

# Get app usage
app_usage = client.get_app_usage(
    start_date="2024-02-01",
    end_date="2024-02-28"
)

# Get website usage
web_usage = client.get_website_usage(
    start_date="2024-02-01",
    end_date="2024-02-28"
)

# Get reports
reports = client.get_reports()

# Get specific report
report_data = client.get_report("12345")

# Get projects
projects = client.get_projects()
```

## Error Handling

```python
from client import InsightfulClient, InsightfulError

try:
    client = InsightfulClient(api_key="...", workspace_id="...")
    employees = client.get_employees()
except InsightfulError as e:
    print(f"Error: {e}")
```

## License

This integration is provided as-is for use with the Yoom platform.