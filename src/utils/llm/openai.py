from httpx import AsyncClient
from promplate.llm.openai import AsyncChatOpenAI

openai = AsyncChatOpenAI(http_client=AsyncClient(http2=True)).bind(
    model="gpt-3.5-turbo-1106",
    temperature=0.2,
    # response_format={"type": "json_object"},
)
