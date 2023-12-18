from functools import cached_property
from typing import Awaitable, Callable, Protocol

from partial_json_parser import JSON


class AbstractTool(Protocol):
    name: str

    __call__: Callable[..., JSON | Awaitable[JSON]]

    @cached_property
    def description(self):
        return str(self.__doc__)
