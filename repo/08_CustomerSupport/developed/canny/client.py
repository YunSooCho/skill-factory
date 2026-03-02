"""
Canny Client
フィードバックと機能リクエスト管理APIクライアント
"""

import requests
from typing import Optional, Dict, List, Any


class CannyClient:
    """
    Canny API クライアント

    ユーザーフィードバック、機能要求管理のためのクライアント
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://canny.io/api/v1",
        timeout: int = 30
    ):
        """
        Cannyクライアントの初期化

        Args:
            api_key: Canny API キー
            base_url：APIベースURL
            timeout：リクエストタイムアウト（秒）
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()

    def _request(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        APIリクエストの送信

        Args:
            endpoint: API エンドポイント
            data: 要求データ
            params: URL パラメータ

        Returns:
            API応答データ

        Raises:
            requests.RequestException: API リクエストに失敗しました
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        payload = {'apiKey': self.api_key}

        if data:
            payload.update(data)

        response = self.session.post(
            url,
            json=payload,
            params=params,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def create_post(
        self,
        title: str,
        description: str,
        author_id: str,
        board_id: str,
        category_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        新しいフィードバック/投稿の作成

        Args:
            title: タイトル
            description: 説明
            author_id：作成者ID
            board_id：ボードID
            category_id：カテゴリID
            タグ：タグリスト
            details: 追加の詳細

        Returns:
            生成された投稿情報
        """
        data = {
            'title': title,
            'details': description,
            'authorID': author_id,
            'boardID': board_id
        }

        if category_id:
            data['categoryID'] = category_id
        if tags:
            data['tags'] = tags
        if details:
            data['details'] = details

        return self._request('/posts/create', data=data)

    def get_post(self, post_id: str) -> Dict[str, Any]:
        """
        投稿を見る

        Args:
            post_id：投稿ID

        Returns:
            投稿情報
        """
        return self._request('/posts/retrieve', data={'id': post_id})

    def list_posts(
        self,
        board_id: Optional[str] = None,
        author_id: Optional[str] = None,
        limit: int = 50,
        skip: int = 0,
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        投稿リストを見る

        Args:
            board_id：ボードIDフィルタ
            author_id：作成者IDフィルタ
            limit: 返す項目の数
            skip: スキップするアイテム数
            status: ステータスフィルタ

        Returns:
            投稿リスト
        """
        data = {'limit': limit, 'skip': skip}

        if board_id:
            data['boardID'] = board_id
        if author_id:
            data['authorID'] = author_id
        if status:
            data['status'] = status

        response = self._request('/posts/list', data=data)
        return response.get('posts', [])

    def update_post(
        self,
        post_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        投稿の更新

        Args:
            post_id：投稿ID
            title: 新しいタイトル
            description: 新しい説明
            status: 新しい状態
            タグ：新しいタグリスト

        Returns:
            更新された投稿情報
        """
        data = {'id': post_id}

        if title:
            data['title'] = title
        if description:
            data['details'] = description
        if status:
            data['status'] = status
        if tags:
            data['tags'] = tags

        return self._request('/posts/update', data=data)

    def create_comment(
        self,
        post_id: str,
        author_id: str,
        content: str,
        parent_comment_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        コメントを生成

        Args:
            post_id：投稿ID
            author_id：作成者ID
            content：コメント内容
            parent_comment_id：親コメントID（大コメント用）

        Returns:
            生成されたコメント情報
        """
        data = {
            'postID': post_id,
            'authorID': author_id,
            'value': content
        }

        if parent_comment_id:
            data['parentID'] = parent_comment_id

        return self._request('/comments/create', data=data)

    def list_comments(
        self,
        post_id: str,
        limit: int = 50,
        skip: int = 0
    ) -> List[Dict[str, Any]]:
        """
        コメントリストを見る

        Args:
            post_id：投稿ID
            limit: 返す項目の数
            skip: スキップするアイテム数

        Returns:
            コメントリスト
        """
        data = {
            'postID': post_id,
            'limit': limit,
            'skip': skip
        }

        response = self._request('/comments/list', data=data)
        return response.get('comments', [])

    def create_vote(
        self,
        post_id: str,
        author_id: str,
        score: int = 1
    ) -> Dict[str, Any]:
        """
        投票の作成

        Args:
            post_id：投稿ID
            author_id：作成者ID
            score: 投票の重み

        Returns:
            投票情報
        """
        data = {
            'postID': post_id,
            'authorID': author_id,
            'score': score
        }

        return self._request('/votes/create', data=data)

    def delete_vote(
        self,
        post_id: str,
        author_id: str
    ) -> Dict[str, Any]:
        """
        投票の削除

        Args:
            post_id：投稿ID
            author_id：作成者ID

        Returns:
            削除結果
        """
        data = {
            'postID': post_id,
            'authorID': author_id
        }

        return self._request('/votes/delete', data=data)

    def create_user(
        self,
        name: str,
        email: str,
        avatar_url: Optional[str] = None,
        companies: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        ユーザーの作成

        Args:
            name: 名前
            email: メール
            avatar_url：アバターURL
            companies: 会社リスト

        Returns:
            生成されたユーザー情報
        """
        data = {
            'name': name,
            'email': email,
            'createIfNotExists': 'true'
        }

        if avatar_url:
            data['avatarURL'] = avatar_url
        if companies:
            data['companies'] = companies

        return self._request('/users/create', data=data)

    def get_user(self, user_id: str) -> Dict[str, Any]:
        """
        ユーザー検索

        Args:
            user_id：ユーザーID

        Returns:
            ユーザー情報
        """
        return self._request('/users/retrieve', data={'id': user_id})

    def list_boards(self) -> List[Dict[str, Any]]:
        """
        ボードリストの照会

        Returns:
            ボードリスト
        """
        response = self._request('/boards/list')
        return response.get('boards', [])

    def get_board(self, board_id: str) -> Dict[str, Any]:
        """
        ボード検索

        Args:
            board_id：ボードID

        Returns:
            ボード情報
        """
        return self._request('/boards/retrieve', data={'id': board_id})

    def create_status_change(
        self,
        post_id: str,
        user_id: str,
        status: str,
        comment: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        状態変更履歴の作成

        Args:
            post_id：投稿ID
            user_id：ユーザーID
            status: 新しい状態
            comment: 変更理由コメント

        Returns:
            状態変更情報
        """
        data = {
            'postID': post_id,
            'userID': user_id,
            'eventType': 'statusChange',
            'value': status
        }

        if comment:
            data['comment'] = comment

        return self._request('/timelineEntries/create', data=data)

    def close(self):
        """セッション終了"""
        self.session.close()