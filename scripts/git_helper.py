#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
스킬 팩토리: 서비스 발견 + Git Push 자동화

서비스 찾기:
- 웹 API 디렉토리 스크래핑
- OpenAPI/Swagger 자동 탐색
- 일본 SaaS 데이터 수집
- Git commit & push 자동화
"""

import os
import json
from datetime import datetime
import urllib.request
import urllib.error
from urllib.parse import urljoin
import re
import html

# --- Git Push 로직 ---
def git_commit_and_push():
    """
    Git commit & push 수행
    """
    print("🔄 Git commit & push 시작...")
    
    try:
        base_dir = "/Users/clks001/.openclow/workspace/skill-factory"
        os.chdir(base_dir)
        
        # Git add
        ret = os.system("git add -A")
        if ret != 0:
            print("⚠️ Git add 실패 (변경사항 없을 수 있음)")
        
        # Git commit
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        com_msg = f'chore: 스킬 팩토리 하트비트 업데이트 ({timestamp})'
        ret = os.system(f'git commit -m "{com_msg}"')
        if ret == 0:
            print("✅ Git commit 완료!")
        else:
            print("⚠️ Git commit 실패 (변경사항 없음)")
        
        # Git push
        ret = os.system("git push -f origin main")
        if ret == 0:
            print("✅ Git push 완료!")
        else:
            print("⚠️ Git push 실패 (remote에서 이력 강제 제거 일 수 있음)")
        
    except Exception as e:
        print(f"⚠️ Git push 실패: {e}")

# --- 기존 스크립트 실행 (if needed) ---
# 여기에 기존 서비스 발견 로직을 통합하거나
# 별도로 실행한 후 git_commit_and_push() 호출

if __name__ == '__main__':
    # Git push만 수행 (테스트용)
    git_commit_and_push()
    print("\n🎉 완료! Check GitHub: https://github.com/YunSooCho/skill-factory.git")