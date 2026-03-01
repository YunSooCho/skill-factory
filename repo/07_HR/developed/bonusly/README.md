# Bonusly

Bonusly is an employee recognition and rewards platform that helps companies build culture through peer-to-peer appreciation, bonuses, and rewards.

## API Documentation

- **Base URL:** `https://bonus.ly/api/v3`
- **Authentication:** Bearer Token
- **Rate Limit:** Varies by plan

## API Keys & Authentication

### Getting API Key

1. Login to your Bonusly account
2. Go to Settings > Integrations > API
3. Generate and copy your API key

## Installation

```bash
pip install -r requirements.txt
```

## Example Usage

```python
from client import BonuslyClient

# Initialize client
client = BonuslyClient(api_key="YOUR_API_KEY", timeout=30)

# Get all users
users = client.get_users()
print(f"Users: {users}")

# Get specific user
user = client.get_user("12345")
print(f"User: {user}")

# Get current user
me = client.get_current_user()
print(f"Current user: {me}")

# Get bonuses
bonuses = client.get_bonuses()
print(f"Bonuses: {bonuses}")

# Get bonuses for specific user
bonuses = client.get_bonuses(params={'giver_id': '12345'})
print(f"User bonuses: {bonuses}")

# Get specific bonus
bonus = client.get_bonus("67890")
print(f"Bonus: {bonus}")

# Create a bonus
bonus_data = {
    "giver_id": "12345",
    "receiver_ids": ["67890"],
    "amount": 10,
    "reason": "Great work on the project!",
    "expense_id": "12345"
}
result = client.create_bonus(bonus_data)
print(f"Created bonus: {result}")

# Delete a bonus
result = client.delete_bonus("67890")
print(f"Deleted bonus: {result}")

# Get rewards
rewards = client.get_rewards()
print(f"Rewards: {rewards}")

# Get specific reward
reward = client.get_reward("12345")
print(f"Reward: {reward}")

# Get achievements
achievements = client.get_achievements()
print(f"Achievements: {achievements}")

# Get leaderboard
leaderboard = client.get_leaderboard()
print(f"Leaderboard: {leaderboard}")

# Get company info
company = client.get_company()
print(f"Company: {company}")
```

## Error Handling

```python
from client import BonuslyClient, BonuslyError, BonuslyRateLimitError, BonuslyAuthenticationError

try:
    client = BonuslyClient(api_key="YOUR_API_KEY")
    users = client.get_users()
except BonuslyRateLimitError:
    print("Rate limit exceeded - try again later")
except BonuslyAuthenticationError:
    print("Invalid API key")
except BonuslyError as e:
    print(f"Error: {e}")
```

## License

This integration is provided as-is for use with the Yoom platform.