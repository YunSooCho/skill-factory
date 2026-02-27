# Brightcove API Client

Yoom Apps 연계용 Brightcove Video Cloud API 클라이언트

## 인증 정보 획득 방법

1. **Brightcove Studio 로그인**: https://studio.brightcove.com
2. **Admin → API Authentication** 이동
3. **Register New Application** 클릭
4. **Client ID, Client Secret** 확인
5. **Account ID** 확인 (Studi 오른쪽 상단)

## 예제

### 비디오 목록 조회
```bash
python brightcove_client.py list <account_id> <client_id> <client_secret>
```

### 비디오 생성
```bash
python brightcove_client.py create <account_id> <client_id> <client_secret> "My Video"
```

### 업로드 URL 획득
```bash
python brightcove_client.py upload-url <account_id> <client_id> <client_secret> <video_id>
```

### 파일 업로드
```bash
python brightcove_client.py upload-file <account_id> <client_id> <client_secret> <video_id> /path/to/video.mp4
```

## 주요 기능

- **비디오 목록**: 계정의 모든 비디오 목록 가져오기
- **비디오 생성**: 비디오 객체 생성 (메타데이터)
- **비디오 업데이트**: 비디오 메타데이터 수정
- **임시 업로드 URL**: 서명된 업로드 URL 획득
- **파일 업로드**: 비디오 파일 직접 업로드
- **미디어 가져오기**: URL 또는 파일로 미디어 가져오기
- **비디오 삭제**: 비디오 삭제

## 인증

- OAuth 2.0 (Client Credentials Flow)
- Access Token 자동 갱신
- Rate Limiting 처리 (429 상태 코드 감지)