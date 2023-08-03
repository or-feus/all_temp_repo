from typing import Type

from injector import provider, Module


def MyModule(Module):

    @provider
    def provide_dependency(self, *args) -> Type:
        return ...