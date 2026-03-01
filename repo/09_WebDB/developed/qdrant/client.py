"""
Qdrant API Client

This module provides a Python client for interacting with Qdrant vector database.
"""

import requests
from typing import Dict, List, Optional, Any, Union
import json
from datetime import datetime


class QdrantClient:
    """
    Client for Qdrant Vector Database.

    Qdrant provides:
    - Vector similarity search
    - Collection management
    - Point operations (insert, update, delete)
    - Filtering and payload management
    - Distance metrics configuration
    """

    def __init__(
        self,
        api_key: str,
        url: str = "https://api.qdrant.io",
        timeout: int = 30
    ):
        """
        Initialize the Qdrant client.

        Args:
            api_key: Qdrant API key
            url: Base URL for the Qdrant API
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.url = url.rstrip('/')
        self.timeout = timeout

        self.session = requests.Session()
        self.session.headers.update({
            'api-key': api_key,
            'Content-Type': 'application/json'
        })

    def _request(
        self,
        method: str,
        endpoint: str,
        params=None,
        data=None,
        json_data=None
    ) -> Dict[str, Any]:
        """Make an authenticated request to the API."""
        url = f"{self.url}{endpoint}"
        response = self.session.request(
            method,
            url,
            params=params,
            data=data,
            json=json_data,
            timeout=self.timeout
        )

        if response.status_code >= 400:
            error_data = response.json() if response.content else {}
            raise Exception(f"API Error {response.status_code}: {error_data}")

        try:
            return response.json()
        except:
            return response.text if response.text else {}

    def get_collections(self) -> Dict[str, Any]:
        """Get all collections."""
        return self._request('GET', '/collections')

    def create_collection(
        self,
        collection_name: str,
        vector_size: int,
        distance: str = "Cosine",
        hnsw_config: Optional[Dict[str, Any]] = None,
        optimizers_config: Optional[Dict[str, Any]] = None,
        wal_config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a new collection."""
        vectors_config = {
            "size": vector_size,
            "distance": distance
        }

        data = {
            "vectors": vectors_config
        }

        if hnsw_config:
            data["hnsw_config"] = hnsw_config
        if optimizers_config:
            data["optimizers_config"] = optimizers_config
        if wal_config:
            data["wal_config"] = wal_config

        return self._request('PUT', f'/collections/{collection_name}', json_data=data)

    def get_collection(self, collection_name: str) -> Dict[str, Any]:
        """Get collection details."""
        return self._request('GET', f'/collections/{collection_name}')

    def delete_collection(self, collection_name: str) -> Dict[str, Any]:
        """Delete a collection."""
        return self._request('DELETE', f'/collections/{collection_name}')

    def update_collection(
        self,
        collection_name: str,
        optimizers_config: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        vector_params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Update collection configuration."""
        data = {}
        if optimizers_config:
            data["optimizers_config"] = optimizers_config
        if params:
            data["params"] = params
        if vector_params:
            data["vectors_config"] = vector_params

        return self._request('PATCH', f'/collections/{collection_name}', json_data=data)

    def upsert(
        self,
        collection_name: str,
        points: List[Dict[str, Any]],
        wait: bool = True
    ) -> Dict[str, Any]:
        """Insert or update points in a collection."""
        data = {
            "points": points,
            "wait": wait
        }
        return self._request('PUT', f'/collections/{collection_name}/points', json_data=data)

    def insert(
        self,
        collection_name: str,
        points: List[Dict[str, Any]],
        wait: bool = True
    ) -> Dict[str, Any]:
        """Insert points in a collection."""
        data = {
            "points": points,
            "wait": wait
        }
        return self._request('PUT', f'/collections/{collection_name}/points', json_data=data)

    def get_points(
        self,
        collection_name: str,
        ids: Optional[List[int]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        with_payload: Union[bool, List[str]] = True,
        with_vector: bool = False
    ) -> Dict[str, Any]:
        """Get points from a collection."""
        params = {}
        if ids is not None:
            params['ids'] = ids
        if limit:
            params['limit'] = limit
        if offset:
            params['offset'] = offset
        params['with_payload'] = with_payload
        params['with_vector'] = with_vector

        return self._request('POST', f'/collections/{collection_name}/points/scroll', json_data=params)

    def get_point(
        self,
        collection_name: str,
        point_id: int,
        with_payload: Union[bool, List[str]] = True,
        with_vector: bool = False
    ) -> Dict[str, Any]:
        """Get a specific point."""
        params = {
            "with_payload": with_payload,
            "with_vector": with_vector
        }
        return self._request('GET', f'/collections/{collection_name}/points/{point_id}', params=params)

    def delete_points(
        self,
        collection_name: str,
        points: Optional[List[int]] = None,
        filter: Optional[Dict[str, Any]] = None,
        wait: bool = True
    ) -> Dict[str, Any]:
        """Delete points from a collection."""
        data = {
            "wait": wait
        }
        if points:
            data["points"] = points
        if filter:
            data["filter"] = filter

        return self._request('POST', f'/collections/{collection_name}/points/delete', json_data=data)

    def update_vectors(
        self,
        collection_name: str,
        points: List[Dict[str, Any]],
        wait: bool = True
    ) -> Dict[str, Any]:
        """Update vectors for points."""
        data = {
            "points": points,
            "wait": wait
        }
        return self._request('PUT', f'/collections/{collection_name}/points/vectors', json_data=data)

    def delete_vectors(
        self,
        collection_name: str,
        points: List[Dict[str, Any]],
        wait: bool = True
    ) -> Dict[str, Any]:
        """Delete vectors from points."""
        data = {
            "points": points,
            "wait": wait
        }
        return self._request('PUT', f'/collections/{collection_name}/points/vectors/delete', json_data=data)

    def update_payload(
        self,
        collection_name: str,
        payload: Dict[str, Any],
        points: Optional[List[int]] = None,
        filter: Optional[Dict[str, Any]] = None,
        wait: bool = True
    ) -> Dict[str, Any]:
        """Update payload for points."""
        data = {
            "payload": payload,
            "wait": wait
        }
        if points:
            data["points"] = points
        if filter:
            data["filter"] = filter

        return self._request('POST', f'/collections/{collection_name}/points/payload', json_data=data)

    def delete_payload(
        self,
        collection_name: str,
        keys: List[str],
        points: Optional[List[int]] = None,
        filter: Optional[Dict[str, Any]] = None,
        wait: bool = True
    ) -> Dict[str, Any]:
        """Delete payload keys from points."""
        data = {
            "keys": keys,
            "wait": wait
        }
        if points:
            data["points"] = points
        if filter:
            data["filter"] = filter

        return self._request('POST', f'/collections/{collection_name}/points/payload/delete', json_data=data)

    def clear_payload(
        self,
        collection_name: str,
        points: Optional[List[int]] = None,
        filter: Optional[Dict[str, Any]] = None,
        wait: bool = True
    ) -> Dict[str, Any]:
        """Clear all payload from points."""
        data = {
            "wait": wait
        }
        if points:
            data["points"] = points
        if filter:
            data["filter"] = filter

        return self._request('POST', f'/collections/{collection_name}/points/payload/clear', json_data=data)

    def recommend(
        self,
        collection_name: str,
        positive: Optional[List[List[float]]] = None,
        negative: Optional[List[List[float]]] = None,
        limit: int = 10,
        with_payload: Union[bool, List[str]] = True,
        with_vector: bool = False,
        score_threshold: Optional[float] = None,
        filter: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Search for similar points using vector recommendations."""
        data = {
            "limit": limit,
            "with_payload": with_payload,
            "with_vector": with_vector
        }

        if positive:
            data["positive"] = positive
        if negative:
            data["negative"] = negative
        if score_threshold:
            data["score_threshold"] = score_threshold
        if filter:
            data["filter"] = filter

        return self._request('POST', f'/collections/{collection_name}/points/recommend', json_data=data)

    def search(
        self,
        collection_name: str,
        query_vector: List[float],
        limit: int = 10,
        with_payload: Union[bool, List[str]] = True,
        with_vector: bool = False,
        score_threshold: Optional[float] = None,
        vector_name: Optional[str] = None,
        filter: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Search for similar points using query vector."""
        data = {
            "vector": query_vector,
            "limit": limit,
            "with_payload": with_payload,
            "with_vector": with_vector
        }

        if score_threshold:
            data["score_threshold"] = score_threshold
        if vector_name:
            data["vector_name"] = vector_name
        if filter:
            data["filter"] = filter

        return self._request('POST', f'/collections/{collection_name}/points/search', json_data=data)

    def search_batch(
        self,
        collection_name: str,
        search_requests: List[Dict[str, Any]],
        wait: bool = True
    ) -> Dict[str, Any]:
        """Perform multiple search requests in a batch."""
        data = {
            "searches": search_requests,
            "wait": wait
        }
        return self._request('POST', f'/collections/{collection_name}/points/search/batch', json_data=data)

    def scroll(
        self,
        collection_name: str,
        limit: int = 10,
        offset: Optional[int] = None,
        with_payload: Union[bool, List[str]] = True,
        with_vector: bool = False,
        filter: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Scroll through all points in a collection."""
        data = {
            "limit": limit,
            "with_payload": with_payload,
            "with_vector": with_vector
        }

        if offset is not None:
            data["offset"] = offset
        if filter:
            data["filter"] = filter

        return self._request('POST', f'/collections/{collection_name}/points/scroll', json_data=data)

    def count(
        self,
        collection_name: str,
        exact: bool = True,
        filter: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Count points in a collection."""
        params = {"exact": exact}
        if filter:
            params["filter"] = filter

        return self._request('GET', f'/collections/{collection_name}/points/count', params=params)

    def recreate_collection(
        self,
        collection_name: str,
        vector_size: int,
        distance: str = "Cosine",
        hnsw_config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Delete and recreate a collection."""
        self.delete_collection(collection_name)

        vectors_config = {
            "size": vector_size,
            "distance": distance
        }

        data = {
            "vectors": vectors_config
        }

        if hnsw_config:
            data["hnsw_config"] = hnsw_config

        return self._request('PUT', f'/collections/{collection_name}', json_data=data)

    def create_index(
        self,
        collection_name: str,
        field_name: str,
        field_schema: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a payload index for filtering."""
        data = {
            "field_name": field_name,
            "field_schema": field_schema
        }
        return self._request('PUT', f'/collections/{collection_name}/index', json_data=data)

    def delete_index(
        self,
        collection_name: str,
        field_name: str
    ) -> Dict[str, Any]:
        """Delete a payload index."""
        return self._request('DELETE', f'/collections/{collection_name}/index/{field_name}')

    def get_cluster_info(self) -> Dict[str, Any]:
        """Get cluster information."""
        return self._request('GET', '/')

    def lock_collection(self, collection_name: str, reason: Optional[str] = None) -> Dict[str, Any]:
        """Lock a collection for maintenance."""
        data = {}
        if reason:
            data["reason"] = reason

        return self._request('POST', f'/collections/{collection_name}/locks', json_data=data)

    def unlock_collection(self, collection_name: str) -> Dict[str, Any]:
        """Unlock a locked collection."""
        return self._request('DELETE', f'/collections/{collection_name}/locks')