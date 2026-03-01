# CNPJA - Brazilian Company Registry API

CNPJA provides access to the Brazilian National Company Registry (Cadastro Nacional da Pessoa Jurídica), allowing you to query company information by CNPJ number.

## 설치

```bash
pip install -r requirements.txt
```

## API 키 발급 방법

1. [CNPJA 웹사이트](https://cnpj.ws)에 접속합니다.
2. 무료 API 사용은 제한된 수로 가능합니다.
3. 더 많은 요청이 필요하면 유료 플랜에서 API 키를 발급받습니다.
4. API 키를 발급받으면 클라이언트 초기화 시 사용합니다.

## 사용법

### 클라이언트 초기화

```python
from cnpja import CNPJAClient

# 무료 API (기본)
client = CNPJAClient()

# 프리미엄 API
client = CNPJAClient(api_key="your_api_key_here")
```

### 회사 정보 조회

```python
cnpj = "00.000.000/0001-91"

# 전체 회사 정보
company = client.get_company(cnpj)

print(f"회사명: {company['razao_social']}")
print(f"상호명: {company['nome_fantasia']}")
print(f"상태: {company['descricao_situacao_cadastral']}")
print(f"설립일: {company['data_inicio_atividade']}")
```

### CNPJ 유효성 검사

```python
cnpj = "00.000.000/0001-91"

if client.validate_cnpj(cnpj):
    print("유효한 CNPJ입니다")
else:
    print("유효하지 않은 CNPJ입니다")
```

### 회사 요약 정보

```python
summary = client.get_company_summary("00.000.000/0001-91")

print(f"CNPJ: {summary['cnpj']}")
print(f"회사명: {summary['name']}")
print(f"상태: {summary['status']}")
print(f"주소: {summary['address']['city']}, {summary['address']['state']}")
print(f"주요 활동: {summary['activities']['primary']}")
```

### QSA (자격 있는 주주) 정보

```python
qsa_list = client.get_company_qsa("00.000.000/0001-91")

for qsa in qsa_list:
    print(f"이름: {qsa['nome']}")
    print(f"역할: {qsa['qualificacao']}")
    print(f"대표자 여부: {qsa['representante_legal']}")
```

### 회사 파트너 정보

```python
partners = client.get_company_partners("00.000.000/0001-91")

for partner in partners:
    print(f"이름: {partner['nome']}")
    print(f"참여율: {partner['percentual_capital']}%")
    print(f"담당자 역할: {partner['qualificacao_socio']}")
```

### 회사 활동 (CNAE) 정보

```python
activities = client.get_company_activities("00.000.000/0001-91")

print("주요 활동:")
print(f"코드: {activities['atividade_principal'][0]['codigo']}")
print(f"설명: {activities['atividade_principal'][0]['descricao']}")

print("\n부수 활동:")
for atv in activities['atividades_secundarias']:
    print(f"  {atv['codigo']} - {atv['descricao']}")
```

### Simples Nacional 정보

```python
simples = client.get_company_simples("00.000.000/0001-91")

print(f"Simples Nacional: {simples['simples']}")
print(f"MEI: {simples['mei']}")
print(f"옵션: {simples['opcao_pelo_simples']}")
```

### 회사 등록 이력

```python
history = client.get_company_history("00.000.000/0001-91")

for entry in history:
    print(f"날짜: {entry['data']}")
    print(f"이벤트: {entry['evento']}")
    print(f"상태: {entry['situacao']}")
```

### 회사 검색

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

### CNPJ 포맷팅

```python
# 14자리 숫자
cnpj_raw = "00000000000191"
formatted = client.format_cnpj(cnpj_raw)
print(formatted)  # "00.000.000/0001-91"
```

## 주요 기능

- ✅ CNPJ로 회사 정보 조회
- ✅ CNPJ 유효성 검사
- ✅ QSA (자격 있는 주주) 정보
- ✅ 파트너/주주 정보
- ✅ 경제 활동 (CNAE) 정보
- ✅ Simples Nacional 상태
- ✅ 회사 등록 이력
- ✅ 주소 및 연락처 정보
- ✅ CNPJ 포맷팅

## 에러 처리

```python
try:
    company = client.get_company("invalid-cnpj")
except ValueError as e:
    print(f"CNPJ를 찾을 수 없습니다: {e}")
except Exception as e:
    print(f"API 오류: {e}")
```

## 규제 및 사용 제한

- 무료 API: 요청 수 제한
- 프리미엄 API: 더 많은 요청 가능
- 상업적 사용 시 라이선스 확인 필요
- 데이터 사용 시 원본 출처 표기 필요

## 라이선스

MIT License