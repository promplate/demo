from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from .routes.prompts import prompts_router
from .utils.load import generate_pyi
from .utils.time import now

app = FastAPI(title="Promplate Demo", on_startup=[generate_pyi])
app.include_router(prompts_router)


@app.get("/heartbeat", response_model=str, response_class=PlainTextResponse)
async def greet():
    return f"hi from {now()}"
