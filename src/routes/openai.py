from typing import AsyncIterable, cast

from fastapi import APIRouter

from ..utils.llm import Model
from ..utils.llm.dispatch import find_llm
from ..utils.openai_api import stream_output
from ..utils.response import make_response
from .run import ChainInput

openai_router = APIRouter(tags=["openai"])


@openai_router.get("/models")
async def get_models():
    return {
        "object": "list",
        "data": [
            {
                "id": name,
                "object": "model",
            }
            for name in Model.__args__
        ],
    }


@openai_router.post("/chat/completions")
async def chat_completions(data: ChainInput):
    llm = find_llm(data.model)
    return await make_response(
        stream_output(
            cast(AsyncIterable[str], llm.generate(data.messages, **data.config)),
            data.model,
        ),
        "text/event-stream",
    )
