# Jinji-Bugyo

Jinji-Bugyo is a Japanese payroll and HR system that helps manage employees, monthly payroll, salaries, deductions, allowances, bonuses, and social insurance.

## API Documentation

- **Base URL:** `https://api.jinji-bugyo.com/v1`
- **Authentication:** Bearer Token
- **Rate Limit:** Varies by plan

## Installation

```bash
pip install -r requirements.txt
```

## Example Usage

```python
from client import JinjiBugyoClient

client = JinjiBugyoClient(
    api_key="YOUR_API_KEY",
    company_id="YOUR_COMPANY_ID"
)

# Get employees
employees = client.get_employees()
print(f"Employees: {employees}")

# Get employee
employee = client.get_employee("12345")

# Create employee
employee_data = {"name": "John Doe", "email": "john@example.com"}
result = client.create_employee(employee_data)

# Update employee
client.update_employee("12345", {"department_id": "789"})

# Get payroll for month
payroll = client.get_payroll(year=2024, month=2)

# Get employee payroll
emp_payroll = client.get_employee_payroll("12345", year=2024, month=2)

# Get salary records
salaries = client.get_salary_records()

# Update salary
salary_data = {"base_salary": 500000, "effective_date": "2024-03-01"}
client.update_salary("12345", salary_data)

# Get deductions
deductions = client.get_deductions("12345")

# Get allowances
allowances = client.get_allowances("12345")

# Create bonus
bonus_data = {
    "employee_id": "123",
    "amount": 100000,
    "type": "performance_bonus"
}
result = client.create_bonus(bonus_data)

# Get social insurance info
social_insurance = client.get_social_insurance("12345")
```

## Error Handling

```python
from client import JinjiBugyoClient, JinjiBugyoError

try:
    client = JinjiBugyoClient(api_key="...", company_id="...")
    employees = client.get_employees()
except JinjiBugyoError as e:
    print(f"Error: {e}")
```

## License

This integration is provided as-is for use with the Yoom platform.