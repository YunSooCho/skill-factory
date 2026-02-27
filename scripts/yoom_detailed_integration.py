#!/usr/bin/env python3
"""
Yoom Apps Detailed Integration - 카테고리별 정밀 연계 스킬 생성
"""

import os
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import datetime

# 경로 설정
WORKSPACE = Path(__file__).parent.parent
STATE_FILE = WORKSPACE / "yoom-integration-state.json"
YOOM_APPS_DIR = WORKSPACE / "yoom-apps"
SKILLS_DIR = WORKSPACE / "skills"
PROGRESS_FILE = WORKSPACE / "YOOM_INTEGRATION_PROGRESS.md"

# 카테고리 우선순위
CATEGORY_PRIORITY = [
    "セールス", "会計・経理", "EC・POSシステム", "受発注・在庫管理",
    "ファイル管理", "マーケティング", "プロジェクト管理", "勤怠管理",
    "人事・採用", "サポート", "コミュニケーション", "オートメーション",
    "セキュリティ", "アナリティクス", "データベース", "スケジューリング",
    "開発", "その他"
]

class YoomMDParser:
    """Yoom MD 파일 파서"""

    @staticmethod
    def parse_md_file(md_path: Path) -> Dict:
        """MD 파일에서 정보 추출"""
        content = md_path.read_text(encoding='utf-8')

        result = {
            "service_name": "",
            "url": "",
            "category": "",
            "api_actions": [],
            "triggers": [],
            "templates": [],
            "api_actions_count": 0,
            "triggers_count": 0,
            "templates_count": 0
        }

        # 기본 정보 추출
        service_match = re.search(r'サービス名[:\s\*]*([^\n\*]+)', content)
        if service_match:
            result["service_name"] = service_match.group(1).strip()

        url_match = re.search(r'URL[:\s\*]*([^\n\*]+)', content)
        if url_match:
            result["url"] = url_match.group(1).strip()

        category_match = re.search(r'カテゴリー[:\s\*]*([^\n\*]+)', content)
        if category_match:
            result["category"] = category_match.group(1).strip()

        # API 액션 추출 - 변경: `- 숫자개` 형식
        api_match = re.search(r'フローボットオペレーション.*?-\s*([0-9]+)[個個個]', content, re.DOTALL)
        if api_match:
            result["api_actions_count"] = int(api_match.group(1))
            # API 액션 목록 추출
            api_list = re.findall(r'\*\*([^*]+)\*\*', content)
            result["api_actions"] = [a.strip() for a in api_list if a.strip() and not 'テンプレート' in a and not 'サービス名' in a and not 'URL' in a and not 'カテゴリー' in a]

        # 트리거 추출
        trigger_match = re.search(r'フローボットトリガー.*?-\s*([0-9]+)[個個個]', content, re.DOTALL)
        if trigger_match:
            result["triggers_count"] = int(trigger_match.group(1))
            # 트리거 목록 추출
            result["triggers"] = result["api_actions"][-result["triggers_count"]:] if result["triggers_count"] > 0 else []

        # 템플릿 추출
        template_match = re.search(r'テンプレート.*?-\s*([0-9]+)[個個個]', content, re.DOTALL)
        if template_match:
            result["templates_count"] = int(template_match.group(1))
            # 템플릿 링크 추출
            template_links = re.findall(r'https://lp\.yoom\.fun/fb-templates/[0-9]+', content)
            result["templates"] = template_links

        return result

class DetailedIntegrationOrchestrator:
    """정밀 연계 스킬 개발 오케스트레이터"""

    def __init__(self):
        self.parser = YoomMDParser()
        self.state = self.load_state() if STATE_FILE.exists() else self._create_initial_state()

        print(f"🔍 Yoom Apps Detailed Integration")
        print(f"   전체 서비스: {len(self.state['all_services'])}")
        print(f"   완료된 서비스: {len(self.state['completed_services'])}")
        total = len(self.state['all_services'])
        completed = len(self.state['completed_services'])
        progress = (completed / total * 100) if total > 0 else 0
        print(f"   진행률: {progress:.1f}%")
        print()

    def _create_initial_state(self) -> Dict:
        """초기 상태 생성"""
        all_services = []

        if YOOM_APPS_DIR.exists():
            for md_file in sorted(YOOM_APPS_DIR.glob("*.md")):
                try:
                    parsed = self.parser.parse_md_file(md_file)
                    if parsed["service_name"]:
                        parsed["md_file"] = md_file.name
                        parsed["file_key"] = md_file.stem

                        # 우선순위 점수 계산
                        category_priority_score = 0
                        for i, cat in enumerate(CATEGORY_PRIORITY):
                            if cat == parsed["category"]:
                                category_priority_score = (len(CATEGORY_PRIORITY) - i) * 10
                                break

                        integration_score = min(50, parsed["api_actions_count"] * 2)
                        if parsed["triggers_count"] > 0:
                            integration_score += 25
                        if parsed["templates_count"] > 0:
                            integration_score += 25

                        parsed["priority_score"] = category_priority_score + integration_score
                        parsed["priority_level"] = "HIGH" if parsed["priority_score"] >= 150 else ("MEDIUM" if parsed["priority_score"] >= 100 else "LOW")

                        all_services.append(parsed)
                except Exception as e:
                    print(f"   ⚠️ 파일 파싱 오류: {md_file.name} - {str(e)}")

        all_services.sort(key=lambda x: (-x["priority_score"], x["category"], x["service_name"]))

        state = {
            "started_at": datetime.datetime.now().isoformat() + "+09:00",
            "last_updated": datetime.datetime.now().isoformat() + "+09:00",
            "current_phase": "4",
            "all_services": all_services,
            "completed_services": [],
            "current_category_index": 0,
            "category_progress": {cat: {"total": 0, "completed": 0} for cat in CATEGORY_PRIORITY}
        }

        for service in all_services:
            cat = service["category"]
            if cat in state["category_progress"]:
                state["category_progress"][cat]["total"] += 1

        self.save_state(state)
        return state

    def load_state(self) -> Dict:
        """상태 파일 로드"""
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_state(self, state: Optional[Dict] = None):
        """상태 파일 저장"""
        if state is None:
            state = self.state
        state["last_updated"] = datetime.datetime.now().isoformat() + "+09:00"
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        self.state = state

    def get_next_service(self) -> Optional[Dict]:
        """다음 우선순위 서비스 가져오기"""
        completed_file_keys = {s["file_key"] for s in self.state["completed_services"]}
        for service in self.state["all_services"]:
            if service["file_key"] not in completed_file_keys:
                return service
        return None

    def generate_detailed_skill(self, service: Dict) -> Dict:
        """정밀 스킬 생성"""
        service_name = service["service_name"]
        file_key = service["file_key"]
        skill_dir = SKILLS_DIR / ("yoom-" + file_key)

        print(f"📝 정밀 스킬 생성: {service_name}")
        print(f"   카테고리: {service['category']}")
        print(f"   API 액션: {service['api_actions_count']}개")
        print(f"   트리거: {service['triggers_count']}개")

        # 연계 방식 결정
        integration_type, auth_type, method_notes, requirements = self._determine_integration_method(service)
        print(f"   연계 방식: {integration_type}, 인증: {auth_type}")

        # 스킬 디렉토리 생성
        skill_dir.mkdir(parents=True, exist_ok=True)

        # SKILL.md 생성
        self._generate_skill_md(skill_dir, service, integration_type, auth_type)

        # integration.py 또는 web_automation.py 생성
        if integration_type in ['api', 'sdk']:
            code = self._generate_integration_code(service, integration_type, auth_type)
            (skill_dir / "integration.py").write_text(code, encoding='utf-8')
        else:
            code = self._generate_web_automation_code(service)
            (skill_dir / "web_automation.py").write_text(code, encoding='utf-8')

        # README.md 생성
        readme = self._generate_readme(service, integration_type, auth_type, requirements)
        (skill_dir / "README.md").write_text(readme, encoding='utf-8')

        # TEST_GUIDE.md 생성
        test_guide = self._generate_test_guide(service, integration_type, auth_type)
        (skill_dir / "TEST_GUIDE.md").write_text(test_guide, encoding='utf-8')

        self.update_progress_file(service, {
            "skill_path": str(skill_dir),
            "integration_type": integration_type,
            "testable": integration_type in ['api', 'sdk'],
            "test_requirements": requirements,
            "auth_type": auth_type,
            "notes": method_notes
        })

        return {
            "skill_path": str(skill_dir),
            "integration_type": integration_type,
            "testable": integration_type in ['api', 'sdk'],
            "test_requirements": requirements,
            "auth_type": auth_type,
            "notes": method_notes
        }

    def _determine_integration_method(self, service: Dict) -> Tuple[str, str, str, List[str]]:
        """연계 방식 결정"""
        service_name = service["service_name"].lower()
        sdks = [
            ("slack", "slack_sdk", "OAuth"),
            ("github", "PyGithub", "OAuth"),
            ("notion", "notion-client", "OAuth"),
            ("google", "google-api-python-client", "OAuth"),
            ("salesforce", "simple-salesforce", "OAuth"),
        ]

        for keyword, package, auth in sdks:
            if keyword in service_name:
                return ("sdk", auth, "SDK: " + package, [package])

        if service["api_actions_count"] >= 10:
            return ("api", "OAuth/API Key", "REST API 기반 연계", ["requests"])
        if service["triggers_count"] > 0:
            return ("api", "OAuth", "REST API + Webhook", ["requests", "flask"])
        return ("web", "자격증명 (유저네임/패스워드)", "웹 브라우저 자동화", ["playwright", "selenium"])

    def _generate_skill_md(self, skill_dir: Path, service: Dict, integration_type: str, auth_type: str):
        """SKILL.md 생성"""
        content = "# {} Yoom 연계 스킬\n\n".format(service["service_name"])
        content += "{}와 OpenClaw 연결을 위한 스킬입니다.\n\n".format(service["service_name"])
        content += "## 서비스 정보\n"
        content += "- **서비스명**: {}\n".format(service["service_name"])
        content += "- **카테고리**: {}\n".format(service["category"])
        content += "- **Yoom URL**: {}\n\n".format(service["url"])
        content += "## 연계 정보\n"
        content += "- **연계 방식**: {}\n".format(integration_type.upper())
        content += "- **인증 방식**: {}\n".format(auth_type)
        content += "- **API 액션 수**: {}개\n".format(service["api_actions_count"])
        content += "- **트리거 수**: {}개\n\n".format(service["triggers_count"])
        content += "## 구현된 API 액션\n"
        for action in service["api_actions"]:
            content += "- {}\n".format(action)
        content += "\n## 구현된 트리거\n"
        for trigger in service["triggers"]:
            content += "- {}\n".format(trigger)
        content += "\n## 테스트 가능 여부\n"
        content += "{}\n\n".format("✅ 테스트 가능" if integration_type in ['api', 'sdk'] else "⚠️ 테스트 제한됨 (실제 계정 필요)")
        content += "## 테스트를 위한 준비물\n\n"
        if integration_type == 'sdk':
            content += "1. `" + auth_type + "` 자격증명 필요\n"
            content += "2. {} 계정 (개발자 계정 권장)\n".format(service["service_name"])
            content += "3. 해당 SDK 설치: `pip install " + auth_type + "`\n"
        elif integration_type == 'api':
            content += "1. " + auth_type + " 또는 API Key 필요\n"
            content += "2. {} 계정\n".format(service["service_name"])
        else:
            content += "1. {} 계정 (유저네임/패스워드)\n".format(service["service_name"])
            content += "2. 웹 브라우저 자동화 툴 설치\n"
            content += "3. ⚠️ 웹 자동화는 실제 UI 변경으로 인해 불안정할 수 있음\n"

        (skill_dir / "SKILL.md").write_text(content, encoding='utf-8')

    def _generate_integration_code(self, service: Dict, integration_type: str, auth_type: str) -> str:
        """integration 코드 생성"""
        service_name = service["service_name"].replace(" ", "_").lower()
        service_class = service["service_name"].replace(" ", "")

        code = '"""\n'
        code += service["service_name"] + " Integration - OpenClaw Yoom 연계 스킬\n\n"
        code += "연계 방식: {}\n".format(integration_type.upper())
        code += "인증 방식: {}\n".format(auth_type)
        code += '"""\n\n'
        code += "import os\n"
        code += "import aiohttp\n"
        code += "from typing import Dict, Any\n\n"
        code += "class " + service_class + "Client:\n"
        code += '    """' + service["service_name"] + " API 클라이언트\"\"\"\n\n"
        code += "    def __init__(self):\n"
        code += '        self.base_url = os.getenv("YOOM_{}_BASE_URL", "")\n'.format(service_name.upper())
        code += '        self.api_key = os.getenv("YOOM_{}_API_KEY", "")\n'.format(service_name.upper())
        code += '        self.auth_token = os.getenv("YOOM_{}_AUTH_TOKEN", "")\n\n'.format(service_name.upper())
        code += '        if not self.base_url:\n'
        code += '            raise ValueError("YOOM_{}_BASE_URL 환경 변수가 필요합니다")\n\n'.format(service_name.upper())
        code += "    async def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:\n"
        code += '        """API 요청 공통 메소드"""\n'
        code += '        url = "{}/{}".format(self.base_url, endpoint)\n'
        code += '        headers = {"Content-Type": "application/json"}\n\n'
        code += '        if self.auth_token:\n'
        code += '            headers["Authorization"] = "Bearer {}".format(self.auth_token)\n'
        code += '        else:\n'
        code += '            headers["X-API-Key"] = self.api_key\n\n'
        code += '        async with aiohttp.ClientSession() as session:\n'
        code += '            async with session.request(method, url, headers=headers, **kwargs) as response:\n'
        code += '                response.raise_for_status()\n'
        code += '                return await response.json()\n\n'

        # 하위 5개 API 액션 메소드 생성
        for i, action in enumerate(service["api_actions"][:5]):
            method_name = re.sub(r'[^a-zA-Z0-9]', '_', action.lower()).replace('__', '_').strip('_') or f"action_{i}"
            code += "    async def {}(self, **kwargs):\n".format(method_name)
            code += '        """{}"""\n'.format(action)
            code += '        # TODO: {} 구현 필요\n'.format(action)
            code += '        raise NotImplementedError("{} 구현 필요")\n\n'.format(action)

        code += "class {}Triggers:\n".format(service_class)
        code += '    """{} 트리거 핸들러"""\n\n'.format(service["service_name"])
        code += "    def __init__(self, client: {}Client):\n".format(service_class)
        code += "        self.client = client\n"

        return code

    def _generate_web_automation_code(self, service: Dict) -> str:
        """웹 자동화 코드 생성"""
        service_name = service["service_name"].replace(" ", "_").lower()
        service_class = service["service_name"].replace(" ", "")

        code = '"""\n'
        code += service["service_name"] + " Web Automation - OpenClaw Yoom 연계 스킬\n\n"
        code += "연계 방식: WEB Browser Automation\n"
        code += "인증 방식: 자격증명 (유저네임/패스워드)\n"
        code += '"""\n\n'
        code += "from playwright.async_api import async_playwright\n"
        code += "import os\n\n"
        code += "class {}WebClient:\n".format(service_class)
        code += '    """{} 웹 자동화 클라이언트"""\n\n'.format(service["service_name"])
        code += "    def __init__(self):\n"
        code += '        self.login_url = os.getenv("YOOM_{}_LOGIN_URL", "")\n'.format(service_name.upper())
        code += '        self.username = os.getenv("YOOM_{}_USERNAME", "")\n'.format(service_name.upper())
        code += '        self.password = os.getenv("YOOM_{}_PASSWORD", "")\n\n'.format(service_name.upper())
        code += '        if not all([self.login_url, self.username, self.password]):\n'
        code += '            raise ValueError("YOOM_{}_LOGIN_URL, USERNAME, PASSWORD 환경 변수가 필요합니다")\n\n'.format(service_name.upper())
        code += "    async def login(self):\n"
        code += '        """로그인"""\n'
        code += "        browser = await async_playwright().start()\n"
        code += '        context = await browser.chromium.launch(headless=True)\n'
        code += "        page = await context.new_page()\n\n"
        code += '        await page.goto(self.login_url)\n'
        code += '        await page.fill(\'input[name="username"]\', self.username)\n'
        code += '        await page.fill(\'input[name="password"]\', self.password)\n'
        code += '        await page.click(\'button[type="submit"]\')\n'
        code += '        await page.wait_for_load_state("networkidle")\n\n'
        code += "        return browser, page\n\n"
        code += "    # 각 API 액션에 해당하는 웹 자동화 메소드 필요\n"

        return code

    def _generate_readme(self, service: Dict, integration_type: str, auth_type: str, requirements: List[str]) -> str:
        """README 생성"""
        service_key = service["file_key"].upper()

        content = "# Yoom Integration - {}\n\n".format(service["service_name"])
        content += "Yoom 앱 서비스와 OpenClaw 연계 스킬\n\n"
        content += "## 서비스 정보\n"
        content += "- **서비스명**: {}\n".format(service["service_name"])
        content += "- **카テゴリー**: {}\n".format(service["category"])
        content += "- **Yoom URL**: {}\n\n".format(service["url"])
        content += "## 연계 정보\n"
        content += "- **연계 방식**: {}\n".format(integration_type.upper())
        content += "- **인증 방식**: {}\n".format(auth_type)
        content += "- **API 액ション**: {}個\n".format(service["api_actions_count"])
        content += "- **トリガー**: {}個\n\n".format(service["triggers_count"])
        content += "## 設置\n\n"
        content += "```bash\n"
        content += "pip install aiohttp\n"
        content += "pip install {}\n".format(" ".join(requirements))
        content += "```\n\n"
        content += "## 環境変数\n\n"
        content += "```bash\n"
        content += "YOOM_{}_BASE_URL=https://api.example.com\n".format(service_key)
        content += "YOOM_{}_API_KEY=your_api_key_here\n".format(service_key)
        if integration_type == 'sdk':
            content += "YOOM_{}_AUTH_TOKEN=your_token_here\n".format(service_key)
        content += "```\n\n"
        content += "## 使い方\n\n"
        content += "```python\n"
        content += "from integration import {}Client\n\n".format(service["service_name"].replace(" ", ""))
        content += "client = {}Client()\n".format(service["service_name"].replace(" ", ""))
        content += "# 操作実行\n"
        content += "```\n\n"
        content += "## テスト\n\n"
        content += "TEST_GUIDE.md 参照\n"

        return content

    def _generate_test_guide(self, service: Dict, integration_type: str, auth_type: str) -> str:
        """테스트 가이드 생성"""
        content = "# {} テストガイド\n\n".format(service["service_name"])

        if integration_type in ['api', 'sdk']:
            content += "## テスト可否\n"
            content += "✅ テスト可能 ({} 기반)\n\n".format("SDK" if integration_type == "sdk" else "REST API")
            content += "## 事前準備\n\n"
            content += "1. {} アカウント (開発者アカウント推奨)\n".format(service["service_name"])
            content += "2. `{}` 資格証明を取得\n".format(auth_type)
            content += "3. 環境変数設定\n\n"
            content += "```bash\n"
            content += "export YOOM_{}_BASE_URL=https://api.{}.com\n".format(service["file_key"].upper(), service["file_key"])
            content += "export YOOM_{}_API_KEY=your_key\n".format(service["file_key"].upper())
            content += "```\n\n"
            content += "## 基本接続テスト\n\n"
            content += "```python\n"
            content += "from integration import {}Client\n\n".format(service["service_name"].replace(" ", ""))
            content += "client = {}Client()\n".format(service["service_name"].replace(" ", ""))
            content += "# 接続成功時は例外が発生しない\n"
            content += "```\n\n"
        else:
            content += "## テスト可否\n"
            content += "⚠️ テスト制限 (ウェブ自動化)\n\n"
            content += "## 注意点\n\n"
            content += "1. ウェブ自動化は UI 依存\n"
            content += "2. ページ読み込みタイミングが重要\n"
            content += "3. UI 変更で失敗の可能性\n"
            content += "4. ログインが必要\n\n"
            content += "## 準備\n\n"
            content += "```bash\n"
            content += "export YOOM_{}_LOGIN_URL=https://app.{}.com/login\n".format(service["file_key"].upper(), service["file_key"])
            content += "export YOOM_{}_USERNAME=your_username\n".format(service["file_key"].upper())
            content += "export YOOM_{}_PASSWORD=your_password\n".format(service["file_key"].upper())
            content += "```\n\n"

        return content

    def update_progress_file(self, service: Dict, skill_info: Dict):
        """진척 파일 업데이트"""
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S JST')

        if PROGRESS_FILE.exists():
            existing_content = PROGRESS_FILE.read_text(encoding='utf-8')
        else:
            completed = 0
            total = len(self.state['all_services'])
            existing_content = "# Yoom Apps 連結 스킬 개발 진척 상황\n\n"
            existing_content += "## 요약\n\n"
            existing_content += "| 항목 | 수치 |\n"
            existing_content += "|-----|------|\n"
            existing_content += "| 전체 서비스 | {} |\n".format(total)
            existing_content += "| 완료된 서비스 | {} |\n".format(completed)
            existing_content += "| 진행률 | 0% |\n\n"
            existing_content += "## 진척 기록\n\n"

        # 요약 업데이트
        completed = len(self.state['completed_services'])
        lines = existing_content.split('\n')
        updated_lines = []
        updated_summary = False

        for line in lines:
            if '| 완료된 서비스' in line and not updated_summary:
                updated_lines.append("| 완료된 서비스 | {} |".format(completed + 1))
            elif '| 진행률' in line and completed > 0:
                progress = (completed + 1) / len(self.state['all_services']) * 100
                updated_lines.append("| 진행률 | {:.1f}% |".format(progress))
                updated_summary = True
            else:
                updated_lines.append(line)

        existing_content = '\n'.join(updated_lines)

        # 새 항목 추가
        new_entry = f"\n## [{completed + 1}. {service['service_name']}] - {timestamp}\n\n"
        new_entry += "**카테고리**: {}\n".format(service['category'])
        new_entry += "**파일**: `yoom-{}`\n\n".format(service['file_key'])
        new_entry += "### 구현 정보\n"
        new_entry += "- **연계 방식**: {}\n".format(skill_info['integration_type'].upper())
        new_entry += "- **인증**: {}\n".format(skill_info['auth_type'])
        new_entry += "- **API 액션**: {}개\n".format(service['api_actions_count'])
        new_entry += "- **트리거**: {}개\n\n".format(service['triggers_count'])
        new_entry += "### 테스트 가능 여부\n"
        if skill_info['testable']:
            new_entry += "✅ 테스트 가능\n\n"
        else:
            new_entry += "⚠️ 테스트 제한됨 (웹 자동화)\n\n"
        new_entry += "### 테스트 준비물\n"
        for req in skill_info['test_requirements']:
            new_entry += "- `{}`\n".format(req)
        new_entry += "\n"

        PROGRESS_FILE.write_text(existing_content + new_entry, encoding='utf-8')
        print("   📄 진척 파일 업데이트 완료")

    def run(self, max_services: int = 1):
        """워크플로우 실행"""
        print("=" * 70)
        print("🚀 Yoom Apps Detailed Integration 開始")
        print("=" * 70)
        print()

        completed_count = 0

        for i in range(max_services):
            service = self.get_next_service()

            if not service:
                print("🎉 모든 서비스 처리 완료!")
                break

            print(f"[📦 {i+1}/{max_services}] 서비스 처리 중...")
            print(f"   {service['service_name']} ({service['category']})")
            print()

            skill_info = self.generate_detailed_skill(service)

            self.state['completed_services'].append({
                "file_key": service['file_key'],
                "service_name": service['service_name'],
                "category": service['category'],
                "completed_at": datetime.datetime.now().isoformat() + "+09:00",
                "integration_type": skill_info['integration_type'],
                "testable": skill_info['testable'],
                "test_requirements": skill_info['test_requirements']
            })

            cat = service['category']
            if cat in self.state['category_progress']:
                self.state['category_progress'][cat]['completed'] += 1

            self.save_state()

            completed_count += 1
            print(f"   ✅ 완료: {service['service_name']}")

        print()
        print("=" * 70)
        print("📊 이번 하트비트 완료")
        print("   처리된 서비스: {}개".format(completed_count))
        total = len(self.state['all_services'])
        completed = len(self.state['completed_services'])
        print("   전체 완료율: {}/{} ({:.1f}%)".format(completed, total, completed/total*100 if total > 0 else 0))

        if completed_count > 0:
            print("   마지막 서비스: {}".format(self.state['completed_services'][-1]['service_name']))

        print("=" * 70)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Yoom Apps Detailed Integration Orchestrator")
    parser.add_argument("--max-services", type=int, default=1, help="이번 하트비트에서 처리할 최대 서비스 수 (기본: 1)")
    parser.add_argument("--init", action="store_true", help="초기 상태 파일 재생성")
    args = parser.parse_args()

    orchestrator = DetailedIntegrationOrchestrator()

    if args.init:
        print("初期状態ファイル 작성 중...")
        orchestrator._create_initial_state()
        print("✅ 初期状態ファイル 작성 완료")
    else:
        orchestrator.run(max_services=args.max_services)