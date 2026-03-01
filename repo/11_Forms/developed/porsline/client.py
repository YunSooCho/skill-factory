"""
Porsline API Client

Supports:
- Get survey responses
- List surveys
- Get survey details
"""

import requests
from typing import Optional, Dict, Any, List


class PorslineClient:
    """
    Porsline client for survey management.

    Authentication: API Key
    Base URL: https://survey.porsline.ir/api
    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://survey.porsline.ir/api"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"API-Key {api_key}",
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

    def list_surveys(self, page: int = 1, per_page: int = 20) -> List[Dict[str, Any]]:
        """List all surveys."""
        result = self._request("GET", "surveys", params={"page": page, "per_page": per_page})
        return result.get("results", [])

    def get_survey(self, survey_id: str) -> Dict[str, Any]:
        """Get survey details."""
        return self._request("GET", f"surveys/{survey_id}")

    def get_responses(self, survey_id: str, page: int = 1, per_page: int = 20) -> List[Dict[str, Any]]:
        """Get survey responses."""
        result = self._request("GET", f"surveys/{survey_id}/responses",
                               params={"page": page, "per_page": per_page})
        return result.get("results", [])

    def get_response(self, survey_id: str, response_id: str) -> Dict[str, Any]:
        """Get single response."""
        return self._request("GET", f"surveys/{survey_id}/responses/{response_id}")

    def get_response_count(self, survey_id: str) -> Dict[str, Any]:
        """Get response count."""
        return self._request("GET", f"surveys/{survey_id}/responses/count")

    def close(self):
        self.session.close()


def main():
    client = PorslineClient(api_key="your_key")
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
