from Agent.rag_agent import handle_rag
from Agent.ml_agent import handle_ml
from dst.state_tracker import get_user_intent

def route_query(user_input):
    # 일단 intent 분기를 단순하게 if로 구성
    intent = get_user_intent(user_input)
    
    if intent == "rag":
        return handle_rag(user_input)
    elif intent == "ml":
        return handle_ml(user_input)
    else:
        return "죄송합니다. 이해하지 못했어요."