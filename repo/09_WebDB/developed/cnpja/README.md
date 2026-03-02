# CNPJA - Brazilian Company Registry API

CNPJA provides access to the Brazilian National Company Registry (Cadastro Nacional da Pessoa Jurídica), allowing you to query company information by CNPJ number.

## インストール

```bash
pip install -r requirements.txt
```

## API キーの発行方法

1. [CNPJAウェブサイト]（https://cnpj.ws)에にアクセスします。
2.無料APIの使用は限られた数で可能です。
3. さらにリクエストが必要な場合は、有料プランからAPIキーを発行します。
4. APIキーが発行されたら、クライアントの初期化に使用します。

##使用法

### クライアントの初期化

```python
from cnpja import CNPJAClient

# 무료 API (기본)
client = CNPJAClient()

# 프리미엄 API
client = CNPJAClient(api_key="your_api_key_here")
```

###会社情報の照会

```python
cnpj = "00.000.000/0001-91"

# 전체 회사 정보
company = client.get_company(cnpj)

print(f"회사명: {company['razao_social']}")
print(f"상호명: {company['nome_fantasia']}")
print(f"상태: {company['descricao_situacao_cadastral']}")
print(f"설립일: {company['data_inicio_atividade']}")
```

### CNPJ検証

```python
cnpj = "00.000.000/0001-91"

if client.validate_cnpj(cnpj):
    print("유효한 CNPJ입니다")
else:
    print("유효하지 않은 CNPJ입니다")
```

###会社概要情報

```python
summary = client.get_company_summary("00.000.000/0001-91")

print(f"CNPJ: {summary['cnpj']}")
print(f"회사명: {summary['name']}")
print(f"상태: {summary['status']}")
print(f"주소: {summary['address']['city']}, {summary['address']['state']}")
print(f"주요 활동: {summary['activities']['primary']}")
```

### QSA（資格のある株主）情報

```python
qsa_list = client.get_company_qsa("00.000.000/0001-91")

for qsa in qsa_list:
    print(f"이름: {qsa['nome']}")
    print(f"역할: {qsa['qualificacao']}")
    print(f"대표자 여부: {qsa['representante_legal']}")
```

###会社パートナー情報

```python
partners = client.get_company_partners("00.000.000/0001-91")

for partner in partners:
    print(f"이름: {partner['nome']}")
    print(f"참여율: {partner['percentual_capital']}%")
    print(f"담당자 역할: {partner['qualificacao_socio']}")
```

###会社活動(CNAE)情報

```python
activities = client.get_company_activities("00.000.000/0001-91")

print("주요 활동:")
print(f"코드: {activities['atividade_principal'][0]['codigo']}")
print(f"설명: {activities['atividade_principal'][0]['descricao']}")

print("\n부수 활동:")
for atv in activities['atividades_secundarias']:
    print(f"  {atv['codigo']} - {atv['descricao']}")
```

### Simples Nacionalについて

```python
simples = client.get_company_simples("00.000.000/0001-91")

print(f"Simples Nacional: {simples['simples']}")
print(f"MEI: {simples['mei']}")
print(f"옵션: {simples['opcao_pelo_simples']}")
```

###会社登録履歴

```python
history = client.get_company_history("00.000.000/0001-91")

for entry in history:
    print(f"날짜: {entry['data']}")
    print(f"이벤트: {entry['evento']}")
    print(f"상태: {entry['situacao']}")
```

###会社検索

```python
# 프리미엄 API 기능
results = client.lookup_company(
    name="Empresa LTDA",
    city="São Paulo",
    state="SP",
    limit=5
)

for company in results:
    print(f"{company['cnpj']} - {company['razao_social']}")
```

### CNPJフォーマット

```python
# 14자리 숫자
cnpj_raw = "00000000000191"
formatted = client.format_cnpj(cnpj_raw)
print(formatted)  # "00.000.000/0001-91"
```

##主な機能

- ✅ CNPJで会社情報を照会
- ✅ CNPJ検証
- ✅ QSA（資格のある株主）情報
- ✅パートナー/株主情報
- ✅経済活動(CNAE)情報
- ✅ Simples Nacional ステータス
- ✅会社登録履歴
- ✅住所と連絡先情報
- ✅ CNPJフォーマット

## エラー処理

```python
try:
    company = client.get_company("invalid-cnpj")
except ValueError as e:
    print(f"CNPJ를 찾을 수 없습니다: {e}")
except Exception as e:
    print(f"API 오류: {e}")
```

##規制と使用制限

- 無料API：リクエスト数制限
- プレミアムAPI：より多くのリクエストが可能
- 商業使用時にライセンス確認が必要
- データを使用する際に元のソース表記が必要

##ライセンス

MIT License