import os
import aiohttp

class PipedriveClient:
    def __init__(self):
        self.base_url = os.getenv("YOOM_PIPEDRIVE_BASE_URL", "")
        self.auth_token = os.getenv("YOOM_PIPEDRIVE_AUTH_TOKEN", "")
        if not self.base_url or not self.auth_token:
            raise ValueError("YOOM_PIPEDRIVE_BASE_URL and YOOM_PIPEDRIVE_AUTH_TOKEN required")

    async def _request(self, method, endpoint, **kwargs):
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.auth_token}"}
        async with aiohttp.ClientSession() as session:
            async with session.request(method, f"{self.base_url}/{endpoint}", headers=headers, **kwargs) as response:
                response.raise_for_status()
                return await response.json()

    # 28개 API 메소드
    async def search_organization(self, **kwargs):
        raise NotImplementedError("組織を検색")

    async def delete_organization(self, **kwargs):
        raise NotImplementedError("組織を削除")

    async def update_lead(self, **kwargs):
        raise NotImplementedError("リード를更新")

    async def add_organization(self, **kwargs):
        raise NotImplementedError("組織を追加")

    async def add_file(self, **kwargs):
        raise NotImplementedError("ファイルを追加")

    async def get_deal_products(self, **kwargs):
        raise NotImplementedError("取引に紐づく製品一覧の取得")

    async def search_lead(self, **kwargs):
        raise NotImplementedError("リード를検索")

    async def create_activity(self, **kwargs):
        raise NotImplementedError("アクティビティを作成")

    async def update_person(self, **kwargs):
        raise NotImplementedError("人物情報를更新")

    async def get_lead(self, **kwargs):
        raise NotImplementedError("リード情報를取得")

    async def update_organization(self, **kwargs):
        raise NotImplementedError("組織を更新")

    async def create_user(self, **kwargs):
        raise NotImplementedError("ユーザーを作成")

    async def add_deal(self, **kwargs):
        raise NotImplementedError("取引를追加")

    async def get_organization_persons(self, **kwargs):
        raise NotImplementedError("組織に関連付けられた人物를取得")

    async def add_person(self, **kwargs):
        raise NotImplementedError("人物を追加")

    async def update_activity(self, **kwargs):
        raise NotImplementedError("アクティビ티を更新")

    async def get_organization(self, **kwargs):
        raise NotImplementedError("組織情報를取得")

    async def get_deal(self, **kwargs):
        raise NotImplementedError("取引の詳細を取得")

    async def search_person(self, **kwargs):
        raise NotImplementedError("人物情報を검색")

    async def get_person(self, **kwargs):
        raise NotImplementedError("人物情報를取得")

    async def delete_lead(self, **kwargs):
        raise NotImplementedError("リード를削除")

    async def add_note(self, **kwargs):
        raise NotImplementedError("ノートを追加")

    async def delete_person(self, **kwargs):
        raise NotImplementedError("人物를削除")

    async def search_activity(self, **kwargs):
        raise NotImplementedError("アクティビティを검색")

    async def update_deal(self, **kwargs):
        raise NotImplementedError("取引를更新")

    async def delete_deal(self, **kwargs):
        raise NotImplementedError("取引를削除")

    async def get_products(self, **kwargs):
        raise NotImplementedError("製品一覧を取得")

    async def create_lead(self, **kwargs):
        raise NotImplementedError("リードを作成")

class PipedriveTriggers:
    def __init__(self, client):
        self.client = client

    # 10개 트리거
    async def on_deal_deleted(self, callback):
        pass

    async def on_person_updated(self, callback):
        pass

    async def on_organization_updated(self, callback):
        pass

    async def on_deal_added(self, callback):
        pass

    async def on_deal_updated(self, callback):
        pass

    async def on_person_deleted(self, callback):
        pass

    async def on_person_added(self, callback):
        pass

    async def on_organization_deleted(self, callback):
        pass

    async def on_organization_added(self, callback):
        pass

    async def on_activity_added(self, callback):
        pass