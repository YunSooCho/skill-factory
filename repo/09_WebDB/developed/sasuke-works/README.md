#Sasuke Works Business Management SDK

Sasuke Worksは、プロジェクトおよびタスク管理プラットフォーム用のPython SDKです。

## インストール

```bash
pip install -r requirements.txt
```

## API キーの発行方法

1. [Sasuke Works]（https://sasukeworks.com) Webサイトにアクセスしてアカウントを作成します。
2. 「設定」(Settings) > API Keys セクションに移動します。
3. 新しい API キーを生成します。
4. 生成された API キーを安全な場所に保存します。

##使用法

### クライアントの初期化

```python
from sasuke_works import SasukeWorksClient

client = SasukeWorksClient(
    api_key="your_api_key_here"
)
```

### クライアント（顧客）管理

```python
# 모든 클라이언트 목록
clients = client.get_clients(
    page=1,
    per_page=50
)

for client in clients:
    print(f"클라이언트 ID: {client['id']}, 이름: {client['name']}, 회사: {client['company_name']}")

# 클라이언트 상세 정보
client = client.get_client(client_id="client_id")

# 클라이언트 생성
new_client = client.create_client(
    name="홍길동",
    email="hong@example.com",
    phone="010-1234-5678",
    company_name="ABC Corporation",
    address="서울시 강남구",
    tax_id="123-45-67890",
    notes="주요 고객"
)

# 클라이언트 업데이트
client.update_client(
    client_id="client_id",
    phone="010-9876-5432",
    notes="VIP 고객"
)

# 클라이언트 삭제
client.delete_client(client_id="client_id")
```

###プロジェクト管理

```python
# 프로젝트 목록 조회
projects = client.get_projects(
    page=1,
    per_page=50,
    client_id="client_id",
    status="active"
)

for project in projects:
    print(f"프로젝트 ID: {project['id']}, 이름: {project['name']}, 상태: {project['status']}")
    print(f"예산: {project['budget']}, 기간: {project['start_date']} ~ {project['end_date']}")

# 프로젝트 상세 정보
project = client.get_project(project_id="project_id")

# 프로젝트 생성
new_project = client.create_project(
    name="웹사이트 개발",
    client_id="client_id",
    description="반응형 웹사이트 개발 프로젝트",
    start_date="2024-01-01",
    end_date="2024-03-31",
    budget=10000000,
    status="active"
)

# 프로젝트 업데이트
client.update_project(
    project_id="project_id",
    status="in_progress",
    budget=12000000
)

# 프로젝트 삭제
client.delete_project(project_id="project_id")
```

### タスク(Task)の管理

```python
# 작업 목록 조회
tasks = client.get_tasks(
    page=1,
    per_page=50,
    project_id="project_id",
    status="in_progress",
    assignee_id="user_id"
)

for task in tasks:
    print(f"작업 ID: {task['id']}, 제목: {task['title']}, 상태: {task['status']}")
    print(f"우선순위: {task['priority']}, 담당자: {task['assignee']}, 마감일: {task['due_date']}")

# 작업 상세 정보
task = client.get_task(task_id="task_id")

# 작업 생성
new_task = client.create_task(
    title="메인 페이지 디자인",
    project_id="project_id",
    description="홈페이지 메인 화면 UI/UX 디자인",
    status="todo",
    priority="high",
    assignee_id="user_id",
    due_date="2024-01-15",
    estimated_hours=8.0
)

# 작업 업데이트
client.update_task(
    task_id="task_id",
    status="in_progress",
    priority="urgent",
    due_date="2024-01-10"
)

# 작업 삭제
client.delete_task(task_id="task_id")
```

### 時間追跡(Time Tracking)

```python
# 시간 기록 목록 조회
time_entries = client.get_time_entries(
    page=1,
    per_page=50,
    project_id="project_id",
    task_id="task_id",
    user_id="user_id",
    start_date="2024-01-01",
    end_date="2024-01-31"
)

for entry in time_entries:
    print(f"날짜: {entry['date']}, 설명: {entry['description']}, 시간: {entry['duration']}시간")
    print(f"청구 가능: {entry['billable']}")

# 시간 기록 생성
new_time_entry = client.create_time_entry(
    project_id="project_id",
    description="디자인 작업",
    duration=4.5,
    date="2024-01-10",
    task_id="task_id",
    billable=True
)

# 시간 기록 업데이트
client.update_time_entry(
    entry_id="entry_id",
    duration=5.0,
    description="디자인 작업 및 수정"
)

# 시간 기록 삭제
client.delete_time_entry(entry_id="entry_id")
```

### 請求書(Invoice)の管理

```python
# 송장서 목록 조회
invoices = client.get_invoices(
    page=1,
    per_page=50,
    client_id="client_id",
    status="sent"
)

for invoice in invoices:
    print(f"송장서 번호: {invoice['invoice_number']}, 금액: {.invoice['total_amount']}")
    print(f"발행일: {invoice['issue_date']}, 결제기한: {invoice['due_date']}, 상태: {invoice['status']}")

# 송장서 상세 정보
invoice = client.get_invoice(invoice_id="invoice_id")

# 송장서 생성
new_invoice = client.create_invoice(
    client_id="client_id",
    project_id="project_id",
    invoice_number="INV-2024-001",
    issue_date="2024-01-31",
    due_date="2024-02-15",
    items=[
        {
            "description": "디자인 서비스",
            "quantity": 40,
            "unit_price": 50000
        },
        {
            "description": "개발 서비스",
            "quantity": 80,
            "unit_price": 75000
        }
    ],
    notes="감사합니다"
)

# 송장서 상태 업데이트
client.update_invoice(
    invoice_id="invoice_id",
    status="paid",
    paid_date="2024-02-10"
)

# 송장서 삭제
client.delete_invoice(invoice_id="invoice_id")
```

###チームメンバーの管理

```python
# 팀 멤버 목록
members = client.get_team_members(
    page=1,
    per_page=50
)

for member in members:
    print(f"멤버: {member['name']}, 이메일: {member['email']}, 역할: {member['role']}")

# 팀 멤버 추가
client.add_team_member(
    email="newuser@example.com",
    name="새 멤버",
    role="member"
)

# 팀 멤버 업데이트
client.update_team_member(
    member_id="member_id",
    role="admin",
    name="업데이트된 이름"
)

# 팀 멤버 제거
client.remove_team_member(member_id="member_id")
```

### レポート

```python
# 시간 추적 리포트
time_report = client.get_reports(
    report_type="time",
    start_date="2024-01-01",
    end_date="2024-01-31",
    project_id="project_id"
)

print(f"총 작업 시간: {time_report['total_hours']}")
print(f"청구 가능 시간: {time_report['billable_hours']}")
print(f"청구 불가능 시간: {time_report['non_billable_hours']}")

# 프로젝트 리포트
project_report = client.get_reports(
    report_type="project",
    start_date="2024-01-01",
    end_date="2024-01-31",
    client_id="client_id"
)

for project in project_report['projects']:
    print(f"프로젝트: {project['name']}, 완료도: {project['progress']}%")

# 매출 리포트
revenue_report = client.get_reports(
    report_type="revenue",
    start_date="2024-01-01",
    end_date="2024-01-31"
)

print(f"총 매출: {revenue_report['total_revenue']}")
print(f"미수금: {revenue_report['outstanding']}")
```

### ユーザー情報

```python
# 현재 사용자 정보
user_info = client.get_user_info()
print(f"사용자: {user_info['name']}, 이메일: {user_info['email']}")
```

＃＃ステータス（Status）の例

###プロジェクトステータス
- **draft**: ドラフト
- **active**: アクティブ
- **in_progress**：進行中
- **completed**: 完了
- **on_hold**: 保留
- **キャンセル済み**：キャンセル済み

### ジョブステータス
- **todo**: やるべきこと
- **in_progress**：進行中
- **review**: レビュー中
- **completed**: 完了
- **キャンセル済み**：キャンセル済み

### 優先順位
- **low**: 低
- **medium**：中（デフォルト）
- **high**: 高
- **urgent**: 緊急

### 請求書のステータス
- **draft**: ドラフト
- **sent**: 送信済み
- **viewed**：確認済み
- **paid**: お支払い済み
- **overdue**: 遅延
- **キャンセル済み**：キャンセル済み

### 役割(Role)
- **owner**: 所有者
- **admin**: 管理者
- **manager**: マネージャー
- **member**: メンバー

##主な機能

- ✅クライアント/顧客管理
- ✅プロジェクト管理
- ✅タスク（Task）管理
- ✅時間追跡
- ✅ 請求書の作成と管理
- ✅チームメンバー管理
- ✅さまざまなレポートを提供
- ✅時間ベースの請求

##ライセンス

MIT License