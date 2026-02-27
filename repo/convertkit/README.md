# ConvertKit API Client

Yoom Apps 연계용 ConvertKit V3 API 클라이언트

## API Secret 획득 방법

1. **ConvertKit 계정**: https://app.convertkit.com/
2. **Account Settings → Advanced → API Secret**
3. API Secret 확인

## 예제

### 구독자 검색
```bash
python convertkit_client.py search <API_SECRET> test@example.com
```

### 폼에 구독자 추가
```bash
python convertkit_client.py add-form <API_SECRET> <form_id> test@example.com
```

### 태그 추가
```bash
python convertkit_client.py add-tag <API_SECRET> <subscriber_id> <tag_id>
```

### Webhook 서버 실행
```bash
python convertkit_client.py webhook 8080
```

## 주요 기능

- **구독자 관리**: 검색, 생성, 수정, 삭제
- **폼 연동**: 폼에 구독자 추가, 구독 해지
- **태그 관리**: 태그 추가/제거
- **Webhook**: 활성화, 태깅, 구독, 구매, 바운스 이벤트

## 인증

- API Secret
- Rate Limiting 처리 (429 상태 코드 감지)