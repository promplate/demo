from fastapi import APIRouter
from promplate import Context

from ..logic import get_node
from ..utils.load import Template

run_router = APIRouter(tags=["run"])


@run_router.post("/invoke/{node:path}")
async def invoke(node: Template, context: Context):
    n = get_node(node)
    return await n.ainvoke(context)
