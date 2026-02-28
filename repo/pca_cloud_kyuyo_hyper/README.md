# PCA Cloud Kyuyo Hyper

PCA Cloud Kyuyo Hyper is an advanced Japanese cloud-based payroll system with comprehensive features for managing monthly payroll, payslips, compensation, deductions, allowances, bonuses, and social insurance.

## API Documentation

- **Base URL:** `https://api-cloud.pc-cloud.jp/hyper/v1`
- **Authentication:** Bearer Token + X-Company-Code header
- **Rate Limit:** Varies by plan

## Installation

```bash
pip install -r requirements.txt
```

## Example Usage

```python
from client import PcaCloudKyuyoHyperClient

client = PcaCloudKyuyoHyperClient(
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
    "department_id": "dept_123"
}
result = client.create_employee(emp_data)

# Get payroll
payroll = client.get_payroll(2024, 3)

# Get employee payroll
emp_payroll = client.get_employee_payroll("12345", 2024, 3)

# Get payslips
payslips = client.get_payslips(2024, 3)

# Get payslip
payslip = client.get_payslip("12345", 2024, 3)

# Get compensation
compensation = client.get_compensation("12345", 2024, 3)

# Update compensation
client.update_compensation("12345", {
    "base_salary": 500000,
    "bonus_salary": 100000,
    "effective_date": "2024-03-01"
})

# Get deductions
deductions = client.get_deductions("12345", 2024, 3)

# Get allowances
allowances = client.get_allowances("12345", 2024, 3)

# Get bonuses
bonuses = client.get_bonuses(2024)

# Create bonus
bonus_data = {
    "employee_id": "123",
    "amount": 500000,
    "type": "winter_bonus",
    "payment_date": "2024-12-25"
}
client.create_bonus(bonus_data)

# Get social insurance
social = client.get_social_insurance("12345", 2024, 3)

# Get taxes
taxes = client.get_taxes("12345", 2024, 3)

# Get payroll report
report = client.get_payroll_report(2024, 3, "detailed")

# Close month
client.close_month(2024, 3)

# Get closing status
status = client.get_closing_status(2024, 3)
```

## Error Handling

```python
from client import PcaCloudKyuyoHyperClient, PcaCloudKyuyoHyperError

try:
    client = PcaCloudKyuyoHyperClient(api_key="...", company_code="...")
    payroll = client.get_payroll(2024, 3)
except PcaCloudKyuyoHyperError as e:
    print(f"Error: {e}")
```

## License

This integration is provided as-is for use with the Yoom platform.