#Brushup APIクライアント

Brushup用のPython APIクライアント。デザインレビュー機能を提供します。

## インストール

```bash
pip install requests
```

##使用法

```python
from brushup import BrushupClient, BrushupError

client = BrushupClient(api_key="YOUR_API_KEY")

# 디자인 검토 생성
review = client.create_design_review({
    "projectId": "123",
    "designUrl": "https://example.com/preview"
})
```

##ライセンス

MIT License