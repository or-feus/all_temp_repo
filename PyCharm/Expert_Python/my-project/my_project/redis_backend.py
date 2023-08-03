from typing import Dict

from view_storage_backend import ViewsStorageBackend
from redis import Redis


class RedisBackend(ViewsStorageBackend):

    def __init__(self, redis_client: Redis, set_name: str):
        self._client = redis_client
        self._set_name = set_name

    def increment(self, key: str):
        self._client.zincrby(self._set_name, 1, key)

    def most_common(self, n: int) -> Dict[str, int]:
        return {
            key.decode(): int(value)
            for key, value in self._client.zrange(
                self._set_name,
                0,
                n - 1,
                desc=True,
                withscores=True,
            )
        }
