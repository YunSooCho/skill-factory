#!/usr/bin/env python3
"""
Yoom Apps Integration - 하트비트 워크플로우

하트비트마다 실행되어 다음 작업을 순차적으로 처리:
1. 현재 진행 상황 확인
2. 다음 서비스 조사/개발
3. 상태 업데이트
"""

import os
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional

# 경로 설정
WORKSPACE = Path(__file__).parent.parent
STATE_FILE = WORKSPACE / "yoom-integration-state.json"
INTEGRATION_DIR = WORKSPACE / "yoom-integration"
BATCH_FILE = INTEGRATION_DIR / "batch_config.json"
PRIORITIZED_FILE = INTEGRATION_DIR / "prioritized_services.json"
SKILLS_TEMPLATE = WORKSPACE / "skills" / "yoom-integration-template"

class IntegrationOrchestrator:
    """
    연계 스킬 개발 오케스트레이터
    """

    def __init__(self):
        self.state = self.load_state()
        print(f"🔍 Yoom Apps Integration Orchestrator")
        print(f"   현재 단계: {self.state['current_phase']}/7")
        print(f"   완료된 서비스: {len(self.state['stats']['services_completed'])}/{self.state['stats']['total_services']}")
        print()

    def load_state(self) -> Dict:
        """상태 파일 로드"""
        if STATE_FILE.exists():
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            raise FileNotFoundError("상태 파일이 존재하지 않습니다. 먼저 initialize.py를 실행하세요.")

    def save_state(self):
        """상태 파일 저장"""
        import datetime

        self.state["last_updated"] = datetime.datetime.now().isoformat() + "+09:00"
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2)

    def get_next_service(self) -> Optional[Dict]:
        """다음 서비스 가져오기"""
        # 완료된 서비스와 진행 중인 서비스 ID 추출
        completed_ids = set(s["file"] for s in self.state["stats"]["services_completed"])
        in_progress_ids = set(s["file"] for s in self.state["stats"]["services_in_progress"])

        # 우선순위 정렬된 서비스 로드
        with open(PRIORITIZED_FILE, 'r', encoding='utf-8') as f:
            all_services = json.load(f)

        # 완료/진행 중이 아닌 첫 번째 서비스 반환
        for service in all_services:
            if service["file"] not in completed_ids and service["file"] not in in_progress_ids:
                return service

        return None

    def research_service(self, service: Dict) -> Dict:
        """
        서비스 연계 가능성 조사

        Returns:
            {
                "can_automate": bool,
                "integration_method": "api|sdk|web",
                "auth_type": "oauth|api_key|token|none",
                "api_documentation": str,
                "sdk_package": str or None,
                "estimated_cost": "low|medium|high",
                "notes": str
            }
        """
        service_name = service["service_name"]
        yoom_url = service["url"]

        print(f"🔍 서비스 조사: {service_name}")
        print(f"   URL: {yoom_url}")

        research_result = {
            "service_name": service_name,
            "file": service["file"],
            "category": service["category"],
            "api_actions": service.get("api_actions", 0),
            "triggers": service.get("triggers", 0),
            "can_automate": False,
            "integration_method": "web",  # 기본값
            "auth_type": "none",
            "api_documentation": "",
            "sdk_package": None,
            "estimated_cost": "high",
            "notes": "",
            "researched_at": None
        }

        # 여기서 서비스별 API/SDK 존재 여부를 조사
        # 실제 구현 시에는 웹 스크래핑 또는 정적 파일에서 조사 결과 참고

        # 임시: API 액션 수가 많은 경우 API 기반으로 가정
        if service.get("api_actions", 0) >= 5:
            research_result["can_automate"] = True
            research_result["integration_method"] = "api"
            research_result["auth_type"] = "oauth"  # 임시
            research_result["estimated_cost"] = "low"
            research_result["notes"] = "API 액션 기반 연계 가능 (추정)"

        # 인기 서비스의 경우 SDK 존재 가정
        popular_sdks = {
            "slack": "slack_sdk",
            "github": "PyGithub",
            "notion": "notion-client",
            "google": "google-api-python-client",
            "aws": "boto3",
            "salesforce": "simple-salesforce",
            "zendesk": "zendesk-python-client"
        }

        for key, pkg in popular_sdks.items():
            if key.lower() in service_name.lower():
                research_result["integration_method"] = "sdk"
                research_result["sdk_package"] = pkg
                research_result["estimated_cost"] = "low"
                research_result["notes"] = f"SDK 존재: {pkg}"
                break

        import datetime
        research_result["researched_at"] = datetime.datetime.now().isoformat() + "+09:00"

        print(f"   연계 방식: {research_result['integration_method']}")
        print(f"   자동화 가능: {'✅' if research_result['can_automate'] else '❌'}")
        print(f"   추정 코스트: {research_result['estimated_cost']}")

        return research_result

    def create_skill(self, service: Dict, research: Dict) -> bool:
        """
        연계 스킬 생성

        Returns:
            성공 여부
        """
        service_name = research["service_name"]
        skill_folder = WORKSPACE / "skills" / f"yoom-{service_name.lower().replace(' ', '-')}"

        print(f"📝 스킬 생성: {service_name}")

        try:
            skill_folder.mkdir(parents=True, exist_ok=True)

            # 템플릿 파일 복사
            template_files = {
                "SKILL.md": "SKILL.md",
            }

            for src, dest in template_files.items():
                src_file = SKILLS_TEMPLATE / src
                dest_file = skill_folder / dest

                if src_file.exists():
                    content = src_file.read_text(encoding='utf-8')

                    # 템플릿 변수 치환
                    content = content.replace("{{SERVICE_NAME}}", service_name)
                    content = content.replace("{{SERVICE_CATEGORY}}", research["category"])
                    content = content.replace("{{INTEGRATION_TYPE}}", research["integration_method"])
                    content = content.replace("{{AUTH_TYPE}}", research["auth_type"])
                    content = content.replace("{{BASE_URL}}", research.get("api_documentation", ""))
                    content = content.replace("{{SDK_PACKAGE}}", research.get("sdk_package", ""))

                    dest_file.write_text(content, encoding='utf-8')

            # 연계 방식에 따른 코드 파일 복사
            if research["integration_method"] in ["api", "sdk"]:
                integration_template = SKILLS_TEMPLATE / "integration.py"
                dest_file = skill_folder / "integration.py"
                content = integration_template.read_text(encoding='utf-8')

                content = content.replace("{{SERVICE_NAME}}", service_name)
                content = content.replace("{{SERVICE_CATEGORY}}", research["category"])
                content = content.replace("{{INTEGRATION_TYPE}}", research["integration_method"])
                content = content.replace("{{AUTH_TYPE}}", research["auth_type"])
                content = content.replace("{{BASE_URL}}", research.get("api_documentation", ""))
                content = content.replace("{{SDK_PACKAGE}}", research.get("sdk_package", ""))

                dest_file.write_text(content, encoding='utf-8')
            elif research["integration_method"] == "web":
                web_template = SKILLS_TEMPLATE / "web_automation.py"
                dest_file = skill_folder / "web_automation.py"
                content = web_template.read_text(encoding='utf-8')

                content = content.replace("{{SERVICE_NAME}}", service_name)
                content = content.replace("{{SERVICE_CATEGORY}}", research["category"])
                content = content.replace("{{LOGIN_URL}}", research.get("api_documentation", ""))

                dest_file.write_text(content, encoding='utf-8')

            # README 생성
            readme_content = f"""# Yoom Integration - {service_name}

Yoom 앱 서비스와 OpenClaw 연계 스킬

## 서비스 정보
- **서비스명**: {service_name}
- **카테고리**: {research["category"]}
- **Yoom URL**: {service.get("url", "N/A")}

## 연계 방식
- **방식**: {research["integration_method"]}
- **인증**: {research["auth_type"]}
- **자동화 가능**: {"예" if research["can_automate"] else "아니오"}
- **추정 코스트**: {research["estimated_cost"]}

## 설치

### API 기반
```bash
pip install requests
# SDK 존재 시
pip install {research.get("sdk_package", "N/A")}
```

### 웹 조작 기반
```bash
pip install playwright
playwright install chromium

# 또는
pip install selenium
```

## 환경 변수

```
# API/SDK 기반
YOOM_{service_name.upper()}_API_KEY=your_api_key

# OAuth 기반
YOOM_{service_name.upper()}_OAUTH_TOKEN=your_token

# 웹 조작 기반
YOOM_{service_name.upper()}_USERNAME=your_username
YOOM_{service_name.upper()}_PASSWORD=your_password
```

## 사용법

### Python API

```python
from integration import Client

# 클라이언트 설정
client = Client()

# 항목 조회
items = client.list_items()

# 항목 생성
client.create_item({{"name": "test"}})
```

## 참고

- Yoom Apps: {service.get("url", "")}
"""

            (skill_folder / "README.md").write_text(readme_content, encoding='utf-8')

            print(f"   ✅ 스킬 생성 완료: {skill_folder}")
            return True

        except Exception as e:
            print(f"   ❌ 스킬 생성 실패: {str(e)}")
            return False

    def run(self, max_services: int = 1):
        """
        워크플로우 실행

        Args:
            max_services: 이번 하트비트에서 처리할 최대 서비스 수
        """
        print("=" * 60)
        print(f"🚀 Yoom Apps Integration 작업 시작")
        print("=" * 60)
        print()

        completed_count = 0

        for i in range(max_services):
            # 다음 서비스 가져오기
            service = self.get_next_service()

            if not service:
                print("🎉 모든 서비스 처리 완료!")
                break

            print(f"\n[{i+1}/{max_services}] 서비스 처리 중...")

            # 서비스 조사
            research = self.research_service(service)

            # 상태 업데이트 (진행 중)
            self.state["stats"]["services_in_progress"].append({
                "file": service["file"],
                "started_at": research["researched_at"]
            })
            self.save_state()

            # 스킬 생성
            success = self.create_skill(service, research)

            # 상태 업데이트
            if success:
                import datetime
                completed_info = {
                    "file": service["file"],
                    "service_name": research["service_name"],
                    "completed_at": datetime.datetime.now().isoformat() + "+09:00",
                    "integration_method": research["integration_method"],
                    "estimated_cost": research["estimated_cost"],
                    "status": "created"
                }

                self.state["stats"]["services_completed"].append(completed_info)
                self.state["stats"]["services_in_progress"] = [
                    s for s in self.state["stats"]["services_in_progress"]
                    if s["file"] != service["file"]
                ]

                # 배치 진행률 업데이트
                batch_progress = self.state["stats"]["batch_progress"]
                batch_progress["services_completed_in_current_batch"] += 1

                completed_count += 1
                print(f"   ✅ 서비스 처리 완료: {research['service_name']}")

            self.save_state()

        # 요약
        print()
        print("=" * 60)
        print(f"📊 이번 하트비트 완료")
        print(f"   처리된 서비스: {completed_count}개")
        print(f"   전체 완료율: {len(self.state['stats']['services_completed'])}/{self.state['stats']['total_services']} ({len(self.state['stats']['services_completed'])/self.state['stats']['total_services']*100:.1f}%)")
        print(f"   현재 단계: {self.state['current_phase']}/7")
        print("=" * 60)

# ==================== 메인 ====================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Yoom Apps Integration Orchestrator")
    parser.add_argument("--max-services", type=int, default=1,
                       help="이번 하트비트에서 처리할 최대 서비스 수 (기본: 1)")
    args = parser.parse_args()

    orchestrator = IntegrationOrchestrator()
    orchestrator.run(max_services=args.max_services)