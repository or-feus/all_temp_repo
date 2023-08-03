from injector import Module, provider, singleton
from redis import Redis

from view_storage_backend import ViewsStorageBackend
from redis_backend import RedisBackend


class RedisModule(Module):
    @provider
    def provide_storage(self, client: Redis) -> ViewsStorageBackend:
        return RedisBackend(client, "my-set")


    @provider
    @singleton
    def provide_redis_client(self) -> Redis:
        return Redis(host="redis")