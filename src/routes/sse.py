from collections import deque
from functools import wraps
from typing import AsyncGenerator, Callable

from promptools.stream.sse import as_event_stream


def non_duplicated_event_stream(generator: Callable[..., AsyncGenerator[tuple[str, str], None]]):
    @wraps(generator)
    async def wrapper(*args, **kwargs):
        last3 = deque(maxlen=3)
        async for event in as_event_stream(generator(*args, **kwargs)):
            if event not in last3:
                yield str(event)
                last3.append(event)

    return wrapper
