#!/usr/bin/env python3
"""
Update progress file for Batch 34 implementations
"""

import json
from pathlib import Path
import subprocess

PROGRESS_FILE = Path("/Users/clks001/.openclaw/workspace/github/skill-factory/yoom-automation-progress.json")
REPO_DIR = Path("/Users/clks001/.openclaw/workspace/github/skill-factory/repo")

SERVICE_CATEGORIES = {
    # General services
    "smartsheet.md": {
        "service_name": "Smartsheet",
        "category": "03_업무일반_General",
        "api_actions": [
            "share_sheet",
            "update_row",
            "search_rows",
            "get_row",
            "add_user",
            "get_discussion",
            "add_comment",
            "list_discussions",
            "add_row",
            "create_sheet",
            "delete_row",
            "create_folder",
            "attach_file_to_sheet",
            "attach_file_to_row"
        ]
    },
    "techulus_push.md": {
        "service_name": "Techulus Push",
        "category": "03_업무일반_General",
        "api_actions": [
            "send_push_notification",
            "send_bulk_notifications"
        ]
    },
    "trint.md": {
        "service_name": "Trint",
        "category": "03_업무일반_General",
        "api_actions": [
            "create_transcription",
            "get_transcription",
            "list_transcriptions",
            "delete_transcription"
        ]
    },
    "uniqode.md": {
        "service_name": "Uniqode",
        "category": "03_업무일반_General",
        "api_actions": [
            "create_qr",
            "get_qr",
            "update_qr",
            "delete_qr",
            "list_qrs"
        ]
    },
    "viewdns.md": {
        "service_name": "ViewDNS",
        "category": "03_업무일반_General",
        "api_actions": [
            "dns_lookup",
            "whois_lookup",
            "reverse_ip",
            "dns_records",
            "subdomain_scan"
        ]
    },
    "whereby.md": {
        "service_name": "Whereby",
        "category": "03_업무일반_General",
        "api_actions": [
            "create_meeting",
            "get_meeting",
            "update_meeting",
            "delete_meeting",
            "list_meetings"
        ]
    },
    "workplace.md": {
        "service_name": "Workplace",
        "category": "03_업무일반_General",
        "api_actions": [
            "create_post",
            "get_post",
            "update_post",
            "delete_post",
            "list_posts"
        ]
    },
    "xai.md": {
        "service_name": "xAI",
        "category": "03_업무일반_General",
        "api_actions": [
            "chat_completion",
            "list_models",
            "get_model"
        ]
    },
    "zoho-mail.md": {
        "service_name": "Zoho Mail",
        "category": "03_업무일반_General",
        "api_actions": [
            "send_email",
            "get_email",
            "list_emails",
            "delete_email",
            "mark_as_read"
        ]
    },
    "zoho_sheet.md": {
        "service_name": "Zoho Sheet",
        "category": "03_업무일반_General",
        "api_actions": [
            "create_sheet",
            "get_sheet",
            "update_cell",
            "add_row",
            "get_data"
        ]
    },
    "zoho_writer.md": {
        "service_name": "Zoho Writer",
        "category": "03_업무일반_General",
        "api_actions": [
            "create_document",
            "get_document",
            "update_document",
            "export_document"
        ]
    },
    "zoom.md": {
        "service_name": "Zoom",
        "category": "03_업무일반_General",
        "api_actions": [
            "create_meeting",
            "get_meeting",
            "update_meeting",
            "delete_meeting",
            "list_meetings",
            "get_user"
        ]
    },

    # Automation services
    "airparser.md": {
        "service_name": "Airparser",
        "category": "04_오토메이션_Automation",
        "api_actions": [
            "parse_document",
            "get_parser",
            "list_parsers",
            "create_parser"
        ]
    },
    "apify.md": {
        "service_name": "Apify",
        "category": "04_오토메이션_Automation",
        "api_actions": [
            "run_actor",
            "get_actor",
            "list_actors",
            "get_run",
            "list_runs"
        ]
    },
    "apitemplate.md": {
        "service_name": "APITemplate",
        "category": "04_오토메이션_Automation",
        "api_actions": [
            "create_image",
            "create_pdf",
            "list_templates",
            "get_template"
        ]
    },
    "axiom.md": {
        "service_name": "Axiom",
        "category": "04_오토메이션_Automation",
        "api_actions": [
            "ingest_events",
            "query_events",
            "list_datasets",
            "get_dataset"
        ]
    },
    "beLazy.md": {
        "service_name": "BeLazy",
        "category": "04_오토메이션_Automation",
        "api_actions": [
            "create_task",
            "get_task",
            "list_tasks",
            "update_task"
        ]
    },
    "bland_ai.md": {
        "service_name": "Bland AI",
        "category": "04_오토메이션_Automation",
        "api_actions": [
            "create_call",
            "get_call",
            "list_calls",
            "end_call",
            "analyze_call"
        ]
    },
    "botpress.md": {
        "service_name": "Botpress",
        "category": "04_오토메이션_Automation",
        "api_actions": [
            "create_bot",
            "get_bot",
            "list_bots",
            "send_message",
            "get_analytics"
        ]
    },
    "botsonic.md": {
        "service_name": "Botsonic",
        "category": "04_오토메이션_Automation",
        "api_actions": [
            "create_chatbot",
            "get_chatbot",
            "train_chatbot",
            "chat"
        ]
    },
    "browse-ai.md": {
        "service_name": "Browse AI",
        "category": "04_오토메이션_Automation",
        "api_actions": [
            "create_robot",
            "run_robot",
            "get_robot",
            "list_robots",
            "get_robot_data"
        ]
    },
    "carbone.md": {
        "service_name": "Carbone",
        "category": "04_오토메이션_Automation",
        "api_actions": [
            "render_template",
            "get_template",
            "delete_template"
        ]
    },
    "cdata-connect.md": {
        "service_name": "CData Connect",
        "category": "04_오토메이션_Automation",
        "api_actions": [
            "list_tables",
            "query_table",
            "insert_row",
            "update_row",
            "delete_row"
        ]
    },
    "cloudbot.md": {
        "service_name": "CloudBot",
        "category": "04_오토메이션_Automation",
        "api_actions": [
            "deploy_bot",
            "get_bot",
            "list_bots",
            "update_bot"
        ]
    },
    "cloudconvert.md": {
        "service_name": "CloudConvert",
        "category": "04_오토메이션_Automation",
        "api_actions": [
            "convert_file",
            "create_job",
            "get_job",
            "list_jobs"
        ]
    },
    "cloudmersive.md": {
        "service_name": "Cloudmersive",
        "category": "04_오토메이션_Automation",
        "api_actions": [
            "validate_email",
            "convert_document",
            "virus_scan",
            "ocr_scan"
        ]
    },
    "convertapi.md": {
        "service_name": "ConvertAPI",
        "category": "04_오토메이션_Automation",
        "api_actions": [
            "convert",
            "get_info",
            "list_formats"
        ]
    },
    "convertio.md": {
        "service_name": "Convertio",
        "category": "04_오토메이션_Automation",
        "api_actions": [
            "convert",
            "get_status",
            "get_result",
            "get_usage"
        ]
    },
    "craftmypdf.md": {
        "service_name": "CraftMyPDF",
        "category": "04_오토메이션_Automation",
        "api_actions": [
            "create_pdf",
            "get_pdf",
            "list_templates"
        ]
    },
    "deepgram.md": {
        "service_name": "Deepgram",
        "category": "04_오토메이션_Automation",
        "api_actions": [
            "transcribe_audio",
            "get_transcript",
            "list_projects",
            "create_project"
        ]
    }
}


def load_progress():
    """Load progress file"""
    try:
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"completed": {}, "currentCategory": "Batch 34"}


def save_progress(progress):
    """Save progress file"""
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)


def update_progress():
    """Update progress file with Batch 34 implementations"""
    print("\n🔄 Updating progress file...")
    progress = load_progress()

    timestamp = subprocess.check_output(['date', '-u', '+%Y-%m-%dT%H:%M:%S.000000']).decode().strip()

    for service_file, info in SERVICE_CATEGORIES.items():
        service_name = info['service_name']
        safe_name = info['service_name'].lower().replace(' ', '-').replace('_', '-')
        category = info['category']
        actions = info['api_actions']

        # Get the actual folder name in repo
        service_folder = service_name.lower().replace(' ', '-', 1).replace('_-', '_')
        if '-' in service_folder:
            parts = service_folder.split('-')
            service_folder = parts[0] + ('-' + parts[1] if len(parts) > 1 else '')

        # Map special cases
        folder_name_map = {
            "zoho-mail": "zoho_mail",
            "zoho-sheet": "zoho_sheet",
            "zoho-writer": "zoho_writer",
            "techulus-push": "techulus_push",
            "bland-ai": "bland_ai",
            "browse-ai": "browse_ai",
            "cdata-connect": "cdata_connect",
            "craftmypdf": "craftmypdf"
        }
        if service_file in [k for k in folder_name_map.keys()]:
            actual_folder = folder_name_map.get(service_file.lower(), service_folder)
        else:
            actual_folder = service_folder

        # Check if folder exists
        if not (REPO_DIR / actual_folder).exists():
            # Try matching folder name
            for existing in REPO_DIR.iterdir():
                if existing.is_dir() and actual_folder.lower() in existing.name.lower():
                    actual_folder = existing.name
                    break

        api_actions = {}
        for action in actions:
            method_name = action.replace('_', '-').lower()
            api_actions[action] = {
                "status": "completed",
                "testable": True,
                "code_file": f"github/skill-factory/repo/{actual_folder}/{actual_folder}_client.py",
                "method": f"{actual_folder.replace('-', '_')}_client.{action}()",
                "implemented_at": timestamp
            }

        progress['completed'][service_file] = {
            "service_name": service_name,
            "category": category,
            "integration_type": "api_key",
            "integration_confidence": "high",
            "api_actions": api_actions,
            "triggers": {},
            "implemented_at": timestamp
        }

        print(f"  ✅ Updated {service_name}")

    progress['currentCategory'] = "Batch 34 Completed - 30 Yoom Services"
    save_progress(progress)
    print("\n✅ Progress file updated successfully!")


if __name__ == "__main__":
    update_progress()