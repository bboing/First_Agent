from agent.embedding import get_embedding, search_similar_texts
from langchain_openai import AzureOpenAI
import os

def handle_rag(query: str) -> str:
    """
    RAG(Retrieval-Augmented Generation) 관련 쿼리를 처리하는 함수
    
    Args:
        query (str): 사용자의 입력 쿼리
        
    Returns:
        str: RAG 에이전트의 응답
    """
    # 1. Milvus에서 유사 문서 검색
    results = search_similar_texts(query, limit=3)
    context = "\n".join([hit.entity.get('text') for hits in results for hit in hits])
    if not context:
        context = "(관련 문서가 없습니다.)"

    # 2. 프롬프트 생성
    prompt = f"""[컨텍스트]\n{context}\n\n[질문]\n{query}\n\n위 컨텍스트를 참고해서 질문에 답변해 주세요."""

    # 3. LLM 호출 (Azure OpenAI)
    llm = AzureOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        openai_api_type="azure"
    )
    response = llm.invoke(prompt)
    return response 