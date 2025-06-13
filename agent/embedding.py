from langchain_openai import AzureOpenAIEmbeddings
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility
from dotenv import load_dotenv
import os
import sys

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
connections.connect(
    host=os.getenv("MILVUS_HOST", "localhost"),
    port=os.getenv("MILVUS_PORT", "19530")
)

# 5. Milvus 컬렉션 생성 (없으면)
def recreate_collection_if_needed(name: str, vector_dim: int):
    if name not in utility.list_collections():
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=vector_dim),
            FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=2048)
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


collection_name = "embedding_test"
vector = get_embedding("이 문장을 벡터로 변환해줘")
collection = recreate_collection_if_needed(collection_name, len(vector))

# 6. Milvus에 벡터 삽입
def insert_text_and_embedding(text: str):
    vector = [float(x) for x in get_embedding(text)]

    insert_data = [
        {
            "embedding": vector,
            "text": text
        }
    ]
    collection.insert(insert_data)
    collection.flush()
    print(f"Milvus에 벡터 저장 완료! (text: {text[:50]}...)")

# 7. Milvus에서 벡터 검색
def search_similar_texts(query: str, limit: int = 3):
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

    return results
    # for hits in results:
    #     for hit in hits:
    #         print(f"Score: {hit.distance}, Text: {hit.entity.get('text')}")

# 8. 임시 파일에서 청킹된 텍스트 처리
def process_chunked_file(temp_file_path: str):
    """
    임시 파일에서 청킹된 텍스트를 읽어서 임베딩하고 벡터DB에 저장합니다.
    Args:
        temp_file_path (str): 임시 파일 경로
    """
    if not os.path.exists(temp_file_path):
        print(f"❌ 파일을 찾을 수 없습니다: {temp_file_path}")
        return
    
    print(f"📄 임시 파일 처리 시작: {temp_file_path}")
    
    with open(temp_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 청크별로 분리 (--- Chunk로 구분)
    chunks = content.split("--- Chunk")
    chunks = [chunk.strip() for chunk in chunks if chunk.strip()]
    
    print(f"✅ {len(chunks)}개 청크를 찾았습니다.")
    
    # 각 청크를 임베딩해서 벡터DB에 저장
    for i, chunk in enumerate(chunks):
        # "Chunk X ---" 부분 제거하고 실제 텍스트만 추출
        if "---" in chunk:
            text = chunk.split("---", 1)[1].strip()
        else:
            text = chunk
        
        if text:
            print(f"💾 청크 {i+1}/{len(chunks)} 임베딩 중...")
            insert_text_and_embedding(text)
    
    print(f"🎉 모든 청크가 벡터DB에 저장되었습니다!")
    
    # 임시 파일 삭제
    try:
        os.unlink(temp_file_path)
        print(f"🗑️ 임시 파일 삭제 완료: {temp_file_path}")
    except Exception as e:
        print(f"⚠️ 임시 파일 삭제 실패: {e}")

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
