"""
BigML API - Machine Learning Platform Client

Supports:
- Create Anomaly Score
- Create Topic Distribution
- Create Centroid
- Create Prediction
"""

import aiohttp
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class AnomalyScore:
    """Anomaly detection score"""
    score: float
    id: str
    anomaly: bool


@dataclass
class AnomalyResponse:
    """Anomaly score response"""
    resource: str
    anomaly: Dict[str, Any]
    objective_field: str
    input_data: Dict[str, Any]


@dataclass
class TopicDistribution:
    """Topic probability distribution"""
    topics: List[Dict[str, float]]
    id: str


@dataclass
class TopicResponse:
    """Topic distribution response"""
    resource: str
    topic_distribution: Dict[str, Any]
    input_data: Dict[str, Any]


@dataclass
class Centroid:
    """Cluster centroid information"""
    centroid_id: str
    centroid_name: str
    distance: float
    coordinates: Dict[str, float]


@dataclass
class CentroidResponse:
    """Centroid prediction response"""
    resource: str
    centroid: Centroid
    input_data: Dict[str, Any]
    model: str


@dataclass
class Prediction:
    """Model prediction result"""
    prediction: Any
    confidence: float
    id: str


@dataclass
class PredictionResponse:
    """Prediction response"""
    resource: str
    prediction: Prediction
    model: str
    input_data: Dict[str, Any]


class BigMLAPIClient:
    """
    BigML API client for machine learning operations.

    API Documentation: https://bigml.com/api/
    """

    BASE_URL = "https://bigml.io/andromeda"

    def __init__(self, username: str, api_key: str):
        """
        Initialize BigML API client.

        Args:
            username: BigML username
            api_key: BigML API key (from account settings)
        """
        self.username = username
        self.api_key = api_key
        self.session = None

    def _get_auth(self) -> str:
        """Get basic auth string"""
        import base64
        credentials = f"{self.username}:{self.api_key}"
        encoded = base64.b64encode(credentials.encode()).decode()
        return f"Basic {encoded}"

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={
                "Authorization": self._get_auth(),
                "Content-Type": "application/json"
            }
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def create_anomaly_score(
        self,
        anomaly: str,
        input_data: Dict[str, Any]
    ) -> AnomalyResponse:
        """
        Create an anomaly score for given input data.

        Args:
            anomaly: Anomaly detector ID
            input_data: Dictionary of input features

        Returns:
            AnomalyResponse with anomaly score

        Raises:
            ValueError: If anomaly ID or input_data is empty
            aiohttp.ClientError: If request fails
        """
        if not anomaly:
            raise ValueError("Anomaly detector ID cannot be empty")
        if not input_data:
            raise ValueError("Input data cannot be empty")

        payload = {
            "anomaly": anomaly,
            "input_data": input_data
        }

        async with self.session.post(
            f"{self.BASE_URL}/anomalyscore",
            json=payload
        ) as response:
            data = await response.json()

            if response.status not in [200, 201]:
                error_msg = data.get("error", {}).get("message", str(data))
                raise Exception(f"BigML Anomaly Score error: {error_msg}")

            anomaly_result = data.get("object", {}).get("result", {})

            return AnomalyResponse(
                resource=data.get("resource", ""),
                anomaly={
                    "score": anomaly_result.get("anomaly_score", 0.0),
                    "id": anomaly_result.get("id", ""),
                    "is_anomaly": anomaly_result.get("anomaly_score", 0.0) > 0.5
                },
                objective_field=data.get("object", {}).get("objective_field", ""),
                input_data=data.get("object", {}).get("input_data", {})
            )

    async def create_topic_distribution(
        self,
        topicmodel: str,
        input_data: Dict[str, Any]
    ) -> TopicResponse:
        """
        Create topic distribution for given text/document.

        Args:
            topicmodel: Topic model ID
            input_data: Dictionary with text data

        Returns:
            TopicResponse with topic probabilities

        Raises:
            ValueError: If topic model ID or input_data is empty
            aiohttp.ClientError: If request fails
        """
        if not topicmodel:
            raise ValueError("Topic model ID cannot be empty")
        if not input_data:
            raise ValueError("Input data cannot be empty")

        payload = {
            "topicmodel": topicmodel,
            "input_data": input_data
        }

        async with self.session.post(
            f"{self.BASE_URL}/topicdistribution",
            json=payload
        ) as response:
            data = await response.json()

            if response.status not in [200, 201]:
                error_msg = data.get("error", {}).get("message", str(data))
                raise Exception(f"BigML Topic Distribution error: {error_msg}")

            return TopicResponse(
                resource=data.get("resource", ""),
                topic_distribution=data.get("object", {}).get("topic_distribution", {}),
                input_data=data.get("object", {}).get("input_data", {})
            )

    async def create_centroid(
        self,
        centroid: str,
        input_data: Dict[str, Any]
    ) -> CentroidResponse:
        """
        Create centroid assignment for input data.

        Args:
            centroid: Cluster model ID
            input_data: Dictionary of input features

        Returns:
            CentroidResponse with cluster assignment

        Raises:
            ValueError: If centroid ID or input_data is empty
            aiohttp.ClientError: If request fails
        """
        if not centroid:
            raise ValueError("Cluster ID cannot be empty")
        if not input_data:
            raise ValueError("Input data cannot be empty")

        payload = {
            "centroid": centroid,
            "input_data": input_data
        }

        async with self.session.post(
            f"{self.BASE_URL}/centroid",
            json=payload
        ) as response:
            data = await response.json()

            if response.status not in [200, 201]:
                error_msg = data.get("error", {}).get("message", str(data))
                raise Exception(f"BigML Centroid error: {error_msg}")

            centroid_result = data.get("object", {}).get("result", {})

            return CentroidResponse(
                resource=data.get("resource", ""),
                centroid=Centroid(
                    centroid_id=centroid_result.get("centroid_id", ""),
                    centroid_name=centroid_result.get("centroid_name", ""),
                    distance=centroid_result.get("distance", 0.0),
                    coordinates=centroid_result.get("coordinates", {})
                ),
                input_data=data.get("object", {}).get("input_data", {}),
                model=centroid_result.get("model", "")
            )

    async def create_prediction(
        self,
        model: str,
        input_data: Dict[str, Any],
        missing_strategy: str = "last"
    ) -> PredictionResponse:
        """
        Create a prediction using a trained model.

        Args:
            model: Model ID
            input_data: Dictionary of input features
            missing_strategy: How to handle missing values ('last', 'mean', etc.)

        Returns:
            PredictionResponse with prediction result

        Raises:
            ValueError: If model ID or input_data is empty
            aiohttp.ClientError: If request fails
        """
        if not model:
            raise ValueError("Model ID cannot be empty")
        if not input_data:
            raise ValueError("Input data cannot be empty")

        payload = {
            "model": model,
            "input_data": input_data,
            "missing_strategy": missing_strategy
        }

        async with self.session.post(
            f"{self.BASE_URL}/prediction",
            json=payload
        ) as response:
            data = await response.json()

            if response.status not in [200, 201]:
                error_msg = data.get("error", {}).get("message", str(data))
                raise Exception(f"BigML Prediction error: {error_msg}")

            prediction_result = data.get("object", {}).get("result", {})

            return PredictionResponse(
                resource=data.get("resource", ""),
                prediction=Prediction(
                    prediction=prediction_result.get("prediction", None),
                    confidence=prediction_result.get("confidence", 0.0),
                    id=data.get("resource", "")
                ),
                model=prediction_result.get("model", ""),
                input_data=data.get("object", {}).get("input_data", {})
            )


async def main():
    """Example usage"""
    username = "your-username"
    api_key = "your-api-key"

    async with BigMLAPIClient(username, api_key) as client:
        # Anomaly score example
        try:
            anomaly_result = await client.create_anomaly_score(
                anomaly="anomaly/1234567890",
                input_data={"feature1": 10.5, "feature2": 20.3, "feature3": 15.7}
            )
            print(f"Anomaly score: {anomaly_result.anomaly['score']}")
        except Exception as e:
            print(f"Anomaly score error: {e}")

        # Topic distribution example
        try:
            topic_result = await client.create_topic_distribution(
                topicmodel="topicmodel/1234567890",
                input_data={"text": "This is a sample document about machine learning."}
            )
            print(f"Topic distribution: {topic_result.topic_distribution}")
        except Exception as e:
            print(f"Topic distribution error: {e}")

        # Centroid example
        try:
            centroid_result = await client.create_centroid(
                centroid="cluster/1234567890",
                input_data={"x": 1.5, "y": 2.3, "z": 0.8}
            )
            print(f"Centroid ID: {centroid_result.centroid.centroid_id}")
            print(f"Distance: {centroid_result.centroid.distance:.2f}")
        except Exception as e:
            print(f"Centroid error: {e}")

        # Prediction example
        try:
            prediction_result = await client.create_prediction(
                model="model/1234567890",
                input_data={"age": 30, "income": 50000, "education": "bachelor"}
            )
            print(f"Prediction: {prediction_result.prediction.prediction}")
            print(f"Confidence: {prediction_result.prediction.confidence:.2f}")
        except Exception as e:
            print(f"Prediction error: {e}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())