# Kyuyo-Bugyo

Kyuyo-Bugyo is a Japanese payroll system that helps manage monthly payroll, salaries, deductions, allowances, bonuses, social insurance, and tax calculations.

## API Documentation

- **Base URL:** `https://api.kingtime.jp/v1`
- **Authentication:** Bearer Token + X-Company-Code header
- **Rate Limit:** Varies by plan

## Installation

```bash
pip install -r requirements.txt
```

## Example Usage

```python
from client import KyuyoBugyoClient

client = KyuyoBugyoClient(
    api_key="YOUR_API_KEY",
    company_code="YOUR_COMPANY_CODE"
)

# Get payroll
payroll = client.get_payroll(year=2024, month=3)
print(f"Payroll: {payroll}")

# Get employee payroll
emp_payroll = client.get_employee_payroll("12345", 2024, 3)

# Calculate payroll
result = client.calculate_payroll(2024, 3)

# Get salaries
salaries = client.get_salaries(2024, 3)

# Update salary
client.update_salary("12345", {
    "base_salary": 500000,
    "effective_date": "2024-03-01"
})

# Get bonuses
bonuses = client.get_bonuses(2024, 1)

# Create bonus
bonus_data = {
    "employee_id": "123",
    "amount": 500000,
    "type": "winter_bonus",
    "payment_date": "2024-12-25"
}
client.create_bonus(bonus_data)

# Get deductions
deductions = client.get_deductions("12345", 2024, 3)

# Add deduction
client.add_deduction("12345", {
    "type": "life_insurance",
    "amount": 10000,
    "month": 3,
    "year": 2024
})

# Get allowances
allowances = client.get_allowances("12345", 2024, 3)

# Add allowance
client.add_allowance("12345", {
    "type": "commutation",
    "amount": 15000,
    "month": 3,
    "year": 2024
})

# Get social insurance
social = client.get_social_insurance("12345", 2024, 3)

# Get tax info
taxes = client.get_tax_info("12345", 2024, 3)

# Get payslips
payslips = client.get_payslips(2024, 3)

# Get employee payslip
payslip = client.get_payslip("12345", 2024, 3)

# Close month
client.close_month(2024, 3)

# Get closing status
status = client.get_closing_status(2024, 3)
```

## Error Handling

```python
from client import KyuyoBugyoClient, KyuyoBugyoError

try:
    client = KyuyoBugyoClient(api_key="...", company_code="...")
    payroll = client.get_payroll(2024, 3)
except KyuyoBugyoError as e:
    print(f"Error: {e}")
```

## License

This integration is provided as-is for use with the Yoom platform.