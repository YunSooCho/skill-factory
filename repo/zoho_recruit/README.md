# Zoho Recruit ATS Integration

Zoho Recruit is an applicant tracking system (ATS) that helps companies manage their recruitment process from job postings to candidate hiring.

## Features

- Job posting and management
- Candidate database and tracking
- Application management
- Interview scheduling
- Offer management
- Recruitment pipeline visualization
- Client management (for agencies)
- Resume parsing

## Installation

```bash
pip install -e .
```

## API Key Setup

1. Log in to your Zoho Recruit account
2. Go to Setup > Developer Space > API
3. Generate an authentication token
4. Find your organization ID in setup
5. Store credentials securely

## Usage

```python
from zoho_recruit import ZohoRecruitClient

# Initialize client
client = ZohoRecruitClient(
    auth_token="your-auth-token",
    organization_id="your-org-id"
)

# Get job openings
jobs = client.get_jobs(status="Open")
for job in jobs:
    print(f"{job['Job_Title']} - {job['Department']}")

# Create job
new_job = client.create_job({
    "Job_Title": "Senior Software Engineer",
    "Department": "Engineering",
    "Job_Description": "We're looking for...",
    "Hiring_Manager": "John Doe",
    "Status": "Open"
})

# Get candidates
candidates = client.get_candidates(status="Active")
for candidate in candidates:
    print(f"{candidate['First_Name']} {candidate['Last_Name']} - {candidate['Current_Status']}")

# Create candidate
candidate = client.create_candidate({
    "First_Name": "Jane",
    "Last_Name": "Smith",
    "Email": "jane@example.com",
    "Phone": "+1234567890",
    "Current_Status": "Active"
})

# Get applications
applications = client.get_applications(job_id="JOB123")

# Create application
application = client.create_application({
    "Candidate_ID": candidate['id'],
    "Job_Opening_ID": "JOB123",
    "Status": "Applied"
})

# Get pipeline
pipeline = client.get_pipeline("JOB123")
for stage in pipeline.get('stages', []):
    print(f"{stage['name']}: {len(stage['candidates'])} candidates")

# Move application to next stage
client.move_application(application_id="APP123", stage_id="STAGE003")

# Create interview
interview = client.create_interview({
    "Candidate_ID": candidate['id'],
    "Job_Opening_ID": "JOB123",
    "Interview_Title": "Technical Interview",
    "Interview_Type": "Video",
    "From_Time": "2024-03-15T10:00:00",
    "To_Time": "2024-03-15T11:00:00",
    "Interviewer": "john@company.com"
})

# Get interviews
interviews = client.get_interviews(candidate_id="CAND123")

# Create offer
offer = client.create_offer({
    "Candidate_ID": candidate['id'],
    "Job_Opening_ID": "JOB123",
    "Offer_Status": "Draft",
    "Salary": "150000",
    "Currency": "USD"
})

# Get offers
offers = client.get_offers(status="Sent")

# Add note to candidate
client.create_note(
    record_id=candidate['id'],
    note_text="Candidate has strong technical skills and great communication",
    module="Candidates"
)

# Upload resume
client.upload_file(
    record_id=candidate['id'],
    file_url="https://example.com/resume.pdf",
    module="Candidates"
)

# Search candidates
results = client.search_candidates("python developer", limit=20)

# Get activities
activities = client.get_activities(record_id="CAND123")

# Get clients (for agencies)
clients = client.get_clients()

# Get client contacts
contacts = client.get_contacts(client_id="CLIENT123")
```

## API Methods

### Job Management
- `get_jobs(status, limit, offset)` - List job openings
- `get_job(job_id)` - Get job details
- `create_job(data)` - Create job opening
- `update_job(job_id, data)` - Update job
- `delete_job(job_id)` - Delete job

### Candidate Management
- `get_candidates(job_id, status, limit, offset)` - List candidates
- `get_candidate(candidate_id)` - Get candidate details
- `create_candidate(data)` - Create candidate
- `update_candidate(candidate_id, data)` - Update candidate
- `delete_candidate(candidate_id)` - Delete candidate
- `search_candidates(query, limit)` - Search candidates

### Application Management
- `get_applications(job_id, candidate_id, status, limit, offset)` - List applications
- `get_application(application_id)` - Get application details
- `create_application(data)` - Create application
- `update_application(application_id, data)` - Update application

### Interview Management
- `get_interviews(job_id, candidate_id, status, limit)` - List interviews
- `create_interview(data)` - Create interview
- `update_interview(interview_id, data)` - Update interview
- `delete_interview(interview_id)` - Delete interview

### Offer Management
- `get_offers(job_id, status, limit)` - List offers
- `get_offer(offer_id)` - Get offer details
- `create_offer(data)` - Create offer
- `update_offer(offer_id, data)` - Update offer

### Pipeline Management
- `get_pipeline(job_id)` - Get recruitment pipeline
- `move_application(application_id, stage_id)` - Move application in pipeline

### Notes & Files
- `get_activities(record_id, limit)` - Get activity history
- `create_note(record_id, note_text, module)` - Create note
- `upload_file(record_id, file_url, module)` - Upload file

### Client Management (Agencies)
- `get_clients()` - List clients
- `get_contacts(client_id)` - Get client contacts

## Application Status

Common application statuses:
- `Applied` - Candidate submitted application
- `Screening` - Initial screening phase
- `Shortlisted` - Candidate moved to interview stage
- `Interview` - Interview in progress
- `Offer Sent` - Offer sent to candidate
- `Rejected` - Candidate rejected
- `Hired` - Candidate accepted offer

## Interview Types

- `In Person` - Face-to-face interview
- `Phone` - Phone screening
- `Video` - Video conference interview
- `Assessment` - Technical assessment

## Error Handling

```python
try:
    candidate = client.get_candidate("CAND123")
except requests.RequestException as e:
    print(f"Error fetching candidate: {e}")
```

## Webhooks

Zoho Recruit supports webhooks for real-time notifications:
- Job creation/update
- New candidate
- Application status change
- Interview scheduled
- Offer status change

Configure webhooks in your Zoho Recruit settings.

## Support

For API documentation, visit https://www.zoho.com/recruit/developer-guide/