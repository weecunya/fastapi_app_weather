import redis.asyncio as redis

from app.config import settings

redis_client = redis.from_url(settings.REDIS_URL ,decode_responses=True)

async def check_redis():
    try:
        await redis_client.ping()
        print("redis connected")
    except Exception as e:
        print("redis is not connected,", e)
