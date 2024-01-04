from collections import deque
from functools import wraps
from typing import AsyncGenerator, Callable

from promptools.utils.sse import Event


def server_sent_events(generator: Callable[..., AsyncGenerator[tuple[str, str], None]]):
    @wraps(generator)
    async def wrapper(*args, **kwargs):
        last3 = deque(maxlen=3)
        async for event, data in generator(*args, **kwargs):
            evt = Event(data, event)
            if evt not in last3:
                yield str(evt)
                last3.append(evt)

    return wrapper
