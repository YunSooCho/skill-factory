# Workable Recruiting Platform Integration

Workable is a modern recruiting platform that helps companies hire talent efficiently. It provides applicant tracking, candidate management, interview scheduling, and offer management.

## Features

- Job posting and management
- Applicant tracking system (ATS)
- Candidate communication
- Interview scheduling
- Offer management
- Pipeline management
- Team collaboration

## Installation

```bash
pip install -e .
```

## API Key Setup

1. Log in to your Workable account
2. Go to Settings > Integrations & API > API Access
3. Generate an API key
4. Note your account's subdomain (e.g., `yourcompany.workable.com`)
5. Store your credentials securely

## Usage

```python
from workable import WorkableClient

# Initialize client
client = WorkableClient(
    api_key="your-api-key",
    subdomain="yourcompany"
)

# List all jobs
jobs = client.get_jobs()
for job in jobs:
    print(f"{job['title']} - {job['state']}")

# Get job details
job = client.get_job("JOB123")
print(job['description'])

# Create a new job
new_job = client.create_job({
    "title": "Senior Software Engineer",
    "department": "Engineering",
    "location": ["San Francisco, CA"],
    "employment_type": "full_time",
    "description": "We're looking for a senior engineer..."
})

# List candidates
candidates = client.get_candidates(job_id="JOB123")
for candidate in candidates:
    print(f"{candidate['name']} - {candidate['headline']}")

# Get candidate details
candidate = client.get_candidate("CAND456")
print(candidate)

# Add candidate to job
client.add_candidate_to_job(candidate_id="CAND456", job_id="JOB123")

# Create an interview
interview = client.create_interview({
    "candidate_id": "CAND456",
    "job_id": "JOB123",
    "interview_type": "video",
    "date": "2024-03-15",
    "time": "10:00",
    "duration": 60,
    "interviewers": ["USER001", "USER002"]
})

# List interviews for a job
interviews = client.get_interviews(job_id="JOB123")

# Move candidate to next stage
client.move_candidate(
    candidate_id="CAND456",
    job_id="JOB123",
    stage_id="STAGE003"
)

# Create an offer
offer = client.create_offer({
    "candidate_id": "CAND456",
    "job_id": "JOB123",
    "salary": "150000",
    "currency": "USD"
})

# Send offer to candidate
client.send_offer(offer_id="OFFER123")

# Get recruiters
recruiters = client.get_recruiters()
```

## API Methods

### Job Management
- `get_jobs(state, limit, offset)` - List jobs
- `get_job(job_id)` - Get job details
- `create_job(data)` - Create a new job
- `update_job(job_id, data)` - Update a job

### Candidate Management
- `get_candidates(job_id, stage, limit, offset)` - List candidates
- `get_candidate(candidate_id)` - Get candidate details
- `create_candidate(data)` - Create a new candidate
- `update_candidate(candidate_id, data)` - Update candidate
- `get_candidate_activities(candidate_id, limit)` - Get activity history
- `add_candidate_to_job(candidate_id, job_id)` - Add candidate to job
- `move_candidate(candidate_id, job_id, stage_id)` - Move candidate in pipeline

### Interview Management
- `get_interviews(job_id, candidate_id, limit, offset)` - List interviews
- `create_interview(data)` - Create interview
- `update_interview(interview_id, data)` - Update interview
- `delete_interview(interview_id)` - Delete interview

### Offer Management
- `get_offers(job_id, status, limit)` - List offers
- `get_offer(offer_id)` - Get offer details
- `create_offer(data)` - Create offer
- `update_offer(offer_id, data)` - Update offer
- `send_offer(offer_id)` - Send offer to candidate

### Team Management
- `get_users()` - List all users
- `get_user(user_id)` - Get user details
- `get_recruiters()` - List recruiters
- `get_departments()` - List departments

### Pipeline Management
- `get_stages(job_id)` - Get hiring stages for a job

## Candidate Stages

Typical hiring pipeline stages:
- `applied` - Candidate submitted application
- `screened` - Initial phone screen complete
- `interview` - In-person or video interview
- `offer` - Offer sent
- `hired` - Candidate accepted offer
- `rejected` - Candidate rejected

## Error Handling

```python
try:
    candidate = client.get_candidate("CAND456")
except requests.RequestException as e:
    print(f"Error fetching candidate: {e}")
```

## Webhooks

Workable supports webhooks for real-time updates:
- Candidate created/updated
- Stage changes
- Interview scheduled
- Offer status changes

Configure webhooks in your Workable account settings.

## Rate Limits

Workable has rate limits on API requests. The SDK handles basic retry logic, but you should implement exponential backoff for high-volume operations.

## Support

For API documentation and support, visit https://developer.workable.com/