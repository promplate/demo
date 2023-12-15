from httpx import AsyncClient
from promplate.llm.openai import AsyncChatOpenAI

openai = AsyncChatOpenAI(http_client=AsyncClient(http2=True)).bind(model="gpt-3.5-turbo-1106")
