from typing import Literal, cast

from httpx import AsyncClient
from promplate.prompt.chat import Message, ensure
from typing_extensions import TypedDict

client = AsyncClient(http2=True)


class SafeMessage(TypedDict):
    role: Literal["user", "assistant"]
    content: str


def ensure_safe(prompt: str | list[Message]):
    return [
        cast(SafeMessage, {"role": i["role"] if i["role"] != "system" else "user", "content": i["content"]})
        for i in ensure(prompt)
    ]
