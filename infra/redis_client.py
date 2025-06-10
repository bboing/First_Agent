from redis import Redis
from config import REDIS_HOST, REDIS_PORT
import json

redis = Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def save_chat_message(user_id: str, role: str, content: str):
    key = f"user:{user_id}:chat_history"
    message = {"role": role, "content": content}
    redis.rpush(key, json.dumps(message))

def get_chat_history(user_id: str):
    key = f"user:{user_id}:chat_history"
    raw_messages = redis.lrange(key, 0, -1)
    return [json.loads(msg) for msg in raw_messages]

def clear_chat_history(user_id: str):
    key = f"user:{user_id}:chat_history"
    redis.delete(key)