# BigML API Client

Python async client for BigML's machine learning platform.

## Features

- ✅ Create anomaly scores
- ✅ Generate topic distributions
- ✅ Cluster data with centroids
- ✅ Make predictions with trained models
- ✅ Async/await support
- ✅ Type hints and dataclasses
- ✅ Comprehensive error handling

## Installation

```bash
pip install -r requirements.txt
```

## API Credentials

Get your credentials from: https://bigml.com/account/api-key

You'll need:
- **Username**: Your BigML username
- **API Key**: Your API key

## Usage

### Initialize Client

```python
import asyncio
from bigml_client import BigMLAPIClient

async def main():
    username = "your-username"
    api_key = "your-api-key"

    async with BigMLAPIClient(username, api_key) as client:
        # Use the client
        pass

asyncio.run(main())
```

### Create Anomaly Score

Detect anomalies in your data.

```python
async with BigMLAPIClient(username, api_key) as client:
    result = await client.create_anomaly_score(
        anomaly="anomaly/1234567890abc1234567890abc123",
        input_data={
            "feature1": 10.5,
            "feature2": 20.3,
            "feature3": 15.7
        }
    )

    print(f"Anomaly score: {result.anomaly['score']}")
    print(f"Is anomaly: {result.anomaly['is_anomaly']}")
```

**Interpreting Results:**
- Score close to 0: Normal data point
- Score > 0.5: Likely anomalous
- Score close to 1: Highly anomalous

### Create Topic Distribution

Analyze topics in text data.

```python
async with BigMLAPIClient(username, api_key) as client:
    result = await client.create_topic_distribution(
        topicmodel="topicmodel/1234567890abc1234567890abc123",
        input_data={
            "text": "Machine learning is transforming industries worldwide."
        }
    )

    print(f"Topic distribution: {result.topic_distribution}")

    # Get top topics
    topics = result.topic_distribution.get("topic_distribution", [])
    for i, (topic_id, probability) in enumerate(topics.items()[:5], 1):
        print(f"Topic {i}: {topic_id} (prob: {probability:.3f})")
```

### Create Centroid

Assign data points to clusters.

```python
async with BigMLAPIClient(username, api_key) as client:
    result = await client.create_centroid(
        centroid="cluster/1234567890abc1234567890abc123",
        input_data={
            "x": 1.5,
            "y": 2.3,
            "z": 0.8
        }
    )

    centroid = result.centroid
    print(f"Cluster ID: {centroid.centroid_id}")
    print(f"Cluster name: {centroid.centroid_name}")
    print(f"Distance to center: {centroid.distance:.4f}")
    print(f"Coordinates: {centroid.coordinates}")
```

### Create Prediction

Make predictions with trained models.

```python
async with BigMLAPIClient(username, api_key) as client:
    result = await client.create_prediction(
        model="model/1234567890abc1234567890abc123",
        input_data={
            "age": 30,
            "income": 50000,
            "education": "bachelor",
            "experience": 5
        },
        missing_strategy="last"  # or "mean", "proportional", etc.
    )

    print(f"Prediction: {result.prediction.prediction}")
    print(f"Confidence: {result.prediction.confidence:.2f}")
```

## API Actions

### Create Anomaly Score

Detect anomalies using an anomaly detector model.

**Parameters:**
- `anomaly` (str): Anomaly detector resource ID
- `input_data` (Dict[str, Any]): Dictionary of input features

**Returns:** `AnomalyResponse`

### Create Topic Distribution

Get topic probabilities for text/document data.

**Parameters:**
- `topicmodel` (str): Topic model resource ID
- `input_data` (Dict[str, Any]): Dictionary with text data

**Returns:** `TopicResponse`

### Create Centroid

Assign data points to clusters using a cluster model.

**Parameters:**
- `centroid` (str): Cluster model resource ID
- `input_data` (Dict[str, Any]): Dictionary of input features

**Returns:** `CentroidResponse`

### Create Prediction

Make predictions using a trained model.

**Parameters:**
- `model` (str): Model resource ID
- `input_data` (Dict[str, Any]): Dictionary of input features
- `missing_strategy` (str): How to handle missing values ('last', 'mean', 'proportional', etc.)

**Returns:** `PredictionResponse`

## Model IDs

BigML uses resource IDs like:
- `anomaly/abc123...`
- `topicmodel/abc123...`
- `cluster/abc123...`
- `model/abc123...`

Get these IDs from the BigML dashboard or API.

## Missing Values Strategies

- `last`: Use last known value (default)
- `mean`: Use mean of the feature
- `proportional`: Use proportional distribution
- `zero`: Use zero value

## Error Handling

All methods raise exceptions on errors:

```python
try:
    result = await client.create_prediction(
        model="model/invalid",
        input_data={"feature": 10}
    )
except Exception as e:
    print(f"Error: {e}")
```

## API Reference

Official documentation: https://bigml.com/api/

## Model Training

Before using these operations, you need to:
1. Upload your dataset to BigML
2. Train a model (anomaly detector, topic model, cluster, or prediction model)
3. Use the model ID in the API calls

## Workflow Example

```python
# 1. Anomaly detection workflow
anomaly_score = await client.create_anomaly_score(
    anomaly="your_anomaly_detector_id",
    input_data=get_new_data_point()
)

if anomaly_score.anomaly['score'] > 0.7:
    print("Detected anomaly! Investigating...")
    trigger_alert(anomaly_score)

# 2. Customer segmentation workflow
centroid = await client.create_centroid(
    centroid="your_cluster_model_id",
    input_data={"age": 35, "spending": 1000, "frequency": 10}
)

segment = centroid.centroid.centroid_name
apply_segment_offer(segment)

# 3. Prediction workflow
prediction = await client.create_prediction(
    model="your_model_id",
    input_data=get_customer_features()
)

if prediction.prediction.prediction == "churn":
    send_retention_offer()
```

## Rate Limits

Check your account dashboard for rate limit information.

## Support

For issues, visit: https://bigml.com/developers/