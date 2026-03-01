# Splitwise API Client

Expense sharing platform for tracking shared expenses and settling debts between friends, roommates, and groups.

## API Key Setup

1. Log in to [Splitwise](https://splitwise.com)
2. Go to `Account` → `Your API Key`
3. Copy your API key

For OAuth 2.0 access (optional):
- Create an OAuth app in your account settings
- Get your Consumer Key and Consumer Secret

## Installation

```bash
pip install -r requirements.txt
```

## Basic Usage

```python
from splitwise import SplitwiseClient

# Initialize client
client = SplitwiseClient(api_key='your_api_key')

# Get current user info
user = client.get_current_user()
print(f"Hello, {user['user']['first_name']}")

# Get all groups
groups = client.get_groups()
print(f"You have {len(groups['groups'])} groups")

# Create a group
group = client.create_group(
    name='Roommates 2024',
    simplify_by_default=True
)
print(f"Created group: {group['group']['id']}")

# Create an expense
expense = client.create_expense(
    description='Groceries',
    cost=150.50,
    payment_method=1,  # Cash
    group_id=group['group']['id'],
    split_equally=True,
    date='2024-02-15',
    category_id=1  # Food
)
print(f"Created expense: {expense['expense']['id']}")

# Get expenses
expenses = client.get_expenses(group_id=group['group']['id'])
print(f"Total expenses in group: {len(expenses['expenses'])}")
```

## Methods

### Users
- `get_current_user()` - Get current user info
- `get_user(user_id)` - Get specific user
- `get_friends()` - Get friends list

### Groups
- `get_groups()` - List all groups
- `get_group(group_id)` - Get specific group
- `create_group(name, simplify_by_default, users)` - Create group
- `update_group(group_id, group_data)` - Update group

### Expenses
- `get_expenses(group_id, friend_id, dated_after, dated_before, limit)` - List expenses
- `get_expense(expense_id)` - Get specific expense
- `create_expense(description, cost, payment_method, ...)` - Create expense
- `update_expense(expense_id, expense_data)` - Update expense
- `delete_expense(expense_id)` - Delete expense

### Other
- `get_notifications(limit)` - Get notifications
- `get_categories()` - Get expense categories
- `send_reminder(group_id, user_id)` - Send payment reminder

## Error Handling

```python
try:
    expense = client.create_expense(description='Dinner', cost=50.0, payment_method=1)
except SplitwiseAuthenticationError:
    print("Invalid API credentials")
except SplitwiseRateLimitError:
    print("Too many requests, retry later")
except SplitwiseError as e:
    print(f"API error: {e}")
```