import logging
import os
from pymilvus import connections, utility

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clear_collection(collection_name: str = "embedding_test"):
    """
    지정된 Milvus 컬렉션을 삭제합니다.
    
    Args:
        collection_name (str): 삭제할 컬렉션 이름 (기본값: "embedding_test")
    """
    try:
        # Milvus 연결
        connections.connect(
            host=os.getenv("MILVUS_HOST", "localhost"),
            port=os.getenv("MILVUS_PORT", "19530")
        )
        logger.info("✅ Milvus 연결 성공!")
        
        # 컬렉션 존재 여부 확인
        collections = utility.list_collections()
        logger.info(f"📋 현재 컬렉션 목록: {collections}")
        
        if collection_name in collections:
            # 컬렉션 삭제
            utility.drop_collection(collection_name)
            logger.info(f"🗑️ 컬렉션 '{collection_name}' 삭제 완료!")
            
            # 삭제 확인
            updated_collections = utility.list_collections()
            logger.info(f"📋 삭제 후 컬렉션 목록: {updated_collections}")
        else:
            logger.warning(f"⚠️ 컬렉션 '{collection_name}'이 존재하지 않습니다.")
            
    except Exception as e:
        logger.error(f"❌ 컬렉션 삭제 실패: {e}")
        raise

def get_collections_info():
    """
    모든 컬렉션의 정보를 동적으로 가져옵니다.
    
    Returns:
        dict: 컬렉션 정보 딕셔너리
    """
    try:
        # Milvus 연결
        connections.connect(
            host=os.getenv("MILVUS_HOST", "localhost"),
            port=os.getenv("MILVUS_PORT", "19530")
        )
        
        # 모든 컬렉션 목록 동적으로 가져오기
        collections = utility.list_collections()
        
        collections_info = {}
        for collection_name in collections:
            try:
                from pymilvus import Collection
                collection = Collection(collection_name)
                collection.load()
                
                # 컬렉션 정보 수집
                collections_info[collection_name] = {
                    "name": collection_name,
                    "num_entities": collection.num_entities,
                    "schema_fields": [field.name for field in collection.schema.fields],
                    "indexes": collection.indexes
                }
                
                logger.info(f"📊 컬렉션 '{collection_name}': {collection.num_entities}개 데이터")
                
            except Exception as e:
                logger.warning(f"⚠️ 컬렉션 '{collection_name}' 정보 가져오기 실패: {e}")
                collections_info[collection_name] = {"name": collection_name, "error": str(e)}
        
        return collections_info
        
    except Exception as e:
        logger.error(f"❌ 컬렉션 정보 가져오기 실패: {e}")
        return {}

def list_collections():
    """
    모든 컬렉션 목록을 동적으로 가져와서 출력합니다.
    """
    try:
        # Milvus 연결
        connections.connect(
            host=os.getenv("MILVUS_HOST", "localhost"),
            port=os.getenv("MILVUS_PORT", "19530")
        )
        logger.info("✅ Milvus 연결 성공!")
        
        # 모든 컬렉션 목록 동적으로 가져오기
        collections = utility.list_collections()
        
        if not collections:
            logger.info("📭 현재 컬렉션이 없습니다.")
            return []
        
        logger.info(f"📋 현재 컬렉션 목록 ({len(collections)}개):")
        for i, collection_name in enumerate(collections, 1):
            logger.info(f"  {i}. {collection_name}")
        
        return collections
        
    except Exception as e:
        logger.error(f"❌ 컬렉션 목록 가져오기 실패: {e}")
        return []

def clear_all_collections():
    """
    모든 컬렉션을 삭제합니다.
    """
    try:
        # Milvus 연결
        connections.connect(
            host=os.getenv("MILVUS_HOST", "localhost"),
            port=os.getenv("MILVUS_PORT", "19530")
        )
        logger.info("✅ Milvus 연결 성공!")
        
        # 모든 컬렉션 목록 동적으로 가져오기
        collections = utility.list_collections()
        logger.info(f"📋 삭제 전 컬렉션 목록: {collections}")
        
        if not collections:
            logger.info("📭 삭제할 컬렉션이 없습니다.")
            return
        
        # 모든 컬렉션 삭제
        for collection_name in collections:
            utility.drop_collection(collection_name)
            logger.info(f"🗑️ 컬렉션 '{collection_name}' 삭제 완료!")
        
        logger.info("🎉 모든 컬렉션이 삭제되었습니다!")
        
    except Exception as e:
        logger.error(f"❌ 컬렉션 삭제 실패: {e}")
        raise

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--all":
            # 모든 컬렉션 삭제
            clear_all_collections()
        elif sys.argv[1] == "--list":
            # 컬렉션 목록만 보기
            list_collections()
        elif sys.argv[1] == "--info":
            # 컬렉션 상세 정보 보기
            collections_info = get_collections_info()
            logger.info("📊 컬렉션 상세 정보:")
            for name, info in collections_info.items():
                logger.info(f"  {name}: {info}")
        else:
            # 특정 컬렉션 삭제
            collection_name = sys.argv[1]
            clear_collection(collection_name)
    else:
        # 기본: 컬렉션 목록 보기
        logger.info("🔍 사용법:")
        logger.info("  python clear_collection.py              # 컬렉션 목록 보기")
        logger.info("  python clear_collection.py --list       # 컬렉션 목록 보기")
        logger.info("  python clear_collection.py --info       # 컬렉션 상세 정보 보기")
        logger.info("  python clear_collection.py --all        # 모든 컬렉션 삭제")
        logger.info("  python clear_collection.py '컬렉션명'   # 특정 컬렉션 삭제")
        logger.info("")
        list_collections() 