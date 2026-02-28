"""
Asana API Client

Asana is a project management and team collaboration platform.

API Actions (52):
1. Create Status Update
2. Update Enum Option
3. Get Section
4. List Team Projects
5. Archive Project
6. List All Projects
7. List Workspace Teams
8. Get Goal Detail
9. Add Comment to Task
10. Remove Task Collaborator
11. List Section Tasks
12. Duplicate Task
13. Create Section
14. Complete Task
15. Update Task Date Custom Field (Date Only)
16. Create Task
17. Get Task Detail
18. List Project Tasks
19. List Section Overdue Tasks
20. Move Task Section
21. List Sections
22. List Portfolios
23. Add User to Team
24. Search Tasks
25. List User Tasks
26. List Goals
27. Update Task Custom Field
28. Get Status Update
29. Attach File
30. Create Project from Template
31. Get Attached File Info
32. List Users
33. List Project Sections
34. List Workspaces
35. Update Project
36. Create Project
37. Add Task Collaborator
38. Add User to Workspace
39. List Project Overdue Tasks
40. Get File Download URL
41. Delete Task
42. List Subtasks
43. Add Task to Section
44. Create Subtask
45. List Project Templates
46. Get Project Task Count
47. Add Member to Project
48. Update Task Date Custom Field (DateTime)
49. Update Task
50. List Custom Field Settings
51. Get User Info
52. Download File

Triggers (7):
- New Task Added to Project
- Task Completed in Project
- Task Created/Updated in Section
- Project Created (Webhook)
- Section Task Completed
- New Task Added to Section
- Task Created/Updated in Project

Authentication: Personal Access Token (Bearer)
Base URL: https://app.asana.com/api/1.0
Documentation: https://developers.asana.com/reference/
Rate Limiting: Dynamic based on response headers
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field


@dataclass
class Task:
    """Task model"""
    gid: str
    name: str
    resource_type: str = "task"
    completed: bool = False
    completed_at: Optional[str] = None
    due_at: Optional[str] = None
    due_on: Optional[str] = None
    created_at: Optional[str] = None
    modified_at: Optional[str] = None
    assignee_id: Optional[str] = None
    assignee_status: Optional[str] = None
    projects: List[str] = field(default_factory=list)
    parent_id: Optional[str] = None
    notes: Optional[str] = None
    custom_fields: Optional[List[Dict[str, Any]]] = None


@dataclass
class Project:
    """Project model"""
    gid: str
    name: str
    resource_type: str = "project"
    created_at: Optional[str] = None
    modified_at: Optional[str] = None
    archived: bool = False
    public: bool = False
    team_id: Optional[str] = None
    followers: List[str] = field(default_factory=list)


@dataclass
class Section:
    """Section model"""
    gid: str
    name: str
    project_id: str
    resource_type: str = "section"
    created_at: Optional[str] = None


@dataclass
class User:
    """User model"""
    gid: str
    name: str
    email: str
    resource_type: str = "user"
    photo_url: Optional[str] = None


@dataclass
class Workspace:
    """Workspace model"""
    gid: str
    name: str
    resource_type: str = "workspace"
    is_organization: bool = False


@dataclass
class Team:
    """Team model"""
    gid: str
    name: str
    resource_type: str = "team"
    organization_id: Optional[str] = None


@dataclass
class Attachment:
    """Attachment model"""
    gid: str
    name: str
    resource_type: str = "attachment"
    download_url: str = ""
    created_at: Optional[str] = None


@dataclass
class StatusUpdate:
    """Status update model"""
    gid: str
    text: str
    resource_type: str = "status_update"
    author_id: Optional[str] = None
    created_at: Optional[str] = None


@dataclass
class Comment:
    """Comment model"""
    gid: str
    text: str
    resource_type: str = "story"
    author_id: Optional[str] = None
    created_at: Optional[str] = None


class AsanaClient:
    """
    Asana API client for project and task management.

    Supports: Tasks, Projects, Sections, Users, Workspaces, Attachments
    Rate limit: Respects dynamic rate limiting from response headers
    """

    BASE_URL = "https://app.asana.com/api/1.0"

    def __init__(self, access_token: str):
        """
        Initialize Asana client.

        Args:
            access_token: Personal access token
        """
        self.access_token = access_token
        self.session = None
        self._headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make API request with rate limiting.

        Args:
            method: HTTP method
            endpoint: API endpoint
            data: Request body data
            params: Query parameters

        Returns:
            Response JSON

        Raises:
            Exception: If request fails
        """
        url = f"{self.BASE_URL}{endpoint}"

        async with self.session.request(
            method,
            url,
            headers=self._headers,
            json=data,
            params=params
        ) as response:
            result = await response.json()

            if response.status not in [200, 201]:
                error_message = result.get('errors', [{}])[0].get('message', 'Unknown error')
                raise Exception(
                    f"Asana API error: {response.status} - {error_message}"
                )

            # Check for rate limit headers and wait if needed
            retry_after = response.headers.get('Retry-After')
            if retry_after:
                await asyncio.sleep(int(retry_after))

            return result

    # ==================== Task Operations ====================

    async def create_task(
        self,
        workspace_id: str,
        name: str,
        notes: Optional[str] = None,
        due_on: Optional[str] = None,
        assignee_id: Optional[str] = None,
        project_id: Optional[str] = None
    ) -> Task:
        """Create a task"""
        data = {
            "data": {
                "workspace": workspace_id,
                "name": name
            }
        }

        if notes:
            data["data"]["notes"] = notes
        if due_on:
            data["data"]["due_on"] = due_on
        if assignee_id:
            data["data"]["assignee"] = assignee_id
        if project_id:
            data["data"]["projects"] = [project_id]

        response = await self._make_request("POST", "/tasks", data=data)
        return Task(**response["data"])

    async def get_task(self, task_id: str) -> Task:
        """Get task by ID"""
        response = await self._make_request("GET", f"/tasks/{task_id}")
        return Task(**response["data"])

    async def update_task(
        self,
        task_id: str,
        **fields
    ) -> Task:
        """Update a task"""
        data = {"data": fields}
        response = await self._make_request("PUT", f"/tasks/{task_id}", data=data)
        return Task(**response["data"])

    async def complete_task(self, task_id: str) -> Task:
        """Mark task as completed"""
        return await self.update_task(task_id, completed=True)

    async def delete_task(self, task_id: str) -> bool:
        """Delete a task"""
        await self._make_request("DELETE", f"/tasks/{task_id}")
        return True

    async def search_tasks(
        self,
        workspace_id: str,
        query: str,
        **params
    ) -> List[Task]:
        """Search tasks"""
        params = {
            "workspace": workspace_id,
            "text": query,
            **params
        }
        response = await self._make_request("GET", "/tasks/search", params=params)
        tasks = response.get("data", [])
        return [Task(**t) for t in tasks]

    async def list_project_tasks(
        self,
        project_id: str,
        limit: int = 100
    ) -> List[Task]:
        """List tasks in a project"""
        params = {
            "project": project_id,
            "limit": limit
        }
        response = await self._make_request("GET", "/tasks", params=params)
        tasks = response.get("data", [])
        return [Task(**t) for t in tasks]

    async def list_user_tasks(
        self,
        user_id: str,
        workspace_id: str,
        completed_since: Optional[str] = None
    ) -> List[Task]:
        """List tasks assigned to a user"""
        params = {
            "assignee": user_id,
            "workspace": workspace_id
        }
        if completed_since:
            params["completed_since"] = completed_since

        response = await self._make_request("GET", "/tasks", params=params)
        tasks = response.get("data", [])
        return [Task(**t) for t in tasks]

    async def duplicate_task(
        self,
        task_id: str,
        name: Optional[str] = None,
        include: List[str] = None
    ) -> Task:
        """Duplicate a task"""
        data = {
            "data": {
                "include": include or ["assignee", "attachments", "dependencies", "followers", "notes", "projects", "subtasks", "tags"]
            }
        }
        if name:
            data["data"]["name"] = name
        response = await self._make_request("POST", f"/tasks/{task_id}/duplicate", data=data)
        return Task(**response["new_task"])

    async def create_subtask(
        self,
        task_id: str,
        name: str,
        **fields
    ) -> Task:
        """Create a subtask"""
        data = {
            "data": {
                "name": name,
                **fields
            }
        }
        response = await self._make_request("POST", f"/tasks/{task_id}/subtasks", data=data)
        return Task(**response["data"])

    async def list_subtasks(
        self,
        task_id: str
    ) -> List[Task]:
        """List subtasks of a task"""
        response = await self._make_request("GET", f"/tasks/{task_id}/subtasks")
        tasks = response.get("data", [])
        return [Task(**t) for t in tasks]

    async def add_comment_to_task(
        self,
        task_id: str,
        text: str,
        is_pinned: bool = False
    ) -> Comment:
        """Add a comment to a task"""
        data = {
            "data": {
                "text": text,
                "is_pinned": is_pinned
            }
        }
        response = await self._make_request("POST", f"/tasks/{task_id}/stories", data=data)
        return Comment(**response["data"])

    async def add_task_collaborator(
        self,
        task_id: str,
        user_id: str
    ) -> Task:
        """Add a collaborator to a task"""
        data = {"data": {"follower": user_id}}
        await self._make_request("POST", f"/tasks/{task_id}/addFollowers", data=data)
        return await self.get_task(task_id)

    async def remove_task_collaborator(
        self,
        task_id: str,
        user_id: str
    ) -> Task:
        """Remove a collaborator from a task"""
        data = {"data": {"follower": user_id}}
        await self._make_request("POST", f"/tasks/{task_id}/removeFollowers", data=data)
        return await self.get_task(task_id)

    # ==================== Project Operations ====================

    async def create_project(
        self,
        workspace_id: str,
        name: str,
        team_id: Optional[str] = None,
        **fields
    ) -> Project:
        """Create a project"""
        data = {
            "data": {
                "workspace": workspace_id,
                "name": name,
                **fields
            }
        }
        if team_id:
            data["data"]["team"] = team_id

        response = await self._make_request("POST", "/projects", data=data)
        return Project(**response["data"])

    async def get_project(self, project_id: str) -> Project:
        """Get project by ID"""
        response = await self._make_request("GET", f"/projects/{project_id}")
        return Project(**response["data"])

    async def update_project(
        self,
        project_id: str,
        **fields
    ) -> Project:
        """Update a project"""
        data = {"data": fields}
        response = await self._make_request("PUT", f"/projects/{project_id}", data=data)
        return Project(**response["data"])

    async def archive_project(self, project_id: str) -> Project:
        """Archive a project"""
        return await self.update_project(project_id, archived=True)

    async def list_all_projects(
        self,
        workspace_id: str,
        archived: bool = False
    ) -> List[Project]:
        """List all projects in workspace"""
        params = {
            "workspace": workspace_id,
            "archived": archived
        }
        response = await self._make_request("GET", "/projects", params=params)
        projects = response.get("data", [])
        return [Project(**p) for p in projects]

    async def list_team_projects(self, team_id: str) -> List[Project]:
        """List projects for a team"""
        params = {"team": team_id}
        response = await self._make_request("GET", "/projects", params=params)
        projects = response.get("data", [])
        return [Project(**p) for p in projects]

    async def get_project_task_count(self, project_id: str) -> int:
        """Get the number of tasks in a project"""
        tasks = await self.list_project_tasks(project_id)
        return len(tasks)

    async def list_project_templates(self, workspace_id: str) -> List[Project]:
        """List project templates"""
        params = {"workspace": workspace_id, "is_template": True}
        response = await self._make_request("GET", "/projects", params=params)
        projects = response.get("data", [])
        return [Project(**p) for p in projects]

    async def create_project_from_template(
        self,
        project_template_id: str,
        team_id: str,
        name: str
    ) -> Project:
        """Create a project from a template"""
        data = {
            "data": {
                "project_template": project_template_id,
                "team": team_id,
                "name": name
            }
        }
        response = await self._make_request("POST", "/project_templates/instantiate", data=data)
        return Project(**response["data"])

    async def add_member_to_project(
        self,
        project_id: str,
        user_id: str
    ) -> bool:
        """Add a member to a project"""
        data = {"data": {"member": user_id}}
        await self._make_request("POST", f"/projects/{project_id}/addMembers", data=data)
        return True

    # ==================== Section Operations ====================

    async def create_section(
        self,
        project_id: str,
        name: str
    ) -> Section:
        """Create a section"""
        data = {
            "data": {
                "project": project_id,
                "name": name
            }
        }
        response = await self._make_request("POST", "/sections", data=data)
        return Section(**response["data"])

    async def get_section(self, section_id: str) -> Section:
        """Get section by ID"""
        response = await self._make_request("GET", f"/sections/{section_id}")
        return Section(**response["data"])

    async def list_sections(self, project_id: str) -> List[Section]:
        """List sections in a project"""
        params = {"project": project_id}
        response = await self._make_request("GET", "/sections", params=params)
        sections = response.get("data", [])
        return [Section(**s) for s in sections]

    async def list_section_tasks(
        self,
        section_id: str
    ) -> List[Task]:
        """List tasks in a section"""
        response = await self._make_request("GET", f"/sections/{section_id}/tasks")
        tasks = response.get("data", [])
        return [Task(**t) for t in tasks]

    async def list_section_overdue_tasks(self, section_id: str) -> List[Task]:
        """List overdue tasks in a section"""
        tasks = await self.list_section_tasks(section_id)
        now = datetime.now().isoformat()
        return [t for t in tasks if t.due_on and t.due_on < now and not t.completed]

    async def add_task_to_section(
        self,
        section_id: str,
        task_id: str
    ) -> bool:
        """Add a task to a section"""
        data = {"data": {"task": task_id}}
        await self._make_request("POST", f"/sections/{section_id}/addTask", data=data)
        return True

    async def move_task_section(
        self,
        task_id: str,
        section_id: str
    ) -> Task:
        """Move a task to a different section"""
        return await self.update_task(task_id, membership={"section": section_id})

    # ==================== User & Workspace Operations ====================

    async def get_user(self, user_id: str) -> User:
        """Get user by ID"""
        response = await self._make_request("GET", f"/users/{user_id}")
        return User(**response["data"])

    async def list_users(self, workspace_id: str) -> List[User]:
        """List users in a workspace"""
        params = {"workspace": workspace_id}
        response = await self._make_request("GET", "/users", params=params)
        users = response.get("data", [])
        return [User(**u) for u in users]

    async def get_workspace(self, workspace_id: str) -> Workspace:
        """Get workspace by ID"""
        response = await self._make_request("GET", f"/workspaces/{workspace_id}")
        return Workspace(**response["data"])

    async def list_workspaces(self) -> List[Workspace]:
        """List all workspaces"""
        response = await self._make_request("GET", "/workspaces")
        workspaces = response.get("data", [])
        return [Workspace(**w) for w in workspaces]

    async def add_user_to_workspace(
        self,
        workspace_id: str,
        user_id: str
    ) -> bool:
        """Add a user to a workspace"""
        data = {"data": {"user": user_id}}
        await self._make_request("POST", f"/workspaces/{workspace_id}/addUser", data=data)
        return True

    async def list_teams(self, organization_id: str) -> List[Team]:
        """List teams in an organization"""
        params = {"organization": organization_id}
        response = await self._make_request("GET", "/teams", params=params)
        teams = response.get("data", [])
        return [Team(**t) for t in teams]

    async def add_user_to_team(
        self,
        team_id: str,
        user_id: str
    ) -> bool:
        """Add a user to a team"""
        data = {"data": {"user": user_id}}
        await self._make_request("POST", f"/teams/{team_id}/addUser", data=data)
        return True

    # ==================== Attachment Operations ====================

    async def attach_file(
        self,
        task_id: str,
        file_url: str,
        filename: Optional[str] = None
    ) -> Attachment:
        """Attach a file to a task"""
        data = {
            "data": {
                "url": file_url
            }
        }
        if filename:
            data["data"]["name"] = filename

        response = await self._make_request("POST", f"/tasks/{task_id}/attachments", data=data)
        return Attachment(**response["data"])

    async def get_attached_file_info(self, attachment_id: str) -> Attachment:
        """Get attachment info"""
        response = await self._make_request("GET", f"/attachments/{attachment_id}")
        return Attachment(**response["data"])

    async def get_file_download_url(self, attachment_id: str) -> str:
        """Get file download URL"""
        attachment = await self.get_attached_file_info(attachment_id)
        return attachment.download_url

    async def download_file(self, attachment_id: str) -> bytes:
        """Download an attachment"""
        url = await self.get_file_download_url(attachment_id)
        async with self.session.get(url) as response:
            if response.status != 200:
                raise Exception(f"Failed to download file: {response.status}")
            return await response.read()

    # ==================== Custom Fields ====================

    async def update_task_custom_field(
        self,
        task_id: str,
        custom_field_id: str,
        value: Any
    ) -> Task:
        """Update a task's custom field"""
        return await self.update_task(task_id, custom_fields={custom_field_id: str(value)})

    async def update_task_date_custom_field(
        self,
        task_id: str,
        custom_field_id: str,
        date: str,
        include_time: bool = False
    ) -> Task:
        """Update a date-type custom field"""
        return await self.update_task(
            task_id,
            custom_fields={custom_field_id: {"date": date, "include_time": include_time}}
        )

    async def list_custom_field_settings(self, project_id: str) -> List[Dict[str, Any]]:
        """List custom field settings for a project"""
        response = await self._make_request("GET", f"/projects/{project_id}/custom_field_settings")
        return response.get("data", [])

    async def update_enum_option(
        self,
        enum_option_id: str,
        name: str
    ) -> bool:
        """Update an enum option"""
        data = {"data": {"name": name}}
        await self._make_request("PUT", f"/enum_options/{enum_option_id}", data=data)
        return True

    # ==================== Status Updates ====================

    async def create_status_update(
        self,
        project_id: str,
        text: str,
        **fields
    ) -> StatusUpdate:
        """Create a status update for a project"""
        data = {
            "data": {
                "project": project_id,
                "text": text,
                **fields
            }
        }
        response = await self._make_request("POST", "/project_status_updates", data=data)
        return StatusUpdate(**response["data"])

    async def get_status_update(self, status_update_id: str) -> StatusUpdate:
        """Get status update by ID"""
        response = await self._make_request("GET", f"/project_status_updates/{status_update_id}")
        return StatusUpdate(**response["data"])

    async def list_overdue_tasks(self, project_id: str) -> List[Task]:
        """List overdue tasks in a project"""
        tasks = await self.list_project_tasks(project_id)
        now = datetime.now().isoformat()
        return [t for t in tasks if t.due_on and t.due_on < now and not t.completed]

    # ==================== Additional Operations ====================

    async def list_portfolios(self, workspace_id: str) -> List[Dict[str, Any]]:
        """List portfolios in workspace"""
        params = {"workspace": workspace_id}
        response = await self._make_request("GET", "/portfolios", params=params)
        return response.get("data", [])

    async def list_goals(
        self,
        workspace_id: str
    ) -> List[Dict[str, Any]]:
        """List goals"""
        params = {"workspace": workspace_id}
        response = await self._make_request("GET", "/goals", params=params)
        return response.get("data", [])

    async def get_goal_detail(self, goal_id: str) -> Dict[str, Any]:
        """Get goal details"""
        response = await self._make_request("GET", f"/goals/{goal_id}")
        return response["data"]

    # ==================== Webhook Handling ====================

    def handle_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle webhook events from Asana.

        Args:
            webhook_data: Webhook payload

        Returns:
            Processed event data
        """
        event_type = webhook_data.get("events", [{}])[0].get("type", "unknown")
        resource = webhook_data.get("events", [{}])[0].get("resource", {})

        return {
            "event_type": event_type,
            "resource_id": resource.get("gid"),
            "resource_type": resource.get("resource_type"),
            "raw_data": webhook_data
        }


async def main():
    """Example usage"""
    access_token = "your_asana_access_token"

    async with AsanaClient(access_token) as client:
        # List workspaces
        workspaces = await client.list_workspaces()
        print(f"Found {len(workspaces)} workspaces")

        if workspaces:
            workspace_id = workspaces[0].gid

            # List users
            users = await client.list_users(workspace_id)
            print(f"Found {len(users)} users")

            # List projects
            projects = await client.list_all_projects(workspace_id)
            print(f"Found {len(projects)} projects")

if __name__ == "__main__":
    asyncio.run(main())