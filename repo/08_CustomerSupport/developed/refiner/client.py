"""
Refiner Client
AI 기반 콘텐츠 최적화 API 클라이언트
"""

import requests
from typing import Optional, Dict, List, Any


class RefinerClient:
    """
    Refiner API 클라이언트

    AI 기반 콘텐츠 최적화, 파라프레이징, 문서 개선을 위한 클라이언트
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.refiner.ai/v1",
        timeout: int = 30
    ):
        """
        Refiner 클라이언트 초기화

        Args:
            api_key: Refiner API 키
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

    def refine_text(
        self,
        text: str,
        tone: str = "professional",
        length: str = "same",
        goal: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        텍스트 최적화 (글 고치기)

        Args:
            text: 최적화할 텍스트
            tone: 톤 (professional, casual, formal, friendly)
            length: 길이 (shorter, same, longer)
            goal: 최적화 목표 (클라리티, 설득력, 명확성 등)

        Returns:
            최적화된 텍스트 및 메타데이터
        """
        data = {
            'text': text,
            'tone': tone,
            'length': length
        }

        if goal:
            data['goal'] = goal

        return self._request('POST', '/refine', data=data)

    def paraphrase(
        self,
        text: str,
        style: str = "standard",
        variations: int = 3
    ) -> Dict[str, Any]:
        """
        텍스트 파라프레이징 (다시 쓰기)

        Args:
            text: 파라프레이징할 텍스트
            style: 스타일 (standard, academic, creative, business)
            variations: 변형 개수

        Returns:
            파라프레이징된 텍스트 목록
        """
        data = {
            'text': text,
            'style': style,
            'variations': variations
        }

        return self._request('POST', '/paraphrase', data=data)

    def summarize(
        self,
        text: str,
        max_length: Optional[int] = None,
        format: str = "paragraph"
    ) -> Dict[str, Any]:
        """
        텍스트 요약

        Args:
            text: 요약할 텍스트
            max_length: 최대 길이 (문자 수)
            format: 요약 포맷 (paragraph, bullet, sentence)

        Returns:
            요약된 텍스트
        """
        data = {
            'text': text,
            'format': format
        }

        if max_length:
            data['maxLength'] = max_length

        return self._request('POST', '/summarize', data=data)

    def check_grammar(
        self,
        text: str,
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        문법 및 맞춤법 검사

        Args:
            text: 검사할 텍스트
            language: 언어 코드 (en, ko, ja, zh)

        Returns:
            문법 오류 및 수정 제안
        """
        data = {
            'text': text,
            'language': language
        }

        return self._request('POST', '/grammar/check', data=data)

    def expand_text(
        self,
        text: str,
        context: Optional[str] = None,
        length: int = 200
    ) -> Dict[str, Any]:
        """
        텍스트 확장 (내용 추가)

        Args:
            text: 확장할 텍스트
            context: 추가 컨텍스트
            length: 추가할 길이 (문자 수)

        Returns:
            확장된 텍스트
        """
        data = {
            'text': text,
            'length': length
        }

        if context:
            data['context'] = context

        return self._request('POST', '/expand', data=data)

    def translate(
        self,
        text: str,
        target_language: str,
        source_language: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        텍스트 번역

        Args:
            text: 번역할 텍스트
            target_language: 대상 언어 코드 (en, ko, ja, zh, fr, de, es)
            source_language: 원본 언어 코드 (선택 - 자동 감지)

        Returns:
            번역된 텍스트
        """
        data = {
            'text': text,
            'targetLanguage': target_language
        }

        if source_language:
            data['sourceLanguage'] = source_language

        return self._request('POST', '/translate', data=data)

    def detect_sentiment(
        self,
        text: str
    ) -> Dict[str, Any]:
        """
        감성 분석

        Args:
            text: 분석할 텍스트

        Returns:
            감성 분석 결과 (긍정/부정/중립, 점수)
        """
        data = {'text': text}

        return self._request('POST', '/sentiment/detect', data=data)

    def extract_keywords(
        self,
        text: str,
        max_keywords: int = 10
    ) -> Dict[str, Any]:
        """
        키워드 추출

        Args:
            text: 키워드 추출할 텍스트
            max_keywords: 최대 키워드 개수

        Returns:
            추출된 키워드 목록 및 점수
        """
        data = {
            'text': text,
            'maxKeywords': max_keywords
        }

        return self._request('POST', '/keywords/extract', data=data)

    def generate_title(
        self,
        text: str,
        count: int = 5,
        style: str = "engaging"
    ) -> Dict[str, Any]:
        """
        제목 생성

        Args:
            text: 텍스트 본문
            count: 제안 개수
            style: 스타일 (engaging, professional, creative, concise)

        Returns:
            생성된 제안 제목 목록
        """
        data = {
            'text': text,
            'count': count,
            'style': style
        }

        return self._request('POST', '/titles/generate', data=data)

    def improve_readability(
        self,
        text: str,
        target_audience: str = "general",
        reading_level: str = "medium"
    ) -> Dict[str, Any]:
        """
        가독성 개선

        Args:
            text: 개선할 텍스트
            target_audience: 타겟 오디언스 (general, academic, business, children)
            reading_level: 읽기 수준 (easy, medium, advanced)

        Returns:
            개선된 텍스트 및 원본 점수 비교
        """
        data = {
            'text': text,
            'targetAudience': target_audience,
            'readingLevel': reading_level
        }

        return self._request('POST', '/readability/improve', data=data)

    def batch_refine(
        self,
        texts: List[str],
        operation: str = "refine",
        **kwargs
    ) -> Dict[str, Any]:
        """
        배치 처리

        Args:
            texts: 처리할 텍스트 목록
            operation: 작업 유형 (refine, paraphrase, summarize, grammar)
            **kwargs: 작업별 추가 파라미터

        Returns:
            배치 처리 결과 목록
        """
        data = {
            'texts': texts,
            'operation': operation
        }

        data.update(kwargs)

        return self._request('POST', '/batch', data=data)

    def get_usage_stats(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        사용 통계 조회

        Args:
            start_date: 시작 날짜 (YYYY-MM-DD)
            end_date: 종료 날짜 (YYYY-MM-DD)

        Returns:
            사용 통계
        """
        params = {}
        if start_date:
            params['startDate'] = start_date
        if end_date:
            params['endDate'] = end_date

        return self._request('GET', '/stats', params=params)

    def close(self):
        """세션 종료"""
        self.session.close()