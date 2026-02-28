# CATS

CATS is an applicant tracking system (ATS) that helps businesses manage their recruitment process, candidates, job postings, and hiring pipelines.

## API Documentation

- **Base URL:** `https://api.catsone.com/v3`
- **Authentication:** Bearer Token
- **Rate Limit:** Varies by plan

## API Keys & Authentication

### Getting API Key

1. Login to your CATS account
2. Go to Settings > API Access
3. Generate and copy your API key

## Installation

```bash
pip install -r requirements.txt
```

## Example Usage

```python
from client import CATSClient

# Initialize client
client = CATSClient(api_key="YOUR_API_KEY", timeout=30)

# Get candidates
candidates = client.get_candidates()
print(f"Candidates: {candidates}")

# Get specific candidate
candidate = client.get_candidate("12345")
print(f"Candidate: {candidate}")

# Create a candidate
candidate_data = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone": "555-1234"
}
result = client.create_candidate(candidate_data)
print(f"Created candidate: {result}")

# Update candidate
update_data = {"title": "Senior Engineer"}
result = client.update_candidate("12345", update_data)
print(f"Updated candidate: {result}")

# Get jobs
jobs = client.get_jobs()
print(f"Jobs: {jobs}")

# Get specific job
job = client.get_job("12345")
print(f"Job: {job}")

# Create a job
job_data = {
    "title": "Software Engineer",
    "description": "..."
}
result = client.create_job(job_data)
print(f"Created job: {result}")

# Get pipelines
pipelines = client.get_pipelines()
print(f"Pipelines: {pipelines}")

# Get activities
activities = client.get_activities()
print(f"Activities: {activities}")

# Get companies
companies = client.get_companies()
print(f"Companies: {companies}")
```

## Error Handling

```python
from client import CATSClient, CATSError, CATSRateLimitError, CATSAuthenticationError

try:
    client = CATSClient(api_key="YOUR_API_KEY")
    candidates = client.get_candidates()
except CATSRateLimitError:
    print("Rate limit exceeded")
except CATSAuthenticationError:
    print("Invalid API key")
except CATSError as e:
    print(f"Error: {e}")
```

## License

This integration is provided as-is for use with the Yoom platform.