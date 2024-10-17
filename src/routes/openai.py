from typing import AsyncIterable, cast

from fastapi import APIRouter
from promplate import Message

from ..utils.llm import Model
from ..utils.llm.dispatch import find_llm
from ..utils.openai_api import format_response, stream_output
from ..utils.response import make_response
from .run import ChainInput

openai_router = APIRouter(tags=["openai"])


@openai_router.get("/models")
async def get_models():
    return {
        "object": "list",
        "data": [
            {
                "id": name,
                "object": "model",
            }
            for name in Model.__args__
        ],
    }


class ChatInput(ChainInput):
    stream: bool = False
    messages: list[Message]  # type: ignore

    @property
    def config(self):
        return self.model_dump(exclude_unset=True)


@openai_router.post("/chat/completions")
async def chat_completions(data: ChatInput):
    llm = find_llm(data.model)

    if not data.stream:
        return format_response(
            await llm.complete(data.messages, **data.config),
            data.model,
        )

    return await make_response(
        stream_output(
            cast(AsyncIterable[str], llm.generate(data.messages, **data.config)),
            data.model,
        ),
        "text/event-stream",
    )
