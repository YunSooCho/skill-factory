# Eden

Eden is an employee engagement platform that helps companies measure and improve employee satisfaction through surveys, recognition, and goals.

## API Documentation

- **Base URL:** `https://api.eden.io/v1`
- **Authentication:** Bearer Token
- **Rate Limit:** Varies by plan

## Installation

```bash
pip install -r requirements.txt
```

## Example Usage

```python
from client import EdenClient

client = EdenClient(api_key="YOUR_API_KEY")

# Get employees
employees = client.get_employees()
print(f"Employees: {employees}")

# Create employee
employee_data = {"name": "John Doe", "email": "john@example.com"}
result = client.create_employee(employee_data)

# Get surveys
surveys = client.get_surveys()

# Create survey
survey_data = {"title": "Employee Satisfaction", "questions": [...]}
result = client.create_survey(survey_data)

# Get recognitions
recognitions = client.get_recognitions()

# Create recognition
recognition_data = {
    "from_user_id": "1",
    "to_user_id": "2",
    "message": "Great work!"
}
result = client.create_recognition(recognition_data)

# Get goals
goals = client.get_goals()

# Create goal
goal_data = {"title": "Complete project", "employee_id": "1"}
result = client.create_goal(goal_data)
```

## Error Handling

```python
from client import EdenClient, EdenError

try:
    client = EdenClient(api_key="...")
    employees = client.get_employees()
except EdenError as e:
    print(f"Error: {e}")
```

## License

This integration is provided as-is for use with the Yoom platform.