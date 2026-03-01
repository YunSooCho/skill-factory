# Pinecone 벡터 데이터베이스 SDK

Pinecone는 고성능 벡터 유사도 검색을 위한 Python SDK입니다.

## 설치

```bash
pip install -r requirements.txt
```

## API 키 발급 방법

1. [Pinecone 웹사이트](https://www.pinecone.io)에 접속하여 계정을 생성합니다.
2. 대시보드에서 API Keys 섹션으로 이동합니다.
3. 'Create API Key' 버튼을 클릭하여 새 API 키를 생성합니다.
4. Environment 정보(예: us-west1-gcp)를 확인합니다.
5. 생성된 API 키를 안전한 곳에 저장합니다.

## 사용법

### 클라이언트 초기화

```python
from pinecone import PineconeClient

client = PineconeClient(
    api_key="your_api_key_here",
    environment="us-west1-gcp"
)
```

### 인덱스 생성

```python
response = client.create_index(
    name="my-index",
    dimension=1536,  # OpenAI embeddings 용
    metric="cosine",
    pods=1,
    replicas=1
)

print(f"인덱스 생성 완료: {response}")
```

### 벡터 업서트 (Upsert)

```python
vectors = [
    {
        'id': 'vec1',
        'values': [0.1, 0.2, 0.3, 0.4, 0.5],
        'metadata': {
            'category': 'electronics',
            'product_id': 'p123',
            'price': 99.99
        }
    },
    {
        'id': 'vec2',
        'values': [0.5, 0.4, 0.3, 0.2, 0.1],
        'metadata': {
            'category': 'books',
            'product_id': 'b456',
            'price': 29.99
        }
    }
]

result = client.upsert_vectors(
    index_name="my-index",
    vectors=vectors,
    namespace="products"
)

print(f"업서트된 벡터 수: {result['upsertedCount']}")
```

### 벡터 검색

```python
query_vector = [0.15, 0.18, 0.35, 0.42, 0.48]

results = client.query_vectors(
    index_name="my-index",
    vector=query_vector,
    top_k=5,
    namespace="products",
    include_metadata=True,
    filter={'category': 'electronics'}
)

for match in results.get('matches', []):
    print(f"ID: {match['id']}, Score: {match['score']}")
    if match.get('metadata'):
        print(f"  Metadata: {match['metadata']}")
```

### 벡터 가져오기

```python
vectors = client.fetch_vectors(
    index_name="my-index",
    ids=['vec1', 'vec2'],
    namespace="products"
)

for vec_id, vector_data in vectors.get('vectors', {}).items():
    print(f"벡터 ID: {vec_id}")
    print(f"  차원: {len(vector_data['values'])}")
```

### 벡터 업데이트

```python
client.update_vector(
    index_name="my-index",
    id="vec1",
    set_metadata={'price': 89.99, 'discount': True}
)
```

### 벡터 삭제

```python
# 특정 ID로 삭제
client.delete_vectors(
    index_name="my-index",
    ids=['vec1', 'vec2'],
    namespace="products"
)

# 필터로 삭제
client.delete_vectors(
    index_name="my-index",
    filter={'category': 'books'},
    namespace="products"
)

# 네임스페이스의 모든 벡터 삭제
client.delete_vectors(
    index_name="my-index",
    delete_all=True,
    namespace="products"
)
```

### 인덱스 관리

```python
# 모든 인덱스 목록
indexes = client.list_indexes()
for index in indexes:
    print(f"인덱스: {index['name']}, 차원: {index['dimension']}")

# 인덱스 상세 정보
details = client.describe_index("my-index")
print(f"상태: {details['status']['ready']}")

# 인덱스 통계
stats = client.get_index_stats("my-index")
print(f"전체 벡터 수: {stats.get('totalVectorCount', 0)}")

# 인덱스 삭제
client.delete_index("my-index")
```

### 컬렉션 관리

```python
# 컬렉션 생성 (인덱스 스냅샷)
client.create_collection(
    name="my-collection",
    source="my-index"
)

# 컬렉션 목록
collections = client.list_collections()

# 컬렉션에서 인덱스 생성
client.create_index_from_collection(
    name="restored-index",
    collection_name="my-collection"
)

# 컬렉션 삭제
client.delete_collection("my-collection")
```

## 주요 기능

- ✅ 벡터 인덱스 생성 및 관리
- ✅ 대규모 벡터 업서트 (배치 처리 지원)
- ✅ 고성능 유사도 검색
- ✅ 메타데이터 필터링
- ✅ 네임스페이스 지원
- ✅ 컬렉션을 통한 스냅샷 및 복원
- ✅ 실시간 인덱싱
- ✅ 다양한 거리 지표 (cosine, euclidean, dotproduct)

## 라이선스

MIT License