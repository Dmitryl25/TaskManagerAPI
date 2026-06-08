import json

from ..api.deps import get_redis
import redis
import redis.asyncio as aioredis


async def get_cached(redis_client: redis.Redis,
                     key: str,
                     ttl: int,
                     func,
                     *args, **kwargs):
    data = await redis_client.get(key)
    if not data:
        data = await func(*args, **kwargs)
        await redis_client.set(key, json.dumps(data), ex=ttl)
        return data
    return json.loads(data)
