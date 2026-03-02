# Microsoft Teams API クライアント

Microsoft Teams用のPython APIクライアント。

## 概要

このクライアントは、Microsoft Graph APIを使用してTeamsのチーム、チャンネル、チャット、ユーザー、カレンダー、ファイルなど、さまざまなタスクをサポートします。

## インストール

依存パッケージ：

```bash
pip install requests
```

または：

```bash
pip install -r requirements.txt
```

## アクセストークン発行

1. Azureポータルへのアクセス：https://portal.azure.com
2. 「Azure Active Directory」>「アプリ登録」を選択
3. 「新規登録」をクリック
4. アプリ名の作成とリダイレクト URI の設定
5. 登録後、「API権限」 > 「追加」をクリック
6. 「Microsoft Graph」>「委任された権限」で必要な権限を追加します。
   - TeamMember.Read.All
   - TeamMember.ReadWrite.All
   - Channel.Read.All
   - ChannelMessage.Read.All
   - ChannelMessage.Send
   - Chat.Read
   - Chat.ReadWrite
   - User.Read
   - User.Read.All
   - Presence.Read
   - Calendars.ReadWrite
   - Files.Read
   - Files.Read.All
7. 「権限付与」をクリック
8. トークン発行 (client credentials flow または auth code flow)

APIドキュメント：
https://docs.microsoft.com/en-us/graph/api/team-overview

##使用法

### 初期化

```python
from teams import TeamsClient

client = TeamsClient(
    access_token="YOUR_ACCESS_TOKEN"
)
```

### サンプルコード

```python
# 팀 목록
teams = client.list_teams()
print(teams)

# 팀 멤버 목록
members = client.get_team_members("team-id")
print(members)

# 채널 목록
channels = client.list_channels("team-id")
print(channels)

# 채널 생성
channel = client.create_channel(
    team_id="team-id",
    display_name="New Channel",
    description="Channel description"
)

# 채널에 메시지 전송
result = client.send_channel_message(
    team_id="team-id",
    channel_id="channel-id",
    content="Hello from Teams API!"
)

# 멘션이 포함된 채널 메시지
result = client.send_channel_message_with_mention(
    team_id="team-id",
    channel_id="channel-id",
    content="<at id=\"user-id\">@User</at> Hello!",
    mention_text="<at id=\"user-id\">@User</at>"
)

# 채널 메시지 목록
messages = client.get_channel_messages("team-id", "channel-id")

# 채널 메시지에 답장
result = client.reply_to_channel_message(
    team_id="team-id",
    channel_id="channel-id",
    message_id="message-id",
    content="Reply from API"
)

# 메시지 답장 목록
replies = client.get_message_replies("team-id", "channel-id", "message-id")

# 채팅 목록
chats = client.list_chats()

# 채팅 메시지 전송
result = client.send_chat_message(
    chat_id="chat-id",
    content="Message from API"
)

# 사용자 정보 조회
user = client.get_user_info()
print(f"User: {user.display_name}")

# 특정 사용자 정보
user = client.get_user_info(user_id="user-id")

# 사용자 프레젠스 확인
from teams import Presence
presence = client.get_user_presence("user-id")
print(f"Presence: {presence.activity} ({presence.availability})")

# 팀에 멤버 추가
result = client.add_team_member(
    team_id="team-id",
    userPrincipalName="user@example.com",
    role="member"
)

# 캘린더 이벤트 생성
event = client.create_calendar_event(
    subject="Team Meeting",
    start="2024-01-15T14:00:00Z",
    end="2024-01-15T15:00:00Z",
    attendees=["user1@example.com", "user2@example.com"],
    location="Conference Room A",
    body="<b>Meeting details...</b>",
    is_online=True
)

# 폴더 정보 조회
folder = client.get_folder_info("drive-id", "item-id")

# 파일 다운로드
file_content = client.download_file("drive-id", "item-id")
with open("downloaded_file.pdf", "wb") as f:
    f.write(file_content)
```

## APIアクション

###チームワーク
- `list_teams` - チームの一覧を取得
- `add_team_member` - チームにメンバーを追加
- `get_team_members` - チームメンバーの一覧を取得

###チャンネル操作
- `list_channels` - チャネルの一覧を取得
- `create_channel` - チャネルを作成
- `send_channel_message` - チャネルにメッセージを送る
- `send_channel_message_with_mention` - チャネルにメッセージを送る（チャネルにメンションをする）
- `get_channel_messages` - 特定のチャネル内のメッセージ一覧を取得
- `reply_to_channel_message` - チャネルに投稿されたメッセージに返信する
- `get_message_replies` - 特定のメッセージの返信一覧を取得

###チャットタスク
- `list_chats` - チャットの一覧を取得
- `send_chat_message` - チャットにメッセージを送る

###ユーザー操作
- `get_user_info` - ユーザー情報を取得
- `get_user_presence` - ユーザーのプレゼンスを取得する

###カレンダーの操作
- `create_calendar_event` - カレンダーに予定を作成する

###ファイル操作
- `get_folder_info` - フォルダ情報を取得する
- `download_file` - ファイルをダウンロード

## エラー処理

```python
try:
    result = client.send_channel_message("team-id", "channel-id", "Hello!")
except Exception as e:
    print("Error:", str(e))
```

## Rate Limiting

Microsoft Graph APIにはレートリミットが適用されます。詳細は：
https://docs.microsoft.com/en-us/graph/throttling

## 参考資料

- Microsoft Graph Teams API: https://docs.microsoft.com/en-us/graph/api/resources/teams-api-overview
- Microsoft Graph v1.0: https://docs.microsoft.com/en-us/graph/api/overview

##ライセンス

MIT License