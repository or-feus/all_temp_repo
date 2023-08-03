from injector import Module, provider, singleton

from view_storage_backend import ViewsStorageBackend
from counter_backend import CounterBackend

class CounterModule(Module):

    @provider
    @singleton
    def provide_storage(self) -> ViewsStorageBackend:
        return CounterBackend()

