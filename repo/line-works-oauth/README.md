# LINE WORKS OAuth API 클라이언트

LINE WORKS OAuth를 위한 Python API 클라이언트입니다.

## 개요

이 클라이언트는 LINE WORKS OAuth API에 접근하여 사용자 관리, 메시지 전송, 캘린더 운영, 그룹 관리, 파일 관리, 메일, 게시판 등 다양한 작업을 지원합니다.

## 설치

의존성 패키지:

```bash
pip install requests
```

또는:

```bash
pip install -r requirements.txt
```

## OAuth 인증 설정

1. LINE WORKS 개발자 포털 접속: https://developers.works.mobile.co.kr
2. 앱 (Service) 생성
3. 클라이언트 ID, 시크릿 설정
4. OAuth 2.0 액세스 토큰 발급
5. 발급된 액세스 토큰 저장

API 문서:
https://developers.works.mobile.co.kr/reference

## 사용법

### 초기화

```python
from line_works_oauth import LineWorksOAuthClient

client = LineWorksOAuthClient(
    access_token="YOUR_ACCESS_TOKEN",
    api_id="YOUR_API_ID"
)
```

### 예시 코드

```python
# 사용자 목록 조회
users = client.list_users(limit=20)
print(users)

# 특정 사용자 정보 조회
user = client.get_user("user_id")
print(f"User: {user.name} ({user.email})")

# 사용자 생성
new_user = client.create_user(
    name="John Doe",
    email="john@example.com",
    phone="821012345678",
    department="IT",
    position="Engineer"
)

# 사용자 정지
client.suspend_user("user_id")

# 사용자 정지 취소
client.unsuspend_user("user_id")

# 사용자에게 메시지 전송
result = client.send_message_to_user(
    "user_id",
    "Hello from LINE WORKS!"
)

# 토크룸에 메시지 전송
result = client.send_message_to_room(
    "room_id",
    "Hello room!"
)

# 버튼이 있는 메시지 전송
result = client.send_message_with_button(
    "user_id",
    "Please select an option:",
    [
        {"type": "message", "text": "Option 1"},
        {"type": "message", "text": "Option 2"}
    ]
)

# Incoming Webhook으로 메시지 전송
result = client.send_message_via_webhook(
    "https://your-webhook-url",
    "Test message"
)

# 사용자에게 파일 전송
result = client.send_file_to_user(
    "user_id",
    "/path/to/file.pdf"
)

# 토크룸에 파일 전송
result = client.send_file_to_room(
    "room_id",
    "/path/to/file.pdf"
)

# 캘린더 목록 조회
calendars = client.list_calendars(user_id="user_id")

# 캘린더 이벤트 조회
events = client.get_calendar_events(
    calendar_id="calendar_id",
    from_date="2024-01-01",
    to_date="2024-01-31"
)

# 캘린더 이벤트 생성
event = client.create_event(
    calendar_id="calendar_id",
    title="Meeting",
    start_time="2024-01-15T14:00:00+09:00",
    end_time="2024-01-15T15:00:00+09:00",
    location="Conference Room A",
    description="Team meeting"
)

# 종일 이벤트 생성
event = client.create_event(
    calendar_id="calendar_id",
    title="Company Holiday",
    start_time="2024-01-01",
    end_time="2024-01-02",
    is_all_day=True
)

# 이벤트 업데이트
updated_event = client.update_event(
    calendar_id="calendar_id",
    event_id="event_id",
    title="Updated Meeting",
    location="Conference Room B"
)

# 이벤트 삭제
client.delete_event(calendar_id="calendar_id", event_id="event_id")

# 그룹 생성
group = client.create_group(
    name="Development Team",
    description="Software development group"
)

# 그룹 멤버 업데이트
client.update_group_members(
    group_id="group_id",
    add_user_ids=["user1", "user2"],
    remove_user_ids=["user3"]
)

# 파일 업로드 URL 획득
upload_info = client.get_upload_url("file.pdf", 1024000)
upload_url = upload_info["uploadUrl"]

# 파일 업로드
client.upload_file(upload_url, "/path/to/file.pdf")

# 그룹 루트 폴더 파일 목록
files = client.list_group_files(group_id="group_id")

# 그룹 특정 폴더 파일 목록
folder_files = client.list_group_folder_files(group_id="group_id", folder_id="folder_id")

# 그룹 폴더 생성
folder = client.create_group_folder(group_id="group_id", folder_name="Documents")

# 그룹 파일 복제
duplicated = client.duplicate_group_file(
    group_id="group_id",
    file_id="file_id",
    destination_folder_id="folder_id"
)

# 메일 목록 조회
mails = client.get_mails(folder_path="INBOX")

# 메일 발송
result = client.send_mail(
    to=["recipient@example.com"],
    subject="Test Mail",
    body="Hello!",
    cc=["cc@example.com"],
    bcc=["bcc@example.com"]
)

# 게시판 생성
board = client.create_bulletin_board(
    group_id="group_id",
    title="Announcements",
    content="General announcements"
)

# 게시판 게시물 작성
post = client.create_bulletin_post(
    board_id="board_id",
    title="Welcome",
    content="Welcome to the team!"
)

# 외부 브라우저 설정 활성화
client.enable_external_browser()

# 외부 브라우저 설정 비활성화
client.disable_external_browser()

# 외부 브라우저 사용 상태 확인
status = client.get_external_browser_status()

# 봇이 포함된 토크룸 생성
room = client.create_bot_talk_room(
    bot_id="bot_id",
    room_name="Support Chat"
)
```

## API 액션

### 사용자 관리
- `list_users` - 사용자 목록 조회
- `get_user` - 사용자 정보 조회
- `create_user` - 새 사용자 생성
- `update_user` - 사용자 정보 업데이트
- `delete_user` - 사용자 삭제
- `suspend_user` - 사용자 정지
- `unsuspend_user` - 사용자 정지 취소

### 메시지 작업
- `send_message_to_user` - 특정 사용자에게 메시지 전송
- `send_message_to_room` - 토크룸에 메시지 전송
- `send_message_with_button` - 버튼이 있는 메시지 전송
- `send_message_via_webhook` - Incoming Webhook으로 메시지 전송
- `send_file_to_user` - 사용자에게 파일 전송
- `send_file_to_room` - 토크룸에 파일 전송

### 캘린더 작업
- `list_calendars` - 사용자 캘린더 목록 조회
- `get_calendar_events` - 캘린더 이벤트 목록 조회
- `create_event` - 캘린더 이벤트 생성
- `create_event` (종일) - 종일 이벤트 생성
- `update_event` - 캘린더 이벤트 업데이트
- `update_event` (종일) - 종일 이벤트 업데이트
- `delete_event` - 캘린더 이벤트 삭제
- `get_event_detail` - 캘린더 이벤트 상세 조회

### 그룹 관리
- `create_group` - 그룹 생성
- `update_group_members` - 그룹 멤버 목록 업데이트

### 파일 작업
- `get_upload_url` - 파일 업로드 URL 획득
- `upload_file` - 파일 업로드 실행
- `list_group_files` - 그룹 루트 폴더 파일 목록
- `list_group_folder_files` - 그룹 특정 폴더 파일 목록
- `create_group_folder` - 그룹 루트 폴더에 폴더 생성
- `create_group_folder` - 그룹 특정 폴더 내에 폴더 생성
- `duplicate_group_file` - 그룹 폴더 내 파일/폴더 복제

### 메일 작업
- `get_mails` - 메일 목록 조회
- `get_mail` - 메일 상세 조회
- `send_mail` - 메일 전송
- `get_mails` - 메일 폴더 내 메일 조회

### 게시판 작업
- `create_bulletin_board` - 게시판 생성
- `create_bulletin_post` - 게시판 게시물 작성

### 외부 브라우저 설정
- `enable_external_browser` - 외부 브라우저 설정 활성화
- `disable_external_browser` - 외부 브라우저 설정 비활성화
- `get_external_browser_status` - 외부 브라우저 이용 상태 조회

### 봇 작업
- `create_bot_talk_room` - 봇이 포함된 토크룸 생성

## 에러 처리

```python
try:
    result = client.send_message_to_user("user_id", "Hello!")
except Exception as e:
    print("Error:", str(e))
```

## Rate Limiting

LINE WORKS API는 요청에 대한 레이트 리밋이 적용됩니다.

## 참고 문서

- LINE WORKS 개발자 문서: https://developers.works.mobile.co.kr
- API 레퍼런스: https://developers.works.mobile.co.kr/reference

## 라이선스

MIT License