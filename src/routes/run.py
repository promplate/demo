from json import dumps
from sys import stderr
from traceback import print_exc
from typing import Annotated, Literal, cast

from fastapi import APIRouter, Depends, Request
from fastapi.responses import PlainTextResponse
from promplate import Node
from pydantic import BaseModel, Field

from ..logic import get_node
from ..logic.tools import tool_map
from ..utils.config import env
from ..utils.http import forward_headers
from ..utils.llm import Model, find_llm, openai_compatible_providers
from ..utils.response import make_response
from .sse import non_duplicated_event_stream

run_router = APIRouter(tags=["call"])


class Msg(BaseModel):
    content: str
    role: Literal["user", "assistant", "system"]
    name: Annotated[Literal.__getitem__(tuple(tool_map)), str] | None = None  # type: ignore


run_config_fields = {"model", "temperature", "stop", "stop_sequences"}


class ChainInput(BaseModel):
    messages: list[Msg] = []
    model: Model = "gpt-4o-mini"
    temperature: float = Field(0.7, ge=0, le=2)
    stop: str | list[str] = []  # openai
    stop_sequences: list[str] = []  # anthropic

    @property
    def context(self):
        return self.model_dump(exclude=run_config_fields, exclude_unset=True)

    @property
    def config(self):
        return self.model_dump(include=run_config_fields, exclude_unset=True)

    model_config = {
        "json_schema_extra": {"example": {"messages": [{"content": "What's the date today?", "role": "user"}]}},
        "extra": "allow",
    }


def mix_config(r: Request, data: ChainInput):
    config = data.config

    if find_llm(data.model) in openai_compatible_providers:
        config["extra_headers"] = forward_headers(r.headers)

    return config


@run_router.post(f"{env.base}/invoke/{{template:path}}")
async def invoke(data: ChainInput, node: Node = Depends(get_node), config: dict = Depends(mix_config)):
    try:
        return await node.ainvoke(data.context, find_llm(data.model).complete, **config)
    except Exception as e:
        print_exc(file=stderr)
        return PlainTextResponse(str(e), 500)


@run_router.post(f"{env.base}/stream/{{template:path}}")
async def stream(data: ChainInput, node: Node = Depends(get_node), config: dict = Depends(mix_config)):
    @non_duplicated_event_stream
    async def make_stream():
        try:
            async for c in node.astream(data.context, find_llm(data.model).generate, **config):
                if "parsed" in c:
                    yield dumps(c["parsed"], ensure_ascii=False), "partial" if c.get("partial") else "whole"
                else:
                    yield dumps(c.result, ensure_ascii=False), "result"
            yield dumps(c.maps[0], ensure_ascii=False), "finish"  # type: ignore
        except Exception as e:
            print_exc(file=stderr)
            yield str(e), "error"

    return await make_response(make_stream(), "text/event-stream")


@run_router.put(f"{env.base}/single/{{template}}")
async def step_run(r: Request, data: ChainInput, node: Node = Depends(get_node), config: dict = Depends(mix_config)):
    if data.model.startswith("gpt-3.5-turbo"):
        data.model = "gpt-4o-mini"

    for msg in data.messages:
        for string in env.banned_substrings:
            if string in msg.content:
                print(await node.arender(data.context))
                return PlainTextResponse(env.banned_response)

    async def make_stream():
        last = ""

        async for c in node.astream(data.context, find_llm(data.model).generate, **config):
            if c.result != last:
                yield cast(str, c.result).removeprefix(last)
                last = c.result

    return await make_response(make_stream())
