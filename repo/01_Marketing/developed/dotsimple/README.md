# Dotsimple API Client

Yoom Apps 연계용 Dotsimple 소셜 미디어 스케줄링 API 클라이언트

## API 키 획득 방법

1. **Dotsimple 계정**: https://dotsimple.com/
2. **Settings → API Keys**
3. API Key 확인

## 예제

### 포스트 생성
```bash
python dotsimple_client.py create <API_KEY> "Hello world" "2026-03-01T10:00:00Z"
```

### 목록 조회
```bash
python dotsimple_client.py list <API_KEY>
```

### 미디어 업로드
```bash
python dotsimple_client.py upload <API_KEY> /path/to/image.jpg image
```

### Webhook 서버 실행
```bash
python dotsimple_client.py webhook 8080
```

## 주요 기능

- **포스트 관리**: 생성, 수정, 조회, 목록, 스케줄, 큐 추가
- **미디어 업로드**: 이미지/비디오/오디오 업로드
- **계정 관리**: 연결된 소셜 미디어 계정 목록
- **Webhook**: 새 계정, 포스트, 파일 업로드 이벤트

## 인증

- Bearer Token (API Key)
- Rate Limiting 처리 (429 상태 코드 감지)