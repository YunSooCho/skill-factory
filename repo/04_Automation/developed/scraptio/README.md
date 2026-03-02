#Scraptio APIクライアント

Scraptio用のPython APIクライアント。ウェブサイトからテキスト、リンク、電子メールを簡単に抽出できます。

## 概要

Scraptioは、複雑なWebスクレイピングを簡素化したサービスです。 Zapier、Make、その他の自動化ツールと連携して、ウェブサイトのデータを自動的に抽出できます。

## インストール

依存パッケージ：

```bash
pip install requests
```

または：

```bash
pip install -r requirements.txt
```

## API キー発行

1. [Scraptio](https://scraptio.com/)에서 アカウントの作成
2.無料プランで開始（月30回要請）
3.ダッシュボードでAPIキーを確認または発行
4. API キーを安全に保存

##使用法

### 初期化

```python
from scraptio import ScraptioClient, ScraptioError

client = ScraptioClient(
    api_key="YOUR_API_KEY",
    timeout=30
)
```

###デフォルトURLスクレイピング

```python
try:
    result = client.scrape_url("https://example.com")
    print("Scraped data:", result)
except ScraptioError as e:
    print("Error:", str(e))
```

### CSSセレクタによる特定のデータの抽出

```python
css_selectors = {
    "title": "h1",
    "description": ".description",
    "price": ".price"
}

result = client.scrape_url(
    "https://example.com",
    css_selectors=css_selectors
)
```

### メール抽出

```python
result = client.scrape_url(
    "https://example.com/contact",
    extract_emails=True
)
print("Emails:", result.get("emails", []))
```

### リンク抽出

```python
result = client.scrape_url(
    "https://example.com",
    extract_links=True
)
print("Links:", result.get("links", []))
```

###待機時間の設定（JavaScriptレンダリング待ち）

```python
result = client.scrape_url(
    "https://example.com",
    wait=2000  # 2초 대기
)
```

### スクレイピング結果の照会

```python
# 비동기 스크래핑인 경우 결과 ID로 조회
result = client.get_scrape_result("scrape_id_here")
```

###最近のスクレイピングリスト

```python
result = client.list_scrapes(limit=20, offset=0)
print("Recent scrapes:", result.get("scrapes", []))
```

## APIメソッド

### scrape_url

WebサイトのURLをスクラップしてデータを抽出します。

**パラメータ：**
- `url`（str）：スクラップするURL（必須）
- `wait` (int, optional): スクレイピング前の待機時間 (ミリ秒)
- `css_selectors`（dict、optional）：フィールド名とCSSセレクタのマッピング
- `extract_emails`（bool）：電子メールを抽出するかどうか（デフォルト：False）
- `extract_links`（bool）：リンクを抽出するかどうか（デフォルト：False）
- `extract_texts`（bool）：テキストを抽出するかどうか（デフォルト：True）

**戻り値:**
- `dict`：抽出されたデータを含む辞書

### get_scrape_result

非同期スクレイピング操作の結果を照会します。

**パラメータ：**
- `scrape_id`（str）：スクレイピングジョブID

**戻り値:**
- `dict`：スクレイピング結果

### list_scrapes

最近のスクレイピングジョブのリストを照会します。

**パラメータ：**
- `limit`（int）：返される結果の数（デフォルト：10）
- `offset`（int）：スキップした結果の数（デフォルト：0）

**戻り値:**
- `dict`：スクレイピングジョブリスト

## エラー処理

```python
from scraptio import ScraptioError, ScraptioRateLimitError, ScraptioAuthenticationError

try:
    result = client.scrape_url("https://example.com")
except ScraptioAuthenticationError:
    print("API 키가 올바르지 않습니다")
except ScraptioRateLimitError:
    print("속도 제한이 초과되었습니다. 잠시 후 다시 시도하세요")
except ScraptioError as e:
    print(f"스크래핑 실패: {str(e)}")
```

## Rate Limiting

APIリクエスト間の最低100msの遅延が自動的に適用されます。

## 例コード

###完全な例

```python
from scraptio import ScraptioClient, ScraptioError

# 클라이언트 초기화
client = ScraptioClient(api_key="YOUR_API_KEY")

# 웹사이트 스크래핑
try:
    # 텍스트, 링크, 이메일 추출
    result = client.scrape_url(
        "https://example.com",
        extract_emails=True,
        extract_links=True
    )

    print("Title:", result.get("title"))
    print("Text:", result.get("text", "")[:200])  # 첫 200자
    print("Links found:", len(result.get("links", [])))
    print("Emails found:", len(result.get("emails", [])))

    # 최근 스크래핑 내역 확인
    history = client.list_scrapes(limit=5)
    print(f"Total scrapes: {history.get('total', 0)}")

except ScraptioError as e:
    print(f"Error: {str(e)}")
```

##ライセンス

MIT License

## サポート

- [Scraptio公式サイト]（https://scraptio.com/)
- [Scraptioドキュメント]（https://scraptio.notion.site/)
- [Zapier統合ガイド]（https://scraptio.notion.site/How-to-use-Scraptio-with-Zapier-45ba2b93ffb94df5966d0a9f9b7394a2)
- [Make統合ガイド]（https://scraptio.notion.site/How-to-use-Scraptio-with-Make-2a727a5acb8746bf9eed039661781722)