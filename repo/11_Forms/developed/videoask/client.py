"""
VideoAsk API Client

Supports:
- Get interactions (responses)
- List videoasks (forms)
- Get contact details
"""

import requests
from typing import Optional, Dict, Any, List


class VideoAskClient:
    """
    VideoAsk client for video form management.

    Authentication: API Key (Bearer token)
    Base URL: https://api.videoask.com
    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.videoask.com"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
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

    def list_videoasks(self, page: int = 1, limit: int = 10) -> Dict[str, Any]:
        """List all videoasks."""
        return self._request("GET", "videoasks", params={"page": page, "limit": limit})

    def get_videoask(self, videoask_id: str) -> Dict[str, Any]:
        """Get videoask details."""
        return self._request("GET", f"videoasks/{videoask_id}")

    def get_interactions(self, videoask_id: str, page: int = 1, limit: int = 10) -> Dict[str, Any]:
        """Get interactions (responses) for a videoask."""
        return self._request("GET", f"videoasks/{videoask_id}/interactions",
                             params={"page": page, "limit": limit})

    def get_interaction(self, interaction_id: str) -> Dict[str, Any]:
        """Get single interaction details."""
        return self._request("GET", f"interactions/{interaction_id}")

    def list_contacts(self, page: int = 1, limit: int = 10) -> Dict[str, Any]:
        """List contacts."""
        return self._request("GET", "contacts", params={"page": page, "limit": limit})

    def get_contact(self, contact_id: str) -> Dict[str, Any]:
        """Get contact details."""
        return self._request("GET", f"contacts/{contact_id}")

    def close(self):
        self.session.close()


def main():
    client = VideoAskClient(api_key="your_key")
    try:
        videoasks = client.list_videoasks()
        print(f"VideoAsks: {videoasks}")
        if videoasks.get("data"):
            interactions = client.get_interactions(videoasks["data"][0]["id"])
            print(f"Interactions: {interactions}")
        contacts = client.list_contacts()
        print(f"Contacts: {contacts}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main()
