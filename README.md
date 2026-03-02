# Skill Factory (スキルファクトリー)

> **Skill Factory**は、日本のSaaSエコシステム全体をカバーする大規模なAPI / SDKインターロック実装リポジトリです。
> 1,000以上のB2Bサービス仕様を収集し、OpenClaw AIがすぐに活用できる形態のスキルデータベースを構築することを目指します。

---

## 🏗️ プロジェクトアーキテクチャ (Kanban Workflow)

このリポジトリは、**750以上のサービス**を効率的に管理し、進捗状況を一目で把握するために、ディレクトリ構造自体が巨大な**カンバンボード**として機能するように設計されています。巨大な外部Excelや進捗も追跡スクリプトなしで**ファイルシステム（フォルダ移動）**だけで状態を管理します。

### 🗂️コアフォルダ構造

合計751のサービスは、用途に応じて** 20のビジネスカテゴリ**（「01_Marketing」、「06_Accounting」など）に分類され、「repo /」ディレクトリの下にあります。

```text
repo/
├── 01_Marketing/           # 카테고리명
│   ├── developed/          # [To-Do] 개발 및 스펙 수집 완료 (테스트 작성이 필요한 상태)
│   │   ├── activecampaign/
│   │   │   ├── client.py   # API 구현체
│   │   │   └── SPEC.md     # 📄 해당 서비스의 요구사항 및 API 명세서
│   │   └── hubspot/
│   └── verified/           # [Done] 검증 및 테스트 통과 완료 (배포 준비 완료 상태)
│       └── mailchimp/
│           ├── client.py
│           ├── SPEC.md
│           └── tests/      # ✅ 테스트 코드가 작성된 상태
```

---

＃＃🚀開発者＆AIコラボレーションワークフロー

1. **タスク割り当て(Pick)**
   - `repo/*/developed/`フォルダ内で作業するサービスを1つ選択します。
   
2. **仕様書の確認と開発(Develop & Test)**
   - 該当するサービスフォルダ内に同梱されている「SPEC.md」を開き、要件を確認します。
   - `client.py`にAPI連携コードを実装し、 `tests /`フォルダを作成して検証コードを作成します。

3. **作業完了処理(Move to Verified)**
   - 機能およびテスト作成が100%完了したら、該当サービスのフォルダを丸ごと**`developed/`から`verified/`に移動(Move)**させます。
   - この「フォルダを移動する行為」自体が進捗率上昇を意味する物理的証票になります。

---

## 📊 進捗率の把握方法

既存の複雑なPython進捗状況追跡スクリプトはすべて削除されました（レガシー）。
現在の統合状態やチームの生産性を確認したい場合は、単に端末で** `verified`フォルダと `developed`フォルダの数を数えること**で100%正確なリアルタイム進捗度を把握できます。

```bash
# 예시: 검증 완료된 서비스 개수 파악
find repo/ -type d -path "*/verified/*" -mindepth 1 -maxdepth 1 | wc -l
```

---

## ⚙️ 要件

- Python 3.10+
- `aiohttp`、`pytest`などの個々のサービス `requirements.txt`に指定されたパッケージ
- **Zero Configuration**: 複雑な依存関係なしにすぐに実行できるように設計

---

##🤖ターゲットユーザー

**このプロジェクトの主なユーザーはAIです。**

OpenClaw AIシステムはすぐにこのリポジトリの構造（ `client.py`、 `SPEC.md`）を解析し、何百ものインターロックスキルを自動生成し、サービスエージェントに注入します。

---

## 📝 License

MIT License

**Skill Factory** · Made for OpenClaw · by [YunSooCho](https://github.com/YunSooCho)