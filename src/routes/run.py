from json import dumps
from sys import stderr
from traceback import print_exc
from typing import Annotated, Literal, cast

from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse, StreamingResponse
from promplate import Message, Node
from pydantic import BaseModel, Field

from ..logic import get_node
from ..logic.tools import tool_map
from ..utils.config import env
from .sse import server_sent_events

run_router = APIRouter(tags=["call"])


class Msg(BaseModel):
    content: str
    role: Literal["user", "assistant", "system"]
    name: Annotated[Literal.__getitem__(tuple(tool_map)), str] | None = None  # type: ignore


class ChainInput(BaseModel):
    messages: list[Msg]
    model: Literal["gpt-3.5-turbo-0301", "gpt-3.5-turbo-0613", "gpt-3.5-turbo-1106", "chatglm_turbo"] = "gpt-3.5-turbo-1106"
    temperature: float = Field(0.7, ge=0, le=1)

    @property
    def context(self):
        return self.model_dump(include={"messages"})

    @property
    def config(self):
        return self.model_dump(exclude={"messages"}, exclude_unset=True)

    model_config = {"json_schema_extra": {"example": {"messages": [{"content": "What's the date today?", "role": "user"}]}}}


@run_router.post(f"{env.base}/invoke/{{template:path}}")
async def invoke(data: ChainInput, node: Node = Depends(get_node)):
    try:
        return await node.ainvoke(data.context, **data.config)
    except Exception as e:
        print_exc(file=stderr)
        return PlainTextResponse(str(e), 500)


@run_router.post(f"{env.base}/stream/{{template:path}}")
async def stream(data: ChainInput, node: Node = Depends(get_node)):
    @server_sent_events
    async def make_stream():
        try:
            async for c in node.astream(data.context, **data.config):
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
async def step_run(data: ChainInput, node: Node = Depends(get_node)):
    async def make_stream():
        last = ""
        async for c in node.astream(data.context, **data.config):
            if c.result != last:
                yield cast(str, c.result).removeprefix(last)
                last = c.result

    return StreamingResponse(make_stream(), media_type="text/plain")
