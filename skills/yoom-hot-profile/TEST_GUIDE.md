# Hot Profile テストガイド

## テスト可否
✅ テスト可能 (REST API 기반)

## 事前準備

### 1. 계정 준비
- Hot Profile 계정
- API 사용 권한 확인

### 2. API 키 획득
1. Hot Profile 설정 페이지 접속
2. API 설정에서 OAuth 토큰 생성
3. 필요한 권한 선택

### 3. 환경 변수 설정
```bash
export YOOM_HOT_PROFILE_BASE_URL=https://api.hot-profile.com
export YOOM_HOT_PROFILE_API_KEY=your_api_key_here
export YOOM_HOT_PROFILE_AUTH_TOKEN=your_auth_token_here
```

### 4. 의존성 설치
```bash
pip install aiohttp requests flask
```

## 基本接続テスト

### 1. 연결 테스트

```python
import asyncio
from integration import HotProfileClient

async def test_connection():
    try:
        client = HotProfileClient()
        print("✅ 연결 성공!")
        print(f"Base URL: {client.base_url}")
        return True
    except ValueError as e:
        print(f"❌ 연결 실패 (설정 오류): {e}")
    except Exception as e:
        print(f"❌ 연결 실패 (알 수 없는 오류): {e}")
        return False

asyncio.run(test_connection())
```

### 2. API 액션 테스트

```python
async def test_api_actions():
    client = HotProfileClient()

    # 리드 검색
    try:
        leads = await client.search_leads(keyword="テスト")
        print(f"✅ 리드 검색 성공: {len(leads)}개 찾음")
    except Exception as e:
        print(f"❌ 리드 검색 실패: {e}")

    # 회사 검색
    try:
        companies = await client.search_company(keyword="テスト")
        print(f"✅ 회사 검색 성공: {len(companies)}개 찾음")
    except Exception as e:
        print(f"❌ 회사 검색 실패: {e}")

    # 필드 정보 가져오기
    try:
        fields = await client.get_lead_field_info()
        print(f"✅ 리드 필드 정보 젯급 성공: {len(fields)}개 필드")
    except Exception as e:
        print(f"❌ 리드 필드 정보 젯급 실패: {e}")

asyncio.run(test_api_actions())
```

## 트리거 테스트

### Web훅 설정 테스트

```python
from flask import Flask, request
import threading

app = Flask(__name__)

@app.route('/webhook/hot-profile', methods=['POST'])
def handle_webhook():
    """Hot Profile Web훅 핸들러"""
    data = request.json
    print("웹훅 수신:")
    print(f"이벤트 타입: {data.get('event_type', 'unknown')}")
    print(f"데이터: {data}")
    return {"status": "success"}, 200

def run_webhook_server():
    app.run(port=5000, host='0.0.0.0')

# 별도 스레드로 웹훅 서버 실행
webhook_thread = threading.Thread(target=run_webhook_server)
webhook_thread.daemon = True
webhook_thread.start()

print("🔌 Web훅 서버가 http://localhost:5000/webhook/hot-profile에서 실행 중")
print("Hot Profile 관리에서 이 URL을 웹훅 엔드포인트로 설정하세요")
```

## 테스트 체크리스트

- [ ] 기본 연결 테스트 통과
- [ ] OAuth 토큰 갱신 테스트
- [ ] 리드 검색 테스트
- [ ] 명사 등록 테스트
- [ ] 회사 등록 테스트
- [ ] 상담 등록 테스트
- [ ] 보고 관리 등록 테스트
- [ ] 웹훅 트리거 등록 테스트
- [ ] 에러 처리 테스트

## 테스트 제한사항

- 실제 서비스 데이터는 변경될 수 있음
- 테스트용 더미 데이터 사용 권장
- 속도 제한(Rate Limit) 준수 필요

## 문제 해결

### 401 Unauthorized
- 토큰 만료 여부 확인
- 권한 설정 확인
- API 키 재발급

### 404 Not Found
- 엔드포인트 URL 확인
- API 버전 확인

### 429 Too Many Requests
- 속도 제한 초과
- 요청 간격 늘리기
- 캐시 활용

### 连接 Timeout
- 네트워크 상태 확인
- 타임아웃 값 늘리기
- 재시도 로직 추가

## Web훅 트리거 이벤트

Hot Profile에서 다음 이벤트가 발생하면 웹훅이 호출됩니다:

| 이벤트 | 설명 |
|-------|------|
| name_card_registered | 명사가 등록되면 |
| task_updated | 테스크가 업데이트되면 |
| lead_updated | 리드가 업데이트되면 |
| company_updated | 회사가 업데이트되면 |
| task_created | 테스크가 생성되면 |
| report_created | 보고 관리가 생성되면 |
| report_updated | 보고 관리가 업데이트되면 |
| company_created | 회사가 생성되면 |
| opportunity_created | 상담이 생성되면 |
| name_card_updated | 명사가 업데이트되면 |
| opportunity_updated | 상담이 업데이트되면 |
| lead_created | 리드가 생성되면 |
| opportunity_stage_updated | 상담이 지정된 스테이지로 업데이트되면 |

## 참고

- 테스트 시 본 데이터 백업 권장
- API 문서 참조: [Hot Profile API 문서](https://docs.hot-profile.com)
- 테스트 환경과 본 환경 분리 권장