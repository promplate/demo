from json import dumps
from time import time
from typing import AsyncIterable


def format_chunk(t, id, content, model, stop=False):
    if stop:
        choice = {"index": 0, "delta": {}, "finish_reason": "stop"}
    else:
        choice = {"index": 0, "delta": {"content": content, "role": "assistant"}}
    return {"id": id, "choices": [choice], "model": model, "object": "chat.completion.chunk", "created": t}


def format_response(content, model: str):
    return {
        "id": f"chatcmpl-{int(time())}",
        "choices": [{"index": 0, "message": {"role": "assistant", "content": content}, "finish_reason": "stop"}],
        "model": model,
        "object": "chat.completion",
    }


async def stream_output(stream: AsyncIterable[str], model: str):
    created = int(time())
    response_id = f"chatcmpl-{created}"

    async for delta in stream:
        yield f"data: {dumps(format_chunk(created, response_id, delta, model))}\n\n"

    yield f"data: {dumps(format_chunk(created, response_id, None, model, stop=True))}\n\ndata: [DONE]\n\n"
