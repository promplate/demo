from typing import Literal

from fastapi import APIRouter
from fastapi.responses import FileResponse, JSONResponse, PlainTextResponse
from promplate import Context, Message, parse_chat_markup

from ..utils.load import Templates, glob, load_template

prompts_router = APIRouter(tags=["Prompt templates management"])


@prompts_router.post("/render/{template:path}", response_model=list[Message] | str)
async def render_template(
    template: Templates,
    context: Context,
    format: Literal["text", "list", "script"] = "text",
    sync: bool = False,
):
    """
    Render the specified template with the given context.

    Parameters:
    - template: The template to render.
    - context: The context to use for rendering.
    - format: The format of the output (default: "text").
    - sync: Whether to render synchronously (default: False).

    Returns:
    - If format is "text", returns the rendered template as plain text.
    - If format is "list", returns the rendered template as a list of messages.
    - If format is "script", returns the rendered template as a Python script.
    """
    try:
        t = load_template(template)
        if format == "script":
            return PlainTextResponse(t.get_script(sync), media_type="text/x-python")
        prompt = t.render(context) if sync else await t.arender(context)
        return PlainTextResponse(prompt) if format == "text" else JSONResponse(parse_chat_markup(prompt))
    except Exception as e:
        return PlainTextResponse(str(e), 400)


@prompts_router.get("/{template:path}", response_class=FileResponse)
async def show_raw_template(template: Templates):
    return glob()[template]
