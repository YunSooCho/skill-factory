＃ラクラク販売（活用売買）販売管理SDK

ラクラク販売（活用売買）は、日本の販売および顧客管理プラットフォーム用のPython SDKです。

## インストール

```bash
pip install -r requirements.txt
```

## API キーの発行方法

1. [ラクラク販売]（https://rakuraku-hanbai.jp/)ウェブサイトにアクセスしてアカウントを作成します。
2. 「設定」(Settings) > API Keys セクションに移動します。
3. 新しい API キーを生成します。
4. 生成された API キーを安全な場所に保存します。

##使用法

### クライアントの初期化

```python
from rakuraku_hanbai import RakurakuHanbaiClient

client = RakurakuHanbaiClient(
    api_key="your_api_key_here"
)
```

###顧客管理

```python
# 고객 목록 조회
customers = client.get_customers(
    page=1,
    per_page=50,
    status="active"
)

for customer in customers:
    print(f"고객 ID: {customer['id']}, 이름: {customer['name']}")

# 고객 상세 정보
customer = client.get_customer(customer_id="customer_id")
print(f"고객 이름: {customer['name']}, 회사: {customer['company_name']}")

# 고객 생성
new_customer = client.create_customer(
    name="홍길동",
    email="hong@example.com",
    phone="010-1234-5678",
    company_name="ABC Corporation",
    address="서울시 강남구",
    status="active",
    notes="주요 고객"
)

# 고객 업데이트
client.update_customer(
    customer_id="customer_id",
    phone="010-9876-5432",
    status="inactive"
)

# 고객 삭제
client.delete_customer(customer_id="customer_id")
```

### 販売機会（Deal）管理

```python
# 판매 기회 목록 조회
deals = client.get_deals(
    page=1,
    per_page=50,
    status="prospect",
    customer_id="customer_id"
)

for deal in deals:
    print(f"거래 ID: {deal['id']}, 제목: {deal['title']}, 금액: {deal['amount']}")
    print(f"단계: {deal['stage']}, 확률: {deal['probability']}%")

# 판매 기회 상세 정보
deal = client.get_deal(deal_id="deal_id")

# 판매 기회 생성
new_deal = client.create_deal(
    title="연간 계약",
    customer_id="customer_id",
    amount=1200000,
    stage="proposal",
    probability=70,
    expected_close_date="2024-12-31",
    description="연간 서비스 계약"
)

# 판매 기회 업데이트
client.update_deal(
    deal_id="deal_id",
    stage="negotiation",
    probability=80,
    amount=1500000
)

# 판매 기회 삭제
client.delete_deal(deal_id="deal_id")
```

### 見積書(Quote)の管理

```python
# 견적서 목록 조회
quotes = client.get_quotes(
    page=1,
    per_page=50,
    status="draft",
    deal_id="deal_id"
)

for quote in quotes:
    print(f"견적서 ID: {quote['id']}, 제목: {quote['title']}, 상태: {quote['status']}")

# 견적서 상세 정보
quote = client.get_quote(quote_id="quote_id")

# 견적서 생성
new_quote = client.create_quote(
    customer_id="customer_id",
    title="서비스 견적서",
    valid_until="2024-12-31",
    items=[
        {
            "product_id": "product_id",
            "quantity": 10,
            "unit_price": 50000,
            "description": "서비스 항목 1"
        },
        {
            "product_id": "product_id_2",
            "quantity": 5,
            "unit_price": 30000,
            "description": "서비스 항목 2"
        }
    ],
    discount=0.05,
    tax_rate=0.1,
    notes="견적 유효 기간 내에 승인 필요"
)

# 견적서 업데이트
client.update_quote(
    quote_id="quote_id",
    status="sent",
    discount=0.1
)

# 견적서 삭제
client.delete_quote(quote_id="quote_id")
```

### 注文管理

```python
# 주문 목록 조회
orders = client.get_orders(
    page=1,
    per_page=50,
    status="processing",
    customer_id="customer_id"
)

for order in orders:
    print(f"주문 ID: {order['id']}, 상태: {order['status']}, 총액: {order['total_amount']}")

# 주문 상세 정보
order = client.get_order(order_id="order_id")

# 주문 생성
new_order = client.create_order(
    customer_id="customer_id",
    items=[
        {
            "product_id": "product_id",
            "quantity": 10,
            "price": 50000
        }
    ],
    shipping_address="서울시 강남구 테헤란로 123",
    payment_method="bank_transfer",
    notes="출근 시간에 배달 요청"
)

# 주문 업데이트
client.update_order(
    order_id="order_id",
    status="shipped",
    payment_status="paid"
)

# 주문 삭제
client.delete_order(order_id="order_id")
```

### アクティビティ(Activity)の管理

```python
# 활동 목록 조회
activities = client.get_activities(
    page=1,
    per_page=50,
    customer_id="customer_id",
    deal_id="deal_id"
)

for activity in activities:
    print(f"활동 ID: {activity['id']}, 유형: {activity['type']}, 제목: {activity['subject']}")

# 활동 생성
new_activity = client.create_activity(
    type="call",
    customer_id="customer_id",
    deal_id="deal_id",
    subject="고객 통화",
    description="계약 내용 확인 통화",
    scheduled_at="2024-12-25 14:00:00"
)

# 활동 업데이트 (완료 표시)
client.update_activity(
    activity_id="activity_id",
    status="completed",
    completed_at="2024-12-25 14:30:00"
)

# 활동 삭제
client.delete_activity(activity_id="activity_id")
```

### 製品(Product)の管理

```python
# 제품 목록 조회
products = client.get_products(
    page=1,
    per_page=50
)

for product in products:
    print(f"제품 ID: {product['id']}, 코드: {product['code']}, 이름: {product['name']}")
    print(f"가격: {product['price']}, 재고: {product['stock_quantity']}")

# 제품 상세 정보
product = client.get_product(product_id="product_id")

# 제품 생성
new_product = client.create_product(
    name="서비스 플랜 A",
    code="SVC-001",
    price=50000,
    description="기본 서비스 플랜",
    stock_quantity=100
)

# 제품 업데이트
client.update_product(
    product_id="product_id",
    price=55000,
    stock_quantity=80
)

# 제품 삭제
client.delete_product(product_id="product_id")
```

### レポートと分析

```python
# 판매 보고서
sales_report = client.get_sales_report(
    start_date="2024-01-01",
    end_date="2024-12-31"
)

print(f"총 판매액: {sales_report['total_sales']}")
print(f"총 주문 수: {sales_report['total_orders']}")
print(f"평균 주문액: {sales_report['average_order_value']}")

# 판매 파이프라인 보고서
pipeline_report = client.get_pipeline_report()

for stage in pipeline_report['stages']:
    print(f"단계: {stage['name']}, 건수: {stage['count']}, 가치: {stage['value']}")
```

### ユーザー情報

```python
# 현재 사용자 정보
user_info = client.get_user_info()
print(f"사용자: {user_info['name']}, 이메일: {user_info['email']}")
```

＃＃取引段階（Stage）の例

- **prospect**: 顧客発掘段階
- **qualification**: 顧客資格ステップ
- **proposal**: 提案ステップ
- **negotiation**: 交渉段階
- **closed_won**: 成功で終了
- **closed_lost**: 失敗で終了

＃＃アクティビティタイプ（Type）の例

- **call**: 電話通話
- **email**: メール
- **meeting**: ミーティング/インタビュー
- **task**: タスク
- **note**: メモ

＃＃注文ステータス（Status）の例

- **pending**: 待機中
- **processing**: 処理中
- **shipped**: 配送中
- **delivered**: 配送完了
- **キャンセル済み**：キャンセル済み

## お支払い方法 (Payment Method) の例

- **bank_transfer**: 銀行振込
- **credit_card**: クレジットカード
- **paypal**: PayPal
- **cash**: 現金

##主な機能

- ✅顧客管理
- ✅販売機会（Deal）追跡
- ✅見積書の作成と管理
- ✅注文管理
- ✅活動（Activity）追跡
- ✅製品/サービス管理
- ✅販売レポートと分析
- ✅パイプライン追跡

##ライセンス

MIT License