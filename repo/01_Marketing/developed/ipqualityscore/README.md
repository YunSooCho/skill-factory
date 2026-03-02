# IPQualityScore API Client

Yoom Apps連携用IPQualityScore APIクライアント

## APIキーの取得方法

1. **IPQualityScoreにサインアップ**：https://www.ipqualityscore.com/create-account
2.ダッシュボードでAPIキーを確認する
3.無料プランで毎月5,000件無料利用可能

## 例

### メール検証
```bash
python ipqualityscore_client.py email <API_KEY> test@example.com
```

###電話番号の確認
```bash
python ipqualityscore_client.py phone <API_KEY> +14155551234
python ipqualityscore_client.py phone <API_KEY> 821012345678 KR
```

### プロキシ/VPN 検出
```bash
python ipqualityscore_client.py ip <API_KEY> 8.8.8.8
```

##主な機能

- **電子メール検証**：配信可能性、使い捨て電子メール、スパムトラップ検出、詐欺スコアの確認
- **電話番号検証**：有効性、アクティブ状態、通信会社、ラインタイプ、詐欺スコアの確認
- **IPレピュテーション**：プロキシ、VPN、Tor、データセンター、最新の悪用の検出

##認証

- API Keyヘッダー転送
- Rate Limiting処理(429ステータスコード検出)