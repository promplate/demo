from traceback import print_exc

from fastapi.responses import PlainTextResponse, StreamingResponse
from starlette.responses import AsyncContentStream


async def make_response(stream: AsyncContentStream, media_type="text/plain"):
    it = aiter(stream)

    try:
        first_chunk = await anext(it)
    except Exception as e:
        print_exc()
        return PlainTextResponse("\n".join(map(str, e.args)).strip(), getattr(e, "status_code", 500))

    async def _():
        yield first_chunk
        async for i in it:
            yield i

    return StreamingResponse(_(), media_type=media_type)
