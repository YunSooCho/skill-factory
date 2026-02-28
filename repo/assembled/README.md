# Assembled API Client

Python async client for Assembled workforce management API.

## Features

- Agent management and status
- Scheduling
- Shift management
- Queue monitoring
- Performance metrics
- Schedule adherence tracking
- Webhook event handling

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
import asyncio
from assembled_client import AssembledClient

async def main():
    api_key = "your_key"

    async with AssembledClient(api_key) as client:
        # List agents
        agents = await client.list_agents(status="available")

        # Get queue status
        queues = await client.list_queues()
        if queues:
            status = await client.get_queue_status(queues[0].queue_id)

        # Get agent adherence
        if agents:
            adherence = await client.get_agent_adherence(agents[0].agent_id)

asyncio.run(main())
```

## API Actions

- Agent Management (get, update, list)
- Schedule Management (create, get, update)
- Shift Assignment (create)
- Queue Management (get, list)
- Performance Metrics
- Agent Adherence
- Activity Logs

## Triggers

- Agent Signs On/Off
- Shift Started/Ended
- Adherence Breach
- Queue Threshold Exceeded
- Break Started/Ended

## Documentation

- [Assembled Documentation](https://docs.assembledhq.com/)