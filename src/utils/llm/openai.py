from os import environ

from httpx import AsyncClient
from promplate.llm.openai import AsyncChatOpenAI

from ..config import env

openai = AsyncChatOpenAI(http_client=AsyncClient(http2=True), api_key=env.openai_api_key, base_url=env.openai_base_url).bind(
    model="gpt-3.5-turbo-1106",
    temperature=0.2,
    # response_format={"type": "json_object"},
)


environ.clear()
