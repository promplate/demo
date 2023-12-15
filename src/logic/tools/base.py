from typing import Protocol

from partial_json_parser import JSON


class AbstractTool(Protocol):
    name: str
    description: str

    def __call__(self, **kwargs) -> JSON:
        ...
