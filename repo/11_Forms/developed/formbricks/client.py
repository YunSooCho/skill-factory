"""
Formbricks API Client

Supports:
- Get survey responses
- List surveys
- Create surveys
"""

import requests
from typing import Optional, Dict, Any, List


class FormbricksClient:
    """
    Formbricks client for survey management.

    Authentication: API Key
    Base URL: https://app.formbricks.com/api/v1
    """

    def __init__(self, api_key: str, host: str = "https://app.formbricks.com"):
        self.api_key = api_key
        self.base_url = f"{host}/api/v1"
        self.session = requests.Session()
        self.session.headers.update({
            "x-api-key": api_key,
            "Content-Type": "application/json"
        })

    def _request(self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None, data: Optional[Dict[str, Any]] = None) -> Any:
        url = f"{self.base_url}/{endpoint}"
        try:
            resp = getattr(self.session, method.lower())(url, params=params, json=data if method != "GET" else None)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    def list_surveys(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """List all surveys."""
        result = self._request("GET", "management/surveys", params={"limit": limit, "offset": offset})
        return result.get("data", [])

    def get_survey(self, survey_id: str) -> Dict[str, Any]:
        """Get survey details."""
        return self._request("GET", f"management/surveys/{survey_id}")

    def get_responses(self, survey_id: str, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """Get survey responses."""
        result = self._request("GET", f"management/surveys/{survey_id}/responses", params={"limit": limit, "offset": offset})
        return result.get("data", [])

    def create_survey(self, survey_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new survey."""
        return self._request("POST", "management/surveys", data=survey_data)

    def delete_survey(self, survey_id: str) -> Dict[str, Any]:
        """Delete a survey."""
        return self._request("DELETE", f"management/surveys/{survey_id}")

    def close(self):
        self.session.close()


def main():
    client = FormbricksClient(api_key="your_key")
    try:
        surveys = client.list_surveys()
        print(f"Surveys: {surveys}")
        if surveys:
            responses = client.get_responses(surveys[0]["id"])
            print(f"Responses: {responses}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()


if __name__ == "__main__":
    main()
