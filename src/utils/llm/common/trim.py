from functools import wraps
from inspect import isasyncgenfunction
from typing import AsyncIterable, Awaitable, Callable, TypeVar

F = TypeVar("F", bound=Callable[..., Awaitable[str] | AsyncIterable[str]])


def trim_start(f: F) -> F:
    if isasyncgenfunction(f):

        @wraps(f)
        async def _(*args, **kwargs):
            first_token = True
            async for token in f(*args, **kwargs):
                if first_token:
                    first_token = False
                    yield token.lstrip()
                else:
                    yield token

    else:

        @wraps(f)
        async def _(*args, **kwargs):
            return (await f(*args, **kwargs)).lstrip()  # type: ignore

    return _  # type: ignore
