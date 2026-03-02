# ConvertKit API Client

Yoom Apps連携用ConvertKit V3 APIクライアント

## API Secretの取得方法

1. **ConvertKit アカウント**: https://app.convertkit.com/
2. **Account Settings → Advanced → API Secret**
3. API Secretの確認

## 例

### 購読者を検索
```bash
python convertkit_client.py search <API_SECRET> test@example.com
```

###フォームに購読者を追加する
```bash
python convertkit_client.py add-form <API_SECRET> <form_id> test@example.com
```

### タグの追加
```bash
python convertkit_client.py add-tag <API_SECRET> <subscriber_id> <tag_id>
```

### Webhookサーバーの実行
```bash
python convertkit_client.py webhook 8080
```

##主な機能

- **購読者管理**：検索、作成、編集、削除
- **フォーム連動**：フォームに購読者を追加、購読解除
- **タグ管理**：タグの追加/削除
- **Webhook**: アクティベーション、タグ付け、購読、購入、バウンスイベント

##認証

- API Secret
- Rate Limiting処理(429ステータスコード検出)