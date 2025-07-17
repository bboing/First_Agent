import logging
import os
from langchain_openai import AzureOpenAIEmbeddings
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility



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
    logging.info("embedding.py: ✅ Milvus 연결 성공!")
    MILVUS_AVAILABLE = True
except Exception as e:
    logging.warning(f"embedding.py: ⚠️ Milvus 연결 실패: {e}")
    logging.info("embedding.py: Milvus 없이 애플리케이션을 실행합니다.")
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
        
        # 압축 알고리즘 선택 (환경 변수로 설정 가능)
        index_type = os.getenv("MILVUS_INDEX_TYPE", "IVF_FLAT")
        
        # 인덱스 파라미터 설정
        if index_type == "IVF_FLAT":
            index_params = {
                "index_type": "IVF_FLAT",
                "metric_type": "COSINE",
                "params": {"nlist": int(os.getenv("MILVUS_NLIST", "128"))}
            }
        elif index_type == "IVF_SQ8":
            index_params = {
                "index_type": "IVF_SQ8",
                "metric_type": "COSINE",
                "params": {"nlist": int(os.getenv("MILVUS_NLIST", "128"))}
            }
        elif index_type == "IVF_PQ":
            index_params = {
                "index_type": "IVF_PQ",
                "metric_type": "COSINE",
                "params": {
                    "nlist": int(os.getenv("MILVUS_NLIST", "128")),
                    "m": int(os.getenv("MILVUS_PQ_M", "8")),  # 서브벡터 개수
                    "nbits": int(os.getenv("MILVUS_PQ_NBITS", "8"))  # 비트 수
                }
            }
        elif index_type == "HNSW":
            index_params = {
                "index_type": "HNSW",
                "metric_type": "COSINE",
                "params": {
                    "M": int(os.getenv("MILVUS_HNSW_M", "16")),
                    "efConstruction": int(os.getenv("MILVUS_HNSW_EF_CONSTRUCTION", "200"))
                }
            }
        else:
            # 기본값
            index_params = {
                "index_type": "IVF_FLAT",
                "metric_type": "COSINE",
                "params": {"nlist": 128}
            }
        
        logging.info(f"embedding.py: 🔧 Milvus 인덱스 생성: {index_type}")
        collection.create_index(field_name="embedding", index_params=index_params)
        collection.load()
        return collection
    else:
        collection = Collection(name)
        collection.load()
        return collection

# LLM을 이용한 topic 추출 함수 예시 (OpenAI)
def extract_topic(text: str) -> str:
    from langchain_openai import AzureChatOpenAI
    from langchain_core.messages import HumanMessage # Code added by Gemini
    llm = AzureChatOpenAI( # Code added by Gemini
        azure_deployment=os.getenv("DEPLOYMENT_CHAT"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        openai_api_type="azure"
    )
    prompt = f"다음 텍스트의 주제를 짧은 문장으로 요약해줘:\n{text[:300]}"
    return llm.invoke([HumanMessage(content=prompt)]).content # Code added by Gemini

collection_name = "embedding_test"
vector = get_embedding("이 문장을 벡터로 변환해줘")

if MILVUS_AVAILABLE:
    try:
        collection = recreate_collection_if_needed(collection_name, len(vector))
        logging.info(f"embedding.py: ✅ 컬렉션 '{collection_name}' 준비 완료")
    except Exception as e:
        logging.error(f"embedding.py: ❌ 컬렉션 생성 실패: {e}")
        collection = None
else:
    collection = None

# 6. Milvus에 벡터 삽입
def insert_text_and_embedding(text: str, page: int, category: str, topic: str):
    if collection is None:
        logging.error("embedding.py: ❌ 컬렉션이 초기화되지 않았습니다.")
        return
    
    try:
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
        logging.info(f"embedding.py: Milvus에 벡터 저장 완료! (page: {page}, category: {category}, topic: {topic}, text: {text[:50]}...)")
    except Exception as e:
        logging.error(f"embedding.py: ❌ 벡터 삽입 실패: {e}")
        raise

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
        logging.warning("embedding.py: ⚠️ Milvus가 연결되지 않아 검색을 수행할 수 없습니다.")
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
    
    logging.info(f"embedding.py: 🔍 검색 결과: {len(results[0])}개 중 {len(filtered_results)}개가 임계값({similarity_threshold}) 이상")
    for hit in filtered_results:
        logging.info(f"embedding.py:   - 유사도: {hit.distance:.3f}, 텍스트: {hit.entity.get('text')[:50]}...")
    
    return filtered_results

# 8. 임시 파일에서 청킹된 텍스트 처리
def process_chunks(chunks: list, category: str = ""):
    """
    (텍스트, 페이지번호) 리스트와 카테고리를 받아 임베딩 및 벡터DB에 저장합니다.
    Args:
        chunks (list): (텍스트, 페이지번호) 튜플 리스트
        category (str): 수동 입력 카테고리 (선택 사항)
    """
    for i, (text, page) in enumerate(chunks):
        logging.info(f"embedding.py: 💾 청크 {i+1}/{len(chunks)} 임베딩 중... (page: {page}, category: {category})")
        topic_llm = extract_topic(text)
        # 카테고리가 있으면 토픽에 포함, 없으면 LLM이 추출한 토픽만 사용
        topic = f"{category} - {topic_llm}" if category else topic_llm
        insert_text_and_embedding(text, page, category, topic)
    logging.info(f"embedding.py: 🎉 모든 청크가 벡터DB에 저장되었습니다!")

# 8-1. 테이블 메타데이터를 포함한 청크 처리 (개선된 버전)
def process_chunks_with_metadata(chunks: list):
    """
    (텍스트, 페이지번호, 카테고리, 토픽, 테이블메타데이터) 리스트를 받아 임베딩 및 벡터DB에 저장합니다.
    Args:
        chunks (list): (텍스트, 페이지번호, 카테고리, 토픽, 테이블메타데이터) 튜플 리스트
    """
    table_count = 0
    text_count = 0
    
    for i, chunk_data in enumerate(chunks):
        try:
            if len(chunk_data) == 5:
                text, page, category, topic, table_metadata = chunk_data
            else:
                # 기존 형식 호환성 유지
                text, page = chunk_data[:2]
                category = chunk_data[2] if len(chunk_data) > 2 else ""
                topic = chunk_data[3] if len(chunk_data) > 3 else ""
                table_metadata = chunk_data[4] if len(chunk_data) > 4 else None
            
            # 텍스트 길이 검증
            if not text or len(text.strip()) == 0:
                logging.warning(f"embedding.py: ⚠️ 빈 텍스트 건너뛰기 (청크 {i+1})")
                continue
            
            logging.info(f"embedding.py: 💾 청크 {i+1}/{len(chunks)} 임베딩 중... (page: {page}, category: {category}, topic: {topic[:50]}...)")
            
            # 테이블 메타데이터가 있으면 추가 정보 로깅
            if table_metadata:
                table_count += 1
                logging.info(f"embedding.py: 📊 테이블 정보 - 행: {table_metadata.get('rows', 'N/A')}, 열: {table_metadata.get('columns', 'N/A')}, 키: {table_metadata.get('key', 'N/A')}")
                
                # 병합된 테이블 정보
                if table_metadata.get('merged_indices'):
                    logging.info(f"embedding.py: 🔗 병합된 테이블 - 병합된 인덱스: {table_metadata.get('merged_indices')}")
            else:
                text_count += 1
            
            insert_text_and_embedding(text, page, category, topic)
            
        except Exception as e:
            logging.error(f"embedding.py: ❌ 청크 {i+1} 처리 중 오류: {e}")
            continue
    
    logging.info(f"embedding.py: 🎉 모든 청크가 벡터DB에 저장되었습니다!")
    logging.info(f"embedding.py: 📈 통계 - 테이블: {table_count}개, 일반 텍스트: {text_count}개, 총: {len(chunks)}개")

# 9. 컬렉션 정보 확인
def check_collection_info():
    """
    Milvus 컬렉션 정보를 확인합니다.
    """
    logging.info("embedding.py: 📊 Milvus 컬렉션 정보 확인")
    logging.info("embedding.py: =" * 50)
    
    # 모든 컬렉션 목록
    collections = utility.list_collections()
    logging.info(f"embedding.py: 📋 전체 컬렉션 개수: {len(collections)}")
    for col in collections:
        logging.info(f"embedding.py:   - {col}")
    
    # embedding_test 컬렉션 정보
    if "embedding_test" in collections:
        collection = Collection("embedding_test")
        collection.load()
        
        # 데이터 개수
        num_entities = collection.num_entities
        logging.info(f"embedding.py: \n📈 embedding_test 컬렉션:")
        logging.info(f"embedding.py:   - 저장된 데이터 개수: {num_entities}")
        
        # 스키마 정보
        schema = collection.schema
        logging.info(f"embedding.py:   - 필드 개수: {len(schema.fields)}")
        for field in schema.fields:
            logging.info(f"embedding.py:     * {field.name}: {field.dtype}")
        
        # 샘플 데이터 확인 (처음 3개)
        if num_entities > 0:
            logging.info(f"embedding.py: \n📝 샘플 데이터 (처음 3개):")
            results = collection.query(
                expr="id >= 0",
                output_fields=["id", "text"],
                limit=3
            )
            for i, result in enumerate(results):
                text = result['text'][:100] + "..." if len(result['text']) > 100 else result['text']
                logging.info(f"embedding.py:   {i+1}. ID: {result['id']}, 텍스트: {text}")
    else:
        logging.info("embedding.py: ❌ embedding_test 컬렉션이 없습니다.")

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
