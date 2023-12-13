from typing import Literal

from fastapi import FastAPI
from fastapi.responses import JSONResponse, PlainTextResponse
from promplate import Context, Message, parse_chat_markup

from .utils.load import Templates, load_template
from .utils.time import now

app = FastAPI()


@app.get("/heartbeat", response_model=str, response_class=PlainTextResponse)
async def greet():
    return f"hi from {now()}"


@app.post("/render/{template}", response_model=list[Message] | str)
async def render_template(
    template: Templates,
    context: Context,
    format: Literal["text", "list", "script"] = "text",
    sync: bool = False,
):
    try:
        t = load_template(template)
        if format == "script":
            return PlainTextResponse(t.get_script(sync), media_type="text/x-python")
        prompt = t.render(context) if sync else await t.arender(context)
        return PlainTextResponse(prompt) if format == "text" else JSONResponse(parse_chat_markup(prompt))
    except Exception as e:
        return PlainTextResponse(str(e), 400)
