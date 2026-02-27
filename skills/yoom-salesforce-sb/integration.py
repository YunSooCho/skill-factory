import os
from simple_salesforce import Salesforce

class SalesforceSbClient:
    def __init__(self):
        self.username = os.getenv("YOOM_SALESFORCE_SB_USERNAME", "")
        self.password = os.getenv("YOOM_SALESFORCE_SB_PASSWORD", "")
        self.security_token = os.getenv("YOOM_SALESFORCE_SB_AUTH_TOKEN", "")
        if not all([self.username, self.password, self.security_token]):
            raise ValueError("Credentials required")
        self.sf = Salesforce(username=self.username, password=self.password, security_token=self.security_token)

    # 상위 5개
    async def download_report(self, report_id):
        raise NotImplementedError()
    async def update_opportunity(self, **kwargs):
        raise NotImplementedError()
    async def create_custom_object(self, **kwargs):
        raise NotImplementedError()
    async def link_email_to_person(self, email_id, person_id):
        raise NotImplementedError()
    async def register_lead_action(self, **kwargs):
        raise NotImplementedError()

class SalesforceSbTriggers:
    def __init__(self, client):
        self.client = client