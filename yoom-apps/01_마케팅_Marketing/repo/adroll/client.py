"""
AdRoll API Client
Documentation: https://developers.adroll.com/docs/
"""

import logging
import requests
from typing import List, Optional, Dict, Any
from .models import Segment, SegmentCreateRequest

logger = logging.getLogger(__name__)


class AdRollClient:
    """
    AdRoll API Client for Yoom Integration

    API Actions:
    - List Segments
    - Create Segment
    """

    BASE_URL = "https://services.adroll.com/api/v1"

    def __init__(self, api_key: str, advertiser_eid: Optional[str] = None):
        """
        Initialize AdRoll Client

        Args:
            api_key: AdRoll API key
            advertiser_eid: Advertiser Entity ID (optional, can be specified per request)
        """
        self.api_key = api_key
        self.default_advertiser_eid = advertiser_eid
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make HTTP request to AdRoll API

        Args:
            method: HTTP method
            endpoint: API endpoint
            **kwargs: Additional arguments for requests

        Returns:
            JSON response data

        Raises:
            requests.RequestException: If request fails
        """
        url = f"{self.BASE_URL}/{endpoint}"
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"AdRoll API Error: {e}")
            if hasattr(e, 'response') and e.response:
                logger.error(f"Response: {e.response.text}")
            raise

    # ========== SEGMENT OPERATIONS ==========

    def list_segments(
        self,
        advertiser_eid: Optional[str] = None,
        segment_type: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 100
    ) -> List[Segment]:
        """
        List Segments

        Args:
            advertiser_eid: Advertiser Entity ID (optional, uses default if not specified)
            segment_type: Filter by segment type ('rule', 'upload', 'api')
            status: Filter by status ('active', 'inactive')
            limit: Maximum number of segments to return

        Returns:
            List of Segment objects
        """
        eid = advertiser_eid or self.default_advertiser_eid
        if not eid:
            raise ValueError("advertiser_eid must be specified")

        params = {'advertiser': eid, 'limit': limit}
        if segment_type:
            params['type'] = segment_type
        if status:
            params['status'] = status

        result = self._request('GET', 'segments', params=params)
        segments = []

        for segment_data in result.get('results', {}).get('segments', []):
            segments.append(Segment(
                eid=segment_data.get('eid'),
                name=segment_data.get('name'),
                type=segment_data.get('type'),
                status=segment_data.get('status'),
                advertiser=segment_data.get('advertiser'),
                created_at=segment_data.get('created_at'),
                updated_at=segment_data.get('updated_at'),
                description=segment_data.get('description'),
                size=segment_data.get('size'),
                conversion=segment_data.get('conversion')
            ))

        return segments

    def create_segment(
        self,
        request: Optional[SegmentCreateRequest] = None,
        **kwargs
    ) -> Segment:
        """
        Create Segment

        Args:
            request: SegmentCreateRequest object (optional)
            **kwargs: Alternative way to pass parameters
                - name: Segement name
                - type: Segment type ('rule', 'upload', 'api')
                - description: Description (optional)
                - rules: Rules dictionary (optional)
                - advertiser_eid: Advertiser Entity ID (optional)

        Returns:
            Created Segment object
        """
        if request:
            data = request.to_dict()
        else:
            data = {
                'name': kwargs.get('name'),
                'type': kwargs.get('type')
            }
            if 'description' in kwargs:
                data['description'] = kwargs['description']
            if 'rules' in kwargs:
                data['rules'] = kwargs['rules']

        # Set advertiser if specified
        advertiser_eid = kwargs.get('advertiser_eid') or self.default_advertiser_eid
        if advertiser_eid:
            data['advertiser_eid'] = advertiser_eid

        result = self._request('POST', 'segments', json=data['segments'])

        segment_data = result.get('results', {}).get('segments', [{}])[0]
        return Segment(
            eid=segment_data.get('eid'),
            name=segment_data.get('name'),
            type=segment_data.get('type'),
            status=segment_data.get('status'),
            advertiser=segment_data.get('advertiser'),
            created_at=segment_data.get('created_at'),
            updated_at=segment_data.get('updated_at'),
            description=segment_data.get('description'),
            size=segment_data.get('size'),
            conversion=segment_data.get('conversion')
        )

    def get_segment(self, segment_eid: str) -> Segment:
        """
        Get Segment Details

        Args:
            segment_eid: Segment Entity ID

        Returns:
            Segment object
        """
        result = self._request('GET', f'segments/{segment_eid}')
        segment_data = result.get('results', {}).get('segments', [{}])[0]
        return Segment(
            eid=segment_data.get('eid'),
            name=segment_data.get('name'),
            type=segment_data.get('type'),
            status=segment_data.get('status'),
            advertiser=segment_data.get('advertiser'),
            created_at=segment_data.get('created_at'),
            updated_at=segment_data.get('updated_at'),
            description=segment_data.get('description'),
            size=segment_data.get('size'),
            conversion=segment_data.get('conversion')
        )

    def update_segment(
        self,
        segment_eid: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None
    ) -> Segment:
        """
        Update Segment

        Args:
            segment_eid: Segment Entity ID
            name: New segment name (optional)
            description: New description (optional)
            status: New status ('active', 'inactive', optional)

        Returns:
            Updated Segment object
        """
        data = {'segments': {}}
        if name:
            data['segments']['name'] = name
        if description:
            data['segments']['description'] = description
        if status:
            data['segments']['status'] = status

        result = self._request('PUT', f'segments/{segment_eid}', json=data)
        segment_data = result.get('results', {}).get('segments', [{}])[0]
        return Segment(
            eid=segment_data.get('eid'),
            name=segment_data.get('name'),
            type=segment_data.get('type'),
            status=segment_data.get('status'),
            advertiser=segment_data.get('advertiser'),
            created_at=segment_data.get('created_at'),
            updated_at=segment_data.get('updated_at'),
            description=segment_data.get('description'),
            size=segment_data.get('size'),
            conversion=segment_data.get('conversion')
        )

    def delete_segment(self, segment_eid: str) -> Dict[str, Any]:
        """
        Delete Segment

        Args:
            segment_eid: Segment Entity ID

        Returns:
            Deletion response
        """
        return self._request('DELETE', f'segments/{segment_eid}')

    # ========== UTILITY ==========

    def test_connection(self) -> bool:
        """
        Test API connection

        Returns:
            True if connection successful
        """
        try:
            if self.default_advertiser_eid:
                self.list_segments(limit=1)
            return True
        except Exception:
            return False