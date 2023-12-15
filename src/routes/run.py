from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse
from promplate import Context

from ..logic import get_node
from ..utils.load import Template

run_router = APIRouter(tags=["call"])


@run_router.post("/invoke/{node:path}")
async def invoke(node: Template, context: Context):
    """
    Invoke the specified node with the given context.

    Args:
        node (Template): The template node to invoke.
        context (Context): The context to use for the invocation.

    Returns:
        The result of the invocation.

    Raises:
        Exception: If there is an error during the invocation.
    """
    n = get_node(node)
    try:
        return await n.ainvoke(context)
    except Exception as e:
        return PlainTextResponse(str(e), 500)
