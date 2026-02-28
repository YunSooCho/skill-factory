"""
Brightback API Client

Supports:
- Create Cancellation Survey
- Create Churn Prediction
- Get Churn Risk Score
- Update Customer Status
"""

import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class CancellationSurvey:
    """Cancellation survey response"""
    survey_id: Optional[str] = None
    customer_id: Optional[str] = None
    reason: Optional[str] = None
    feedback: Optional[str] = None
    satisfaction_score: Optional[int] = None
    retention_offer_shown: bool = False
    retention_offer_accepted: bool = False
    created_at: Optional[str] = None


@dataclass
class ChurnPrediction:
    """Churn prediction data"""
    customer_id: Optional[str] = None
    churn_risk_score: Optional[float] = None
    risk_level: Optional[str] = None
    prediction_reasons: List[str] = None
    recommended_actions: List[str] = None
    analyzed_at: Optional[str] = None

    def __post_init__(self):
        if self.prediction_reasons is None:
            self.prediction_reasons = []
        if self.recommended_actions is None:
            self.recommended_actions = []


@dataclass
class CustomerStatus:
    """Customer churn status"""
    customer_id: Optional[str] = None
    status: Optional[str] = None
    churn_date: Optional[str] = None
    saved: bool = False
    save_reason: Optional[str] = None


class BrightbackClient:
    """
    Brightback API client for churn prediction and cancellation surveys.

    Authentication: API Key (Header: Authorization: Bearer {api_key})
    Base URL: https://api.brightback.com/v1
    """

    BASE_URL = "https://api.brightback.com/v1"

    def __init__(self, api_key: str):
        """
        Initialize Brightback client.

        Args:
            api_key: Brightback API key
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
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

    # ==================== Cancellation Survey ====================

    def create_cancellation_survey(
        self,
        customer_id: str,
        reason: Optional[str] = None,
        feedback: Optional[str] = None,
        satisfaction_score: Optional[int] = None
    ) -> CancellationSurvey:
        """
        Create a cancellation survey response.

        Args:
            customer_id: Customer ID
            reason: Cancellation reason
            feedback: Additional feedback
            satisfaction_score: Satisfaction score (1-10)

        Returns:
            CancellationSurvey object
        """
        if not customer_id:
            raise ValueError("Customer ID is required")

        payload: Dict[str, Any] = {"customer_id": customer_id}

        if reason:
            payload["reason"] = reason
        if feedback:
            payload["feedback"] = feedback
        if satisfaction_score:
            if not 1 <= satisfaction_score <= 10:
                raise ValueError("Satisfaction score must be between 1 and 10")
            payload["satisfaction_score"] = satisfaction_score

        result = self._request("POST", "/surveys", json=payload)
        return self._parse_cancellation_survey(result)

    def update_survey_retention(
        self,
        survey_id: str,
        offer_shown: bool,
        offer_accepted: bool
    ) -> CancellationSurvey:
        """
        Update survey with retention offer information.

        Args:
            survey_id: Survey ID
            offer_shown: Whether retention offer was shown
            offer_accepted: Whether customer accepted the offer

        Returns:
            Updated CancellationSurvey object
        """
        if not survey_id:
            raise ValueError("Survey ID is required")

        payload = {
            "retention_offer_shown": offer_shown,
            "retention_offer_accepted": offer_accepted
        }

        result = self._request("PATCH", f"/surveys/{survey_id}", json=payload)
        return self._parse_cancellation_survey(result)

    # ==================== Churn Prediction ====================

    def create_churn_prediction(
        self,
        customer_id: str,
        attributes: Optional[Dict[str, Any]] = None
    ) -> ChurnPrediction:
        """
        Create a churn prediction for a customer.

        Args:
            customer_id: Customer ID
            attributes: Customer attributes for prediction

        Returns:
            ChurnPrediction object
        """
        if not customer_id:
            raise ValueError("Customer ID is required")

        payload: Dict[str, Any] = {"customer_id": customer_id}

        if attributes:
            payload["attributes"] = attributes

        result = self._request("POST", "/predictions", json=payload)
        return self._parse_churn_prediction(result)

    def get_churn_risk_score(self, customer_id: str) -> ChurnPrediction:
        """
        Get current churn risk score for a customer.

        Args:
            customer_id: Customer ID

        Returns:
            ChurnPrediction object
        """
        if not customer_id:
            raise ValueError("Customer ID is required")

        result = self._request("GET", f"/customers/{customer_id}/risk")
        return self._parse_churn_prediction(result)

    # ==================== Customer Status ====================

    def update_customer_status(
        self,
        customer_id: str,
        status: str,
        save_reason: Optional[str] = None
    ) -> CustomerStatus:
        """
        Update customer churn status.

        Args:
            customer_id: Customer ID
            status: Customer status (active, churned, saved)
            save_reason: Reason if customer was saved

        Returns:
            CustomerStatus object
        """
        if not customer_id:
            raise ValueError("Customer ID is required")
        if not status:
            raise ValueError("Status is required")

        payload: Dict[str, Any] = {"status": status}

        if save_reason:
            payload["save_reason"] = save_reason

        result = self._request("PATCH", f"/customers/{customer_id}/status", json=payload)
        return self._parse_customer_status(result)

    # ==================== Helper Methods ====================

    def _parse_cancellation_survey(self, data: Dict[str, Any]) -> CancellationSurvey:
        """Parse cancellation survey data from API response"""
        return CancellationSurvey(
            survey_id=data.get("survey_id"),
            customer_id=data.get("customer_id"),
            reason=data.get("reason"),
            feedback=data.get("feedback"),
            satisfaction_score=data.get("satisfaction_score"),
            retention_offer_shown=data.get("retention_offer_shown", False),
            retention_offer_accepted=data.get("retention_offer_accepted", False),
            created_at=data.get("created_at")
        )

    def _parse_churn_prediction(self, data: Dict[str, Any]) -> ChurnPrediction:
        """Parse churn prediction data from API response"""
        return ChurnPrediction(
            customer_id=data.get("customer_id"),
            churn_risk_score=data.get("churn_risk_score"),
            risk_level=data.get("risk_level"),
            prediction_reasons=data.get("prediction_reasons", []),
            recommended_actions=data.get("recommended_actions", []),
            analyzed_at=data.get("analyzed_at")
        )

    def _parse_customer_status(self, data: Dict[str, Any]) -> CustomerStatus:
        """Parse customer status data from API response"""
        return CustomerStatus(
            customer_id=data.get("customer_id"),
            status=data.get("status"),
            churn_date=data.get("churn_date"),
            saved=data.get("saved", False),
            save_reason=data.get("save_reason")
        )

    def close(self):
        """Close the HTTP session"""
        self.session.close()


def main():
    """Example usage"""
    api_key = "your_brightback_api_key"

    client = BrightbackClient(api_key=api_key)

    try:
        # Create churn prediction
        prediction = client.create_churn_prediction(
            customer_id="cust123",
            attributes={
                "subscription_length": 180,
                "usage_score": 0.7,
                "support_tickets": 3,
                "plan_tier": "premium"
            }
        )
        print(f"Churn Risk Score: {prediction.churn_risk_score}")
        print(f"Risk Level: {prediction.risk_level}")
        print(f"Reasons: {prediction.prediction_reasons}")

        # Create cancellation survey
        survey = client.create_cancellation_survey(
            customer_id="cust123",
            reason="Price",
            feedback="Too expensive for our budget",
            satisfaction_score=6
        )
        print(f"\nSurvey created: {survey.survey_id}")
        print(f"Reason: {survey.reason}")

        # Update survey with retention offer
        updated = client.update_survey_retention(
            survey_id=survey.survey_id,
            offer_shown=True,
            offer_accepted=True
        )
        print(f"Retention offer accepted: {updated.retention_offer_accepted}")

        # Update customer status as saved
        status = client.update_customer_status(
            customer_id="cust123",
            status="saved",
            save_reason="Accepted discount offer"
        )
        print(f"Customer status: {status.status}")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        client.close()


if __name__ == "__main__":
    main()