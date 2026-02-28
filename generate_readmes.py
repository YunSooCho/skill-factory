#!/usr/bin/env python3
import os
import re

def extract_api_actions_from_client(file_path):
    """Extract API action methods from client.py"""
    actions = []
    
    if not os.path.exists(file_path):
        return actions
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all method definitions
    pattern = r'def ([a-z_]+)\(self[^)]*\):\s*\n\s*"""(.*?)"""'
    matches = re.findall(pattern, content, re.DOTALL)
    
    for method_name, docstring in matches:
        # Clean up docstring
        doc = re.sub(r'\s+', ' ', docstring).strip()
        actions.append("- `{}` - {}".format(method_name, doc[:80] + "..." if len(doc) > 80 else doc))
    
    return actions

def extract_triggers_info(file_path):
    """Extract trigger information"""
    triggers = []
    
    if not os.path.exists(file_path):
        return triggers
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for webhook functions
    patterns = [
        r'def ([a-z_]+_(?:trigger|handler))\(self[^)]*\):\s*\n\s*"""(.*?)"""',
        r'class (\w+Trigger)',
    ]
    
    found_triggers = False
    for pattern in patterns:
        matches = re.findall(pattern, content, re.DOTALL)
        for match in matches:
            found_triggers = True
            if len(match) == 1:
                trigger_class_name = match[0]
                triggers.append("- **{}** - 트리거".format(trigger_class_name.replace('_', ' ').title()))
            else:
                trigger_name, docstring = match
                doc = re.sub(r'\s+', ' ', docstring).strip()
                triggers.append("- **{}** - {}".format(trigger_name.replace('_', ' ').title(), doc[:60] + "..." if len(doc) > 60 else doc))
    
    if content.lower().count('webhook') > 2 and not triggers:
        triggers.append("- **Webhook** - 이 서비스는 Webhook 트리거를 지원합니다")
    
    return triggers

def generate_readme(service_name, repo_dir):
    """Generate README for a service"""
    service_path = os.path.join(repo_dir, service_name)
    
    # Find client file
    client_file = None
    possible_files = [
        os.path.join(service_path, "client.py"),
        os.path.join(service_path, service_name.replace('-', '_') + "_client.py"),
        os.path.join(service_path, service_name + "_client.py"),
        os.path.join(service_path, "main.py"),
    ]
    
    for f in possible_files:
        if os.path.exists(f):
            client_file = f
            break
    
    if not client_file:
        return None
    
    # Extract info
    actions = extract_api_actions_from_client(client_file)
    triggers_file = os.path.join(service_path, "triggers.py")
    triggers = extract_triggers_info(triggers_file) if os.path.exists(triggers_file) else []
    
    # Check for triggers in client file too
    try:
        with open(client_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if not triggers:
                triggers = extract_triggers_info(client_file)
    except:
        pass
    
    # Parse service name for display
    display_name = service_name.replace('_', ' ').replace('-', ' ').title()
    module_name = service_name.replace('-', '_')
    client_class = display_name.replace(' ', '')
    
    # Generate README
    readme_lines = [
        "# {} API 클라이언트".format(display_name),
        "",
        "{}를 위한 Python API 클라이언트입니다.".format(display_name),
        "",
        "## 개요",
        "",
        "이 클라이언트는 {} API에 접근하여 각종 CRUD 작업 및 이벤트 처리를 지원합니다.".format(display_name),
        "",
        "## 설치",
        "",
        "의존성 패키지:",
        "",
        "```bash",
        "pip install requests",
        "```",
        "",
        "또는:",
        "",
        "```bash",
        "pip install -r requirements.txt",
        "```",
        "",
        "## API 키 발급",
        "",
        "1. {} 개발자 포털에서 앱 생성".format(display_name),
        "2. API 키/토큰 발급",
        "3. 발급된 API 키/토큰 저장",
        "",
        "## 사용법",
        "",
        "### 초기화",
        "",
        "```python",
        "from {}.client import {}Client".format(module_name, client_class),
        "",
        "client = {}Client(".format(client_class),
        "    api_key=\"YOUR_API_KEY\",",
        "    timeout=30",
        ")",
        "```",
        "",
        "### 예시 코드",
        "",
        "```python",
        "# CRUD 작업",
        "try:",
        "    result = client.create_item({\"name\": \"test\"})",
        "    print(\"Created:\", result)",
        "except Exception as e:",
        "    print(\"Error:\", str(e))",
        "",
        "# 리스트 조회",
        "items = client.list_items()",
        "for item in items:",
        "    print(item['id'], item['name'])",
        "```",
        "",
        "## API 액션",
        ""
    ]
    
    # Add actions
    if actions:
        for action in actions[:10]:
            readme_lines.append(action)
        if len(actions) > 10:
            readme_lines.append("")
            readme_lines.append("외 {}개 API 액션".format(len(actions)-10))
    
    if triggers:
        readme_lines.append("")
        readme_lines.append("## Webhook 트리거")
        readme_lines.append("")
        for trigger in triggers[:5]:
            readme_lines.append(trigger)
        if len(triggers) > 5:
            readme_lines.append("")
            readme_lines.append("외 {}개 트리거".format(len(triggers)-5))
    
    readme_lines.extend([
        "",
        "## 에러 처리",
        "",
        "```python",
        "try:",
        "    result = client.your_method()",
        "except Exception as e:",
        "    print(\"Error:\", str(e))",
        "```",
        "",
        "## Rate Limiting",
        "",
        "API 요청 간 최소 0.1초 지연이 적용됩니다. 너무 많은 요청이 발생하면 Rate Limit 에러가 발생할 수 있습니다.",
        "",
        "## 라이선스",
        "",
        "MIT License"
    ])
    
    return "\n".join(readme_lines)

# Generate READMEs
repo_dir = "/Users/clks001/.openclaw/workspace/github/skill-factory/repo"
no_readme_services = []

# Get services without README
for service_dir in sorted(os.listdir(repo_dir)):
    dir_path = os.path.join(repo_dir, service_dir)
    if not os.path.isdir(dir_path):
        continue
    
    readme_path = os.path.join(dir_path, "README.md")
    if not os.path.exists(readme_path):
        no_readme_services.append(service_dir)

print("총 {}개 서비스 README 생성 시작...".format(len(no_readme_services)))

generated = 0
failed = []

for i, service in enumerate(no_readme_services, 1):
    try:
        readme_content = generate_readme(service, repo_dir)
        if readme_content:
            readme_path = os.path.join(repo_dir, service, "README.md")
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(readme_content)
            generated += 1
            if i % 20 == 0:
                print("진행: {}/{} ({}개 생성 완료)".format(i, len(no_readme_services), generated))
    except Exception as e:
        failed.append((service, str(e)))
        print("실패 ({}): {}".format(service, e))

print("")
print("완료: {}/{}개 README 생성".format(generated, len(no_readme_services)))
if failed:
    print("실패: {}개".format(len(failed)))
    for service, error in failed[:10]:
        print("  - {}: {}".format(service, error))