"""
This file defines the data structures used for output in the application. It includes the `Span`, `Action`, and `Output` classes, which are TypedDicts that specify the types and optional/required status of various fields in the output data.
"""

from typing import Any

from typing_extensions import NotRequired, TypedDict


class Span(TypedDict):
    """
    The `Span` class represents a span of text and an optional reference. It includes the `text` field, which is an optional string representing the span of text, and the `reference` field, which is an optional string representing a reference.
    """
    text: NotRequired[str]
    reference: NotRequired[str]


class Action(TypedDict):
    
    """
    The `Action` class represents an action with a name and an optional body. It includes the `name` field, which is a string representing the name of the action, and the `body` field, which is an optional dictionary representing the body of the action.
    """
    name: str
    body: NotRequired[dict[str, Any]]


class Output(TypedDict):
    """
    The `Output` class represents the output of the application. It includes the `content` field, which is an optional list of `Span` objects representing the content of the output, and the `end` field, which is an optional boolean indicating whether the output is the end.
    """
    content: NotRequired[list[Span]]
    end: NotRequired[bool]
    actions: NotRequired[list[Action]]
    
    
