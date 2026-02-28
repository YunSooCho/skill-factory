#!/usr/bin/env python3
"""
Script to rebuild the complete Yoom Automation Progress file by scanning all repo/ folders.
"""

import os
import re
import json
import ast
from datetime import datetime
from pathlib import Path
import glob

REPO_DIR = "/Users/clks001/.openclaw/workspace/github/skill-factory/repo"
PROGRESS_FILE = "/Users/clks001/.openclaw/workspace/github/skill-factory/yoom-automation-progress.json"

# Category mapping based on folder names or naming patterns
CATEGORY_PATTERNS = {
    # Marketing
    'woodpecker': '01_마케팅_Marketing',
    'wooxy': '01_마케팅_Marketing',
    'x-oauth': '01_마케팅_Marketing',
    'youtube': '01_마케팅_Marketing',
    'youtube-data': '01_마케팅_Marketing',
    'zerobounce': '01_마케팅_Marketing',
    'zixflow': '01_마케팅_Marketing',
    # Sales
    'salesflare': '02_세일스_Sales',
    'salesforce': '02_세일스_Sales',
    'saleslens': '02_세일스_Sales',
    'salesmate': '02_세일스_Sales',
    'sasuke-lead': '02_세일스_Sales',
    'smslink': '02_세일스_Sales',
    'snov-io': '02_세일스_Sales',
    'synthflow-ai': '02_세일스_Sales',
    'teachable': '02_세일스_Sales',
    'zendesk-sell': '02_세일스_Sales',
    'zoho-bigin': '02_세일스_Sales',
    'zoom-phone': '02_세일스_Sales',
}

def extract_methods_from_file(file_path):
    """Extract API methods from a Python client file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse the file as AST
        tree = ast.parse(content)

        methods = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and not node.name.startswith('_'):
                # Skip internal methods
                if node.name in ['__init__', '__aenter__', '__aexit__']:
                    continue
                methods.append(node.name)

        return methods
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return []

def get_category(service_name):
    """Determine category based on service name"""
    # First check explicit mapping
    for pattern, category in CATEGORY_PATTERNS.items():
        if pattern.lower() in service_name.lower():
            return category

    # Default categorization based on common patterns
    sales_keywords = ['sales', 'crm', 'lead', 'contact', 'deal', 'opportunity',
                      'zoho', 'sf', 'close', 'capsule', 'cloze', 'cogmento',
                      'hubspot', 'pipedrive', 'insightly', 'monday']
    marketing_keywords = ['mail', 'email', 'campaign', 'newsletter', 'send',
                          'mailchimp', 'brevo', 'convertkit', 'activecampaign',
                          'mailgun', 'sendgrid', 'wooxy', 'woodpecker']
    general_keywords = ['google', 'slack', 'zoom', 'meet', 'calendar', 'docs',
                       'drive', 'sheets', 'notion', 'trello', 'asana']

    service_lower = service_name.lower()

    for keyword in sales_keywords:
        if keyword in service_lower:
            return '02_세일스_Sales'

    for keyword in marketing_keywords:
        if keyword in service_lower:
            return '01_마케팅_Marketing'

    for keyword in general_keywords:
        if keyword in service_lower:
            return '03_업무일반_General'

    return '03_업무일반_General'  # Default

def format_method_name(method_name):
    """Convert method_name to readable API action name"""
    # Convert snake_case to Title Case with spaces
    words = method_name.replace('_', ' ').split()
    return ' '.join(word.capitalize() for word in words)

def extract_triggers(file_path):
    """Try to extract trigger information from client file"""
    triggers = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Look for trigger-related classes or methods
        if 'trigger' in content.lower() or 'webhook' in content.lower():
            # Search for webhooks or event handlers
            webhook_match = re.search(r'class.*[Ww]ebhook.*:', content)
            if webhook_match:
                triggers['webhook'] = {
                    'status': 'completed',
                    'testable': False,
                    'test_method': 'Webhook endpoint implemented',
                    'code_file': file_path.split('github/')[-1]
                }

    except Exception as e:
        pass

    return triggers

def build_service_entry(service_dir, client_file):
    """Build a complete service entry for progress file"""
    service_name = service_dir.replace('-', ' ').replace('_', ' ')
    service_name = ' '.join(word.capitalize() for word in service_name.split())

    # Extract methods
    methods = extract_methods_from_file(client_file)

    # Extract triggers
    triggers = extract_triggers(client_file)

    # Build api_actions
    api_actions = {}
    for method in methods:
        action_name = format_method_name(method)
        api_actions[action_name] = {
            'status': 'completed',
            'testable': True,
            'test_method': 'API 호출 필요 - 인증 키로 테스트',
            'code_file': f"repo/{service_dir}/{os.path.basename(client_file)}",
            'method': f"{service_name.replace(' ', '')}Client.{method}"
        }

    # Determine category
    category = get_category(service_dir)

    return {
        'service_name': service_name,
        'category': category,
        'integration_type': 'api_key',
        'integration_confidence': 'high',
        'integration_reasoning': 'Python client implementation with standard API authentication',
        'api_actions': api_actions,
        'triggers': triggers,
        'implemented_at': datetime.fromtimestamp(os.path.getmtime(client_file)).isoformat(),
        'analyzed_at': datetime.utcnow().isoformat(),
        'required_tasks': [
            {
                'task': 'API 문서 검토',
                'priority': 'high',
                'description': f'{service_name} API 문서 확인',
                'status': 'completed'
            },
            {
                'task': 'API 클라이언트 구현',
                'priority': 'high',
                'description': f'{service_name} Python 클라이언트 구현 완료',
                'status': 'completed'
            },
            {
                'task': '테스트 및 검증',
                'priority': 'medium',
                'description': '실제 API 계정을 통한 기능 테스트',
                'status': 'pending'
            }
        ]
    }

def main():
    # Scan all repo directories
    all_services = {}
    completed_count = 0

    for service_dir in sorted(os.listdir(REPO_DIR)):
        service_path = os.path.join(REPO_DIR, service_dir)

        if not os.path.isdir(service_path):
            continue

        # Find client file (look for *_client.py or client.py)
        client_files = glob.glob(os.path.join(service_path, '*_client.py'))
        if not client_files:
            client_files = glob.glob(os.path.join(service_path, 'client.py'))

        if not client_files:
            print(f"Warning: No client file found in {service_dir}")
            continue

        client_file = client_files[0]
        print(f"Processing: {service_dir}")

        # Build service entry
        md_key = f"{service_dir}.md"
        service_entry = build_service_entry(service_dir, client_file)
        all_services[md_key] = service_entry
        completed_count += 1

    # Create progress file structure
    progress_data = {
        'currentCategory': '03_업무일반_General',
        'completed': all_services,
        'total_services': 749,
        'completed_services': completed_count,
        'progress_percentage': round((completed_count / 749) * 100, 2)
    }

    # Write to progress file
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress_data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Progress file rebuilt successfully!")
    print(f"   Total services: 749")
    print(f"   Completed services: {completed_count}")
    print(f"   Progress: {progress_data['progress_percentage']}%")

if __name__ == '__main__':
    main()