# ping.py
from config import DATABASE_URL, REDIS_HOST, REDIS_PORT, MILVUS_HOST, MILVUS_PORT

# PostgreSQL
import psycopg2
from redis import Redis
from pymilvus import connections, utility


def check_postgres():
    print("ping.py: 📦 PostgreSQL 연결 테스트 중...")
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute("SELECT 1;")
        print("ping.py: ✅ PostgreSQL 연결 성공!")
        cursor.close()
        conn.close()
    except Exception as e:
        print("ping.py: ❌ PostgreSQL 연결 실패:", e)


def check_redis():
    print("ping.py: 🚀 Redis 연결 테스트 중...")
    try:
        r = Redis(host=REDIS_HOST, port=REDIS_PORT)
        pong = r.ping()
        print("ping.py: ✅ Redis 연결 성공!" if pong else "ping.py: ❌ Redis 연결 실패!")
    except Exception as e:
        print("ping.py: ❌ Redis 연결 실패:", e)


def check_milvus():
    print("ping.py: 🔍 Milvus 연결 테스트 중...")
    try:
        connections.connect(host=MILVUS_HOST, port=MILVUS_PORT)
        healthy = utility.has_collection("test")  # 존재 여부만 테스트
        print("ping.py: ✅ Milvus 연결 성공!")
    except Exception as e:
        print("ping.py: ❌ Milvus 연결 실패:", e)


if __name__ == "__main__":
    check_postgres()
    check_redis()
    check_milvus()