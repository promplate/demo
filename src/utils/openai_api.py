from contextvars import ContextVar
from json import dumps
from time import time
from typing import AsyncIterable

need_notice = ContextVar("notice", default=False)

NOTICE = {
    "____N_O_T_I_C_E____": {
        "_": "Hi developer! It seems you're using our API. I want to contact you, could you please reach out to me at me@promplate.dev? Thank you!",
        "zh_CN": "你好开发者，看来你正在使用我们的免费 API。如果看到该消息，欢迎通过 me@promplate.dev 联系我。我想了解一下您的 use-case，谢谢！",
    }
}


def _get_notice():
    return NOTICE if need_notice.get() else {}


def format_chunk(t, id, content, model, stop=False):
    if stop:
        choice = {"index": 0, "delta": {}, "finish_reason": "stop"}
    else:
        choice = {"index": 0, "delta": {"content": content, "role": "assistant"}}
    return {**(_get_notice()), "id": id, "choices": [choice], "model": model, "object": "chat.completion.chunk", "created": t}


def format_response(content, model: str):
    return {
        **_get_notice(),
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
