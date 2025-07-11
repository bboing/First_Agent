from pymilvus import utility

def drop_embedding_collection():
    """
    Milvus의 embedding_test 컬렉션을 삭제합니다.
    웹/관리자에서 호출 시 기존 데이터 전체 삭제 및 스키마 초기화 용도로 사용.
    """
    collection_name = "embedding_test"
    if collection_name in utility.list_collections():
        utility.drop_collection(collection_name)
        print(f"{collection_name} 컬렉션 삭제 완료!")
    else:
        print(f"{collection_name} 컬렉션이 존재하지 않습니다.") 