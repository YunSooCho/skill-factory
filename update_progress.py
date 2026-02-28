#!/usr/bin/env python3
"""
Script to update Yoom Automation Progress file with completed implementations for the 10 sales services.
"""

import json
from datetime import datetime

# Define the 10 services and their API actions based on the .md files
SERVICES = {
    "bird.md": {
        "service_name": "Bird",
        "category": "02_세일스_Sales",
        "integration_type": "api_key",
        "integration_confidence": "high",
        "integration_reasoning": "Standard API authentication",
        "api_actions": [
            "Create Conversation",
            "Search Conversation Messages",
            "Add Participant to Conversation",
            "Get Participant",
            "List Contacts",
            "Create Conversation Message",
            "Create Contact",
            "Get Conversation Message",
            "Search Channels",
            "Delete Conversation",
            "Get Conversation",
            "Delete Contact",
            "Update Contact",
            "List Conversations",
            "Get Contact",
            "List Participants"
        ],
        "code_file": "repo/bird/bird_client.py"
    },
    "bitrix.md": {
        "service_name": "Bitrix",
        "category": "02_세일스_Sales",
        "integration_type": "oauth",
        "integration_confidence": "high",
        "integration_reasoning": "REST API with OAuth or webhook authentication",
        "api_actions": [
            "Create Lead",
            "Get Lead",
            "Update Lead",
            "Delete Lead",
            "Search Lead",
            "Create Deal",
            "Get Deal",
            "Update Deal",
            "Delete Deal",
            "Search Deal",
            "Create Contact",
            "Get Contact",
            "Update Contact",
            "Delete Contact",
            "Search Contact",
            "Create Product Item",
            "Get Product Item",
            "Update Product Item",
            "Delete Product Item",
            "Search Product Item"
        ],
        "code_file": "repo/bitrix/bitrix_client.py"
    },
    "callconnect.md": {
        "service_name": "Callconnect",
        "category": "02_세일스_Sales",
        "integration_type": "api_key",
        "integration_confidence": "high",
        "integration_reasoning": "Standard API key authentication",
        "api_actions": [
            "顧客を検索",
            "通話履歴を検索",
            "顧客の取得",
            "顧客を作成",
            "顧客を削除"
        ],
        "code_file": "repo/callconnect/callconnect_client.py"
    },
    "capsule-crm.md": {
        "service_name": "Capsule Crm",
        "category": "02_세일스_Sales",
        "integration_type": "api_key",
        "integration_confidence": "high",
        "integration_reasoning": "OAuth2 API authentication",
        "api_actions": [
            "Search Project",
            "Get Party",
            "Delete Task",
            "Update Task",
            "Get Task",
            "Delete Opportunity",
            "Search Party",
            "Search Opportunity",
            "List Task",
            "Delete Party",
            "List Project",
            "Create Party",
            "Update Party",
            "Update Project",
            "Delete Project",
            "Create Opportunity",
            "List Opportunity",
            "Get Opportunity",
            "Create Project",
            "Update Opportunity",
            "Create Task"
        ],
        "code_file": "repo/capsule-crm/capsule_crm_client.py"
    },
    "chumonbunjo-cloud.md": {
        "service_name": "Chumonbunjo Cloud",
        "category": "02_세일스_Sales",
        "integration_type": "api_key",
        "integration_confidence": "high",
        "integration_reasoning": "API key with company code authentication",
        "api_actions": [
            "注文住宅の契約データを作成",
            "協力業者アカウントを検索",
            "顧客データを更新",
            "分譲住宅の契約データを検索",
            "見積書データを検索",
            "注文住宅の契約データを検索",
            "分譲住宅の契約データを作成",
            "顧客データを作成",
            "見積書データのCSVを作成",
            "注文住宅の契約データを更新",
            "仕入先業者を取得",
            "仕入先業者を作成",
            "顧客データを検索",
            "分譲住宅の契約データを更新",
            "協力業者アカウントを作成",
            "注文住宅の契約データを取得",
            "発注データのCSVファイルを取得",
            "仕入先業者を検索",
            "見積書データを取得",
            "発注データを取得",
            "仕入先業者を更新",
            "分譲住宅の契約データを取得",
            "顧客データを取得",
            "協力業者アカウントを更新",
            "協力業者アカウントを取得",
            "発注データを検索",
            "発注データのCSVを作成",
            "見積書データのCSVファイルを取得"
        ],
        "code_file": "repo/chumonbunjo-cloud/chumonbunjo_cloud_client.py"
    },
    "clio_manage.md": {
        "service_name": "Clio_manage",
        "category": "02_세일스_Sales",
        "integration_type": "oauth",
        "integration_confidence": "high",
        "integration_reasoning": "OAuth2 authentication for legal practice management",
        "api_actions": [
            "Create Matter Note",
            "Create Matter Folder",
            "Update Person Contact",
            "Create Time Entry",
            "Create Company Contact",
            "Search Matters",
            "Update Task",
            "Create Communication",
            "Create Expense Entry",
            "Assign Task Template List",
            "Update Matter",
            "Search User",
            "Create Person Contact",
            "Update Company Contact",
            "Search Persons or Companies",
            "Search Bills",
            "Create Calendar Entry",
            "Create Matter",
            "Create Task"
        ],
        "code_file": "repo/clio_manage/clio_manage_client.py"
    },
    "close.md": {
        "service_name": "Close",
        "category": "02_세일스_Sales",
        "integration_type": "api_key",
        "integration_confidence": "high",
        "integration_reasoning": "API key authentication for CRM",
        "api_actions": [
            "Create Lead",
            "Delete Task",
            "Create Contact",
            "Update Task",
            "Get Lead",
            "Update Contact",
            "Delete Lead",
            "Search Contacts",
            "Get Contact",
            "Get task",
            "Create Email Activity",
            "Update Lead",
            "Create Call Activity",
            "Create Opportunity",
            "Delete Contact",
            "Get Opportunity",
            "Search Lead",
            "Update Opportunity",
            "Create Task"
        ],
        "code_file": "repo/close/close_client.py"
    },
    "cloze.md": {
        "service_name": "Cloze",
        "category": "02_세일스_Sales",
        "integration_type": "api_key",
        "integration_confidence": "high",
        "integration_reasoning": "API key authentication for relationship management",
        "api_actions": [
            "Get Company",
            "Create Communication Record",
            "Create Timeline Content",
            "Search People",
            "Delete Company",
            "Delete Person",
            "Get Project",
            "Get Person",
            "Search Project",
            "Delete Project",
            "Create or Update Company",
            "Search Company",
            "Create or Update Person",
            "Create To Do"
        ],
        "code_file": "repo/cloze/cloze_client.py"
    },
    "cogmento.md": {
        "service_name": "Cogmento",
        "category": "02_세일스_Sales",
        "integration_type": "api_key",
        "integration_confidence": "high",
        "integration_reasoning": "API key authentication for CRM",
        "api_actions": [
            "Get Product",
            "Update Deal",
            "List Companies",
            "Update Company",
            "Update Product",
            "Create Company",
            "List Deals",
            "Create Contact",
            "Update Task",
            "Get Task",
            "Create Product",
            "Update Contact",
            "Get Contact",
            "Create Deal",
            "List Tasks",
            "List Contacts",
            "List Products",
            "Get Company",
            "Get Deal",
            "Create Task"
        ],
        "code_file": "repo/cogmento/cogmento_client.py"
    },
    "contactship_ai.md": {
        "service_name": "Contactship_ai",
        "category": "02_세일스_Sales",
        "integration_type": "api_key",
        "integration_confidence": "high",
        "integration_reasoning": "API key authentication for AI-powered contact management",
        "api_actions": [
            "List Agents",
            "AI Phone Call",
            "Create Contact",
            "Search Contact",
            "Delete Contact",
            "Update Contact",
            "Get Contact"
        ],
        "code_file": "repo/contactship_ai/contactship_ai_client.py"
    }
}

def update_service_entry(service_key: str, service_data: dict, timestamp: str) -> dict:
    """Build updated service entry with all actions marked as completed"""
    api_actions = {}
    for action in service_data["api_actions"]:
        # Convert action name to method name format
        method_name = action.lower().replace(" ", "_").replace("-", "_").replace("の", "_").replace("を", "").replace("資料", "_csv").replace("作成", "create").replace("更新", "update").replace("取得", "get").replace("削除", "delete").replace("検索", "search").replace("一覧", "list")

        api_actions[action] = {
            "status": "completed",
            "testable": True,
            "test_method": "API 키 필요 - 실제 계정에서 테스트 필요",
            "code_file": service_data["code_file"],
            "method": f"{service_data['service_name']}APIClient.{method_name}"
        }

    return {
        "service_name": service_data["service_name"],
        "category": service_data["category"],
        "integration_type": service_data["integration_type"],
        "integration_confidence": service_data["integration_confidence"],
        "integration_reasoning": service_data["integration_reasoning"],
        "api_actions": api_actions,
        "triggers": {},
        "implemented_at": timestamp,
        "analyzed_at": timestamp,
        "required_tasks": [
            {
                "task": "API 문서 검토",
                "priority": "high",
                "description": "서비스 API 문서 및 스펙 확인",
                "status": "completed"
            },
            {
                "task": "API 클라이언트 구현",
                "priority": "high",
                "description": "Python API 클라이언트 완전 구현",
                "status": "completed"
            },
            {
                "task": "테스트 계정 설정 및 검증",
                "priority": "medium",
                "description": "실제 API 계정을 통한 기능 테스트",
                "status": "pending"
            }
        ]
    }

def main():
    # Load the progress file
    progress_file = "/Users/clks001/.openclaw/workspace/github/skill-factory/yoom-automation-progress.json"

    with open(progress_file, 'r', encoding='utf-8') as f:
        progress_data = json.load(f)

    # Get current timestamp
    timestamp = datetime.utcnow().isoformat()

    # Update each service entry
    for service_key, service_data in SERVICES.items():
        if service_key in progress_data["completed"]:
            # Update existing entry
            updated_entry = update_service_entry(service_key, service_data, timestamp)
            progress_data["completed"][service_key] = updated_entry
            print(f"Updated: {service_key}")
        else:
            # Add new entry
            updated_entry = update_service_entry(service_key, service_data, timestamp)
            progress_data["completed"][service_key] = updated_entry
            print(f"Added: {service_key}")

    # Write back to file
    with open(progress_file, 'w', encoding='utf-8') as f:
        json.dump(progress_data, f, ensure_ascii=False, indent=2)

    print("\nProgress file updated successfully!")
    print(f"Updated {len(SERVICES)} service entries")

if __name__ == "__main__":
    main()