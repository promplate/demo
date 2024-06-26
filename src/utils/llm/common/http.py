from httpx import AsyncClient

client = AsyncClient(http2=True)
