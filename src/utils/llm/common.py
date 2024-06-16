from typing import Literal, cast

from httpx import AsyncClient
from promplate.prompt.chat import Message, ensure
from typing_extensions import TypedDict

client = AsyncClient(http2=True)


class SafeMessage(TypedDict):
    role: Literal["user", "assistant"]
    content: str


def ensure_no_system(prompt: str | list[Message]):
    return [
        cast(SafeMessage, {"role": i["role"] if i["role"] != "system" else "user", "content": i["content"]})
        for i in ensure(prompt)
    ]


def join_adjacent_inplace(messages: list[SafeMessage]):
    i = 1
    while i < len(messages):
        if messages[i - 1]["role"] == messages[i]["role"]:
            if messages[i - 1]["content"] != messages[i]["content"]:
                messages[i - 1]["content"] += "\n\n" + messages[i]["content"]
            messages.pop(i)
        else:
            i += 1


def ensure_safe(prompt: str | list[Message]):
    messages = ensure_no_system(prompt)
    join_adjacent_inplace(messages)
    if messages[0]["role"] == "assistant":
        messages.insert(0, {"role": "user", "content": "..."})

    return messages
