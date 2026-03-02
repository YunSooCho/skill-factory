#Spiral Business Platform SDK

Spiralは、統合ビジネス管理プラットフォーム用のPython SDKです。

## インストール

```bash
pip install -r requirements.txt
```

## API キーの発行方法

1. [Spiral](https://spiralplatform.com)에 にアクセスしてアカウントを作成します。
2. 「設定」(Settings) > API Keys セクションに移動します。
3. 新しい API キーを生成します。
4. 生成された API キーを安全な場所に保存します。

##使用法

### クライアントの初期化

```python
from spiral import SpiralClient

client = SpiralClient(
    api_key="your_api_key_here"
)
```

###顧客管理

```python
# 고객 목록
customers = client.get_customers(page=1, per_page=50)

# 고객 생성
client.create_customer(
    name="홍길동",
    email="hong@example.com",
    phone="010-1234-5678",
    company="ABC Corporation"
)

# 고객 업데이트 및 삭제
client.update_customer(customer_id="id", name="수정된 이름")
client.delete_customer(customer_id="id")
```

###プロジェクト管理

```python
# 프로젝트 목록
projects = client.get_projects(page=1, per_page=50, customer_id="customer_id")

# 프로젝트 생성
client.create_project(
    name="웹 개발 프로젝트",
    customer_id="customer_id",
    description="반응형 웹사이트 개발",
    status="active"
)
```

###ジョブ管理

```python
# 작업 목록
tasks = client.get_tasks(page=1, per_page=50, project_id="project_id")

# 작업 생성
client.create_task(
    title="디자인 완료",
    project_id="project_id",
    description="메인 페이지 UI 디자인",
    status="in_progress",
    priority="high"
)
```

### 販売機会（Deal）管理

```python
# 딜 목록
deals = client.get_deals(page=1, per_page=50)

# 딜 생성
client.create_deal(
    title="연간 계약",
    customer_id="customer_id",
    amount=12000000,
    stage="negotiation"
)
```

##主な機能

- ✅顧客管理
- ✅プロジェクト管理
- ✅タスク（Task）管理
- ✅販売機会（Deal）追跡
- ✅レポート

##ライセンス

MIT License