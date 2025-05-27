from typing import AsyncIterable, Literal, cast, get_args

from fastapi import APIRouter, Depends, Request
from openai.types.chat import ChatCompletionContentPartTextParam
from promplate import Message
from pydantic import field_validator
from typing_extensions import TypedDict

from ..utils.http import forward_headers
from ..utils.llm import Model, openai_compatible_providers
from ..utils.llm.dispatch import find_llm
from ..utils.openai_api import format_response, stream_output
from ..utils.response import make_response
from .run import ChainInput

openai_router = APIRouter(tags=["openai"])


class ModelItem(TypedDict):
    id: Model
    object: Literal["model"]


class ModelList(TypedDict):
    object: Literal["list"]
    data: list[ModelItem]


@openai_router.get("/models")
async def get_models() -> ModelList:
    return {
        "object": "list",
        "data": [
            {
                "id": name,
                "object": "model",
            }
            for name in get_args(Model)
        ],
    }


class CompatibleMessage(Message):
    content: str | list[ChatCompletionContentPartTextParam]  # type: ignore


class ChatInput(ChainInput):
    stream: bool = False
    messages: list[CompatibleMessage]  # type: ignore

    @field_validator("messages", mode="after")
    def serialize_messages(cls, value: list[CompatibleMessage]):
        for msg in value:
            content = msg["content"]
            if isinstance(content, str):
                continue
            msg["content"] = "".join(i["text"] for i in content)
        return value

    @property
    def config(self):
        return self.model_dump(exclude_unset=True, exclude={"messages", "stream"})


def mix_config(r: Request, data: ChatInput):
    config = data.config

    if find_llm(data.model) in openai_compatible_providers:
        config["extra_headers"] = forward_headers(r.headers)

    return config


@openai_router.post("/chat/completions")
async def chat_completions(data: ChatInput, config: dict = Depends(mix_config)):
    llm = find_llm(data.model)

    if not data.stream:
        return format_response(
            await llm.complete(data.messages, **config),  # type: ignore
            data.model,
        )

    return await make_response(
        stream_output(
            cast(AsyncIterable[str], llm.generate(data.messages, **config)),  # type: ignore
            data.model,
        ),
        "text/event-stream",
    )
