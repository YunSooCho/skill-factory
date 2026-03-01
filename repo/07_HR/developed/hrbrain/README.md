# HRBrain

HRBrain is a Japanese HR management platform that provides employee management, performance tracking, training, and goals management.

## API Documentation

- **Base URL:** `https://api.hrbrain.co.jp/v1`
- **Authentication:** Bearer Token
- **Rate Limit:** Varies by plan

## Installation

```bash
pip install -r requirements.txt
```

## Example Usage

```python
from client import HRBrainClient

client = HRBrainClient(
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

# Get performances
performances = client.get_performances()

# Get employee performances
performances = client.get_performances(employee_id="12345")

# Create performance record
performance_data = {
    "employee_id": "123",
    "rating": 5,
    "reviewer_id": "456"
}
result = client.create_performance(performance_data)

# Get trainings
trainings = client.get_trainings()

# Create training
training_data = {
    "title": "Leadership Workshop",
    "employee_ids": ["123", "456"]
}
result = client.create_training(training_data)

# Get goals
goals = client.get_goals()

# Create goal
goal_data = {
    "title": "Complete certification",
    "employee_id": "123"
}
result = client.create_goal(goal_data)

# Get surveys
surveys = client.get_surveys()
```

## Error Handling

```python
from client import HRBrainClient, HRBrainError

try:
    client = HRBrainClient(api_key="...", company_id="...")
    employees = client.get_employees()
except HRBrainError as e:
    print(f"Error: {e}")
```

## License

This integration is provided as-is for use with the Yoom platform.