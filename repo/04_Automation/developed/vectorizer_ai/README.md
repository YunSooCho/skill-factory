#Vectorizer AI APIクライアント

Vectorizer AI用のPython APIクライアント。画像をベクターグラフィックに変換する機能を提供します。

## 概要

Vectorizer AIは、ラスター画像（SVG、PNGなど）をベクターグラフィックに変換するサービスです。

## インストール

```bash
pip install requests
```

または：

```bash
pip install -r requirements.txt
```

## API キー発行

1. [Vectorizer AI]（https://vectorizer.ai/)에서アカウントの作成
2. API キー発行
3. API キーを安全に保存

##使用法

### 初期化

```python
from vectorizer_ai import VectorizerAIClient, VectorizerAIError

client = VectorizerAIClient(
    api_key="YOUR_API_KEY",
    timeout=60
)
```

###画像のベクトル化

```python
result = client.vectorize_image(
    image="logo.png",
    output_format="svg",
    detail_level="high",
    colors="color"
)

job_id = result.get("job_id")
```

### ジョブステータスの確認

```python
status = client.get_vectorization_status(job_id)
print(f"Status: {status.get('status')}")
```

### ベクトルファイルのダウンロード

```python
# 메모리에 다운로드
content = client.download_vector(job_id)

# 파일로 저장
output_path = client.download_vector(job_id, "output.svg")
print(f"Saved to: {output_path}")
```

## エラー処理

```python
try:
    result = client.vectorize_image("input.png")
except VectorizerAIAuthenticationError:
    print("API 키가 올바르지 않습니다")
except VectorizerAIRateLimitError:
    print("속도 제한이 초과되었습니다")
except VectorizerAIError as e:
    print(f"요청 실패: {str(e)}")
```

##ライセンス

MIT License

## サポート

- [Vectorizer AI公式サイト]（https://vectorizer.ai/)
- [Vectorizer AIドキュメント]（https://docs.vectorizer.ai/)