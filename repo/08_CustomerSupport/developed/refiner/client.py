"""
Refiner Client
AIベースのコンテンツ最適化APIクライアント
"""

import requests
from typing import Optional, Dict, List, Any


class RefinerClient:
    """
    Refiner APIクライアント

    AIベースのコンテンツ最適化、パラフレージング、文書改善のためのクライアント
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.refiner.ai/v1",
        timeout: int = 30
    ):
        """
        Refiner クライアントの初期化

        Args:
            api_key: Refiner API キー
            base_url：APIベースURL
            timeout：リクエストタイムアウト（秒）
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
        APIリクエストの送信

        Args:
            method: HTTP メソッド
            endpoint: API エンドポイント
            data: 要求本文データ
            params: URL パラメータ

        Returns:
            API応答データ

        Raises:
            requests.RequestException: API リクエストに失敗しました
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
        テキストの最適化(書き換え)

        Args:
            text: 最適化するテキスト
            tone: トーン (professional, casual, formal, friendly)
            length: 長さ (shorter, same, longer)
            goal：最適化目標（クラリティ、説得力、明確性など）

        Returns:
            最適化されたテキストとメタデータ
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
        テキストパラフレージング(再書き込み)

        Args:
            text: パラフレージングするテキスト
            style: スタイル (standard, academic, creative, business)
            variations: 変形数

        Returns:
            パラフレージングされたテキストのリスト
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
        テキストの要約

        Args:
            text: 要約するテキスト
            max_length：最大長（文字数）
            format: 要約フォーマット (paragraph, bullet, sentence)

        Returns:
            要約されたテキスト
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
        文法とスペルチェック

        Args:
            text: 検査するテキスト
            language: 言語コード (en, ja, ja, zh)

        Returns:
            文法エラーと修正提案
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
        テキスト拡張(コンテンツの追加)

        Args:
            text: 拡張するテキスト
            context: 追加のコンテキスト
            length：追加する長さ（文字数）

        Returns:
            拡張テキスト
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
        テキスト翻訳

        Args:
            text: 翻訳するテキスト
            target_language：ターゲット言語コード（en、ja、ja、zh、fr、de、es）
            source_language：元の言語コード（選択 - 自動検出）

        Returns:
            翻訳されたテキスト
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
        感情分析

        Args:
            text: 分析するテキスト

        Returns:
            感性分析結果（肯定/否定/中立、スコア）
        """
        data = {'text': text}

        return self._request('POST', '/sentiment/detect', data=data)

    def extract_keywords(
        self,
        text: str,
        max_keywords: int = 10
    ) -> Dict[str, Any]:
        """
        キーワード抽出

        Args:
            text: キーワード抽出するテキスト
            max_keywords：最大キーワード数

        Returns:
            抽出されたキーワードのリストとスコア
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
        タイトルの作成

        Args:
            text: テキスト本文
            count：提案数
            style: スタイル (engaging, professional, creative, concise)

        Returns:
            生成された提案タイトルのリスト
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
        読みやすさの改善

        Args:
            text: 改善するテキスト
            target_audience：ターゲットオーディエンス（general、academic、business、children）
            reading_level：読み取りレベル（easy、medium、advanced）

        Returns:
            改善されたテキストと元のスコアの比較
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
        バッチ処理

        Args:
            texts: 処理するテキストのリスト
            operation: ジョブタイプ (refine, paraphrase, summarize, grammar)
            **kwargs：タスク別の追加パラメータ

        Returns:
            バッチ処理結果一覧
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
        使用統計の照会

        Args:
            start_date：開始日（YYYY-MM-DD）
            end_date: 終了日 (YYYY-MM-DD)

        Returns:
            使用統計
        """
        params = {}
        if start_date:
            params['startDate'] = start_date
        if end_date:
            params['endDate'] = end_date

        return self._request('GET', '/stats', params=params)

    def close(self):
        """セッション終了"""
        self.session.close()