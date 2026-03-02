# Brightcove API Client

Yoom Apps 連携用 Brightcove Video Cloud API クライアント

##認証情報取得方法

1. **Brightcove Studio ログイン**: https://studio.brightcove.com
2. **Admin→API Authentication**の移動
3. **Register New Application**をクリック
4. **Client ID、Client Secret**の確認
5. **Account ID**の確認（Studiの右上）

## 例

### 動画リストの閲覧
```bash
python brightcove_client.py list <account_id> <client_id> <client_secret>
```

###動画を作成
```bash
python brightcove_client.py create <account_id> <client_id> <client_secret> "My Video"
```

###アップロードURLを取得
```bash
python brightcove_client.py upload-url <account_id> <client_id> <client_secret> <video_id>
```

### ファイルのアップロード
```bash
python brightcove_client.py upload-file <account_id> <client_id> <client_secret> <video_id> /path/to/video.mp4
```

##主な機能

- **ビデオリスト**：アカウントのすべてのビデオリストを取得する
- **ビデオ作成**：ビデオオブジェクトの作成（メタデータ）
- **ビデオアップデート**：ビデオメタデータを編集
- **一時アップロードURL**：署名付きアップロードURLを取得
- **ファイルアップロード**：ビデオファイルを直接アップロード
- **メディアのインポート**：URLまたはファイルにメディアをインポートする
- **ビデオを削除**：ビデオを削除

##認証

- OAuth 2.0 (Client Credentials Flow)
- アクセストークンの自動更新
- Rate Limiting処理(429ステータスコード検出)