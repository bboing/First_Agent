from agent.embedding import search_similar_texts
from langchain_openai import AzureChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import os
import sys
from pathlib import Path


def handle_rag(query: str, collection_name: str = None) -> str:
    """
    RAG(Retrieval-Augmented Generation) 관련 쿼리를 처리하는 함수
    
    Args:
        query (str): 사용자의 입력 쿼리
        collection_name (str): 사용할 벡터 데이터베이스 컬렉션 이름 (선택사항)
        
    Returns:
        str: RAG 에이전트의 응답
    """
    # 1. Milvus에서 유사 문서 검색 (유사도 임계값 0.3 적용)
    # collection_name이 제공되면 해당 컬렉션에서 검색
    results = search_similar_texts(query, limit=3, similarity_threshold=0.2, collection_name=collection_name)
    
    # 필터링된 결과가 없으면 관련 문서 없음 메시지 반환
    if not results:
        collection_info = f" (컬렉션: {collection_name})" if collection_name else ""
        return f"죄송합니다. 질문과 관련된 문서를 찾을 수 없습니다{collection_info}. 다른 질문을 해주시거나, 더 구체적으로 질문해주세요."
    
    # 2. 필터링된 결과에서 컨텍스트 생성
    context = "\n".join([hit.entity.get('text') for hit in results])
    collection_info = f" (컬렉션: {collection_name})" if collection_name else ""
    print(f"RAG 에이전트 컨텍스트{collection_info}: {context}")

    # 3. 역할별 메시지 생성 (System: 컨텍스트, Human: 질문)
    messages = [
        SystemMessage(content=f"다음 컨텍스트를 참고해서 질문에 답변해 주세요.\n\n[컨텍스트]\n{context}"),
        HumanMessage(content=f"[질문]\n{query}")
    ]

    # 4. LLM 호출 (Azure OpenAI)
    llm = AzureChatOpenAI(
        azure_deployment=os.getenv("DEPLOYMENT_CHAT"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        openai_api_type="azure"
    )
    response = llm.invoke(messages)
    return response.content 