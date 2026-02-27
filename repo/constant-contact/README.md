# Constant Contact API Client

Yoom Apps 연계용 Constant Contact V3 API 클라이언트

## 인증 정보 획득 방법

1. **Constant Contact 개발자 계정**: https://app.constantcontact.com/
2. **API Key 생성**:
   - My Account → API & OAuth → Register Application
   - API Key 확인
3. **OAuth Access Token 획득**:
   - OAuth 2.0 Authorization Code Flow 사용
   - Access Token 발급

## 예제

### 컨택트 생성
```bash
python constant_contact_client.py create <API_KEY> test@example.com John Doe
```

### 컨택트 검색
```bash
python constant_contact_client.py search <API_KEY> test@example.com
```

### 리스트 생성
```bash
python constant_contact_client.py create-list <API_KEY> "My List"
```

### Webhook 서버 실행
```bash
python constant_contact_client.py webhook 8080
```

## 주요 기능

- **컨택트 관리**: 생성, 검색, 수정, 삭제
- **컨택트 리스트**: 생성, 검색, 수정, 삭제
- **태그**: 생성, 검색, 수정, 삭제
- **활동 데이터**: 컨택트 활동, 행동 요약
- **Webhook**: 새 컨택트, 수정, 이메일 이벤트 처리

## 인증

- OAuth 2.0 Bearer Token
- Rate Limiting 처리 (429 상태 코드 감지)