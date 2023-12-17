from collections import deque
from functools import wraps
from itertools import count
from typing import AsyncGenerator, Callable

from ..utils.load import load_template

get_id = count().__next__


def server_sent_events(generator: Callable[..., AsyncGenerator[tuple[str, str], None]]):
    """
    A decorator that converts a generator function into a server-sent events endpoint.

    Args:
        generator: A generator function yielding event and data pairs to be sent.

    Yields:
        tuple[str, str]: Event and data pairs for server-sent events.
    """
    @wraps(generator)
    async def wrapper(*args, **kwargs):
        last3 = deque(maxlen=3)
        async for event, data in generator(*args, **kwargs):
            if [event, data] not in last3:
                yield load_template("sse").render({"event": event, "data": data, "get_id": get_id})
                last3.append([event, data])

    return wrapper
