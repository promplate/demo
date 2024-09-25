from promplate import Message
from promplate.llm.openai import AsyncChatComplete, AsyncChatGenerate, AsyncChatOpenAI
from promplate_trace.auto import patch

from ..config import env
from .common import client
from .dispatch import link_llm

complete = AsyncChatComplete(http_client=client, base_url=env.cerebras_base_url, api_key=env.cerebras_api_key)
generate = AsyncChatGenerate(http_client=client, base_url=env.cerebras_base_url, api_key=env.cerebras_api_key)


@link_llm("llama3.1")
class Cerebras(AsyncChatOpenAI):
    async def complete(self, prompt: str | list[Message], /, **config):
        config = self._run_config | config
        return (await complete(prompt, **config)).removeprefix(" ")

    async def generate(self, prompt: str | list[Message], /, **config):
        config = self._run_config | config

        if config.get("response_format") == {"type": "json_object"}:
            # streaming json is not supported
            yield await complete(prompt, **config)
            return

        async for token in generate(prompt, **config):
            yield token

    def bind(self, **run_config):  # type: ignore
        self._run_config.update(run_config)  # inplace
        return self


cerebras = Cerebras()


cerebras.complete = patch.chat.acomplete(cerebras.complete)  # type: ignore
cerebras.generate = patch.chat.agenerate(cerebras.generate)  # type: ignore
