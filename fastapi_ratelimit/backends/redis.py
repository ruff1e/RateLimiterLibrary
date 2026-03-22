import redis
from fastapi_ratelimit.backends.base import BaseBackend


class RedisBackend(BaseBackend):

    def __init__(self, host, port, db):
        self.client = redis.Redis(host=host, port=port, db=db)

    def is_allowed(self, key: str, limit: int, window: int, algorithm) -> bool:
        return algorithm(self.client, key, limit, window)
