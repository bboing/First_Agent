from typing import Dict, Any
from pathlib import Path

# 기본 설정
BASE_DIR = Path(__file__).parent.parent

# RAG 에이전트 설정
RAG_CONFIG = {
    "model_name": "gpt-3.5-turbo",  # 기본 모델
    "temperature": 0.7,
    "max_tokens": 1000,
    "chunk_size": 1000,
    "chunk_overlap": 200,
}

# ML 에이전트 설정
ML_CONFIG = {
    "model_path": str(BASE_DIR / "models"),
    "default_model": "random_forest",
    "batch_size": 32,
    "learning_rate": 0.001,
}

# 에이전트 상태 설정
AGENT_STATUS = {
    "rag": {
        "is_active": True,
        "max_retries": 3,
        "timeout": 30,
    },
    "ml": {
        "is_active": True,
        "max_retries": 3,
        "timeout": 60,
    }
}

def get_agent_config(agent_type: str) -> Dict[str, Any]:
    """
    특정 에이전트의 설정을 반환하는 함수
    
    Args:
        agent_type (str): 에이전트 타입 ('rag' 또는 'ml')
        
    Returns:
        Dict[str, Any]: 에이전트 설정
    """
    if agent_type == "rag":
        return RAG_CONFIG
    elif agent_type == "ml":
        return ML_CONFIG
    else:
        raise ValueError(f"Unknown agent type: {agent_type}")

def is_agent_active(agent_type: str) -> bool:
    """
    특정 에이전트가 활성화되어 있는지 확인하는 함수
    
    Args:
        agent_type (str): 에이전트 타입 ('rag' 또는 'ml')
        
    Returns:
        bool: 에이전트 활성화 상태
    """
    if agent_type not in AGENT_STATUS:
        raise ValueError(f"Unknown agent type: {agent_type}")
    return AGENT_STATUS[agent_type]["is_active"] 