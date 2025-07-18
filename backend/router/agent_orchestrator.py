from agent.embedding import search_similar_texts
from agent.ml_agent import handle_ml
from agent.rag_agent import handle_rag

def route_query(user_input):
    results = search_similar_texts(user_input, limit=1)
    if results and len(results[0]) > 0:
        best_hit = results[0][0]
        score = best_hit.distance  # L2 거리(작을수록 유사)
        # 예시: 0.1 이하(유사도 높음)면 ML, 아니면 RAG
        if score < 0.05:
            print("router/agent_orchestrator.py: ML 에이전트 호출")
            return handle_ml(user_input)
        else:
            print("router/agent_orchestrator.py: RAG 에이전트 호출")
            return handle_rag(user_input)
    else:
        # 검색 결과 없으면 RAG로
        print("router/agent_orchestrator.py: 검색 결과 없음, RAG 에이전트 호출")
        return handle_rag(user_input)