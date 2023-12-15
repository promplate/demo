from json import dumps
from sys import stderr
from traceback import print_exc
from typing import Literal

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse, StreamingResponse
from pydantic import BaseModel

from src.routes.sse import server_sent_events

from ..logic import get_node
from ..logic.main import EOC
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
    except EOC as err:
        return err.context.maps[0]
    except Exception as e:
        print_exc(file=stderr)
        return PlainTextResponse(str(e), 500)


@run_router.post("/stream/{node:path}")
async def stream(node: Template, context: ContextIn, astream_func=None):
    n = get_node(node)

    @server_sent_events
    async def make_stream():
        try:
            stream_func = n.astream if astream_func is None else astream_func
            async for c in stream_func(context.model_dump(exclude_unset=True) | {"<stream>": True}):
                yield "partial", dumps(c["parsed"], ensure_ascii=False)
        except EOC:
            yield "complete", dumps(c.maps[0], ensure_ascii=False)  # type: ignore
        except Exception as e:
            print_exc(file=stderr)
            yield "error", str(e)

    return StreamingResponse(make_stream(), media_type="text/event-stream")
