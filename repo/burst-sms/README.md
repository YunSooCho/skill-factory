# Burst SMS API Client

Yoom Apps 연계용 Burst SMS API 클라이언트

## API 키 획득 방법

1. **Burst SMS 가입**: https://app.burstsms.com/signup
2. 대시보드에서 API 키 확인
3. Webhook URL 설정 필요

## 예제

### SMS 발송
```bash
python burst_sms_client.py send <API_KEY> +821012345678 "Hello World" "Sender"
```

### 메시지 조회
```bash
python burst_sms_client.py get <API_KEY>
```

### 메시지 상태 확인
```bash
python burst_sms_client.py status <API_KEY> <message_id>
```

### Webhook 서버 실행
```bash
python burst_sms_client.py webhook [webhook_secret] [port]
```

## 주요 기능

- **SMS 발송**: 단일/대량 SMS 발송
- **메시지 조회**: 발송/수신 메시지 목록
- **관련 메시지**: 특정 메시지와 관련된 메시지 목록
- **Webhook 핸들러**: 수신 메시지, 새 메시지 이벤트 처리

## Webhook

Burst SMS에서 다음 이벤트를 수신:
- **New Message**: SMS 발송 완료/상태 변경 시
- **Received Message**: 수신 SMS 수신 시

## 인증

- API Key 헤더 전송
- Rate Limiting 처리 (429 상태 코드 감지)
- HMAC-SHA256 서명 검증 (Webhook)