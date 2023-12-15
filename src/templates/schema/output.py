from typing import Any

from typing_extensions import NotRequired, TypedDict


class Span(TypedDict):
    text: NotRequired[str]
    reference: NotRequired[str]


class Action(TypedDict):
    name: str
    body: NotRequired[dict[str, Any]]


class Output(TypedDict):
    content: NotRequired[list[Span]]
    end: NotRequired[bool]
    actions: NotRequired[list[Action]]
