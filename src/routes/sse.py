from functools import wraps
from typing import AsyncGenerator, Callable

from promptools.stream.sse import as_event_stream


def non_duplicated_event_stream(generator: Callable[..., AsyncGenerator[tuple[str, str], None]]):
    @wraps(generator)
    async def wrapper(*args, **kwargs):
        last = {}
        async for event in as_event_stream(generator(*args, **kwargs)):
            if last.get(event.event) != event:
                yield str(event)
                last[event.event] = event

    return wrapper
