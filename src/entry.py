from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from .routes.prompts import prompts_router
from .routes.run import run_router
from .utils.config import env
from .utils.time import now

app = FastAPI(title="Promplate Demo", description="<https://github.com/promplate/demo>")
app.add_middleware(CORSMiddleware, allow_origins="*", allow_credentials=True, allow_methods="*", allow_headers="*")
app.include_router(prompts_router, prefix="/prompts")
app.include_router(run_router)
if env.openai_compatible_api:
    from .routes.openai import openai_router

    app.include_router(openai_router)
    app.include_router(openai_router, prefix="/v1")


@app.get("/heartbeat", response_model=str, response_class=PlainTextResponse)
async def greet():
    return f"hi from {now()}"


app.mount("/", StaticFiles(directory="frontend/dist", html=True, check_dir=False))
