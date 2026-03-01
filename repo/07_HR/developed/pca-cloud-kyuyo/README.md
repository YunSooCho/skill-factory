# PCA Cloud Kyuyo

PCA Cloud Kyuyo is a Japanese cloud-based payroll system that helps organizations manage monthly payroll, payslips, salaries, deductions, allowances, bonuses, and social insurance.

## API Documentation

- **Base URL:** `https://api-cloud.pc-cloud.jp/payslip/v2`
- **Authentication:** Bearer Token + X-Company-Code header
- **Rate Limit:** Varies by plan

## Installation

```bash
pip install -r requirements.txt
```

## Example Usage

```python
from client import PcaCloudKyuyoClient

client = PcaCloudKyuyoClient(
    api_key="YOUR_API_KEY",
    company_code="YOUR_COMPANY_CODE"
)

# Get employees
employees = client.get_employees()
print(f"Employees: {employees}")

# Get employee details
employee = client.get_employee("12345")

# Get payroll
payroll = client.get_payroll(2024, 3)

# Get employee payroll
emp_payroll = client.get_employee_payroll("12345", 2024, 3)

# Get payslips
payslips = client.get_payslips(2024, 3)

# Get payslip
payslip = client.get_payslip("12345", 2024, 3)

# Download payslip PDF
pdf_data = client.download_payslip_pdf("12345", 2024, 3)
with open("payslip_202403.pdf", "wb") as f:
    f.write(pdf_data)

# Get salaries
salaries = client.get_salaries(2024, 3)

# Update salary
client.update_salary("12345", {
    "base_salary": 500000,
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
report = client.get_payroll_report(2024, 3)

# Close month
client.close_month(2024, 3)

# Get closing status
status = client.get_closing_status(2024, 3)
```

## Error Handling

```python
from client import PcaCloudKyuyoClient, PcaCloudKyuyoError

try:
    client = PcaCloudKyuyoClient(api_key="...", company_code="...")
    payroll = client.get_payroll(2024, 3)
except PcaCloudKyuyoError as e:
    print(f"Error: {e}")
```

## License

This integration is provided as-is for use with the Yoom platform.