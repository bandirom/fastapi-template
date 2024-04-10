from aioredis import Redis


class AsyncRedisClient:
    DEFAULT_PREFIX = ""

    def __init__(self, redis_instance: Redis) -> None:
        self.redis = redis_instance
