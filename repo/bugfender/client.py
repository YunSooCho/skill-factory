"""
Bugfender API Client

Supports:
- Send Line
- Send Logs
- Get Logs
- Get Devices
- Get Device Info
- Create Issue
"""

import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class LogLine:
    """Log line entry"""
    line: Optional[str] = None
    level: Optional[str] = None
    timestamp: Optional[str] = None
    device_id: Optional[str] = None
    app_version: Optional[str] = None
    os_version: Optional[str] = None
    file: Optional[str] = None
    method: Optional[str] = None
    line_number: Optional[int] = None


@dataclass
class Device:
    """Device information"""
    device_id: Optional[str] = None
    app_id: Optional[str] = None
    device_name: Optional[str] = None
    model: Optional[str] = None
    os_name: Optional[str] = None
    os_version: Optional[str] = None
    app_version: Optional[str] = None
    carrier: Optional[str] = None
    network_type: Optional[str] = None
    last_seen: Optional[str] = None
    total_lines: int = 0
    total_crashes: int = 0


@dataclass
class Issue:
    """Issue/bug report"""
    issue_id: Optional[str] = None
    device_id: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    severity: Optional[str] = None
    created_at: Optional[str] = None


class BugfenderClient:
    """
    Bugfender API client for app monitoring, logging, and crash reporting.

    Authentication: API Key (Header: X-Bugfender-REST-API-Key)
    Base URL: https://api.bugfender.io
    """

    BASE_URL = "https://api.bugfender.io"

    def __init__(self, api_key: str, app_id: str):
        """
        Initialize Bugfender client.

        Args:
            api_key: Bugfender REST API key
            app_id: Application ID
        """
        self.api_key = api_key
        self.app_id = app_id
        self.session = requests.Session()
        self.session.headers.update({
            "X-Bugfender-REST-API-Key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make API request with error handling and rate limiting"""
        url = f"{self.BASE_URL}{endpoint}"

        try:
            response = self.session.request(method, url, **kwargs)

            if response.status_code in (200, 201, 202, 204):
                if response.status_code == 204:
                    return {}
                data = response.json()
                return data
            elif response.status_code == 401:
                raise Exception("Authentication failed: Invalid API key")
            elif response.status_code == 404:
                raise Exception(f"Resource not found: {endpoint}")
            elif response.status_code == 429:
                raise Exception("Rate limit exceeded. Please retry later.")
            elif response.status_code >= 500:
                raise Exception(f"Server error: {response.status_code}")
            else:
                error_data = response.json() if response.content else {}
                raise Exception(f"API error {response.status_code}: {error_data}")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    # ==================== Logging ====================

    def send_line(
        self,
        device_id: str,
        line: str,
        level: str = "LOG",
        method: Optional[str] = None,
        file: Optional[str] = None,
        line_number: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Send a log line to Bugfender.

        Args:
            device_id: Device ID
            line: Log message
            level: Log level (LOG, WARNING, ERROR, FATAL)
            method: Method name
            file: File name
            line_number: Line number

        Returns:
            Send response
        """
        if not device_id:
            raise ValueError("Device ID is required")
        if not line:
            raise ValueError("Log line is required")

        payload: Dict[str, Any] = {
            "line": line,
            "level": level
        }

        if method:
            payload["method"] = method
        if file:
            payload["file"] = file
        if line_number:
            payload["lineNumber"] = line_number

        return self._request("POST", f"/logs/{self.app_id}/{device_id}", json=payload)

    def send_logs(
        self,
        device_id: str,
        logs: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Send multiple log lines in batch.

        Args:
            device_id: Device ID
            logs: List of log entries

        Returns:
            Send response
        """
        if not device_id:
            raise ValueError("Device ID is required")
        if not logs:
            raise ValueError("Logs list is required")

        return self._request("POST", f"/logs/{self.app_id}/{device_id}/bulk", json={"logs": logs})

    # ==================== Log Retrieval ====================

    def get_logs(
        self,
        device_id: str,
        level: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
        search: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Retrieve logs for a device.

        Args:
            device_id: Device ID
            level: Filter by log level
            limit: Number of results
            offset: Pagination offset
            search: Search query

        Returns:
            Log lines and pagination info
        """
        if not device_id:
            raise ValueError("Device ID is required")

        params: Dict[str, Any] = {
            "limit": limit,
            "offset": offset
        }

        if level:
            params["level"] = level
        if search:
            params["search"] = search

        result = self._request("GET", f"/logs/{self.app_id}/{device_id}", params=params)

        logs = [self._parse_log_line(log) for log in result.get("logs", [])]
        total = result.get("total", 0)

        return {
            "logs": logs,
            "total": total,
            "limit": limit,
            "offset": offset
        }

    # ==================== Device Management ====================

    def get_devices(
        self,
        limit: int = 50,
        offset: int = 0,
        search: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get list of devices.

        Args:
            limit: Number of results
            offset: Pagination offset
            search: Search query

        Returns:
            Device list and pagination info
        """
        params: Dict[str, Any] = {
            "limit": limit,
            "offset": offset
        }

        if search:
            params["search"] = search

        result = self._request("GET", f"/devices/{self.app_id}", params=params)

        devices = [self._parse_device(d) for d in result.get("devices", [])]
        total = result.get("total", 0)

        return {
            "devices": devices,
            "total": total,
            "limit": limit,
            "offset": offset
        }

    def get_device_info(self, device_id: str) -> Device:
        """
        Get detailed device information.

        Args:
            device_id: Device ID

        Returns:
            Device object
        """
        if not device_id:
            raise ValueError("Device ID is required")

        result = self._request("GET", f"/devices/{self.app_id}/{device_id}")
        return self._parse_device(result)

    # ==================== Issue/Crash Management ====================

    def create_issue(
        self,
        device_id: str,
        title: str,
        description: Optional[str] = None,
        severity: Optional[str] = None
    ) -> Issue:
        """
        Create a new issue/bug report.

        Args:
            device_id: Device ID
            title: Issue title
            description: Issue description
            severity: Severity level (low, medium, high, critical)

        Returns:
            Issue object
        """
        if not device_id:
            raise ValueError("Device ID is required")
        if not title:
            raise ValueError("Issue title is required")

        payload: Dict[str, Any] = {
            "title": title
        }

        if description:
            payload["description"] = description
        if severity:
            payload["severity"] = severity

        result = self._request("POST", f"/issues/{self.app_id}/{device_id}", json=payload)
        return self._parse_issue(result)

    # ==================== Helper Methods ====================

    def _parse_log_line(self, data: Dict[str, Any]) -> LogLine:
        """Parse log line data from API response"""
        return LogLine(
            line=data.get("line"),
            level=data.get("level"),
            timestamp=data.get("timestamp"),
            device_id=data.get("device"),
            app_version=data.get("appVersion"),
            os_version=data.get("osVersion"),
            file=data.get("file"),
            method=data.get("method"),
            line_number=data.get("lineNumber")
        )

    def _parse_device(self, data: Dict[str, Any]) -> Device:
        """Parse device data from API response"""
        return Device(
            device_id=data.get("device"),
            app_id=data.get("app"),
            device_name=data.get("deviceName"),
            model=data.get("model"),
            os_name=data.get("osName"),
            os_version=data.get("osVersion"),
            app_version=data.get("appVersion"),
            carrier=data.get("carrier"),
            network_type=data.get("networkType"),
            last_seen=data.get("lastSeen"),
            total_lines=data.get("totalLines", 0),
            total_crashes=data.get("totalCrashes", 0)
        )

    def _parse_issue(self, data: Dict[str, Any]) -> Issue:
        """Parse issue data from API response"""
        return Issue(
            issue_id=data.get("id"),
            device_id=data.get("device"),
            title=data.get("title"),
            description=data.get("description"),
            status=data.get("status"),
            severity=data.get("severity"),
            created_at=data.get("createdAt")
        )

    def close(self):
        """Close the HTTP session"""
        self.session.close()


def main():
    """Example usage"""
    api_key = "your_bugfender_api_key"
    app_id = "your_app_id"

    client = BugfenderClient(api_key=api_key, app_id=app_id)

    try:
        # Send a log line
        client.send_line(
            device_id="device123",
            line="Application started successfully",
            level="LOG",
            method="main()",
            file="app.py",
            line_number=10
        )
        print("Log line sent successfully")

        # Send multiple logs in batch
        logs = [
            {"line": "Loading user data", "level": "LOG"},
            {"line": "Failed to connect to database", "level": "ERROR"},
            {"line": "Retrying connection", "level": "WARNING"}
        ]
        client.send_logs(device_id="device123", logs=logs)
        print("Batch logs sent successfully")

        # Get logs
        log_response = client.get_logs(device_id="device123", limit=10)
        print(f"\nRetrieved {len(log_response['logs'])} log lines")
        for log in log_response['logs'][:3]:
            print(f"  [{log.level}] {log.line}")

        # Get devices
        devices_response = client.get_devices(limit=10)
        print(f"\nTotal devices: {devices_response['total']}")
        for device in devices_response['devices'][:3]:
            print(f"  - {device.device_name} ({device.model})")

        # Get device info
        if devices_response['devices']:
            device_info = client.get_device_info(devices_response['devices'][0].device_id)
            print(f"\nDevice OS: {device_info.os_name} {device_info.os_version}")
            print(f"App Version: {device_info.app_version}")

        # Create issue
        issue = client.create_issue(
            device_id="device123",
            title="Critical login failure",
            description="Users unable to login due to database connection timeout",
            severity="high"
        )
        print(f"\nIssue created: {issue.issue_id}")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        client.close()


if __name__ == "__main__":
    main()