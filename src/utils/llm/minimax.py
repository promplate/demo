from json import loads

from promplate.llm.base import LLM
from promplate.prompt.chat import Message, ensure
from promplate_trace.auto import patch

from ..config import env
from .common import client
from .dispatch import link_llm

URL = "https://api.minimax.chat/v1/text/chatcompletion_v2"

headers = {"authorization": f"Bearer {env.minimax_api_key}", "content-type": "application/json"}


@link_llm("abab")
class MiniMax(LLM):
    """MiniMax Class for implementing the minimax algorithm."""
    @staticmethod
    @patch.chat.acomplete
    async def complete(prompt: str | list[Message], /, **config):
        messages = ensure(prompt)
        res = await client.post(URL, json={"messages": messages, **config}, headers=headers)

        try:
            return res.json()["choices"][0]["message"]["content"]
        except KeyError:
            print(res.json())
            raise

    @staticmethod
    @patch.chat.agenerate
    async def generate(prompt: str | list[Message], /, **config):
        messages = ensure(prompt)
        async with client.stream("POST", URL, json={"messages": messages, "stream": True, **config}, headers=headers) as res:
            async for line in res.aiter_lines():
                if not line.strip():
                    continue
                try:
                    yield loads(line.removeprefix("data:").strip())["choices"][0]["delta"]["content"]
                except KeyError:
                    print(line)


minimax = MiniMax()
