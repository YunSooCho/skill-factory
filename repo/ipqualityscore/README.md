# IPQualityScore API Client

Yoom Apps 연계용 IPQualityScore API 클라이언트

## API 키 획득 방법

1. **IPQualityScore 가입**: https://www.ipqualityscore.com/create-account
2. 대시보드에서 API 키 확인
3. 무료 플랜에서 월간 5,000건 무료 사용 가능

## 예제

### 이메일 검증
```bash
python ipqualityscore_client.py email <API_KEY> test@example.com
```

### 전화번호 검증
```bash
python ipqualityscore_client.py phone <API_KEY> +14155551234
python ipqualityscore_client.py phone <API_KEY> 821012345678 KR
```

### 프록시/VPN 탐지
```bash
python ipqualityscore_client.py ip <API_KEY> 8.8.8.8
```

## 주요 기능

- **이메일 검증**: 전달 가능성, 일회용 이메일, 스팸 트랩 감지, 사기 점수 확인
- **전화번호 검증**: 유효성, 활성 상태, 통신사, 라인 타입, 사기 점수 확인
- **IP 평판**: 프록시, VPN, Tor, 데이터 센터, 최신 악용 탐지

## 인증

- API Key 헤더 전송
- Rate Limiting 처리 (429 상태 코드 감지)