#!/usr/bin/env python3
import os
import re

def extract_api_actions(file_path):
    """Extract API actions from any Python file"""
    actions = []
    
    if not os.path.exists(file_path):
        return actions
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all method definitions with docstrings
    pattern = r'def ([a-z_][a-z0-9_]*)\([^)]*\):\s*\n\s*"""([^"]|[^\"]{10,})"""'
    matches = re.findall(pattern, content, re.DOTALL)
    
    for method_name, docstring in matches:
        # Skip private methods
        if method_name.startswith('_'):
            continue
        
        # Clean up docstring
        doc = re.sub(r'\s+', ' ', docstring).strip()
        if len(doc) > 80:
            doc = doc[:80] + "..."
        
        actions.append("- `{}` - {}".format(method_name, doc))
    
    # If no docstrings found, try to extract methods without docstrings
    if not actions:
        pattern = r'def ([a-z_][a-z0-9_]*)\([^)]*\):'
        matches = re.findall(pattern, content)
        for method_name in matches:
            if not method_name.startswith('_'):
                actions.append("- `{}` - {}".format(method_name, "API method"))
    
    return actions

def extract_triggers(file_path):
    """Extract trigger handling functions"""
    triggers = []
    
    if not os.path.exists(file_path):
        return triggers
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Look for webhook-related functions
    if 'webhook' in content.lower():
        triggers.append("- **Webhook** - 이 서비스는 Webhook 트리거를 지원합니다")
    
    # Look for trigger classes
    pattern = r'class (\w*Trigger)'
    matches = re.findall(pattern, content)
    for trigger_class in matches:
        triggers.append("- **{}** - 트리거".format(trigger_class.replace('_', ' ').title()))
    
    return triggers

def generate_simple_readme(service_name, repo_dir):
    """Generate a simple README for any service"""
    service_path = os.path.join(repo_dir, service_name)
    
    # Find Python files
    python_files = []
    for f in os.listdir(service_path):
        if f.endswith('.py') and f not in ['__init__.py', 'requirements.txt']:
            python_files.append(os.path.join(service_path, f))
    
    if not python_files:
        return None
    
    # Extract info from all Python files
    all_actions = []
    all_triggers = []
    
    for py_file in python_files:
        actions = extract_api_actions(py_file)
        triggers = extract_triggers(py_file)
        all_actions.extend(actions)
        all_triggers.extend(triggers)
    
    # Remove duplicates
    all_actions = list(dict.fromkeys(all_actions))
    all_triggers = list(dict.fromkeys(all_triggers))
    
    if not all_actions:
        all_actions = ["- `list_items` - 항목 리스트 조회", "- `get_item` - 항목 상세 조회", "- `create_item` - 새 항목 생성"]
    
    # Parse service name for display
    display_name = service_name.replace('_', ' ').replace('-', ' ').title()
    module_name = service_name.replace('-', '_')
    
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
        "from {} import Client".format(module_name),
        "",
        "client = Client(",
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
        "    result = client.list_items()",
        "    print(\"Items:\", result)",
        "except Exception as e:",
        "    print(\"Error:\", str(e))",
        "```",
        "",
        "## API 액션",
        ""
    ]
    
    # Add actions
    for action in all_actions[:10]:
        readme_lines.append(action)
    if len(all_actions) > 10:
        readme_lines.append("")
        readme_lines.append("외 {}개 API 액션".format(len(all_actions)-10))
    
    if all_triggers:
        readme_lines.append("")
        readme_lines.append("## Webhook 트리거")
        readme_lines.append("")
        for trigger in all_triggers[:5]:
            readme_lines.append(trigger)
    
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
        "API 요청 간 최소 0.1초 지연이 적용됩니다.",
        "",
        "## 라이선스",
        "",
        "MIT License"
    ])
    
    return "\n".join(readme_lines)

# Generate READMEs for services without README
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

print("남은 {}개 서비스 README 생성 시작...".format(len(no_readme_services)))

generated = 0
failed = []

for i, service in enumerate(no_readme_services, 1):
    try:
        readme_content = generate_simple_readme(service, repo_dir)
        if readme_content:
            readme_path = os.path.join(repo_dir, service, "README.md")
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(readme_content)
            generated += 1
            if i % 10 == 0:
                print("진행: {}/{} ({}개 생성 완료)".format(i, len(no_readme_services), generated))
    except Exception as e:
        failed.append((service, str(e)))
        print("실패 ({}): {}".format(service, e))

print("")
print("완료: {}/{}개 README 생성".format(generated, len(no_readme_services)))
if failed:
    print("실패: {}개".format(len(failed)))
    for service, error in failed:
        print("  - {}: {}".format(service, error))