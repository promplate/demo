from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from promplate import Context

from ..logic import get_node
from ..utils.load import Template

run_router = APIRouter(tags=["call"])


@run_router.post("/invoke/{node:path}")
async def invoke(node: Template, context: Context):
    n = get_node(node)
    try:
        return await n.ainvoke(context)
    except Exception as e:
        return PlainTextResponse(str(e), 500)
