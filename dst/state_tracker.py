def get_user_intent(query: str) -> str:
    """
    사용자의 입력에서 의도를 파악하는 함수
    
    Args:
        query (str): 사용자의 입력 쿼리
        
    Returns:
        str: 파악된 의도 ('rag' 또는 'ml')
    """
    # TODO: 실제 의도 파악 로직 구현
    # 임시로 간단한 키워드 기반 분류
    rag_keywords = ['검색', '찾아', 'rag', '검색해', '찾아줘']
    ml_keywords = ['학습', '예측', '분류', 'ml', '머신러닝']
    
    query = query.lower()
    
    if any(keyword in query for keyword in rag_keywords):
        return "rag"
    elif any(keyword in query for keyword in ml_keywords):
        return "ml"
    else:
        return "unknown" 