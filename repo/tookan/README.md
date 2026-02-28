# Tookan API Integration

## Overview
Complete Tookan field service management API client for Yoom automation. Supports tasks, agents, teams, customers, tracking, and analytics.

## Supported Features
- ✅ Create and manage tasks
- ✅ Agent and team management
- ✅ Customer management
- ✅ Pickup and delivery workflows
- ✅ Geofence and zone management
- ✅ Real-time agent tracking
- ✅ Task analytics and statistics
- ✅ Location-based operations

## Setup

### 1. Get API Key
Visit https://tookan.app/developer-apis to get your API key.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure
```bash
export TOOKAN_API_KEY="your_api_key_here"
```

## Usage

```python
import os
from tookan_client import TookanAPIClient

os.environ['TOOKAN_API_KEY'] = 'your_api_key'

client = TookanAPIClient()

# Create task
task = client.create_task(
    customer_id='cust_123',
    team_id='team_456',
    job_description='Deliver package',
    job_address='123 Main St, City',
    job_latitude=40.7128,
    job_longitude=-74.0060,
    has_delivery=True,
    delivery_address='456 Elm St, City'
)

# List tasks
tasks = client.list_tasks(team_id='team_456', status='inprogress')

# Get agent location
location = client.get_agent_location(user_id='agent_789')

# Get stats
stats = client.get_task_stats(
    start_date='2024-01-01',
    end_date='2024-01-31'
)

client.close()
```