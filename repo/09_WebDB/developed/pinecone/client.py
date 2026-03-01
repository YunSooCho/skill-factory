"""
Pinecone Vector Database API Client

This module provides a Python client for interacting with Pinecone's vector database.
"""

import requests
from typing import Dict, List, Optional, Any, Union, Tuple
import json
import numpy as np
from datetime import datetime


class PineconeClient:
    """
    Client for Pinecone Vector Database.

    Pinecone provides:
    - High-performance vector similarity search
    - Efficient storage and retrieval of vector embeddings
    - Real-time indexing and query
    - Scalable infrastructure
    """

    def __init__(
        self,
        api_key: str,
        environment: str = "us-west1-gcp",
        project_id: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 30
    ):
        """
        Initialize the Pinecone client.

        Args:
            api_key: Pinecone API key
            environment: Pinecone environment (e.g., 'us-west1-gcp', 'us-east1-gcp')
            project_id: Optional project ID
            base_url: Optional custom base URL
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.environment = environment
        self.project_id = project_id
        self.timeout = timeout

        if base_url:
            self.base_url = base_url.rstrip('/')
        else:
            self.base_url = f"https://controller.{environment}.pinecone.io"

        self.session = requests.Session()
        self.session.headers.update({
            'Api-Key': api_key,
            'Content-Type': 'application/json'
        })

    def _request(self, method: str, endpoint: str, params=None, data=None, json_data=None) -> Dict[str, Any]:
        """Make an authenticated request to the API."""
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(
            method,
            url,
            params=params,
            data=data,
            json=json_data,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def create_index(
        self,
        name: str,
        dimension: int,
        metric: str = "cosine",
        pods: Optional[int] = None,
        replicas: Optional[int] = None,
        pod_type: Optional[str] = None,
        metadata_config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a new vector index.

        Args:
            name: Index name
            dimension: Vector dimension
            metric: Distance metric ('cosine', 'euclidean', 'dotproduct')
            pods: Number of pods (for pod-based indexes)
            replicas: Number of replicas
            pod_type: Type of pods (e.g., 'p1.x1')
            metadata_config: Metadata filtering configuration

        Returns:
            Index creation response
        """
        data = {
            'name': name,
            'dimension': dimension,
            'metric': metric
        }

        if pods is not None:
            data['pods'] = pods
        if replicas is not None:
            data['replicas'] = replicas
        if pod_type is not None:
            data['pod_type'] = pod_type
        if metadata_config is not None:
            data['metadata_config'] = metadata_config

        return self._request('POST', '/databases', json_data=data)

    def list_indexes(self) -> List[Dict[str, Any]]:
        """List all indexes."""
        response = self._request('GET', '/databases')
        return response.get('databases', [])

    def describe_index(self, index_name: str) -> Dict[str, Any]:
        """Get details about an index."""
        return self._request('GET', f'/databases/{index_name}')

    def delete_index(self, index_name: str) -> Dict[str, Any]:
        """Delete an index."""
        return self._request('DELETE', f'/databases/{index_name}')

    def get_index_stats(self, index_name: str) -> Dict[str, Any]:
        """Get statistics for an index."""
        return self._request('GET', f'/databases/{index_name}/stats')

    def upsert_vectors(
        self,
        index_name: str,
        vectors: List[Dict[str, Union[str, List[float], Dict[str, Any]]]],
        namespace: str = "",
        batch_size: int = 100
    ) -> Dict[str, Any]:
        """
        Upsert vectors into an index.

        Args:
            index_name: Name of the index
            vectors: List of vectors with structure:
                [{'id': 'vec1', 'values': [0.1, 0.2, ...], 'metadata': {...}}, ...]
            namespace: Namespace for the vectors
            batch_size: Number of vectors per batch

        Returns:
            Upsert response
        """
        url = f"https://{index_name}-{self.environment}.pinecone.io/vectors/upsert"

        upserted = 0
        total = len(vectors)

        for i in range(0, total, batch_size):
            batch = vectors[i:i + batch_size]
            data = {
                'vectors': batch,
                'namespace': namespace
            }

            response = self.session.post(
                url,
                headers=self.session.headers,
                json=data,
                timeout=self.timeout
            )
            response.raise_for_status()
            result = response.json()
            upserted += result.get('upsertedCount', 0)

        return {'upsertedCount': upserted}

    def query_vectors(
        self,
        index_name: str,
        vector: List[float],
        top_k: int = 10,
        namespace: str = "",
        include_metadata: bool = True,
        include_values: bool = False,
        filter: Optional[Dict[str, Any]] = None,
        sparse_vector: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Query vectors for similarity search.

        Args:
            index_name: Name of the index
            vector: Query vector
            top_k: Number of results to return
            namespace: Namespace to search
            include_metadata: Include metadata in results
            include_values: Include vector values in results
            filter: Metadata filter criteria
            sparse_vector: Optional sparse vector for hybrid search

        Returns:
            Query results with matched vectors
        """
        url = f"https://{index_name}-{self.environment}.pinecone.io/query"

        data = {
            'vector': vector,
            'topK': top_k,
            'namespace': namespace,
            'includeMetadata': include_metadata,
            'includeValues': include_values
        }

        if filter is not None:
            data['filter'] = filter
        if sparse_vector is not None:
            data['sparse_vector'] = sparse_vector

        response = self.session.post(
            url,
            headers=self.session.headers,
            json=data,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def delete_vectors(
        self,
        index_name: str,
        ids: Optional[List[str]] = None,
        delete_all: bool = False,
        namespace: str = "",
        filter: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Delete vectors from an index.

        Args:
            index_name: Name of the index
            ids: List of vector IDs to delete
            delete_all: Delete all vectors in namespace
            namespace: Namespace to delete from
            filter: Metadata filter for deletion

        Returns:
            Deletion response
        """
        url = f"https://{index_name}-{self.environment}.pinecone.io/vectors/delete"

        data = {'namespace': namespace}
        if ids is not None:
            data['ids'] = ids
        if delete_all:
            data['deleteAll'] = delete_all
        if filter is not None:
            data['filter'] = filter

        response = self.session.post(
            url,
            headers=self.session.headers,
            json=data,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def fetch_vectors(
        self,
        index_name: str,
        ids: List[str],
        namespace: str = ""
    ) -> Dict[str, Any]:
        """
        Fetch vectors by ID.

        Args:
            index_name: Name of the index
            ids: List of vector IDs to fetch
            namespace: Namespace to fetch from

        Returns:
            Fetched vectors
        """
        url = f"https://{index_name}-{self.environment}.pinecone.io/vectors/fetch"

        params = {'ids': ','.join(ids)}
        if namespace:
            params['namespace'] = namespace

        response = self.session.get(
            url,
            headers=self.session.headers,
            params=params,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def update_vector(
        self,
        index_name: str,
        id: str,
        values: Optional[List[float]] = None,
        set_metadata: Optional[Dict[str, Any]] = None,
        namespace: str = ""
    ) -> Dict[str, Any]:
        """
        Update a vector.

        Args:
            index_name: Name of the index
            id: Vector ID
            values: New vector values
            set_metadata: Metadata to set/update
            namespace: Namespace of the vector

        Returns:
            Update response
        """
        url = f"https://{index_name}-{self.environment}.pinecone.io/vectors/update"

        data = {
            'id': id,
            'namespace': namespace
        }

        if values is not None:
            data['values'] = values
        if set_metadata is not None:
            data['setMetadata'] = set_metadata

        response = self.session.post(
            url,
            headers=self.session.headers,
            json=data,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def list_collections(self) -> List[Dict[str, Any]]:
        """List all collections."""
        return self._request('GET', '/collections')

    def create_collection(self, name: str, source: str) -> Dict[str, Any]:
        """
        Create a collection from an index.

        Args:
            name: Collection name
            source: Source index name

        Returns:
            Collection creation response
        """
        data = {
            'name': name,
            'source': source
        }
        return self._request('POST', '/collections', json_data=data)

    def describe_collection(self, name: str) -> Dict[str, Any]:
        """Get details about a collection."""
        return self._request('GET', f'/collections/{name}')

    def delete_collection(self, name: str) -> Dict[str, Any]:
        """Delete a collection."""
        return self._request('DELETE', f'/collections/{name}')

    def create_index_from_collection(self, name: str, collection_name: str, timeout: int = None) -> Dict[str, Any]:
        """
        Create an index from a collection.

        Args:
            name: New index name
            collection_name: Collection name
            timeout: Creation timeout in seconds

        Returns:
            Index creation response
        """
        data = {
            'name': name,
            'collection_name': collection_name
        }
        return self._request('POST', '/indexes', json_data=data)

    def list_indexes_with_status(self) -> List[Dict[str, Any]]:
        """
        List indexes with their status.

        Returns:
            List of indexes with status, dimension, metric, etc.
        """
        indexes = self.list_indexes()
        results = []

        for index in indexes:
            try:
                details = self.describe_index(index['name'])
                result = {
                    'name': index['name'],
                    'dimension': index.get('dimension'),
                    'metric': index.get('metric'),
                    'status': details.get('status', {}).get('ready', False),
                    'replicas': index.get('replicas'),
                    'pods': index.get('pods'),
                    'pod_type': index.get('pod_type')
                }
                results.append(result)
            except Exception as e:
                results.append({
                    'name': index['name'],
                    'error': str(e)
                })

        return results