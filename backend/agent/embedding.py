import logging
import os
import pandas as pd
from langchain_openai import AzureOpenAIEmbeddings
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility


logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)

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
    logger.info("embedding.py: ✅ Milvus 연결 성공!")
    MILVUS_AVAILABLE = True
except Exception as e:
    logger.warning(f"embedding.py: ⚠️ Milvus 연결 실패: {e}")
    logger.info("embedding.py: Milvus 없이 애플리케이션을 실행합니다.")
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
        schema = CollectionSchema(fields, description="Cyberlogitec Test Collection")
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
        
        logger.info(f"embedding.py: 🔧 Milvus 인덱스 생성: {index_type}")
        collection.create_index(field_name="embedding", index_params=index_params)
        collection.load()
        return collection
    else:
        collection = Collection(name)
        collection.load()
        return collection

def extract_topic(text: str, collection_name: str = None) -> str:
    from langchain_openai import AzureChatOpenAI
    from langchain_core.messages import HumanMessage
    
    # 컬렉션 이름이 제공되지 않은 경우 기본값 사용
    if collection_name is None:
        collection_name = "Booking_Embedding"
    
    llm = AzureChatOpenAI(
        azure_deployment=os.getenv("DEPLOYMENT_CHAT"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        openai_api_type="azure"
    )
    
    # 컬렉션 정보를 포함한 프롬프트 생성
    prompt = f"다음 텍스트의 주제를 짧은 문장으로 요약해줘. 컨텍스트: {collection_name} 관련 문서\n텍스트: {text[:300]}"
    return llm.invoke([HumanMessage(content=prompt)]).content

if MILVUS_AVAILABLE:
    try:
        collection = recreate_collection_if_needed(collection_name, len(vector))
        logger.info(f"embedding.py: ✅ 컬렉션 '{collection_name}' 준비 완료")
    except Exception as e:
        logger.error(f"embedding.py: ❌ 컬렉션 생성 실패: {e}")
        collection = None
else:
    collection = None

# 6. Milvus에 벡터 삽입
def insert_text_and_embedding(text: str, page: int, category: str, topic: str):
    global collection
    
    # 컬렉션이 None이거나 오류가 발생한 경우 다시 초기화 시도
    if collection is None:
        try:
            vector = get_embedding("이 문장을 벡터로 변환해줘")
            collection = recreate_collection_if_needed(collection_name, len(vector))
            logger.info(f"embedding.py: ✅ 컬렉션 '{collection_name}' 재초기화 완료")
        except Exception as e:
            logger.error(f"embedding.py: ❌ 컬렉션 재초기화 실패: {e}")
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
        logger.info(f"embedding.py: Milvus에 벡터 저장 완료! (page: {page}, category: {category}, topic: {topic}, text: {text[:50]}...)")
    except Exception as e:
        logger.error(f"embedding.py: ❌ 벡터 삽입 실패: {e}")
        # 컬렉션이 삭제되었을 가능성이 있으므로 None으로 설정하여 다음 호출 시 재초기화
        collection = None
        raise

# 7. Milvus에서 벡터 검색
def search_similar_texts(query: str, limit: int = 3, similarity_threshold: float = 0.7, collection_name: str = None):
    """
    주어진 쿼리와 유사한 텍스트를 Milvus에서 검색합니다.
    
    Args:
        query (str): 검색할 쿼리
        limit (int): 반환할 최대 결과 수
        similarity_threshold (float): 유사도 임계값 (0~1, 1에 가까울수록 유사)
        collection_name (str): 사용할 벡터 데이터베이스 컬렉션 이름 (선택사항)
    
    Returns:
        list: 임계값을 만족하는 검색 결과들
    """
    global collection
    
    if not MILVUS_AVAILABLE:
        logger.warning("embedding.py: ⚠️ Milvus가 연결되지 않아 검색을 수행할 수 없습니다.")
        return []
    
    # 컬렉션이 None인 경우 재초기화 시도
    if collection is None:
        try:
            vector = get_embedding("이 문장을 벡터로 변환해줘")
            # collection_name이 제공되면 해당 컬렉션 사용, 없으면 기본값
            target_collection = collection_name if collection_name else "Booking_Embedding"
            collection = recreate_collection_if_needed(target_collection, len(vector))
            logger.info(f"embedding.py: ✅ 컬렉션 '{target_collection}' 재초기화 완료")
        except Exception as e:
            logger.error(f"embedding.py: ❌ 컬렉션 재초기화 실패: {e}")
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
    
    collection_info = f" (컬렉션: {collection_name})" if collection_name else ""
    logger.info(f"embedding.py: 🔍 검색 결과{collection_info}: {len(results[0])}개 중 {len(filtered_results)}개가 임계값({similarity_threshold}) 이상")
    for hit in filtered_results:
        logger.info(f"embedding.py:   - 유사도: {hit.distance:.3f}, 텍스트: {hit.entity.get('text')[:50]}...")
    
    return filtered_results

# 8. 임시 파일에서 청킹된 텍스트 처리
def process_chunks(chunks: list, category: str = "", collection_name: str = None):
    """
    (텍스트, 페이지번호) 리스트와 카테고리를 받아 임베딩 및 벡터DB에 저장합니다.
    Args:
        chunks (list): (텍스트, 페이지번호) 튜플 리스트
        category (str): 수동 입력 카테고리 (선택 사항)
        collection_name (str): 벡터 데이터베이스 컬렉션 이름 (선택 사항)
    """
    for i, (text, page) in enumerate(chunks):
        logger.info(f"embedding.py: 💾 청크 {i+1}/{len(chunks)} 임베딩 중... (page: {page}, category: {category}, collection: {collection_name})")
        topic_llm = extract_topic(text, collection_name)
        # 카테고리가 있으면 토픽에 포함, 없으면 LLM이 추출한 토픽만 사용
        topic = f"{category} - {topic_llm}" if category else topic_llm
        insert_text_and_embedding(text, page, category, topic)
    logger.info(f"embedding.py: 🎉 모든 청크가 벡터DB에 저장되었습니다!")

# 8-1. 테이블 메타데이터를 포함한 청크 처리 (개선된 버전)
def process_chunks_with_metadata(chunks: list, collection_name: str = None):
    """
    (텍스트, 페이지번호, 카테고리, 토픽, 테이블메타데이터) 리스트를 받아 임베딩 및 벡터DB에 저장합니다.
    Args:
        chunks (list): (텍스트, 페이지번호, 카테고리, 토픽, 테이블메타데이터) 튜플 리스트
        collection_name (str): 벡터 데이터베이스 컬렉션 이름 (선택 사항)
    """
    table_count = 0
    text_count = 0
    
    logger.info(f"embedding.py: 🚀 컬렉션 '{collection_name}'에서 청크 처리 시작")
    
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
                logger.warning(f"embedding.py: ⚠️ 빈 텍스트 건너뛰기 (청크 {i+1})")
                continue
            
            logger.info(f"embedding.py: 💾 청크 {i+1}/{len(chunks)} 임베딩 중... (page: {page}, category: {category}, topic: {topic[:50]}..., collection: {collection_name})")
            
            # 테이블 메타데이터가 있으면 추가 정보 로깅
            if table_metadata:
                table_count += 1
                logger.info(f"embedding.py: 📊 테이블 정보 - 행: {table_metadata.get('rows', 'N/A')}, 열: {table_metadata.get('columns', 'N/A')}, 키: {table_metadata.get('key', 'N/A')}")
                
                # 병합된 테이블 정보
                if table_metadata.get('merged_indices'):
                    logger.info(f"embedding.py: 🔗 병합된 테이블 - 병합된 인덱스: {table_metadata.get('merged_indices')}")
            else:
                text_count += 1
            
            insert_text_and_embedding(text, page, category, topic)
            
        except Exception as e:
            logger.error(f"embedding.py: ❌ 청크 {i+1} 처리 중 오류: {e}")
            continue
    
    logger.info(f"embedding.py: 🎉 모든 청크가 벡터DB에 저장되었습니다!")
    logger.info(f"embedding.py: 📈 통계 - 테이블: {table_count}개, 일반 텍스트: {text_count}개, 총: {len(chunks)}개, 컬렉션: {collection_name}")


def process_excel_file_for_embedding(excel_file_path: str, md_file_name: str):
    """
    엑셀 파일을 읽어서 임베딩 처리하는 함수
    Args:
        excel_file_path (str): 엑셀 파일 경로
        md_file_name (str): 파일명 (타임스탬프 제거된)
    """
    if not MILVUS_AVAILABLE:
        logger.warning("embedding.py: ⚠️ Milvus가 연결되지 않아 임베딩을 수행할 수 없습니다.")
        return
    
    try:
        # 엑셀 파일 읽기
        logger.info(f"embedding.py: 📖 엑셀 파일 읽기: {excel_file_path}")
        df = pd.read_excel(excel_file_path)
        
        logger.info(f"embedding.py: 🚀 {len(df)}개 행의 임베딩 처리 시작")
        
        for idx, row in df.iterrows():
            try:
                # 필요한 컬럼들 추출
                content = row['content']
                pages = row['pages'] if 'pages' in row else [1]
                page = pages[0] if isinstance(pages, list) else pages
                
                # depth 정보 추출
                depth_1 = row.get('1 depth', '')
                depth_2 = row.get('2 depth', '')
                depth_3 = row.get('3 depth', '')
                depth_4 = row.get('4 depth', '')
                
                # 카테고리와 토픽 생성
                if any([depth_1, depth_2, depth_3, depth_4]):
                    # depth가 있으면 구조화된 문서
                    category = "Structured_Document"
                    topic_parts = [d for d in [depth_1, depth_2, depth_3, depth_4] if d]
                    topic = " > ".join(topic_parts)[:200]  # 길이 제한
                else:
                    # depth가 없으면 일반 텍스트
                    category = "Text"
                    topic = f"Page_{page}"
                
                # 텍스트가 튜플인 경우 처리
                if isinstance(content, tuple):
                    content = content[4] if len(content) >= 5 else str(content)
                
                # 페이지 번호 정수 변환
                if not isinstance(page, int):
                    page = int(page) if page else 1
                
                logger.info(f"embedding.py: 📄 임베딩 처리: {category} - {topic} (페이지: {page})")
                
                insert_text_and_embedding(content, page, category, topic)
                
                if (idx + 1) % 10 == 0:
                    logger.info(f"embedding.py: 📈 진행률: {idx + 1}/{len(df)} 완료")
                    
            except Exception as e:
                logger.error(f"embedding.py: ❌ 행 {idx} 처리 실패: {e}")
                continue
        
        logger.info(f"embedding.py: ✅ 엑셀 파일 임베딩 처리 완료!")
        
    except Exception as e:
        logger.error(f"embedding.py: ❌ 엑셀 파일 처리 실패: {e}")
        raise


# 9. 컬렉션 정보 확인
def check_collection_info():
    """
    벡터 데이터베이스 연결 상태와 기본 정보를 확인합니다.
    """
    if not MILVUS_AVAILABLE:
        logger.warning("embedding.py: ⚠️ Milvus 연결이 불가능합니다.")
        return False
    
    try:
        # 연결 확인
        utility.get_server_version()
        logger.info("embedding.py: ✅ Milvus 연결 성공!")
        
        # 전체 컬렉션 목록만 간단히 표시
        collections = utility.list_collections()
        logger.info(f"embedding.py: 📋 사용 가능한 컬렉션: {collections}")
        
        return True
        
    except Exception as e:
        logger.error(f"embedding.py: ❌ Milvus 연결 실패: {e}")
        return False

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
