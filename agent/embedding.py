from langchain_openai import AzureOpenAIEmbeddings
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility
from dotenv import load_dotenv
import os
import sys
import re

# 1. 환경변수 로드
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..",  ".env"))
print(f".env path: {dotenv_path}  exists: {os.path.exists(dotenv_path)}")
load_dotenv(dotenv_path)

# 2. Azure OpenAI 임베딩 모델 준비
embedding_model = AzureOpenAIEmbeddings(
    azure_deployment=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    openai_api_type="azure",
    chunk_size=1000
)

# 3. 임베딩 생성
def get_embedding(text: str):
    return embedding_model.embed_query(text)

# 4. Milvus 연결
try:
    connections.connect(
        host=os.getenv("MILVUS_HOST", "localhost"),
        port=os.getenv("MILVUS_PORT", "19530")
    )
    print("✅ Milvus 연결 성공!")
    MILVUS_AVAILABLE = True
except Exception as e:
    print(f"⚠️ Milvus 연결 실패: {e}")
    print("Milvus 없이 애플리케이션을 실행합니다.")
    MILVUS_AVAILABLE = False

# 5. Milvus 컬렉션 생성 (없으면)
def recreate_collection_if_needed(name: str, vector_dim: int):
    if name not in utility.list_collections():
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=vector_dim),
            FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=2048),
            FieldSchema(name="page", dtype=DataType.INT64),
            FieldSchema(name="category", dtype=DataType.VARCHAR, max_length=128),
            FieldSchema(name="topic", dtype=DataType.VARCHAR, max_length=256)
        ]
        schema = CollectionSchema(fields, description="임베딩 테스트용 컬렉션")
        collection = Collection(name=name, schema=schema)
        collection.create_index(
            field_name="embedding",
            index_params={"index_type": "IVF_FLAT", "metric_type": "COSINE", "params": {"nlist": 128}}
        )
        collection.load()
        return collection
    else:
        collection = Collection(name)
        collection.load()
        return collection

# LLM을 이용한 topic 추출 함수 예시 (OpenAI)
def extract_topic(text: str) -> str:
    from langchain_openai import AzureOpenAI
    llm = AzureOpenAI(
        azure_deployment=os.getenv("DEPLOYMENT_CHAT"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        openai_api_type="azure"
    )
    prompt = f"다음 텍스트의 주제를 짧은 문장으로 요약해줘:\n{text[:300]}"
    return llm(prompt)

collection_name = "embedding_test"
vector = get_embedding("이 문장을 벡터로 변환해줘")

if MILVUS_AVAILABLE:
    collection = recreate_collection_if_needed(collection_name, len(vector))
else:
    collection = None

# 6. Milvus에 벡터 삽입
def insert_text_and_embedding(text: str, page: int, category: str, topic: str):
    vector = [float(x) for x in get_embedding(text)]
    insert_data = [
        {
            "embedding": vector,
            "text": text,
            "page": page,
            "category": category,
            "topic": topic
        }
    ]
    collection.insert(insert_data)
    collection.flush()
    print(f"Milvus에 벡터 저장 완료! (page: {page}, category: {category}, topic: {topic}, text: {text[:50]}...)")

# 7. Milvus에서 벡터 검색
def search_similar_texts(query: str, limit: int = 3, similarity_threshold: float = 0.7):
    """
    유사한 텍스트를 검색합니다.
    
    Args:
        query (str): 검색할 쿼리
        limit (int): 반환할 최대 결과 수
        similarity_threshold (float): 유사도 임계값 (0~1, 1에 가까울수록 유사)
    
    Returns:
        list: 임계값을 만족하는 검색 결과들
    """
    if not MILVUS_AVAILABLE:
        print("⚠️ Milvus가 연결되지 않아 검색을 수행할 수 없습니다.")
        return []
    
    query_vector = get_embedding(query)
    search_params = {"metric_type": "COSINE", 
                     "params": {"nprobe": 10}}
    results = collection.search(
        data=[query_vector],
        anns_field="embedding",
        param=search_params,
        limit=limit,
        output_fields=["text"]
    )

    # 유사도 임계값 필터링
    filtered_results = []
    for hits in results:
        for hit in hits:
            # cosine 유사도: 1에 가까울수록 유사, 임계값 이상인 것만 필터링
            if hit.distance >= similarity_threshold:
                filtered_results.append(hit)
    
    print(f"🔍 검색 결과: {len(results[0])}개 중 {len(filtered_results)}개가 임계값({similarity_threshold}) 이상")
    for hit in filtered_results:
        print(f"  - 유사도: {hit.distance:.3f}, 텍스트: {hit.entity.get('text')[:50]}...")
    
    return filtered_results

# 8. 임시 파일에서 청킹된 텍스트 처리
def process_chunks(chunks: list, category: str):
    """
    (텍스트, 페이지번호) 리스트와 카테고리를 받아 임베딩 및 벡터DB에 저장합니다.
    Args:
        chunks (list): (텍스트, 페이지번호) 튜플 리스트
        category (str): 수동 입력 카테고리
    """
    for i, (text, page) in enumerate(chunks):
        print(f"💾 청크 {i+1}/{len(chunks)} 임베딩 중... (page: {page}, category: {category})")
        topic_llm = extract_topic(text)
        topic = f"{category} - {topic_llm}"
        insert_text_and_embedding(text, page, category, topic)
    print(f"🎉 모든 청크가 벡터DB에 저장되었습니다!")

# 9. 컬렉션 정보 확인
def check_collection_info():
    """
    Milvus 컬렉션 정보를 확인합니다.
    """
    print("📊 Milvus 컬렉션 정보 확인")
    print("=" * 50)
    
    # 모든 컬렉션 목록
    collections = utility.list_collections()
    print(f"📋 전체 컬렉션 개수: {len(collections)}")
    for col in collections:
        print(f"  - {col}")
    
    # embedding_test 컬렉션 정보
    if "embedding_test" in collections:
        collection = Collection("embedding_test")
        collection.load()
        
        # 데이터 개수
        num_entities = collection.num_entities
        print(f"\n📈 embedding_test 컬렉션:")
        print(f"  - 저장된 데이터 개수: {num_entities}")
        
        # 스키마 정보
        schema = collection.schema
        print(f"  - 필드 개수: {len(schema.fields)}")
        for field in schema.fields:
            print(f"    * {field.name}: {field.dtype}")
        
        # 샘플 데이터 확인 (처음 3개)
        if num_entities > 0:
            print(f"\n📝 샘플 데이터 (처음 3개):")
            results = collection.query(
                expr="id >= 0",
                output_fields=["id", "text"],
                limit=3
            )
            for i, result in enumerate(results):
                text = result['text'][:100] + "..." if len(result['text']) > 100 else result['text']
                print(f"  {i+1}. ID: {result['id']}, 텍스트: {text}")
    else:
        print("❌ embedding_test 컬렉션이 없습니다.")

if __name__ == "__main__":
    # 명령행 인수로 임시 파일 경로 받기
    if len(sys.argv) > 1:
        temp_file_path = sys.argv[1]
        process_chunked_file(temp_file_path)
    else:
        # 컬렉션 정보 확인
        check_collection_info()
        
        # 예시: 텍스트 삽입
        # insert_text_and_embedding("이 문장을 벡터로 변환해줘")
        # insert_text_and_embedding("비슷한 의미의 문장도 넣어보자")
        # 예시: 검색
        # print("\n--- 유사 문장 검색 결과 ---")
        # search_similar_texts("문장 벡터화 해줘")
