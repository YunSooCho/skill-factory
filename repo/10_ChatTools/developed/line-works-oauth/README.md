#LINE WORKS OAuth APIクライアント

LINE WORKS OAuth用のPython APIクライアントです。

## 概要

このクライアントはLINE WORKS OAuth APIにアクセスし、ユーザー管理、メッセージ転送、カレンダー操作、グループ管理、ファイル管理、メール、掲示板などのさまざまなタスクをサポートします。

## インストール

依存パッケージ：

```bash
pip install requests
```

または：

```bash
pip install -r requirements.txt
```

## OAuth認証の設定

1. LINE WORKS開発者ポータルへのアクセス：https://developers.works.mobile.co.kr
2. アプリ(Service)の作成
3. クライアントID、シークレット設定
4. OAuth 2.0 アクセストークン発行
5. 発行されたアクセストークンの保存

APIドキュメント：
https://developers.works.mobile.co.kr/reference

##使用法

### 初期化

```python
from line_works_oauth import LineWorksOAuthClient

client = LineWorksOAuthClient(
    access_token="YOUR_ACCESS_TOKEN",
    api_id="YOUR_API_ID"
)
```

### サンプルコード

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

## APIアクション

### ユーザー管理
- `list_users` - ユーザーリストの照会
- `get_user` - ユーザー情報の照会
- `create_user` - 新しいユーザーの作成
- `update_user` - ユーザー情報の更新
- `delete_user` - ユーザーの削除
- `suspend_user` - ユーザーの停止
- `unsuspend_user` - ユーザー停止のキャンセル

### メッセージ操作
- `send_message_to_user` - 特定のユーザーにメッセージを送信する
- `send_message_to_room` - トークルームにメッセージを送信する
- `send_message_with_button` - ボタンでメッセージを送信する
- `send_message_via_webhook` - Incoming Webhookにメッセージを送信する
- `send_file_to_user` - ユーザーにファイルを転送する
- `send_file_to_room` - トークルームへのファイル転送

###カレンダーの操作
- `list_calendars` - ユーザーカレンダーリストの検索
- `get_calendar_events` - カレンダーイベントリストの検索
- `create_event` - カレンダーイベントの生成
- `create_event` (終日) - 終日イベントの生成
- `update_event` - カレンダーイベントの更新
- `update_event`(終日) - 終日イベントの更新
- `delete_event` - カレンダーイベントを削除
- `get_event_detail` - カレンダーイベントの詳細検索

### グループ管理
- `create_group` - グループの作成
- `update_group_members` - グループメンバーリストの更新

###ファイル操作
- `get_upload_url` - ファイルアップロードURLを取得
- `upload_file` - ファイルアップロードの実行
- `list_group_files` - グループルートフォルダファイルのリスト
- `list_group_folder_files` - グループ固有のフォルダファイルのリスト
- `create_group_folder` - グループルートフォルダにフォルダを作成する
- `create_group_folder` - グループ固有のフォルダ内にフォルダを作成する
- `duplicate_group_file` - グループフォルダ内のファイル/フォルダの複製

###メール操作
- `get_mails` - メーリングリストの検索
- `get_mail` - メール詳細検索
- `send_mail` - メール送信
- `get_mails` - メールフォルダ内のメールの検索

###掲示板の操作
- `create_bulletin_board` - 掲示板の作成
- `create_bulletin_post` - 掲示板の投稿を書く

### 外部ブラウザ設定
- `enable_external_browser` - 外部ブラウザ設定を有効にする
- `disable_external_browser` - 外部ブラウザ設定を無効にする
- `get_external_browser_status` - 外部ブラウザ使用状況の照会

### ボット操作
- `create_bot_talk_room` - ボットを含むトークルームを作成する

## エラー処理

```python
try:
    result = client.send_message_to_user("user_id", "Hello!")
except Exception as e:
    print("Error:", str(e))
```

## Rate Limiting

LINE WORKS APIはリクエストのレートリミットが適用されます。

## 参考資料

- LINE WORKS開発者ドキュメント：https://developers.works.mobile.co.kr
- APIリファレンス：https://developers.works.mobile.co.kr/reference

##ライセンス

MIT License