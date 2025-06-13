from agent.embedding import search_similar_texts
from langchain_openai import AzureChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import os
import dotenv   

dotenv.load_dotenv()

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
        return "관련 문서가 없습니다."

    # 2. 역할별 메시지 생성 (System: 컨텍스트, Human: 질문)
    messages = [
        SystemMessage(content=f"다음 컨텍스트를 참고해서 질문에 답변해 주세요.\n\n[컨텍스트]\n{context}"),
        HumanMessage(content=f"[질문]\n{query}")
    ]

    # 3. LLM 호출 (Azure OpenAI)
    llm = AzureChatOpenAI(
        azure_deployment=os.getenv("DEPLOYMENT_CHAT"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        openai_api_type="azure"
    )
    response = llm.invoke(messages)
    return response.content 