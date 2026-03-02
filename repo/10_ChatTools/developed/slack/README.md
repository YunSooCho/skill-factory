#Slack APIクライアント

Slack用のPython APIクライアント。

## 概要

このクライアントはSlack Web APIにアクセスし、ユーザー管理、チャネル操作、メッセージ操作、グループ管理、リアクション検索などのさまざまなタスクをサポートします。

## インストール

依存パッケージ：

```bash
pip install requests
```

または：

```bash
pip install -r requirements.txt
```

## Bot Tokenの発行

1. Slack API サイトへのアクセス: https://api.slack.com
2. 「Create New App」をクリック
3. 「From scratch」を選択
4. アプリ名の作成とワークスペースの選択
5. 「OAuth & Permissions」タブでBot Token Scopesを設定する
6. 「Install to Workspace」をクリック
7. 発行された Bot Token を保存 (xoxb- で始まる)

APIドキュメント：
https://api.slack.com/web

##使用法

### 初期化

```python
from slack import SlackClient

client = SlackClient(
    bot_token="xoxb-your-bot-token"
)
```

### サンプルコード

```python
# 사용자 정보 조회
user = client.get_user_info("U1234567890")
print(f"User: {user.real_name} ({user.name})")

# 이메일로 사용자 찾기
user = client.find_user_by_email("user@example.com")
print(f"Found user: {user.name}")

# 공개 채널 목록
channels = client.list_public_channels(limit=20)
print(channels)

# 채널 생성
channel = client.create_channel("new-channel")
print(f"Created: {channel.id}")

# 채널 아카이브
result = client.archive_channel("C123456")

# 채널에 멤버 초대
result = client.invite_to_channel("C123456", ["U123456", "U789012"])

# 프라이빗 채널에서 멤버 제거
result = client.remove_from_channel("C123456", "U123456")

# 채널 멤버 목록 조회
members = client.get_channel_members("C123456", limit=50)
print(members)

# 메시지 전송
result = client.send_message("C123456", "Hello from Slack API!")

# 스레드에 메시지 전송
result = client.send_message(
    "C123456",
    "Thread message",
    thread_ts="1234567890.123456"
)

# 직접 메시지 전송 (DM)
result = client.send_direct_message("U123456", "DM from API")

# 첨부 파일이 있는 메시지 전송
result = client.send_message_with_attachments(
    "C123456",
    "Message with attachments",
    [
        {
            "title": "Attachment 1",
            "text": "Attachment text",
            "color": "#36a64f"
        },
        {
            "title": "Attachment 2",
            "text": "Another attachment",
            "color": "#ff0000"
        }
    ]
)

# 메시지 삭제
result = client.delete_message("C123456", "1234567890.123456")

# 특정 메시지 조회
message = client.get_message("C123456", "1234567890.123456")

# 채널 메시지 목록
messages = client.get_channel_messages("C123456", limit=50)
print(messages)

# 스레드 메시지 조회
thread = client.get_thread_messages("C123456", "1234567890.123456")
print(thread)

# 메시지 링크 획득
link = client.get_message_link("C123456", "1234567890.123456")
print(f"Permalink: {link.get('permalink')}")

# 사용자 그룹 생성
group = client.create_user_group("Team A", "team-a")

# 사용자 그룹 목록
groups = client.list_user_groups(include_users=True)
print(groups)

# 그룹 내 사용자 목록
users = client.get_user_group_users("S123456")
print(users)

# 메시지 리액션 조회
reactions = client.get_message_reactions("C123456", "1234567890.123456")
print(reactions)
```

## APIアクション

###ユーザー操作
- `get_user_info` - ユーザー情報を取得
- `find_user_by_email` - 電子メールでユーザーを検索

###チャンネル操作
- `list_public_channels` - パブリックチャンネルの一覧を取得
- `create_channel` - チャンネルを作成
- `archive_channel` - チャンネルをアーカイブ
- `invite_to_channel` - チャンネルにメンバーを招待
- `remove_from_channel` - プライベートチャンネルからメンバーを退出させる
- `get_channel_members` - チャンネル内のメンバーIDを取得する

### メッセージ操作
- `send_message` - チャンネルにメッセージを送る
- `send_direct_message` - ダイレクトメッセージを送る
- `send_message_with_attachments` - アタッチメントを指定しチャンネルにメッセージを送る
- `delete_message` - メッセージを削除
- `get_message` - 特定のメッセージを取得
- `get_channel_messages` - チャンネルのメッセージ一覧を取得
- `get_thread_messages` - スレッドのメッセージを取得

###その他の操作
- `get_message_link` - メッセージのリンクを取得
- `create_user_group` - ユーザーグループを作成する
- `list_user_groups` - ユーザーグループの一覧を取得
- `get_user_group_users` - ユーザーグループ内のユーザー一覧を取得
- `get_message_reactions` - 特定のメッセージのリアクション一覧を取得

## エラー処理

```python
try:
    result = client.send_message("C123456", "Hello!")
except Exception as e:
    print("Error:", str(e))
```

## Rate Limiting

Slack Web APIにはレートリミットが適用されます。 Tier T1は、1分あたり1回、1分あたり200回などの制限があります。

## 参考資料

- Slack Web API: https://api.slack.com/web

##ライセンス

MIT License