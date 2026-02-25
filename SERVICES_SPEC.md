# Services Specification (메인 목록 - 업종별)

## 🎯 전체 집계

| 총 서비스 | 음식/레스토랑 | 소매/EC | 기업/사무 | 제조 | 의료 | 교육 |
|---------|-------------|--------|---------|------|------|------|
| 11 | 4 | 4 | 3 | 0 | 0 | 0 |

---

## 📋 서비스 목록 (업종별)

### ☕ 음식 & 레스토랑

| # | 서비스 | 카테고리 | 홈페이지 | 상태 | 개발 | 테스트 | 스펙 파일 |
|---|--------|---------|---------|------|------|--------|---------|
| 1 | eat POS | POS | [eat-sys.jp](https://www.eat-sys.jp) | 📋 대기 | 0% | 0% | [eat-pos.md](services/eat-pos.md) |
| 2 | GMO Payment | 결제 | [gmo-pg.jp](https://www.gmo-pg.jp) | 📋 대기 | 0% | 0% | [gmo-payment.md](services/gmo-payment.md) |
| 3 | StoreMix | 예약 | [store.mixi.co.jp](https://store.mixi.co.jp) | 📋 대기 | 0% | 0% | [storemix.md](services/storemix.md) |
| 4 | TableCheck | 예약 | [tablecheck.com](https://www.tablecheck.com) | 📋 대기 | 0% | 0% | [tablecheck.md](services/tablecheck.md) |

---

### 🛍️ 소매 & EC

| # | 서비스 | 카테고리 | 홈페이지 | 상태 | 개발 | 테스트 | 스펙 파일 |
|---|--------|---------|---------|------|------|--------|---------|
| 1 | Rakuten | EC | [rakuten.co.jp](https://www.rakuten.co.jp) | 🔨 개발중 | 30% | 0% | [rakuten-web-service.md](services/rakuten-web-service.md) |
| 2 | GMO Payment | 결제 | [gmo-pg.jp](https://www.gmo-pg.jp) | 🔨 개발중 | 30% | 0% | [gmo-payment-gateway.md](services/gmo-payment-gateway.md) |
| 3 | Shopify | EC | [shopify.com](https://www.shopify.com) | 📋 대기 | 0% | 0% | [shopify.md](services/shopify.md) |
| 4 | BASE | EC | [thebase.in](https://thebase.in) | 📋 대기 | 0% | 0% | [base.md](services/base.md) |

---

### 💼 기업/사무

| # | 서비스 | 카테고리 | 홈페이지 | 상태 | 개발 | 테스트 | 스펙 파일 |
|---|--------|---------|---------|------|------|--------|---------|
| 1 | freee | 회계 | [freee.co.jp](https://www.freee.co.jp) | 📋 대기 | 0% | 0% | [freee-accounting.md](services/freee-accounting.md) |
| 2 | money forward | 회계 | [moneyforward.com](https://www.moneyforward.com) | 📋 대기 | 0% | 0% | [money-forward.md](services/money-forward.md) |
| 3 | kintone | 그룹웨어 | [kintone.cybozu.co.jp](https://kintone.cybozu.co.jp) | 📋 대기 | 0% | 0% | [kintone.md](services/kintone.md) |

---

## 🎯 진척 상태 가이드

| 상태 | 이모지 | 설명 |
|------|-------|------|
| 📋 대기 | 서비스 발견, 스킬 생성 전 |
| 🔨 개발중 | 스킬 생성, 코드 작성 중 |
| ✅ 개발완료 | 스킬 코드 완성 |
| 🧪 테스트중 | 테스트 실행 중 |
| ✅ 테스트완료 | 모든 테스트 통과 |
| 🚀 배포완료 | 배포 및 공유 완료 |
| ❌ 실패 | 오류/문제 발생 |

---

## 🔄 하트비트 통합

### 하트비트 작업 절차

1. **업종별 서비스 발견**
   - INDUSTRY_SERVICES.md 기반
   - 각 업종의 필수 SaaS 서비스 발견
   - 딥 스크래핑으로 상세 정보 추출

2. **스킬 생성**
   - 업종별로 스킬 생성
   - 개발 상태 추적

3. **테스트**
   - 테스트 상태 추적
   - 결과 기록

4. **정보 업데이트**
   - 하트비트마다 SERVICES_SPEC.md 업데이트 (업종별 그룹화)
   - 홈페이지 링크 포함

---

## 🏢 업종별 필수 서비스 목록

| 업종 | 필수 서비스 |
|------|-----------|
| 음식/레스토랑 | eat POS, GMO Payment, StoreMix, TableCheck |
| 소매/EC | Rakuten, GMO Payment, Shopify, BASE |
| 기업/사무 | freee, money forward, kintone |
| 제조 | SAP ERP, Oracle NetSuite |
| 의료 | MUSE, e-Medical |
| 교육 | Google Workspace, Zoom |

---

## 📁 리포지토리 관리

- **위치:** `/Users/clks001/.openclow/workspace/skill-factory`
- **GitHub:** https://github.com/YunSooCho/skill-factory.git (프라이벗 🔒)
- **INDUSTRY_SERVICES.md:** 업종별 필수 서비스 목록

---

**관리자:** 지니 (Genie) 🧞
**버전:** v4.0 (업종별 + 홈페이지 링크)
**마지막 업데이트:** 2026-02-24 23:45

---

## 🔄 하트비트 업데이트 기록

- 2026-02-24 23:42: 서비스별 md 파일 분리
- 2026-02-24 23:45: 업종별 그룹화 + 홈페이지 링크 추가

## 🔄 하트비트 업데이트 (2026-02-24 23:46:17) - 업종별

📊 **총 4개 서비스 발견**

### 🏢 소매 & EC

| 서비스 | 홈페이지 | 상태 | 개발 |
|--------|---------|------|------|
| GMO Payment | [https://www.gmo-pg.jp](https://www.gmo-pg.jp) | 🔨 개발중 | 30% |
| Rakuten | [https://www.rakuten.co.jp](https://www.rakuten.co.jp) | 🔨 개발중 | 30% |

### 🏢 음식 & 레스토랑

| 서비스 | 홈페이지 | 상태 | 개발 |
|--------|---------|------|------|
| eat POS | [https://www.eat-sys.jp](https://www.eat-sys.jp) | 📋 대기 | 0% |

### 🏢 기업/사무

| 서비스 | 홈페이지 | 상태 | 개발 |
|--------|---------|------|------|
| freee | [https://www.freee.co.jp](https://www.freee.co.jp) | 📋 대기 | 0% |



## 🔄 하트비트 업데이트 (2026-02-25 00:03:54) - 업종별

📊 **총 4개 서비스 발견**

### 🏢 소매 & EC

| 서비스 | 홈페이지 | 상태 | 개발 |
|--------|---------|------|------|
| GMO Payment | [https://www.gmo-pg.jp](https://www.gmo-pg.jp) | 🔨 개발중 | 30% |
| Rakuten | [https://www.rakuten.co.jp](https://www.rakuten.co.jp) | 🔨 개발중 | 30% |

### 🏢 기업/사무

| 서비스 | 홈페이지 | 상태 | 개발 |
|--------|---------|------|------|
| freee | [https://www.freee.co.jp](https://www.freee.co.jp) | 📋 대기 | 0% |

### 🏢 음식 & 레스토랑

| 서비스 | 홈페이지 | 상태 | 개발 |
|--------|---------|------|------|
| eat POS | [https://www.eat-sys.jp](https://www.eat-sys.jp) | 📋 대기 | 0% |



## 🔄 하트비트 업데이트 (2026-02-25 09:30:09) - 로테이션 #1

📊 **총 20개 서비스 발견 (인덱스: 20-40)**

| # | 서비스 | 업종 | 홈페이지 | 상태 | 개발 |
|---|--------|------|---------|------|------|
| 1 | Chatwork | 커뮤니케이션 | [https://go.chatwork.com](https://go.chatwork.com) | 📋 대기 | 0% |
| 2 | Slack | 커뮤니케이션 | [https://slack.com](https://slack.com) | 📋 대기 | 0% |
| 3 | Microsoft Teams | 커뮤니케이션 | [https://www.microsoft.com/ja-jp/microsoft-teams](https://www.microsoft.com/ja-jp/microsoft-teams) | 📋 대기 | 0% |
| 4 | LINE WORKS | 커뮤니케이션 | [https://line.worksmobile.co.jp](https://line.worksmobile.co.jp) | 📋 대기 | 0% |
| 5 | Cisco Webex | 커뮤니케이션 | [https://www.webex.com/jp](https://www.webex.com/jp) | 📋 대기 | 0% |
| 6 | Rakuten Ichiba | EC | [https://www.rakuten.co.jp](https://www.rakuten.co.jp) | 📋 대기 | 0% |
| 7 | Shopify Japan | EC | [https://www.shopify.com/ja](https://www.shopify.com/ja) | 📋 대기 | 0% |
| 8 | BASE | EC | [https://thebase.in](https://thebase.in) | 📋 대기 | 0% |
| 9 | Stores.jp | EC | [https://stores.jp](https://stores.jp) | 📋 대기 | 0% |
| 10 | MakeShop | EC | [https://www.makeshop.jp](https://www.makeshop.jp) | 📋 대기 | 0% |
| 11 | CartStar | EC | [https://cartstar.jp](https://cartstar.jp) | 📋 대기 | 0% |
| 12 | GMO Payment | 결제 | [https://www.gmo-pg.jp](https://www.gmo-pg.jp) | 📋 대기 | 0% |
| 13 | SB Payment | 결제 | [https://www.softbankpayment.co.jp](https://www.softbankpayment.co.jp) | 📋 대기 | 0% |
| 14 | Stripe Japan | 결제 | [https://stripe.com/ja](https://stripe.com/ja) | 📋 대기 | 0% |
| 15 | Square Japan | 결제 | [https://squareup.com/ja/jp](https://squareup.com/ja/jp) | 📋 대기 | 0% |
| 16 | PayPay | 결제 | [https://paypay.ne.jp](https://paypay.ne.jp) | 📋 대기 | 0% |
| 17 | Re:amaze | 고객지원 | [https://www.reamaze.com](https://www.reamaze.com) | 📋 대기 | 0% |
| 18 | Zendesk Japan | 고객지원 | [https://www.zendesk.jp](https://www.zendesk.jp) | 📋 대기 | 0% |
| 19 | Freshdesk Japan | 고객지원 | [https://freshdesk.com/ja](https://freshdesk.com/ja) | 📋 대기 | 0% |
| 20 | Help Scout | 고객지원 | [https://www.helpscout.com](https://www.helpscout.com) | 📋 대기 | 0% |


## 🔄 하트비트 업데이트 (2026-02-25 09:30:11) - 로테이션 #1

📊 **총 20개 서비스 발견 (인덱스: 20-40)**

| # | 서비스 | 업종 | 홈페이지 | 상태 | 개발 |
|---|--------|------|---------|------|------|
| 1 | Chatwork | 커뮤니케이션 | [https://go.chatwork.com](https://go.chatwork.com) | 📋 대기 | 0% |
| 2 | Slack | 커뮤니케이션 | [https://slack.com](https://slack.com) | 📋 대기 | 0% |
| 3 | Microsoft Teams | 커뮤니케이션 | [https://www.microsoft.com/ja-jp/microsoft-teams](https://www.microsoft.com/ja-jp/microsoft-teams) | 📋 대기 | 0% |
| 4 | LINE WORKS | 커뮤니케이션 | [https://line.worksmobile.co.jp](https://line.worksmobile.co.jp) | 📋 대기 | 0% |
| 5 | Cisco Webex | 커뮤니케이션 | [https://www.webex.com/jp](https://www.webex.com/jp) | 📋 대기 | 0% |
| 6 | Rakuten Ichiba | EC | [https://www.rakuten.co.jp](https://www.rakuten.co.jp) | 📋 대기 | 0% |
| 7 | Shopify Japan | EC | [https://www.shopify.com/ja](https://www.shopify.com/ja) | 📋 대기 | 0% |
| 8 | BASE | EC | [https://thebase.in](https://thebase.in) | 📋 대기 | 0% |
| 9 | Stores.jp | EC | [https://stores.jp](https://stores.jp) | 📋 대기 | 0% |
| 10 | MakeShop | EC | [https://www.makeshop.jp](https://www.makeshop.jp) | 📋 대기 | 0% |
| 11 | CartStar | EC | [https://cartstar.jp](https://cartstar.jp) | 📋 대기 | 0% |
| 12 | GMO Payment | 결제 | [https://www.gmo-pg.jp](https://www.gmo-pg.jp) | 📋 대기 | 0% |
| 13 | SB Payment | 결제 | [https://www.softbankpayment.co.jp](https://www.softbankpayment.co.jp) | 📋 대기 | 0% |
| 14 | Stripe Japan | 결제 | [https://stripe.com/ja](https://stripe.com/ja) | 📋 대기 | 0% |
| 15 | Square Japan | 결제 | [https://squareup.com/ja/jp](https://squareup.com/ja/jp) | 📋 대기 | 0% |
| 16 | PayPay | 결제 | [https://paypay.ne.jp](https://paypay.ne.jp) | 📋 대기 | 0% |
| 17 | Re:amaze | 고객지원 | [https://www.reamaze.com](https://www.reamaze.com) | 📋 대기 | 0% |
| 18 | Zendesk Japan | 고객지원 | [https://www.zendesk.jp](https://www.zendesk.jp) | 📋 대기 | 0% |
| 19 | Freshdesk Japan | 고객지원 | [https://freshdesk.com/ja](https://freshdesk.com/ja) | 📋 대기 | 0% |
| 20 | Help Scout | 고객지원 | [https://www.helpscout.com](https://www.helpscout.com) | 📋 대기 | 0% |


## 🔄 하트비트 업데이트 (2026-02-25 09:31:11) - 로테이션 #1

📊 **총 20개 서비스 발견 (인덱스: 20-40)**

| # | 서비스 | 업종 | 홈페이지 | 상태 | 개발 |
|---|--------|------|---------|------|------|
| 1 | Chatwork | 커뮤니케이션 | [https://go.chatwork.com](https://go.chatwork.com) | 📋 대기 | 0% |
| 2 | Slack | 커뮤니케이션 | [https://slack.com](https://slack.com) | 📋 대기 | 0% |
| 3 | Microsoft Teams | 커뮤니케이션 | [https://www.microsoft.com/ja-jp/microsoft-teams](https://www.microsoft.com/ja-jp/microsoft-teams) | 📋 대기 | 0% |
| 4 | LINE WORKS | 커뮤니케이션 | [https://line.worksmobile.co.jp](https://line.worksmobile.co.jp) | 📋 대기 | 0% |
| 5 | Cisco Webex | 커뮤니케이션 | [https://www.webex.com/jp](https://www.webex.com/jp) | 📋 대기 | 0% |
| 6 | Rakuten Ichiba | EC | [https://www.rakuten.co.jp](https://www.rakuten.co.jp) | 📋 대기 | 0% |
| 7 | Shopify Japan | EC | [https://www.shopify.com/ja](https://www.shopify.com/ja) | 📋 대기 | 0% |
| 8 | BASE | EC | [https://thebase.in](https://thebase.in) | 📋 대기 | 0% |
| 9 | Stores.jp | EC | [https://stores.jp](https://stores.jp) | 📋 대기 | 0% |
| 10 | MakeShop | EC | [https://www.makeshop.jp](https://www.makeshop.jp) | 📋 대기 | 0% |
| 11 | CartStar | EC | [https://cartstar.jp](https://cartstar.jp) | 📋 대기 | 0% |
| 12 | GMO Payment | 결제 | [https://www.gmo-pg.jp](https://www.gmo-pg.jp) | 📋 대기 | 0% |
| 13 | SB Payment | 결제 | [https://www.softbankpayment.co.jp](https://www.softbankpayment.co.jp) | 📋 대기 | 0% |
| 14 | Stripe Japan | 결제 | [https://stripe.com/ja](https://stripe.com/ja) | 📋 대기 | 0% |
| 15 | Square Japan | 결제 | [https://squareup.com/ja/jp](https://squareup.com/ja/jp) | 📋 대기 | 0% |
| 16 | PayPay | 결제 | [https://paypay.ne.jp](https://paypay.ne.jp) | 📋 대기 | 0% |
| 17 | Re:amaze | 고객지원 | [https://www.reamaze.com](https://www.reamaze.com) | 📋 대기 | 0% |
| 18 | Zendesk Japan | 고객지원 | [https://www.zendesk.jp](https://www.zendesk.jp) | 📋 대기 | 0% |
| 19 | Freshdesk Japan | 고객지원 | [https://freshdesk.com/ja](https://freshdesk.com/ja) | 📋 대기 | 0% |
| 20 | Help Scout | 고객지원 | [https://www.helpscout.com](https://www.helpscout.com) | 📋 대기 | 0% |


## 🔄 하트비트 업데이트 (2026-02-25 09:31:42) - 로테이션 #1

📊 **총 20개 서비스 발견 (인덱스: 20-40)**

| # | 서비스 | 업종 | 홈페이지 | 상태 | 개발 |
|---|--------|------|---------|------|------|
| 1 | Chatwork | 커뮤니케이션 | [https://go.chatwork.com](https://go.chatwork.com) | 📋 대기 | 0% |
| 2 | Slack | 커뮤니케이션 | [https://slack.com](https://slack.com) | 📋 대기 | 0% |
| 3 | Microsoft Teams | 커뮤니케이션 | [https://www.microsoft.com/ja-jp/microsoft-teams](https://www.microsoft.com/ja-jp/microsoft-teams) | 📋 대기 | 0% |
| 4 | LINE WORKS | 커뮤니케이션 | [https://line.worksmobile.co.jp](https://line.worksmobile.co.jp) | 📋 대기 | 0% |
| 5 | Cisco Webex | 커뮤니케이션 | [https://www.webex.com/jp](https://www.webex.com/jp) | 📋 대기 | 0% |
| 6 | Rakuten Ichiba | EC | [https://www.rakuten.co.jp](https://www.rakuten.co.jp) | 📋 대기 | 0% |
| 7 | Shopify Japan | EC | [https://www.shopify.com/ja](https://www.shopify.com/ja) | 📋 대기 | 0% |
| 8 | BASE | EC | [https://thebase.in](https://thebase.in) | 📋 대기 | 0% |
| 9 | Stores.jp | EC | [https://stores.jp](https://stores.jp) | 📋 대기 | 0% |
| 10 | MakeShop | EC | [https://www.makeshop.jp](https://www.makeshop.jp) | 📋 대기 | 0% |
| 11 | CartStar | EC | [https://cartstar.jp](https://cartstar.jp) | 📋 대기 | 0% |
| 12 | GMO Payment | 결제 | [https://www.gmo-pg.jp](https://www.gmo-pg.jp) | 📋 대기 | 0% |
| 13 | SB Payment | 결제 | [https://www.softbankpayment.co.jp](https://www.softbankpayment.co.jp) | 📋 대기 | 0% |
| 14 | Stripe Japan | 결제 | [https://stripe.com/ja](https://stripe.com/ja) | 📋 대기 | 0% |
| 15 | Square Japan | 결제 | [https://squareup.com/ja/jp](https://squareup.com/ja/jp) | 📋 대기 | 0% |
| 16 | PayPay | 결제 | [https://paypay.ne.jp](https://paypay.ne.jp) | 📋 대기 | 0% |
| 17 | Re:amaze | 고객지원 | [https://www.reamaze.com](https://www.reamaze.com) | 📋 대기 | 0% |
| 18 | Zendesk Japan | 고객지원 | [https://www.zendesk.jp](https://www.zendesk.jp) | 📋 대기 | 0% |
| 19 | Freshdesk Japan | 고객지원 | [https://freshdesk.com/ja](https://freshdesk.com/ja) | 📋 대기 | 0% |
| 20 | Help Scout | 고객지원 | [https://www.helpscout.com](https://www.helpscout.com) | 📋 대기 | 0% |


## 🔄 하트비트 업데이트 (2026-02-25 10:25:29) - 업종별

📊 **총 4개 서비스 발견**

### 🏢 소매 & EC

| 서비스 | 홈페이지 | 상태 | 개발 |
|--------|---------|------|------|
| GMO Payment | [https://www.gmo-pg.jp](https://www.gmo-pg.jp) | 🔨 개발중 | 30% |
| Rakuten | [https://www.rakuten.co.jp](https://www.rakuten.co.jp) | 🔨 개발중 | 30% |

### 🏢 기업/사무

| 서비스 | 홈페이지 | 상태 | 개발 |
|--------|---------|------|------|
| freee | [https://www.freee.co.jp](https://www.freee.co.jp) | 📋 대기 | 0% |

### 🏢 음식 & 레스토랑

| 서비스 | 홈페이지 | 상태 | 개발 |
|--------|---------|------|------|
| eat POS | [https://www.eat-sys.jp](https://www.eat-sys.jp) | 📋 대기 | 0% |

