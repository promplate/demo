from json import dumps
from time import time
from typing import AsyncIterable


def format_chunk(id, content, model, stop=False):
    if stop:
        choice = {"index": 0, "delta": {}, "finish_reason": "stop"}
    else:
        choice = {"index": 0, "delta": {"content": content, "role": "assistant"}}
    return {"id": id, "choices": [choice], "model": model, "object": "chat.completion.chunk"}


async def stream_output(stream: AsyncIterable[str], model: str):
    response_id = int(time())

    async for delta in stream:
        yield f"data: {dumps(format_chunk(response_id, delta, model))}\n\n"

    yield f"data: {dumps(format_chunk(response_id, None, model, stop=True))}\n\ndata: [DONE]\n\n"
