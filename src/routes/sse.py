from functools import wraps
from itertools import count
from typing import AsyncGenerator, Callable, cast

from ..utils.load import load_template

get_id = count().__next__


def server_sent_events(generator: Callable[..., AsyncGenerator[tuple[str, str], None]]):
    @wraps(generator)
    async def wrapper(*args, **kwargs):
        last = []
        async for event, data in generator(*args, **kwargs):
            if [event, data] != last:
                yield load_template("sse").render({"event": event, "data": data, "get_id": get_id})
                last[:] = [event, data]

    return wrapper
