# Dotsimple API Client

Yoom Apps連携用DotsimpleソーシャルメディアスケジューリングAPIクライアント

## APIキーの取得方法

1. **Dotsimple アカウント**: https://dotsimple.com/
2. **Settings → API Keys**
3. API Keyの確認

## 例

### 投稿の作成
```bash
python dotsimple_client.py create <API_KEY> "Hello world" "2026-03-01T10:00:00Z"
```

### リストの照会
```bash
python dotsimple_client.py list <API_KEY>
```

### メディアのアップロード
```bash
python dotsimple_client.py upload <API_KEY> /path/to/image.jpg image
```

### Webhookサーバーの実行
```bash
python dotsimple_client.py webhook 8080
```

##主な機能

- **ポスト管理**：作成、変更、照会、リスト、スケジュール、キューの追加
- **メディアアップロード**：画像/ビデオ/オーディオアップロード
- **アカウント管理**：リンクされたソーシャルメディアアカウントのリスト
- **Webhook**：新しいアカウント、投稿、ファイルアップロードイベント

##認証

- Bearer Token (API Key)
- Rate Limiting処理(429ステータスコード検出)