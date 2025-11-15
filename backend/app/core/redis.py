import os
from app.core.config import settings

# Usar fakeredis si Redis real no está disponible
try:
    import redis
    # Intentar conexión real primero
    test_client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        socket_connect_timeout=2
    )
    test_client.ping()
    
    # Si funciona, usar Redis real
    def get_redis_client():
        return redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            db=settings.REDIS_DB,
            decode_responses=True,
            socket_connect_timeout=5,
            retry_on_timeout=True
        )
    
    redis_client = get_redis_client()
    print("✅ Conectado a Redis real")
    
except (ImportError, Exception):
    # Fallback a fakeredis
    from fakeredis import FakeRedis as Redis
    redis_client = Redis(decode_responses=True)
    print("🚀 Usando Redis fake - Tareas asíncronas activadas!")