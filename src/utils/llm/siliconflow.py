from promplate import Message
from promplate.llm.openai import AsyncChatComplete, AsyncChatGenerate, AsyncChatOpenAI
from promplate_trace.auto import patch

from ..config import env
from .common import client
from .dispatch import link_llm

complete = AsyncChatComplete(http_client=client, base_url=env.siliconflow_base_url, api_key=env.siliconflow_api_key)
generate = AsyncChatGenerate(http_client=client, base_url=env.siliconflow_base_url, api_key=env.siliconflow_api_key)


@link_llm("Qwen/")
@link_llm("01-ai/")
@link_llm("THUDM/")
@link_llm("deepseek-ai/")
class Siliconflow(AsyncChatOpenAI):
    async def complete(self, prompt: str | list[Message], /, **config):
        config = self._run_config | config
        return await complete(prompt, **config)

    async def generate(self, prompt: str | list[Message], /, **config):
        config = self._run_config | config

        async for token in generate(prompt, **config):
            yield token

    def bind(self, **run_config):  # type: ignore
        self._run_config.update(run_config)  # inplace
        return self


siliconflow = Siliconflow()


siliconflow.complete = patch.chat.acomplete(siliconflow.complete)  # type: ignore
siliconflow.generate = patch.chat.agenerate(siliconflow.generate)  # type: ignore
