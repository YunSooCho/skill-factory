# Qdrant 벡터 데이터베이스 SDK

Qdrant는 고성능 벡터 유사도 검색을 위한 오픈소스 벡터 데이터베이스에 대한 Python SDK입니다.

## 설치

```bash
pip install -r requirements.txt
```

## API 키 발급 방법

1. [Qdrant Cloud](https://cloud.qdrant.io/)에 접속하여 계정을 생성합니다.
2. 새 클러스터를 생성하거나 기존 클러스터를 선택합니다.
3. API 탭에서 API 키를 생성합니다.
4. 클러스터 URL과 API 키를 안전한 곳에 저장합니다.

## 사용법

### 클라이언트 초기화

```python
from qdrant import QdrantClient

client = QdrantClient(
    api_key="your_api_key_here",
    url="https://your-cluster.qdrant.io"
)
```

### 컬렉션 관리

```python
# 모든 컬렉션 목록
collections = client.get_collections()
for collection in collections['result']['collections']:
    print(f"컬렉션: {collection['name']}")

# 컬렉션 생성
client.create_collection(
    collection_name="documents",
    vector_size=768,
    distance="Cosine",
    hnsw_config={
        "m": 16,
        "ef_construct": 100
    }
)

# 컬렉션 상세 정보
collection_info = client.get_collection("documents")
print(f"벡터 수: {collection_info['result']['points_count']}")

# 컬렉션 업데이트
client.update_collection(
    collection_name="documents",
    optimizers_config={
        "indexing_threshold": 20000
    }
)

# 컬렉션 삭제
client.delete_collection("documents")

# 컬렉션 재생성
client.recreate_collection(
    collection_name="documents",
    vector_size=768,
    distance="Cosine"
)
```

### 포인트(Point) 관리

```python
# 포인트 삽입
client.upsert(
    collection_name="documents",
    points=[
        {
            "id": 1,
            "vector": [0.1, 0.2, 0.3, ...],
            "payload": {
                "title": "문서 제목",
                "content": "문서 내용",
                "category": "기술"
            }
        },
        {
            "id": 2,
            "vector": [0.4, 0.5, 0.6, ...],
            "payload": {
                "title": "또 다른 문서",
                "content": "내용...",
                "category": "마케팅"
            }
        }
    ]
)

# 단일 포인트 조회
point = client.get_point(
    collection_name="documents",
    point_id=1,
    with_payload=True,
    with_vector=False
)

# 여러 포인트 조회
points = client.get_points(
    collection_name="documents",
    ids=[1, 2, 3],
    with_payload=True,
    with_vector=False
)

# 스크롤을 통한 모든 포인트 조회
all_points = client.scroll(
    collection_name="documents",
    limit=100,
    with_payload=True
)

# 포인트 삭제
client.delete_points(
    collection_name="documents",
    points=[1, 2, 3]
)

# 필터를 통한 포인트 삭제
client.delete_points(
    collection_name="documents",
    filter={
        "must": [
            {
                "key": "category",
                "match": {"value": "기술"}
            }
        ]
    }
)
```

### 벡터 검색

```python
# 벡터 검색
results = client.search(
    collection_name="documents",
    query_vector=[0.1, 0.2, 0.3, ...],
    limit=10,
    with_payload=True,
    with_vector=False,
    score_threshold=0.7
)

for result in results['result']:
    print(f"점수: {result['score']}")
    print(f"제목: {result['payload']['title']}")

# 필터와 함께 검색
results = client.search(
    collection_name="documents",
    query_vector=[0.1, 0.2, 0.3, ...],
    limit=5,
    filter={
        "must": [
            {
                "key": "category",
                "match": {"value": "기술"}
            }
        ]
    }
)

# 일괄 검색
search_requests = [
    {
        "vector": [0.1, 0.2, 0.3, ...],
        "limit": 5
    },
    {
        "vector": [0.4, 0.5, 0.6, ...],
        "limit": 5
    }
]

batch_results = client.search_batch(
    collection_name="documents",
    search_requests=search_requests
)
```

### 추천 검색

```python
# 양성/음성 벡터를 사용한 추천
recommendations = client.recommend(
    collection_name="documents",
    positive=[[0.1, 0.2, 0.3, ...], [0.4, 0.5, 0.6, ...]],
    negative=[[0.7, 0.8, 0.9, ...]],
    limit=10,
    with_payload=True
)

for rec in recommendations['result']:
    print(f"추천: {rec['payload']['title']}, 점수: {rec['score']}")
```

### 벡터 업데이트

```python
# 벡터 업데이트
client.update_vectors(
    collection_name="documents",
    points=[
        {
            "id": 1,
            "vector": [0.9, 0.8, 0.7, ...]
        }
    ]
)

# 벡터 삭제
client.delete_vectors(
    collection_name="documents",
    points=[
        {"id": 1}
    ]
)
```

### 페이로드(Payload) 관리

```python
# 페이로드 업데이트
client.update_payload(
    collection_name="documents",
    payload={
        "status": "검토 완료",
        "review_date": "2024-12-25"
    },
    points=[1, 2, 3]
)

# 필터를 통한 페이로드 업데이트
client.update_payload(
    collection_name="documents",
    payload={"priority": "높음"},
    filter={
        "must": [
            {"key": "category", "match": {"value": "기술"}}
        ]
    }
)

# 페이로드 키 삭제
client.delete_payload(
    collection_name="documents",
    keys=["temp_field"],
    points=[1, 2, 3]
)

# 페이로드 전체 삭제
client.clear_payload(
    collection_name="documents",
    points=[1]
)

# 포인트와 함께 페이로드 키 삭제
client.delete_payload(
    collection_name="documents",
    keys=["tags"],
    filter={
        "must": [
            {"key": "category", "match": {"value": "구형"}}
        ]
    }
)
```

### 필터링 및 인덱스

```python
# 페이로드 인덱스 생성
client.create_index(
    collection_name="documents",
    field_name="category",
    field_schema={"type": "keyword"}
)

# 페이로드 인덱스 삭제
client.delete_index(
    collection_name="documents",
    field_name="category"
)
```

### 카운트 및 통계

```python
# 컬렉션 전체 포인트 수
count = client.count(collection_name="documents")
print(f"총 포인트: {count['result']['count']}")

# 필터로 카운트
filtered_count = client.count(
    collection_name="documents",
    filter={
        "must": [
            {"key": "category", "match": {"value": "기술"}}
        ]
    }
)
```

### 클러스터 정보

```python
# 클러스터 정보 조회
cluster_info = client.get_cluster_info()
print(f"클러스터 상태: {cluster_info['status']}")
```

### 컬렉션 잠금/잠금 해제

```python
# 컬렉션 잠금
client.lock_collection(
    collection_name="documents",
    reason="유지보수"
)

# 컬렉션 잠금 해제
client.unlock_collection(collection_name="documents")
```

## 필터 예제

```python
# 정확히 일치
filter = {
    "must": [
        {"key": "category", "match": {"value": "기술"}}
    ]
}

# 범위 검색
filter = {
    "must": [
        {
            "key": "score",
            "range": {"gte": 0.8, "lte": 1.0}
        }
    ]
}

# 여러 조건 (AND)
filter = {
    "must": [
        {"key": "category", "match": {"value": "기술"}},
        {"key": "year", "range": {"gte": 2020}}
    ]
}

# 여러 조건 (OR)
filter = {
    "should": [
        {"key": "category", "match": {"value": "기술"}},
        {"key": "category", "match": {"value": "과학"}}
    ]
}

# 조건 부정
filter = {
    "must_not": [
        {"key": "status", "match": {"value": "삭제됨"}}
    ]
}
```

## 주요 기능

- ✅ 컬렉션 생성 및 관리
- ✅ 벡터 삽입, 업데이트, 삭제
- ✅ 고성능 벡터 유사도 검색
- ✅ 필터링 및 추천
- ✅ 페이로드 관리
- ✅ 일괄 작업 지원
- ✅ 페이로드 인덱싱
- ✅ 다양한 거리 메트릭 (Cosine, Euclidean, Dot)
- ✅ 클러스터 관리

## 거리 메트릭

- **Cosine**: 코사인 유사도 (기본값)
- **Euclidean**: 유클리드 거리
- **Dot**: 내적

## 라이선스

MIT License