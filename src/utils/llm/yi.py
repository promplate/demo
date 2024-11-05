from promplate import Message
from promplate.llm.openai import AsyncChatComplete, AsyncChatGenerate, AsyncChatOpenAI
from promplate_trace.auto import patch

from ..config import env
from .common import client
from .dispatch import link_llm

complete = AsyncChatComplete(http_client=client, base_url=env.yi_base_url, api_key=env.yi_api_key)
generate = AsyncChatGenerate(http_client=client, base_url=env.yi_base_url, api_key=env.yi_api_key)


@link_llm("yi")
class Yi(AsyncChatOpenAI):
    async def complete(self, prompt: str | list[Message], /, **config):
        config = self._run_config | config
        return await complete(prompt, **config)

    async def generate(self, prompt: str | list[Message], /, **config):
        config = self._run_config | config

        async for token in generate(prompt, **config):
            yield token

    def bind(self, **run_config):
        self._run_config.update(run_config)  # inplace
        return self


yi = Yi()


yi.complete = patch.chat.acomplete(yi.complete)  # type: ignore
yi.generate = patch.chat.agenerate(yi.generate)  # type: ignore
