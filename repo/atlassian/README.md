# Atlassian API Client

Python async client for Atlassian products (Jira, Confluence, Bitbucket).

## Features

- Jira: Issue management, comments, projects
- Confluence: Page management, spaces
- Bitbucket: Repository management, pull requests
- User management
- Cross-product webhooks
- OAuth 2.0 authentication

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
import asyncio
from atlassian_client import AtlassianClient

async def main():
    access_token = "your_oauth_token"

    async with AtlassianClient(access_token) as client:
        # Jira Operations
        issues = await client.list_jira_issues(project_key="PROJ", limit=10)

        # Create Jira issue
        issue = await client.create_jira_issue(
            project_key="PROJ",
            summary="New task",
            issue_type="Task"
        )

        # Confluence Operations
        spaces = await client.list_confluence_spaces(limit=10)

        # Bitbucket Operations
        pr = await client.create_bitbucket_pull_request(
            workspace="myworkspace",
            repository_slug="myrepo",
            title="Fix bug",
            source_branch="fix-bug",
            destination_branch="main"
        )

asyncio.run(main())
```

## API Actions

### Jira (15 actions)
- Issue management (create, get, update, list)
- Comments
- Projects
- Search

### Confluence (4 actions)
- Page management (create, get, update)
- Spaces (list)

### Bitbucket (2 actions)
- Repository (get)
- Pull requests (create)

### Other
- User operations
- Workflow status

## Triggers

- Issue Created/Updated
- Page Created/Updated
- Pull Request Created/Merged
- Comment Added
- Project Created

## Documentation

- [Atlassian Developer Portal](https://developer.atlassian.com/)
- [Jira REST API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/)
- [Confluence REST API](https://developer.atlassian.com/cloud/confluence/rest/v2/)
- [Bitbucket API](https://developer.atlassian.com/cloud/bitbucket/rest/intro/)
- [Atlassian API Gateway](https api.atlassian.com/ex)