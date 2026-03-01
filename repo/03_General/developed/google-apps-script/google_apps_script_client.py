"""
Google Apps Script API - Script Execution and Management Client

Supports:
- Create Project
- Create Project Version
- Create Project Deployment
- Update Project Content
- Execute Script (API-deployed)
- Execute Script (UI-deployed)
"""

import aiohttp
import json
from typing import Optional, Dict, Any, List
from datetime import datetime
from dataclasses import dataclass


@dataclass
class ScriptProject:
    """Google Apps Script project object"""
    script_id: str
    title: str
    parent_id: Optional[str] = None
    create_time: Optional[str] = None
    update_time: Optional[str] = None


@dataclass
class Version:
    """Script version object"""
    version_number: int
    description: str
    created_time: str


@dataclass
class Deployment:
    """Script deployment object"""
    deployment_id: str
    deployment_config: Dict[str, Any]
    entry_points: List[str]
    version_number: Optional[int] = None
    update_time: Optional[str] = None


@dataclass
class ExecutionResult:
    """Script execution result object"""
    response: Any
    done: bool
    error: Optional[Dict[str, Any]] = None


@dataclass
class ScriptFile:
    """Script file object"""
    name: str
    type: str
    source: str


class GoogleAppsScriptClient:
    """
    Google Apps Script API client for script execution and management.

    Provides operations to create, update, version, and execute
    Google Apps Script projects programmatically.

    API Documentation: https://lp.yoom.fun/apps/google-apps-script
    Requires:
    - Google Cloud project with Apps Script API enabled
    - OAuth credentials or service account
    """

    BASE_URL = "https://script.googleapis.com/v1"

    def __init__(self, access_token: str):
        """
        Initialize Google Apps Script client.

        Args:
            access_token: OAuth access token
        """
        self.access_token = access_token
        self.session = None
        self._rate_limit_delay = 0.1

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={"Authorization": f"Bearer {self.access_token}"}
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make an API request with error handling.

        Args:
            method: HTTP method
            endpoint: API endpoint
            params: Query parameters
            json_data: JSON body data

        Returns:
            Response data as dictionary

        Raises:
            Exception: If request fails or returns error
        """
        url = f"{self.BASE_URL}{endpoint}"

        try:
            async with self.session.request(
                method,
                url,
                params=params,
                json=json_data
            ) as response:
                response_data = await response.json()

                if response.status >= 400:
                    error = response_data.get("error", {})
                    error_message = error.get("message", f"HTTP {response.status} error")
                    raise Exception(f"Google Apps Script API error: {error_message}")

                return response_data

        except aiohttp.ClientError as e:
            raise Exception(f"Network error: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON response: {str(e)}")

    # ==================== Create Project ====================

    async def create_project(
        self,
        title: str,
        parent_id: Optional[str] = None
    ) -> ScriptProject:
        """
        Create a new Apps Script project.

        Args:
            title: Project title
            parent_id: Optional parent Drive folder ID

        Returns:
            ScriptProject object

        Raises:
            Exception: If creation fails
            ValueError: If title is empty
        """
        if not title:
            raise ValueError("title is required")

        payload = {
            "title": title
        }

        if parent_id:
            payload["parentId"] = parent_id

        response_data = await self._make_request(
            "POST",
            "/projects",
            json_data=payload
        )

        return ScriptProject(
            script_id=response_data.get("scriptId", ""),
            title=response_data.get("title", title),
            parent_id=response_data.get("parentId"),
            create_time=response_data.get("createTime"),
            update_time=response_data.get("updateTime")
        )

    async def get_project(self, script_id: str) -> Optional[ScriptProject]:
        """
        Get details of a project.

        Args:
            script_id: Script project ID

        Returns:
            ScriptProject object or None if not found

        Raises:
            Exception: If request fails
        """
        try:
            response_data = await self._make_request(
                "GET",
                f"/projects/{script_id}"
            )

            return ScriptProject(
                script_id=response_data.get("scriptId", script_id),
                title=response_data.get("title", ""),
                parent_id=response_data.get("parentId"),
                create_time=response_data.get("createTime"),
                update_time=response_data.get("updateTime")
            )

        except Exception:
            return None

    async def get_project_content(self, script_id: str) -> Dict[str, Any]:
        """
        Get content of a project.

        Args:
            script_id: Script project ID

        Returns:
            Dictionary with project content

        Raises:
            Exception: If request fails
        """
        response_data = await self._make_request(
            "GET",
            f"/projects/{script_id}/content"
        )

        return response_data

    # ==================== Update Project Content ====================

    async def update_project_content(
        self,
        script_id: str,
        files: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Update content of a project.

        Args:
            script_id: Script project ID
            files: List of file objects with name, type, and source

        Returns:
            Updated project content

        Raises:
            Exception: If update fails
            ValueError: If script_id or files is invalid
        """
        if not script_id:
            raise ValueError("script_id is required")
        if not files:
            raise ValueError("files is required")

        payload = {"files": files}

        response_data = await self._make_request(
            "PUT",
            f"/projects/{script_id}/content",
            json_data=payload
        )

        return response_data

    async def update_file(
        self,
        script_id: str,
        file_name: str,
        source: str,
        file_type: str = "SERVER_JS"
    ) -> Dict[str, Any]:
        """
        Update a single file in a project.

        Args:
            script_id: Script project ID
            file_name: File name (e.g., "Code.gs")
            source: File content
            file_type: File type (SERVER_JS, HTML, JSON)

        Returns:
            Updated project content

        Raises:
            Exception: If update fails
        """
        # Get current content
        content = await self.get_project_content(script_id)
        current_files = content.get("files", [])

        # Find and update the file or add it
        file_updated = False
        for file in current_files:
            if file.get("name") == file_name:
                file.get("source", "") and setattr(file, "source", source)
                file_updated = True
                break

        if not file_updated:
            current_files.append({
                "name": file_name,
                "type": file_type,
                "source": source
            })

        return await self.update_project_content(script_id, current_files)

    # ==================== Create Project Version ====================

    async def create_version(
        self,
        script_id: str,
        description: str
    ) -> Version:
        """
        Create a new version of a project.

        Args:
            script_id: Script project ID
            description: Version description

        Returns:
            Version object

        Raises:
            Exception: If version creation fails
            ValueError: If parameters are invalid
        """
        if not script_id:
            raise ValueError("script_id is required")
        if not description:
            raise ValueError("description is required")

        payload = {"description": description}

        response_data = await self._make_request(
            "POST",
            f"/projects/{script_id}/versions",
            json_data=payload
        )

        return Version(
            version_number=response_data.get("versionNumber", 0),
            description=response_data.get("description", description),
            created_time=response_data.get("createdTime", "")
        )

    async def list_versions(self, script_id: str) -> List[Version]:
        """
        List all versions of a project.

        Args:
            script_id: Script project ID

        Returns:
            List of Version objects

        Raises:
            Exception: If request fails
        """
        response_data = await self._make_request(
            "GET",
            f"/projects/{script_id}/versions"
        )

        versions_list = response_data.get("versions", [])

        return [
            Version(
                version_number=ver.get("versionNumber", 0),
                description=ver.get("description", ""),
                created_time=ver.get("createdTime", "")
            )
            for ver in versions_list
        ]

    async def get_version(
        self,
        script_id: str,
        version_number: int
    ) -> Optional[Version]:
        """
        Get details of a specific version.

        Args:
            script_id: Script project ID
            version_number: Version number

        Returns:
            Version object or None if not found

        Raises:
            Exception: If request fails
        """
        try:
            response_data = await self._make_request(
                "GET",
                f"/projects/{script_id}/versions/{version_number}"
            )

            return Version(
                version_number=response_data.get("versionNumber", version_number),
                description=response_data.get("description", ""),
                created_time=response_data.get("createdTime", "")
            )

        except Exception:
            return None

    # ==================== Create Project Deployment ====================

    async def create_deployment(
        self,
        script_id: str,
        entry_point: str,
        description: Optional[str] = None,
        version_number: Optional[int] = None
    ) -> Deployment:
        """
        Create a deployment for a project.

        Args:
            script_id: Script project ID
            entry_point: Function name to deploy
            description: Optional deployment description
            version_number: Optional version number (head if not specified)

        Returns:
            Deployment object

        Raises:
            Exception: If deployment creation fails
            ValueError: If required parameters are missing
        """
        if not script_id:
            raise ValueError("script_id is required")
        if not entry_point:
            raise ValueError("entry_point is required")

        deployment_config = {
            "entryPoint": entry_point
        }

        if version_number:
            deployment_config["versionNumber"] = version_number
        else:
            deployment_config["manifestFileName"] = "appsscript.json"

        payload = {
            "description": description or f"Deployment of {entry_point}",
            "deploymentConfig": deployment_config
        }

        response_data = await self._make_request(
            "POST",
            f"/projects/{script_id}/deployments",
            json_data=payload
        )

        deployment = response_data.get("deployment", {})

        return Deployment(
            deployment_id=deployment.get("deploymentId", ""),
            deployment_config=deployment.get("deploymentConfig", {}),
            entry_points=[entry_point],
            version_number=version_number,
            update_time=deployment.get("updateTime")
        )

    async def list_deployments(self, script_id: str) -> List[Deployment]:
        """
        List all deployments of a project.

        Args:
            script_id: Script project ID

        Returns:
            List of Deployment objects

        Raises:
            Exception: If request fails
        """
        response_data = await self._make_request(
            "GET",
            f"/projects/{script_id}/deployments"
        )

        deployments_list = response_data.get("deployments", [])

        deployments = []
        for dep in deployments_list:
            config = dep.get("deploymentConfig", {})
            deployments.append(
                Deployment(
                    deployment_id=dep.get("deploymentId", ""),
                    deployment_config=config,
                    entry_points=[config.get("entryPoint", "")],
                    version_number=config.get("versionNumber"),
                    update_time=dep.get("updateTime")
                )
            )

        return deployments

    async def get_deployment(
        self,
        script_id: str,
        deployment_id: str
    ) -> Optional[Deployment]:
        """
        Get details of a specific deployment.

        Args:
            script_id: Script project ID
            deployment_id: Deployment ID

        Returns:
            Deployment object or None if not found

        Raises:
            Exception: If request fails
        """
        try:
            response_data = await self._make_request(
                "GET",
                f"/projects/{script_id}/deployments/{deployment_id}"
            )

            deployment = response_data.get("deployment", {})
            config = deployment.get("deploymentConfig", {})

            return Deployment(
                deployment_id=deployment.get("deploymentId", deployment_id),
                deployment_config=config,
                entry_points=[config.get("entryPoint", "")],
                version_number=config.get("versionNumber"),
                update_time=deployment.get("updateTime")
            )

        except Exception:
            return None

    # ==================== Execute Script (API-deployed) ====================

    async def execute_script(
        self,
        script_id: str,
        function_name: str,
        parameters: List[Any],
        dev_mode: bool = False
    ) -> ExecutionResult:
        """
        Execute a function in an API-deployed script.

        Args:
            script_id: Script project ID
            function_name: Function name to execute
            parameters: List of parameters to pass to the function
            dev_mode: Whether to execute in dev mode

        Returns:
            ExecutionResult with response or error

        Raises:
            Exception: If execution fails
            ValueError: If parameters are invalid
        """
        if not script_id:
            raise ValueError("script_id is required")
        if not function_name:
            raise ValueError("function_name is required")

        payload = {
            "function": function_name,
            "parameters": parameters,
            "devMode": dev_mode
        }

        response_data = await self._make_request(
            "POST",
            f"/scripts/{script_id}:run",
            json_data=payload
        )

        return ExecutionResult(
            response=response_data.get("response"),
            done=response_data.get("done", False),
            error=response_data.get("error")
        )

    # ==================== Execute Script (UI-deployed) ====================

    async def execute_ui_deployed_script(
        self,
        deployment_id_or_url: str,
        function_name: str,
        parameters: List[Any]
    ) -> ExecutionResult:
        """
        Execute a function in a UI-deployed script.

        Args:
            deployment_id_or_url: Deployment ID or web app URL
            function_name: Function name to execute
            parameters: List of parameters to pass to the function

        Returns:
            ExecutionResult with response or error

        Raises:
            Exception: If execution fails
            ValueError: If parameters are invalid
        """
        if not deployment_id_or_url:
            raise ValueError("deployment_id_or_url is required")
        if not function_name:
            raise ValueError("function_name is required")

        # If it's a full URL, extract the exec base
        if deployment_id_or_url.startswith("http"):
            base_url = deployment_id_or_url.rstrip("/exec")
            url = f"{base_url}/exec"
        else:
            # Assume it's a deployment ID
            url = f"https://script.google.com/macros/s/{deployment_id_or_url}/exec"

        payload = {
            "function": function_name,
            "parameters": parameters
        }

        try:
            async with self.session.post(url, json=payload) as response:
                response_data = await response.json()

                if response.status >= 400:
                    raise Exception(f"Execution failed (Status {response.status})")

                return ExecutionResult(
                    response=response_data,
                    done=True,
                    error=None
                )

        except aiohttp.ClientError as e:
            raise Exception(f"Network error during execution: {str(e)}")

    async def execute_web_app(
        self,
        web_app_url: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a Google Apps Script web app.

        Args:
            web_app_url: Web app URL
            parameters: Parameters to pass

        Returns:
            Response data

        Raises:
            Exception: If execution fails
        """
        try:
            async with self.session.post(web_app_url, json=parameters) as response:
                response_data = await response.json()

                if response.status >= 400:
                    text = await response.text()
                    raise Exception(f"Web app execution failed: {text}")

                return response_data

        except aiohttp.ClientError as e:
            raise Exception(f"Network error: {str(e)}")


# ==================== Example Usage ====================

async def main():
    """Example usage of Google Apps Script client"""

    # Replace with your actual OAuth access token
    ACCESS_TOKEN = "your_oauth_access_token"

    async with GoogleAppsScriptClient(access_token=ACCESS_TOKEN) as client:
        try:
            # Create a new project
            project = await client.create_project(
                title="My Automation Script",
                parent_id=None
            )
            print(f"Created project: {project.script_id}")

            # Update project content
            await client.update_file(
                script_id=project.script_id,
                file_name="Code.gs",
                source="""
function myFunction(input) {
  return 'Hello, ' + input + '!';
}

function addNumbers(a, b) {
  return a + b;
}
"""
            )
            print("Updated script content")

            # Create a version
            version = await client.create_version(
                script_id=project.script_id,
                description="Initial version"
            )
            print(f"Created version: {version.version_number}")

            # Create a deployment
            deployment = await client.create_deployment(
                script_id=project.script_id,
                entry_point="myFunction",
                description="My function deployment"
            )
            print(f"Created deployment: {deployment.deployment_id}")

            # Execute the script
            result = await client.execute_script(
                script_id=project.script_id,
                function_name="myFunction",
                parameters=["World"]
            )
            print(f"Execution result: {result.response}")

            # List deployments
            deployments = await client.list_deployments(project.script_id)
            print(f"Deployments: {len(deployments)}")

            # List versions
            versions = await client.list_versions(project.script_id)
            print(f"Versions: {len(versions)}")

        except Exception as e:
            print(f"Error: {str(e)}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())