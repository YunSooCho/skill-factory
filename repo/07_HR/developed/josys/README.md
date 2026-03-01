# Josys

Josys is a Japanese IT asset management platform that helps organizations manage SaaS applications, hardware devices, employee access, and compliance.

## API Documentation

- **Base URL:** `https://api.josys.io/v1`
- **Authentication:** Bearer Token
- **Rate Limit:** Varies by plan

## Installation

```bash
pip install -r requirements.txt
```

## Example Usage

```python
from client import JosysClient

client = JosysClient(api_key="YOUR_API_KEY")

# Get SaaS applications
apps = client.get_applications()
print(f"Applications: {apps}")

# Get application details
app = client.get_application("app_123")

# Create application
app_data = {"name": "Slack", "category": "Communication", "url": "https://slack.com"}
result = client.create_application(app_data)

# Get employees
employees = client.get_employees()

# Get employee's applications
emp_apps = client.get_employee_applications("emp_123")

# Assign application to employee
client.assign_application("emp_123", "app_456")

# Revoke application access
client.revoke_application("emp_123", "assignment_789")

# Get devices
devices = client.get_devices()

# Register device
device_data = {"type": "Laptop", "serial": "SN123456", "model": "MacBook Pro"}
client.create_device(device_data)

# Assign device to employee
client.assign_device("dev_123", "emp_456")

# Get usage statistics
stats = client.get_usage_stats("app_123", "2024-01-01", "2024-01-31")

# Get license usage
licenses = client.get_license_usage("app_123")

# Get alerts
alerts = client.get_alerts()
```

## Error Handling

```python
from client import JosysClient, JosysError

try:
    client = JosysClient(api_key="...")
    apps = client.get_applications()
except JosysError as e:
    print(f"Error: {e}")
```

## License

This integration is provided as-is for use with the Yoom platform.