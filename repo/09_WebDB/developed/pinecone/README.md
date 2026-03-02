# Pinecone Vector Database SDK

Pineconeは、高性能ベクトル類似度検索のためのPython SDKです。

## インストール

```bash
pip install -r requirements.txt
```

## API キーの発行方法

1. [Pineconeウェブサイト]（https://www.pinecone.io)에にアクセスしてアカウントを作成します。
2.ダッシュボードのAPI Keysセクションに移動します。
3. [Create API Key]ボタンをクリックして新しいAPIキーを生成します。
4. Environment情報（us-west1-gcpなど）を確認します。
5. 生成された API キーを安全な場所に保存します。

##使用法

### クライアントの初期化

```python
from pinecone import PineconeClient

client = PineconeClient(
    api_key="your_api_key_here",
    environment="us-west1-gcp"
)
```

### インデックスの生成

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

### ベクトルアップサート(Upsert)

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

###ベクトル検索

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

### ベクトルの取得

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

###ベクトル更新

```python
client.update_vector(
    index_name="my-index",
    id="vec1",
    set_metadata={'price': 89.99, 'discount': True}
)
```

### ベクトルの削除

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

### インデックス管理

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

### コレクション管理

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

##主な機能

- ✅ベクトルインデックスの作成と管理
- ✅大規模ベクトルアップサート(バッチ処理サポート)
- ✅高性能類似度検索
- ✅メタデータフィルタリング
- ✅ネームスペースサポート
- ✅コレクションによるスナップショットと復元
- ✅リアルタイムインデックス作成
- ✅様々な距離指標（cosine、euclidean、dotproduct）

##ライセンス

MIT License