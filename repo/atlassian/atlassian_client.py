"""
Atlassian API Client

Atlassian provides multiple collaboration and project management tools:
- Jira (issue tracking)
- Confluence (documentation)
- Bitbucket (code hosting)
- Trello (project boards)
- Jira Service Management

This client provides common operations across Atlassian products.

API Actions (estimated 15-20):
1. Get Jira Issue
2. Create Jira Issue
3. Update Jira Issue
4. List Jira Issues
5. Add Jira Comment
6. Get Confluence Page
7. Create Confluence Page
8. Update Confluence Page
9. List Confluence Spaces
10. Get Bitbucket Repository
11. Create Bitbucket Pull Request
12. Get User Info
13. List Projects
14. Search Content
15. Get Workflow Status

Triggers (estimated 6-8):
- Issue Created/Updated
- Page Created/Updated
- Pull Request Created/Merged
- Comment Added
- Project Created

Authentication: OAuth 2.0 (Authorization Code) or Basic Auth
Base URL: https://api.atlassian.com/ex
Documentation: https://developer.atlassian.com/
Rate Limiting: Dependent on product (typically 1000 requests/hour)
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field


@dataclass
class JiraIssue:
    """Jira Issue model"""
    issue_id: str
    key: str
    summary: str
    description: str = ""
    status: str = ""
    priority: str = ""
    assignee_id: Optional[str] = None
    reporter_id: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    project_key: str = ""


@dataclass
class Comment:
    """Comment model (Jira/Confluence)"""
    comment_id: str
    body: str
    author_id: str
    created_at: str
    updated_at: Optional[str] = None


@dataclass
class ConfluencePage:
    """Confluence Page model"""
    page_id: str
    title: str
    space_key: str
    version: int
    body: str = ""
    author_id: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Space:
    """Confluence Space model"""
    space_key: str
    name: str
    description: Optional[str] = None
    type: str = "global"


@dataclass
class BitbucketRepository:
    """Bitbucket Repository model"""
    slug: str
    name: str
    description: str = ""
    is_private: bool = False
    created_on: Optional[str] = None
    updated_on: Optional[str] = None


@dataclass
class BitbucketPullRequest:
    """Bitbucket Pull Request model"""
    pr_id: int
    title: str
    description: str = ""
    state: str = ""
    source_branch: str = ""
    destination_branch: str = ""
    author_id: Optional[str] = None


@dataclass
class AtlassianUser:
    """Atlassian User model"""
    user_id: str
    display_name: str
    email: str
    account_type: str = "atlassian"
    active: bool = True


class AtlassianClient:
    """
    Atlassian API client for cross-product operations.

    Supports: Jira, Confluence, Bitbucket, and other Atlassian products
    Authentication: OAuth 2.0 (Authorization Code)
    Rate limit: Depends on specific product
    """

    BASE_URL = "https://api.atlassian.com"

    def __init__(self, access_token: str, cloud_id: Optional[str] = None):
        """
        Initialize Atlassian client.

        Args:
            access_token: OAuth 2.0 access token
            cloud_id: Optional Atlassian Cloud ID (can be auto-discovered)
        """
        self.access_token = access_token
        self.cloud_id = cloud_id
        self.session = None
        self._headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        if not self.cloud_id:
            await self._discover_cloud_id()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _discover_cloud_id(self):
        """Discover the user's Atlassian Cloud ID"""
        url = f"{self.BASE_URL}/oauth/token/accessible-resources"
        async with self.session.get(url, headers=self._headers) as response:
            if response.status == 200:
                resources = await response.json()
                if resources:
                    self.cloud_id = resources[0].get("id")

    async def _make_request(
        self,
        method: str,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make API request"""
        async with self.session.request(
            method,
            url,
            headers=self._headers,
            json=data,
            params=params
        ) as response:
            result = await response.json()

            if response.status not in [200, 201, 204]:
                error = result.get("error", str(result))
                raise Exception(
                    f"Atlassian API error: {response.status} - {error}"
                )

            return result

    # ==================== Jira Operations ====================

    async def get_jira_issue(
        self,
        issue_key: str
    ) -> JiraIssue:
        """Get Jira issue by key"""
        url = f"https://api.atlassian.com/ex/jira/{self.cloud_id}/rest/api/3/issue/{issue_key}"
        response = await self._make_request("GET", url)
        fields = response.get("fields", {})

        return JiraIssue(
            issue_id=response.get("id", ""),
            key=response.get("key", issue_key),
            summary=fields.get("summary", ""),
            description=fields.get("description", ""),
            status=fields.get("status", {}).get("name", ""),
            priority=fields.get("priority", {}).get("name", ""),
            assignee_id=fields.get("assignee", {}).get("accountId"),
            reporter_id=fields.get("reporter", {}).get("accountId"),
            created_at=fields.get("created"),
            updated_at=fields.get("updated"),
            project_key=fields.get("project", {}).get("key", "")
        )

    async def create_jira_issue(
        self,
        project_key: str,
        summary: str,
        issue_type: str = "Task",
        description: str = "",
        **fields
    ) -> JiraIssue:
        """Create a Jira issue"""
        url = f"https://api.atlassian.com/ex/jira/{self.cloud_id}/rest/api/3/issue"

        data = {
            "fields": {
                "project": {"key": project_key},
                "summary": summary,
                "issuetype": {"name": issue_type},
                "description": description,
                **fields
            }
        }

        response = await self._make_request("POST", url, data=data)
        return await self.get_jira_issue(response.get("key"))

    async def update_jira_issue(
        self,
        issue_key: str,
        **fields
    ) -> JiraIssue:
        """Update a Jira issue"""
        url = f"https://api.atlassian.com/ex/jira/{self.cloud_id}/rest/api/3/issue/{issue_key}"

        data = {"fields": fields}
        await self._make_request("PUT", url, data=data)

        return await self.get_jira_issue(issue_key)

    async def list_jira_issues(
        self,
        project_key: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50
    ) -> List[JiraIssue]:
        """List Jira issues with filters"""
        url = f"https://api.atlassian.com/ex/jira/{self.cloud_id}/rest/api/3/search"

        jql = ""
        if project_key:
            jql = f'project = "{project_key}"'
        if status:
            jql += f' AND status = "{status}"' if jql else f'status = "{status}"'

        params = {
            "jql": jql,
            "maxResults": limit
        }

        response = await self._make_request("GET", url, params=params)
        issues_data = response.get("issues", [])

        return [
            JiraIssue(
                issue_id=issue.get("id", ""),
                key=issue.get("key", ""),
                summary=issue.get("fields", {}).get("summary", ""),
                description=issue.get("fields", {}).get("description", ""),
                status=issue.get("fields", {}).get("status", {}).get("name", ""),
                priority=issue.get("fields", {}).get("priority", {}).get("name", ""),
                assignee_id=issue.get("fields", {}).get("assignee", {}).get("accountId"),
                created_at=issue.get("fields", {}).get("created"),
                project_key=issue.get("fields", {}).get("project", {}).get("key", "")
            )
            for issue in issues_data
        ]

    async def add_jira_comment(
        self,
        issue_key: str,
        body: str
    ) -> Comment:
        """Add comment to Jira issue"""
        url = f"https://api.atlassian.com/ex/jira/{self.cloud_id}/rest/api/3/issue/{issue_key}/comment"

        data = {"body": body}
        response = await self._make_request("POST", url, data=data)

        return Comment(
            comment_id=response.get("id"),
            body=response.get("body", ""),
            author_id=response.get("author", {}).get("accountId", ""),
            created_at=response.get("created", ""),
            updated_at=response.get("updated")
        )

    # ==================== Confluence Operations ====================

    async def get_confluence_page(
        self,
        page_id: str
    ) -> ConfluencePage:
        """Get Confluence page by ID"""
        url = f"https://api.atlassian.com/ex/confluence/{self.cloud_id}/rest/api/content/{page_id}"
        response = await self._make_request("GET", url)

        return ConfluencePage(
            page_id=response.get("id", ""),
            title=response.get("title", ""),
            space_key=response.get("space", {}).get("key", ""),
            version=response.get("version", {}).get("number", 0),
            body=self._extract_content(response),
            author_id=response.get("history", {}).get("createdBy", {}).get("accountId"),
            created_at=response.get("history", {}).get("createdDate"),
            updated_at=response.get("history", {}).get("lastUpdated", {}).get("when")
        )

    def _extract_content(self, response: Dict[str, Any]) -> str:
        """Extract content from Confluence API response"""
        storage = response.get("body", {}).get("storage", {})
        if isinstance(storage, dict):
            return storage.get("value", "")
        return str(storage)

    async def create_confluence_page(
        self,
        space_key: str,
        title: str,
        body: str,
        parent_id: Optional[str] = None
    ) -> ConfluencePage:
        """Create Confluence page"""
        url = f"https://api.atlassian.com/ex/confluence/{self.cloud_id}/rest/api/content"

        data = {
            "type": "page",
            "title": title,
            "space": {"key": space_key},
            "body": {
                "storage": {
                    "value": body,
                    "representation": "storage"
                }
            }
        }

        if parent_id:
            data["ancestors"] = [{"id": parent_id}]

        response = await self._make_request("POST", url, data=data)
        return await self.get_confluence_page(response.get("id"))

    async def update_confluence_page(
        self,
        page_id: str,
        body: str,
        title: Optional[str] = None,
        version: Optional[int] = None
    ) -> ConfluencePage:
        """Update Confluence page"""
        url = f"https://api.atlassian.com/ex/confluence/{self.cloud_id}/rest/api/content/{page_id}"

        page = await self.get_confluence_page(page_id)

        data = {
            "id": page_id,
            "type": "page",
            "title": title or page.title,
            "version": {"number": version or page.version + 1},
            "space": {"key": page.space_key},
            "body": {
                "storage": {
                    "value": body,
                    "representation": "storage"
                }
            }
        }

        response = await self._make_request("PUT", url, data=data)
        return await self.get_confluence_page(page_id)

    async def list_confluence_spaces(
        self,
        limit: int = 50
    ) -> List[Space]:
        """List Confluence spaces"""
        url = f"https://api.atlassian.com/ex/confluence/{self.cloud_id}/rest/api/space"

        params = {"limit": limit}
        response = await self._make_request("GET", url, params=params)
        spaces_data = response.get("results", [])

        return [
            Space(
                space_key=space.get("key", ""),
                name=space.get("name", ""),
                description=space.get("description", {}).get("plain", {}).get("value", ""),
                type=space.get("type", "global")
            )
            for space in spaces_data
        ]

    # ==================== Bitbucket Operations ====================

    async def get_bitbucket_repository(
        self,
        workspace: str,
        repository_slug: str
    ) -> BitbucketRepository:
        """Get Bitbucket repository"""
        url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repository_slug}"
        response = await self._make_request("GET", url)

        return BitbucketRepository(
            slug=response.get("slug", ""),
            name=response.get("name", ""),
            description=response.get("description", ""),
            is_private=response.get("is_private", False),
            created_on=response.get("created_on"),
            updated_on=response.get("updated_on")
        )

    async def create_bitbucket_pull_request(
        self,
        workspace: str,
        repository_slug: str,
        title: str,
        source_branch: str,
        destination_branch: str,
        description: str = ""
    ) -> BitbucketPullRequest:
        """Create Bitbucket pull request"""
        url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repository_slug}/pullrequests"

        data = {
            "title": title,
            "source": {"branch": {"name": source_branch}},
            "destination": {"branch": {"name": destination_branch}},
            "description": description
        }

        response = await self._make_request("POST", url, data=data)

        return BitbucketPullRequest(
            pr_id=response.get("id"),
            title=response.get("title"),
            description=response.get("description", ""),
            state=response.get("state"),
            source_branch=response.get("source", {}).get("branch", {}).get("name", ""),
            destination_branch=response.get("destination", {}).get("branch", {}).get("name", ""),
            author_id=response.get("author", {}).get("uuid")
        )

    # ==================== User Operations ====================

    async def get_user_info(self, account_id: str) -> AtlassianUser:
        """Get user information"""
        url = f"https://api.atlassian.com/ex/jira/{self.cloud_id}/rest/api/3/user"

        params = {"accountId": account_id}
        response = await self._make_request("GET", url, params=params)

        return AtlassianUser(
            user_id=response.get("accountId", ""),
            display_name=response.get("displayName", ""),
            email=response.get("emailAddress", ""),
            account_type=response.get("accountType", "atlassian"),
            active=response.get("active", True)
        )

    # ==================== Project Operations ====================

    async def list_projects(
        self,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """List Jira projects"""
        url = f"https://api.atlassian.com/ex/jira/{self.cloud_id}/rest/api/3/project"

        params = {"maxResults": limit}
        response = await self._make_request("GET", url, params=params)

        return response

    # ==================== Webhook Handling ====================

    def handle_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle webhook events from Atlassian products"""
        webhook_id = webhook_data.get("webhookId")
        event_type = webhook_data.get("webhookEvent", "unknown")
        issue_id = webhook_data.get("issue", {}).get("id")
        page_id = webhook_data.get("page", {}).get("id")

        return {
            "event_type": event_type,
            "webhook_id": webhook_id,
            "issue_id": issue_id,
            "page_id": page_id,
            "raw_data": webhook_data
        }


async def main():
    """Example usage"""
    access_token = "your_atlassian_access_token"

    async with AtlassianClient(access_token) as client:
        # List projects
        projects = await client.list_projects(limit=10)
        print(f"Found {len(projects)} projects")

        # List Confluence spaces
        spaces = await client.list_confluence_spaces(limit=10)
        print(f"Found {len(spaces)} spaces")

if __name__ == "__main__":
    asyncio.run(main())