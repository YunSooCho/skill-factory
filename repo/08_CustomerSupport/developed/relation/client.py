"""
Relation Client
고객 관계 관리 API 클라이언트
"""

import requests
from typing import Optional, Dict, List, Any
from datetime import datetime


class RelationClient:
    """
    Relation API 클라이언트

    고객 관계 관리, 세그먼트, 캠페인 관리를 위한 클라이언트
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.relation.io/v1",
        timeout: int = 30
    ):
        """
        Relation 클라이언트 초기화

        Args:
            api_key: Relation API 키
            base_url: API 기본 URL
            timeout: 요청 타임아웃 (초)
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        API 요청 전송

        Args:
            method: HTTP 메서드
            endpoint: API 엔드포인트
            data: 요청 본문 데이터
            params: URL 파라미터

        Returns:
            API 응답 데이터

        Raises:
            requests.RequestException: API 요청 실패
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.request(
            method=method,
            url=url,
            json=data,
            params=params,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def create_contact(
        self,
        email: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        phone: Optional[str] = None,
        company: Optional[str] = None,
        title: Optional[str] = None,
        tags: Optional[List[str]] = None,
        attributes: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        새 연락처 생성

        Args:
            email: 이메일 (필수)
            first_name: 이름
            last_name: 성
            phone: 전화번호
            company: 회사
            title: 직함
            tags: 태그 목록
            attributes: 추가 속성

        Returns:
            생성된 연락처 정보
        """
        data = {'email': email}

        if first_name:
            data['firstName'] = first_name
        if last_name:
            data['lastName'] = last_name
        if phone:
            data['phone'] = phone
        if company:
            data['company'] = company
        if title:
            data['title'] = title
        if tags:
            data['tags'] = tags
        if attributes:
            data['attributes'] = attributes

        return self._request('POST', '/contacts', data=data)

    def get_contact(self, contact_id: str) -> Dict[str, Any]:
        """
        연락처 조회

        Args:
            contact_id: 연락처 ID

        Returns:
            연락처 정보
        """
        return self._request('GET', f'/contacts/{contact_id}')

    def update_contact(
        self,
        contact_id: str,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        phone: Optional[str] = None,
        company: Optional[str] = None,
        title: Optional[str] = None,
        add_tags: Optional[List[str]] = None,
        remove_tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        연락처 업데이트

        Args:
            contact_id: 연락처 ID
            email: 새 이메일
            first_name: 새 이름
            last_name: 새 성
            phone: 새 전화번호
            company: 새 회사
            title: 새 직함
            add_tags: 추가할 태그
            remove_tags: 제거할 태그

        Returns:
            업데이트된 연락처 정보
        """
        data = {}
        if email:
            data['email'] = email
        if first_name:
            data['firstName'] = first_name
        if last_name:
            data['lastName'] = last_name
        if phone:
            data['phone'] = phone
        if company:
            data['company'] = company
        if title:
            data['title'] = title
        if add_tags:
            data['addTags'] = add_tags
        if remove_tags:
            data['removeTags'] = remove_tags

        return self._request('PUT', f'/contacts/{contact_id}', data=data)

    def list_contacts(
        self,
        tags: Optional[List[str]] = None,
        created_after: Optional[str] = None,
        created_before: Optional[str] = None,
        search: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        연락처 목록 조회

        Args:
            tags: 태그 필터
            created_after: 생성일 이후 (YYYY-MM-DD)
            created_before: 생성일 이전 (YYYY-MM-DD)
            search: 검색어
            limit: 반환할 항목 수
            offset: 오프셋

        Returns:
            연락처 목록
        """
        params = {'limit': limit, 'offset': offset}
        if tags:
            params['tags'] = tags
        if created_after:
            params['createdAfter'] = created_after
        if created_before:
            params['createdBefore'] = created_before
        if search:
            params['search'] = search

        response = self._request('GET', '/contacts', params=params)
        return response.get('contacts', [])

    def delete_contact(self, contact_id: str) -> Dict[str, Any]:
        """
        연락처 삭제

        Args:
            contact_id: 연락처 ID

        Returns:
            삭제 결과
        """
        return self._request('DELETE', f'/contacts/{contact_id}')

    def create_segment(
        self,
        name: str,
        description: Optional[str] = None,
        criteria: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        새 세그먼트 생성

        Args:
            name: 세그먼트 이름
            description: 설명
            criteria: 필터링 기준

        Returns:
            생성된 세그먼트 정보
        """
        data = {'name': name}

        if description:
            data['description'] = description
        if criteria:
            data['criteria'] = criteria

        return self._request('POST', '/segments', data=data)

    def get_segment(self, segment_id: str) -> Dict[str, Any]:
        """
        세그먼트 조회

        Args:
            segment_id: 세그먼트 ID

        Returns:
            세그먼트 정보
        """
        return self._request('GET', f'/segments/{segment_id}')

    def list_segments(
        self,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        세그먼트 목록 조회

        Args:
            limit: 반환할 항목 수
            offset: 오프셋

        Returns:
            세그먼트 목록
        """
        params = {'limit': limit, 'offset': offset}
        response = self._request('GET', '/segments', params=params)
        return response.get('segments', [])

    def get_segment_contacts(
        self,
        segment_id: str,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        세그먼트에 속한 연락처 조회

        Args:
            segment_id: 세그먼트 ID
            limit: 반환할 항목 수
            offset: 오프셋

        Returns:
            연락처 목록
        """
        params = {'limit': limit, 'offset': offset}
        response = self._request('GET', f'/segments/{segment_id}/contacts', params=params)
        return response.get('contacts', [])

    def create_note(
        self,
        contact_id: str,
        content: str,
        author_id: Optional[str] = None,
        note_type: str = "general"
    ) -> Dict[str, Any]:
        """
        노트 생성

        Args:
            contact_id: 연락처 ID
            content: 노트 내용
            author_id: 작성자 ID
            note_type: 노트 타입 (general, meeting, call, email)

        Returns:
            생성된 노트 정보
        """
        data = {
            'contactId': contact_id,
            'content': content,
            'noteType': note_type
        }

        if author_id:
            data['authorId'] = author_id

        return self._request('POST', '/notes', data=data)

    def get_notes(
        self,
        contact_id: str,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        연락처 노트 목록 조회

        Args:
            contact_id: 연락처 ID
            limit: 반환할 항목 수
            offset: 오프셋

        Returns:
            노트 목록
        """
        params = {'limit': limit, 'offset': offset}
        response = self._request('GET', f'/contacts/{contact_id}/notes', params=params)
        return response.get('notes', [])

    def create_task(
        self,
        contact_id: str,
        title: str,
        description: Optional[str] = None,
        due_date: Optional[str] = None,
        assignee_id: Optional[str] = None,
        priority: str = "medium"
    ) -> Dict[str, Any]:
        """
        태스크 생성

        Args:
            contact_id: 연락처 ID
            title: 제목
            description: 설명
            due_date: 마감일 (YYYY-MM-DD)
            assignee_id: 담당자 ID
            priority: 우선순위 (low, medium, high)

        Returns:
            생성된 태스크 정보
        """
        data = {
            'contactId': contact_id,
            'title': title,
            'priority': priority
        }

        if description:
            data['description'] = description
        if due_date:
            data['dueDate'] = due_date
        if assignee_id:
            data['assigneeId'] = assignee_id

        return self._request('POST', '/tasks', data=data)

    def list_tasks(
        self,
        contact_id: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        태스크 목록 조회

        Args:
            contact_id: 연락처 ID 필터
            status: 상태 필터 (pending, in_progress, completed)
            priority: 우선순위 필터
            limit: 반환할 항목 수
            offset: 오프셋

        Returns:
            태스크 목록
        """
        params = {'limit': limit, 'offset': offset}
        if contact_id:
            params['contactId'] = contact_id
        if status:
            params['status'] = status
        if priority:
            params['priority'] = priority

        response = self._request('GET', '/tasks', params=params)
        return response.get('tasks', [])

    def track_event(
        self,
        contact_id: str,
        event_name: str,
        properties: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        이벤트 추적

        Args:
            contact_id: 연락처 ID
            event_name: 이벤트 이름
            properties: 이벤트 속성

        Returns:
            이벤트 추적 결과
        """
        data = {
            'contactId': contact_id,
            'eventName': event_name
        }

        if properties:
            data['properties'] = properties

        return self._request('POST', '/events/track', data=data)

    def get_contact_events(
        self,
        contact_id: str,
        event_type: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        연락처 이벤트 기록 조회

        Args:
            contact_id: 연락처 ID
            event_type: 이벤트 타입 필터
            limit: 반환할 항목 수
            offset: 오프셋

        Returns:
            이벤트 목록
        """
        params = {'limit': limit, 'offset': offset}
        if event_type:
            params['eventType'] = event_type

        response = self._request('GET', f'/contacts/{contact_id}/events', params=params)
        return response.get('events', [])

    def close(self):
        """세션 종료"""
        self.session.close()