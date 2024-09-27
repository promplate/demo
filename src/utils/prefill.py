from functools import wraps
from typing import ParamSpec, TypeVar

from promplate.llm.base import AsyncComplete, AsyncGenerate
from promplate.prompt.chat import ensure

P = ParamSpec("P")
T = TypeVar("T")


def patch_async_complete(func: AsyncComplete) -> AsyncComplete:
    @wraps(func)
    async def wrapper(prompt, /, **config):
        messages = ensure(prompt)
        res: str = await func(messages, **config)

        last_message = messages[-1]
        if last_message["role"] == "assistant":
            return last_message["content"] + res

        return res

    return wrapper


def patch_async_generate(func: AsyncGenerate) -> AsyncGenerate:
    @wraps(func)
    async def wrapper(prompt, /, **config):
        messages = ensure(prompt)
        last_message = messages[-1]
        if last_message["role"] == "assistant":
            first = True
            async for chunk in func(messages, **config):
                if first:
                    yield last_message["content"]
                    yield chunk
                    first = False
                else:
                    yield chunk

        else:
            async for chunk in func(messages, **config):
                yield chunk

    return wrapper
