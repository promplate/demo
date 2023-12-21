from json import dumps
from sys import stderr
from traceback import print_exc
from typing import Annotated, Literal, cast

from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse, StreamingResponse
from promplate import Node
from pydantic import BaseModel, Field

from ..logic import get_node
from ..logic.tools import tool_map
from ..utils.config import env
from .sse import server_sent_events

run_router = APIRouter(tags=["call"])


class Message(BaseModel):
    content: str
    role: Literal["user", "assistant", "system"]
    name: Annotated[Literal.__getitem__(tuple(tool_map)), str] | None = None  # type: ignore


class ContextIn(BaseModel):
    messages: list[Message]
    model: Literal["gpt-3.5-turbo-0301", "gpt-3.5-turbo-0613", "gpt-3.5-turbo-1106"] = "gpt-3.5-turbo-1106"
    temperature: float = Field(0.7, ge=0, le=1)

    model_config = {"json_schema_extra": {"example": {"messages": [{"content": "What's the date today?", "role": "user"}]}}}


@run_router.post(f"{env.base}/invoke/{{node:path}}")
async def invoke(context: ContextIn, node: Node = Depends(get_node)):
    try:
        return await node.ainvoke(context.model_dump(exclude_unset=True), temperature=context.temperature, model=context.model)
    except Exception as e:
        print_exc(file=stderr)
        return PlainTextResponse(str(e), 500)


@run_router.post(f"{env.base}/stream/{{node:path}}")
async def stream(context: ContextIn, node: Node = Depends(get_node)):
    @server_sent_events
    async def make_stream():
        try:
            async for c in node.astream(context.model_dump(exclude_unset=True)):
                yield "partial" if c.get("partial") else "whole", dumps(c["parsed"], ensure_ascii=False)
            yield "finish", dumps(c.maps[0], ensure_ascii=False)  # type: ignore
        except Exception as e:
            print_exc(file=stderr)
            yield "error", str(e)

    return StreamingResponse(make_stream(), media_type="text/event-stream")


@run_router.put(f"{env.base}/single/{{node}}")
async def step_run(context: ContextIn, node: Node = Depends(get_node)):
    async def make_stream():
        last = ""
        async for c in node.astream(context.model_dump(exclude_unset=True)):
            if c.result != last:
                yield cast(str, c.result).removeprefix(last)
                last = c.result

    return StreamingResponse(make_stream(), media_type="text/plain")
