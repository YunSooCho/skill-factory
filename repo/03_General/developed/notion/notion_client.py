import aiohttp
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


class RateLimiter:
    """Rate limiter for API calls"""

    def __init__(self, max_requests: int = 3, per_seconds: int = 1):
        self.max_requests = max_requests
        self.per_seconds = per_seconds
        self.requests: List[datetime] = []
        self.lock = asyncio.Lock()

    async def acquire(self) -> None:
        """Wait until a request can be made"""
        async with self.lock:
            now = datetime.now(timezone.utc)

            cutoff = now - timedelta(seconds=self.per_seconds)
            self.requests = [req for req in self.requests if req > cutoff]

            if len(self.requests) >= self.max_requests:
                oldest_request = sorted(self.requests)[0]
                sleep_time = (oldest_request + timedelta(seconds=self.per_seconds) - now).total_seconds()
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)

            self.requests.append(now)


class NotionClient:
    """Async Notion API client with rate limiting"""

    BASE_URL = "https://api.notion.com/v1"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = None
        self.rate_limiter = RateLimiter(max_requests=3, per_seconds=1)

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers={
            "Authorization": f"Bearer {self.api_key}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        })
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make API request"""
        await self.rate_limiter.acquire()

        async with self.session.request(method, f"{self.BASE_URL}{endpoint}", json=data) as response:
            response_data = await response.json()
            if response.status >= 400:
                raise ValueError(f"Notion API error ({response.status}): {response_data}")
            return response_data

    # ==================== Core Methods (31 actions) ====================

    # 1. ページまたはブロックの子ブロック一覧を取得
    async def get_block_children(
        self,
        block_id: str,
        page_size: int = 100,
        start_cursor: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get block children (ページまたはブロックの子ブロック一覧を取得).

        Args:
            block_id: Block ID
            page_size: Page size (default: 100)
            start_cursor: Cursor for pagination

        Returns:
            List of children blocks
        """
        params = {"page_size": page_size}
        if start_cursor:
            params["start_cursor"] = start_cursor

        return await self._request("GET", f"/blocks/{block_id}/children", None)

    # 2. ページのプロパティを更新（マルチセレクトプロパティ）
    async def update_page_property_multiselect(
        self,
        page_id: str,
        property_id: str,
        options: List[str]
    ) -> Dict[str, Any]:
        """
        Update page multi-select property (ページのプロパティを更新（マルチセレクトプロパティ）).

        Args:
            page_id: Page ID
            property_id: Property ID
            options: List of option names

        Returns:
            Updated page properties
        """
        data = {
            "properties": {
                property_id: {
                    "multi_select": [{"name": opt} for opt in options]
                }
            }
        }
        return await self._request("PATCH", f"/pages/{page_id}", data)

    # 3. ページにヘッダーと本文を追加
    async def add_page_heading_and_body(
        self,
        page_id: str,
        heading: str,
        body: str
    ) -> Dict[str, Any]:
        """
        Add heading and body to page (ページにヘッダーと本文を追加).

        Args:
            page_id: Page ID
            heading: Heading text
            body: Body text

        Returns:
            Created block data
        """
        data = {
            "children": [
                {
                    "object": "block",
                    "type": "heading_1",
                    "heading_1": {
                        "rich_text": [{"type": "text", "text": {"content": heading}}]
                    }
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": body}}]
                    }
                }
            ]
        }
        return await self._request("PATCH", f"/blocks/{page_id}/children", data)

    # 4. 指定のレコードにサブアイテムを追加する
    async def add_subitem_to_record(
        self,
        page_id: str,
        content: str
    ) -> Dict[str, Any]:
        """
        Add subitem to record (指定のレコードにサブアイテムを追加する).

        Args:
            page_id: Page ID
            content: Content text

        Returns:
            Created subitem data
        """
        data = {
            "children": [
                {
                    "object": "block",
                    "type": "to_do",
                    "to_do": {
                        "rich_text": [{"type": "text", "text": {"content": content}}]
                    }
                }
            ]
        }
        return await self._request("PATCH", f"/blocks/{page_id}/children", data)

    # 5. ページに埋め込みURL付きのテキストを追加
    async def add_embed_text(
        self,
        page_id: str,
        text: str,
        embed_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Add text with embed URL to page (ページに埋め込みURL付きのテキストを追加).

        Args:
            page_id: Page ID
            text: Text content
            embed_url: Embed URL

        Returns:
            Created block data
        """
        block_type = "bookmark" if embed_url else "paragraph"
        data = {
            "children": [
                {
                    "object": "block",
                    "type": block_type,
                    block_type: {
                        "rich_text": [{"type": "text", "text": {"content": text, "link": {"url": embed_url}} if embed_url else {"content": text}}]
                    } if block_type == "paragraph" else {"url": embed_url}
                }
            ]
        }
        return await self._request("PATCH", f"/blocks/{page_id}/children", data)

    # 6. ページにテキストを追加
    async def add_text_to_page(
        self,
        page_id: str,
        text: str,
        text_type: str = "paragraph"
    ) -> Dict[str, Any]:
        """
        Add text to page (ページにテキストを追加).

        Args:
            page_id: Page ID
            text: Text content
            text_type: Type of text block (paragraph, heading_1, heading_2, heading_3)

        Returns:
            Created block data
        """
        data = {
            "children": [
                {
                    "object": "block",
                    "type": text_type,
                    text_type: {
                        "rich_text": [{"type": "text", "text": {"content": text}}]
                    }
                }
            ]
        }
        return await self._request("PATCH", f"/blocks/{page_id}/children", data)

    # 7. データベースのテンプレートを使用したページを作成（タイトルのみ）
    async def create_page_from_template(
        self,
        database_id: str,
        title: str
    ) -> Dict[str, Any]:
        """
        Create page from database template (データベースのテンプレートを使用したページを作成（タイトルのみ）).

        Args:
            database_id: Database ID
            title: Page title

        Returns:
            Created page data
        """
        data = {
            "parent": {"database_id": database_id},
            "properties": {
                "title": {
                    "title": [{"type": "text", "text": {"content": title}}]
                }
            }
        }
        return await self._request("POST", "/pages", data)

    # 8. ユーザーのリストを取得
    async def list_users(
        self,
        page_size: int = 100,
        start_cursor: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get user list (ユーザーのリストを取得).

        Args:
            page_size: Page size (default: 100)
            start_cursor: Cursor for pagination

        Returns:
            List of users
        """
        return await self._request("GET", "/users", None)

    # 9. ページのプロパティを更新（数値プロパティ）
    async def update_page_property_number(
        self,
        page_id: str,
        property_id: str,
        number: float
    ) -> Dict[str, Any]:
        """
        Update page number property (ページのプロパティを更新（数値プロパティ）).

        Args:
            page_id: Page ID
            property_id: Property ID
            number: Number value

        Returns:
            Updated page properties
        """
        data = {
            "properties": {
                property_id: {
                    "number": number
                }
            }
        }
        return await self._request("PATCH", f"/pages/{page_id}", data)

    # 10. データソースを取得
    async def get_database(self, database_id: str) -> Dict[str, Any]:
        """
        Get database (データソースを取得).

        Args:
            database_id: Database ID

        Returns:
            Database information
        """
        return await self._request("GET", f"/databases/{database_id}", None)

    # 11. ファイルアップロードIDの発行
    async def issue_file_upload_id(
        self,
        file_name: str,
        file_type: str,
        file_size: int
    ) -> Dict[str, Any]:
        """
        Issue file upload ID (ファイルアップロードIDの発行).

        Args:
            file_name: File name
            file_type: MIME type
            file_size: File size in bytes

        Returns:
            Upload URL and ID
        """
        data = {
            "name": file_name,
            "type": file_type,
            "size": file_size
        }
        return await self._request("POST", "/files", data)

    # 12. ページのプロパティを更新（チェックボックスプロパティ）
    async def update_page_property_checkbox(
        self,
        page_id: str,
        property_id: str,
        checked: bool
    ) -> Dict[str, Any]:
        """
        Update page checkbox property (ページのプロパティを更新（チェックボックスプロパティ）).

        Args:
            page_id: Page ID
            property_id: Property ID
            checked: Checkbox value

        Returns:
            Updated page properties
        """
        data = {
            "properties": {
                property_id: {
                    "checkbox": checked
                }
            }
        }
        return await self._request("PATCH", f"/pages/{page_id}", data)

    # 13. ページのプロパティを更新（ファイルプロパティ）
    async def update_page_property_file(
        self,
        page_id: str,
        property_id: str,
        file_url: str
    ) -> Dict[str, Any]:
        """
        Update page file property (ページのプロパティを更新（ファイルプロパティ）).

        Args:
            page_id: Page ID
            property_id: Property ID
            file_url: File URL (after upload)

        Returns:
            Updated page properties
        """
        data = {
            "properties": {
                property_id: {
                    "files": [{"type": "external", "external": {"url": file_url}}]
                }
            }
        }
        return await self._request("PATCH", f"/pages/{page_id}", data)

    # 14. ページのプロパティを更新（電話プロパティ）
    async def update_page_property_phone(
        self,
        page_id: str,
        property_id: str,
        phone_number: str
    ) -> Dict[str, Any]:
        """
        Update page phone property (ページのプロパティを更新（電話プロパティ）).

        Args:
            page_id: Page ID
            property_id: Property ID
            phone_number: Phone number

        Returns:
            Updated page properties
        """
        data = {
            "properties": {
                property_id: {
                    "phone_number": phone_number
                }
            }
        }
        return await self._request("PATCH", f"/pages/{page_id}", data)

    # 15. データソースの数式プロパティ内の文字検索
    async def search_formula_property(
        self,
        database_id: str,
        search_text: str,
        formula_property_id: str
    ) -> Dict[str, Any]:
        """
        Search in formula property (データソースの数式プロパティ内の文字検索).

        Args:
            database_id: Database ID
            search_text: Text to search
            formula_property_id: Formula property ID

        Returns:
            Search results
        """
        data = {
            "filter": {
                "property": formula_property_id,
                "formula": {
                    "string": {"contains": search_text}
                }
            }
        }
        return await self._request("POST", f"/databases/{database_id}/query", data)

    # 16. ページのプロパティを更新（メールプロパティ）
    async def update_page_property_email(
        self,
        page_id: str,
        property_id: str,
        email: str
    ) -> Dict[str, Any]:
        """
        Update page email property (ページのプロパティを更新（メールプロパティ）).

        Args:
            page_id: Page ID
            property_id: Property ID
            email: Email address

        Returns:
            Updated page properties
        """
        data = {
            "properties": {
                property_id: {
                    "email": email
                }
            }
        }
        return await self._request("PATCH", f"/pages/{page_id}", data)

    # 17. ページのプロパティを更新（セレクトプロパティ）
    async def update_page_property_select(
        self,
        page_id: str,
        property_id: str,
        option: str
    ) -> Dict[str, Any]:
        """
        Update page select property (ページのプロパティを更新（セレクトプロパティ）).

        Args:
            page_id: Page ID
            property_id: Property ID
            option: Option name

        Returns:
            Updated page properties
        """
        data = {
            "properties": {
                property_id: {
                    "select": {"name": option}
                }
            }
        }
        return await self._request("PATCH", f"/pages/{page_id}", data)

    # 18. ページ・データベースをタイトルで検索
    async def search_by_title(
        self,
        title: str,
        filter_property: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Search by title (ページ・データベースをタイトルで検索).

        Args:
            title: Title to search
            filter_property: Optional filter property

        Returns:
            Search results
        """
        data = {
            "query": title,
            "filter": filter_property
        }
        return data

    # 19. ページのプロパティを更新（タイトルプロパティ）
    async def update_page_title(
        self,
        page_id: str,
        title: str
    ) -> Dict[str, Any]:
        """
        Update page title (ページのプロパティを更新（タイトルプロパティ）).

        Args:
            page_id: Page ID
            title: New title

        Returns:
            Updated page
        """
        data = {
            "properties": {
                "title": {
                    "title": [{"type": "text", "text": {"content": title}}]
                }
            }
        }
        return await self._request("PATCH", f"/pages/{page_id}", data)

    # 20. ページを作成
    async def create_page(
        self,
        parent_id: str,
        parent_type: str = "database_id",
        properties: Optional[Dict[str, Any]] = None,
        children: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Create page (ページを作成).

        Args:
            parent_id: Parent ID
            parent_type: Parent type (database_id or page_id)
            properties: Page properties
            children: Child blocks

        Returns:
            Created page data
        """
        data = {
            "parent": {parent_type: parent_id},
            "properties": properties or {}
        }
        if children:
            data["children"] = children

        return await self._request("POST", "/pages", data)

    # 21. ページのプロパティを更新（URLプロパティ）
    async def update_page_property_url(
        self,
        page_id: str,
        property_id: str,
        url: str
    ) -> Dict[str, Any]:
        """
        Update page URL property (ページのプロパティを更新（URLプロパティ）).

        Args:
            page_id: Page ID
            property_id: Property ID
            url: URL value

        Returns:
            Updated page properties
        """
        data = {
            "properties": {
                property_id: {
                    "url": url
                }
            }
        }
        return await self._request("PATCH", f"/pages/{page_id}", data)

    # 22. ページ情報を取得
    async def get_page(self, page_id: str) -> Dict[str, Any]:
        """
        Get page information (ページ情報を取得).

        Args:
            page_id: Page ID

        Returns:
            Page information
        """
        return await self._request("GET", f"/pages/{page_id}", None)

    # 23. ページ情報を取得（ファイル情報の一覧）
    async def get_page_with_files(self, page_id: str) -> Dict[str, Any]:
        """
        Get page with file information (ページ情報を取得（ファイル情報の一覧）).

        Args:
            page_id: Page ID

        Returns:
            Page information with file details
        """
        return await self._request("GET", f"/pages/{page_id}", None)

    # 24. ファイルをアップロード
    async def upload_file(
        self,
        upload_url: str,
        file_path: str,
        content_type: str
    ) -> Dict[str, Any]:
        """
        Upload file (ファイルをアップロード).

        Args:
            upload_url: Upload URL from issue_file_upload_id
            file_path: Local file path
            content_type: MIME type

        Returns:
            Upload result
        """
        with open(file_path, 'rb') as f:
            async with self.session.put(upload_url, data=f, headers={"Content-Type": content_type}) as response:
                return await response.text()

    # 25. 特定のページのブロック情報を取得
    async def get_page_block_children(
        self,
        page_id: str,
        page_size: int = 100
    ) -> Dict[str, Any]:
        """
        Get page block children (特定のページのブロック情報を取得).

        Args:
            page_id: Page ID
            page_size: Page size (default: 100)

        Returns:
            List of blocks
        """
        return await self._request("GET", f"/blocks/{page_id}/children", None)

    # 26. データソースのプロパティ名を更新
    async def update_database_property(
        self,
        database_id: str,
        property_id: str,
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update database property name (データソースのプロパティ名を更新).

        Args:
            database_id: Database ID
            property_id: Property ID
            updates: Property updates

        Returns:
            Updated database
        """
        return await self._request("PATCH", f"/databases/{database_id}", updates)

    # 27. ページのプロパティを更新（テキストプロパティ）
    async def update_page_property_text(
        self,
        page_id: str,
        property_id: str,
        text: str
    ) -> Dict[str, Any]:
        """
        Update page text property (ページのプロパティを更新（テキストプロパティ）).

        Args:
            page_id: Page ID
            property_id: Property ID
            text: Text value

        Returns:
            Updated page properties
        """
        data = {
            "properties": {
                property_id: {
                    "rich_text": [{"type": "text", "text": {"content": text}}]
                }
            }
        }
        return await self._request("PATCH", f"/pages/{page_id}", data)

    # 28. ページのプロパティを更新（日付プロパティ）
    async def update_page_property_date(
        self,
        page_id: str,
        property_id: str,
        date: str,
        time: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update page date property (ページのプロパティを更新（日付プロパティ）).

        Args:
            page_id: Page ID
            property_id: Property ID
            date: Date string (YYYY-MM-DD)
            time: Optional time string

        Returns:
            Updated page properties
        """
        data = {
            "properties": {
                property_id: {
                    "date": {"start": f"{date}T{time}" if time else date}
                }
            }
        }
        return await self._request("PATCH", f"/pages/{page_id}", data)

    # 29. ファイルをダウンロードする
    async def download_file(self, file_url: str, save_path: str) -> Dict[str, Any]:
        """
        Download file (ファイルをダウンロードする).

        Args:
            file_url: File URL
            save_path: Local save path

        Returns:
            Download result
        """
        async with self.session.get(file_url) as response:
            with open(save_path, 'wb') as f:
                f.write(await response.read())
            return {"status": "success", "path": save_path}

    # 30. ページのプロパティを更新（リレーションプロパティ）
    async def update_page_property_relation(
        self,
        page_id: str,
        property_id: str,
        related_page_ids: List[str]
    ) -> Dict[str, Any]:
        """
        Update page relation property (ページのプロパティを更新（リレーションプロパティ）).

        Args:
            page_id: Page ID
            property_id: Property ID
            related_page_ids: List of related page IDs

        Returns:
            Updated page properties
        """
        data = {
            "properties": {
                property_id: {
                    "relation": [{"id": pid} for pid in related_page_ids]
                }
            }
        }
        return await self._request("PATCH", f"/pages/{page_id}", data)

    # 31. データベース情報を取得
    async def get_database_info(self, database_id: str) -> Dict[str, Any]:
        """
        Get database information (データベース情報を取得).

        Args:
            database_id: Database ID

        Returns:
            Database information
        """
        return await self._request("GET", f"/databases/{database_id}", None)

    # Additional helper methods

    async def search_pages(self, query: str) -> Dict[str, Any]:
        """Helper: Search in workspace"""
        data = {
            "query": query
        }
        return await self._request("POST", "/search", data)

    async def query_database(
        self,
        database_id: str,
        filter: Optional[Dict[str, Any]] = None,
        sorts: Optional[List[Dict[str, Any]]] = None,
        page_size: int = 100
    ) -> Dict[str, Any]:
        """Helper: Query database with optional filters"""
        data = {}
        if filter:
            data["filter"] = filter
        if sorts:
            data["sorts"] = sorts

        return await self._request("POST", f"/databases/{database_id}/query", data)