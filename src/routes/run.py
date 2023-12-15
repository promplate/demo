from sys import stderr
from traceback import print_exc
from typing import Literal

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

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
