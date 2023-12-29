from json import dumps
from sys import stderr
from traceback import print_exc
from typing import Annotated, Literal, cast

from fastapi import APIRouter, Depends, Request
from fastapi.responses import PlainTextResponse, StreamingResponse
from promplate import Node
from pydantic import BaseModel, Field

from ..logic import get_node
from ..logic.tools import tool_map
from ..utils.config import env
from ..utils.http import forward_headers
from ..utils.llm import find_llm
from .sse import server_sent_events

run_router = APIRouter(tags=["call"])


class Msg(BaseModel):
    content: str
    role: Literal["user", "assistant", "system"]
    name: Annotated[Literal.__getitem__(tuple(tool_map)), str] | None = None  # type: ignore


Model = Literal[
    "gpt-3.5-turbo-0301",
    "gpt-3.5-turbo-0613",
    "gpt-3.5-turbo-1106",
    "gpt-4-1106-preview",
    "chatglm_turbo",
    "claude-instant-1.2",
    "claude-2.1",
    "mixtral-8x7b-instruct-fp16",
]


run_config_fields = {"model", "temperature", "stop", "stop_sequences"}


class ChainInput(BaseModel):
    messages: list[Msg] = []
    model: Model = "gpt-3.5-turbo-1106"
    temperature: float = Field(0.7, ge=0, le=1)
    stop: str | list[str] = []  # openai
    stop_sequences: list[str] = []  # anthropic

    @property
    def context(self):
        return self.model_dump(exclude=run_config_fields)

    @property
    def config(self):
        return self.model_dump(include=run_config_fields, exclude_unset=True)

    model_config = {
        "json_schema_extra": {"example": {"messages": [{"content": "What's the date today?", "role": "user"}]}},
        "extra": "allow",
    }


@run_router.post(f"{env.base}/invoke/{{template:path}}")
async def invoke(data: ChainInput, node: Node = Depends(get_node)):
    try:
        return await node.ainvoke(data.context, find_llm(data.model).complete, **data.config)
    except Exception as e:
        print_exc(file=stderr)
        return PlainTextResponse(str(e), 500)


@run_router.post(f"{env.base}/stream/{{template:path}}")
async def stream(data: ChainInput, node: Node = Depends(get_node)):
    @server_sent_events
    async def make_stream():
        try:
            async for c in node.astream(data.context, find_llm(data.model).generate, **data.config):
                if "parsed" in c:
                    yield "partial" if c.get("partial") else "whole", dumps(c["parsed"], ensure_ascii=False)
                else:
                    yield "result", dumps(c.result, ensure_ascii=False)
            yield "finish", dumps(c.maps[0], ensure_ascii=False)  # type: ignore
        except Exception as e:
            print_exc(file=stderr)
            yield "error", str(e)

    return StreamingResponse(make_stream(), media_type="text/event-stream")


@run_router.put(f"{env.base}/single/{{template}}")
async def step_run(r: Request, data: ChainInput, node: Node = Depends(get_node)):
    async def make_stream():
        last = ""

        config = data.config

        if data.model.startswith("gpt"):
            config["extra_headers"] = forward_headers(r.headers)

        async for c in node.astream(data.context, find_llm(data.model).generate, **config):
            if c.result != last:
                yield cast(str, c.result).removeprefix(last)
                last = c.result

    return StreamingResponse(make_stream(), media_type="text/plain")
