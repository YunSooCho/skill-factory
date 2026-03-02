# Constant Contact API Client

Yoom Apps連携用Constant Contact V3 APIクライアント

##認証情報取得方法

1. **Constant Contact 開発者アカウント**: https://app.constantcontact.com/
2. **API Key 生成**:
   - My Account → API & OAuth → Register Application
   - API Keyの確認
3. **OAuth Access Token 獲得**:
   - OAuth 2.0 Authorization Code Flowを使用する
   - アクセストークン発行

## 例

### コンタクトの作成
```bash
python constant_contact_client.py create <API_KEY> test@example.com John Doe
```

### コンタクト検索
```bash
python constant_contact_client.py search <API_KEY> test@example.com
```

### リスト生成
```bash
python constant_contact_client.py create-list <API_KEY> "My List"
```

### Webhookサーバーの実行
```bash
python constant_contact_client.py webhook 8080
```

##主な機能

- **コンタクト管理**：作成、検索、編集、削除
- **コンタクトリスト**：作成、検索、編集、削除
- **タグ**：作成、検索、編集、削除
- **活動データ**：コンタクト活動、行動のまとめ
- **Webhook**：新しい連絡先、編集、電子メールイベントの処理

##認証

- OAuth 2.0 Bearer Token
- Rate Limiting処理(429ステータスコード検出)