from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from starlette.middleware.cors import CORSMiddleware

from .routes.prompts import prompts_router
from .routes.run import run_router
from .utils.load import generate_pyi
from .utils.time import now

app = FastAPI(title="Promplate Demo", description="<https://github.com/promplate/demo>", on_startup=[generate_pyi, load_dotenv])
app.add_middleware(CORSMiddleware, allow_origins="*", allow_credentials=True, allow_methods="*", allow_headers="*")
app.include_router(prompts_router, prefix="/prompts")
app.include_router(run_router)


@app.get("/heartbeat", response_model=str, response_class=PlainTextResponse)
async def greet():
    return f"hi from {now()}"
