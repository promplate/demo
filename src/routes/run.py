from json import dumps
from sys import stderr
from traceback import print_exc
from typing import Literal

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse, StreamingResponse
from pydantic import BaseModel

from src.routes.sse import server_sent_events

from ..logic import get_node
from ..utils.load import Template

run_router = APIRouter(tags=["call"])


class Message(BaseModel):
    content: str
    role: Literal["user", "assistant"]


class ContextIn(BaseModel):
    messages: list[Message]


@run_router.post("/invoke/{node:path}")
async def invoke(node: Template, context: ContextIn):
    n = get_node(node)
    try:
        return await n.ainvoke(context.model_dump(exclude_unset=True))
    except Exception as e:
        print_exc(file=stderr)
        return PlainTextResponse(str(e), 500)


@run_router.post("/stream/{node:path}")
async def stream(node: Template, context: ContextIn):
    n = get_node(node)

    @server_sent_events
    async def make_stream():
        try:
            async for c in n.astream(context.model_dump(exclude_unset=True)):
                yield "partial" if c.get("partial") else "whole", dumps(c["parsed"], ensure_ascii=False)
            yield "finish", dumps(c.maps[0], ensure_ascii=False)  # type: ignore
        except Exception as e:
            print_exc(file=stderr)
            yield "error", str(e)

    return StreamingResponse(make_stream(), media_type="text/event-stream")
