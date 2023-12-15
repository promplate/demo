from typing import Awaitable, Callable, Protocol

from partial_json_parser import JSON


class AbstractTool(Protocol):
    name: str

    __call__: Callable[..., JSON | Awaitable[JSON]]

    @property
    def description(self):
        return self.__doc__
