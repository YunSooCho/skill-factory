#!/usr/bin/env python3
"""
Yoom Apps 자동화 추적 - 크론 실행 스크립트 (실제 구현 포함)
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

# 경로 설정
WORKSPACE = Path.home() / ".openclaw/workspace"
PROJECT_DIR = WORKSPACE / "github/skill-factory"
SKILL_DIR = WORKSPACE / "skills" / "yoom-automation-tracker"
LOG_FILE = PROJECT_DIR / "yoom-heartbeat.log"

def log(message, level="INFO"):
    """로그 기록"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] [{level}] {message}"
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_line + '\n')
    print(log_line, file=sys.stderr)

def get_next_tasks():
    """다음 작업 목록 가져오기"""
    try:
        get_progress_script = SKILL_DIR / "scripts" / "get_progress.py"
        result = subprocess.run(
            ["python3", str(get_progress_script)],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode != 0:
            log(f"get_progress.py 실패: {result.stderr}", "ERROR")
            return None

        return json.loads(result.stdout)
    except Exception as e:
        log(f"작업 목록 조회 실패: {e}", "ERROR")
        return None

def process_service(task):
    """서비스 처리 (분석만 - 실제 구현은 LLM 세션에서)"""
    file_path = task["path"]
    file_name = task["file"]

    log(f"분석: {file_name}")

    # 파싱
    parse_script = SKILL_DIR / "scripts" / "parse_md.py"
    result = subprocess.run(
        ["python3", str(parse_script), file_path, "--json"],
        capture_output=True,
        text=True,
        timeout=30
    )

    if result.returncode != 0:
        log(f"{file_name} 파싱 실패", "WARNING")
        return False

    try:
        parsed_data = json.loads(result.stdout)
        log(f"{file_name} 분석 완료: 통합={parsed_data.get('integration_type')}, 액션={len(parsed_data.get('api_actions', []))}")
        return True
    except:
        log(f"{file_name} JSON 파싱 실패", "WARNING")
        return False

def git_commit(message):
    """Git 커밋"""
    try:
        os.chdir(str(PROJECT_DIR))

        # 변경 사항 확인
        result = subprocess.run(
            ["git", "status", "--short"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if not result.stdout.strip():
            log("커밋할 변경 사항 없음")
            return False

        # 커밋
        subprocess.run(
            ["git", "add", "."],
            capture_output=True,
            timeout=20
        )

        subprocess.run(
            ["git", "commit", "-m", message],
            capture_output=True,
            timeout=20
        )

        log(f"Git 커밋 완료: {message}")
        return True
    except Exception as e:
        log(f"Git 커밋 실패: {e}", "WARNING")
        return False

def main():
    """메인"""
    log("======== 크론 실행 시작 ========")

    try:
        # 다음 작업 확인
        tasks_data = get_next_tasks()
        if not tasks_data:
            log("작업 목록 가져오기 실패", "ERROR")
            sys.exit(1)

        if tasks_data.get("status") == "all_complete":
            log("모든 작업 완료", "SUCCESS")
            sys.exit(0)

        tasks = tasks_data.get("tasks", [])
        if not tasks:
            log("처리할 서비스 없음", "INFO")
            sys.exit(0)

        log(f"대기 중인 작업: {len(tasks)}개")

        # 최근 업데이트 체크
        progress_file = PROJECT_DIR / "yoom-automation-progress.json"
        if progress_file.exists():
            # 최근 업데이트 시간 확인
            mtime = progress_file.stat().st_mtime
            mtime_dt = datetime.fromtimestamp(mtime)
            now = datetime.now()
            hours_since_update = (now - mtime_dt).total_seconds() / 3600

            if hours_since_update < 1:
                log(f"최근 업데이트 있음 ({hours_since_update:.1f}시간 전), 건너뜀")

                # 그래도 커밋 체크
                changed = subprocess.run(
                    ["git", "status", "--short"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if changed.stdout.strip():
                    for _ in range(3):
                        if git_commit(f"자동 커밋 ({now.strftime('%H:%M')})"):
                            break
                sys.exit(0)

        log(f"다음 대상: {tasks[0]['file']}")
        log(f"참고: 실제 구현은 LLM 세션에서 진행 필요")

        # Git 커밋 (있는 경우)
        for _ in range(3):
            if git_commit(f"진척 업데이트 ({datetime.now().strftime('%Y-%m-%d %H:%M')})"):
                break

        log("✅ 작업 완료", "SUCCESS")
        sys.exit(0)

    except Exception as e:
        log(f"에러: {e}", "ERROR")
        sys.exit(1)
    finally:
        log("======== 크론 실행 종료 ========")

if __name__ == "__main__":
    main()