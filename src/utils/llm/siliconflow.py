from promplate import Message
from promplate.llm.openai import AsyncChatComplete, AsyncChatGenerate, AsyncChatOpenAI
from promplate_trace.auto import patch

from ..config import env
from .common import client, trim_start
from .dispatch import link_llm

complete = AsyncChatComplete(http_client=client, base_url=env.siliconflow_base_url, api_key=env.siliconflow_api_key)
generate = AsyncChatGenerate(http_client=client, base_url=env.siliconflow_base_url, api_key=env.siliconflow_api_key)


@link_llm("Qwen/")
@link_llm("THUDM/")
@link_llm("deepseek-ai/")
@link_llm("internlm/")
class Siliconflow(AsyncChatOpenAI):
    @trim_start
    async def complete(self, prompt: str | list[Message], /, **config):
        config = self._run_config | config
        return await complete(prompt, **config)

    @trim_start
    async def generate(self, prompt: str | list[Message], /, **config):
        config = self._run_config | config

        async for token in generate(prompt, **config):
            yield token

    def bind(self, **run_config):
        self._run_config.update(run_config)  # inplace
        return self


siliconflow = Siliconflow()


siliconflow.complete = patch.chat.acomplete(siliconflow.complete)  # type: ignore
siliconflow.generate = patch.chat.agenerate(siliconflow.generate)  # type: ignore
