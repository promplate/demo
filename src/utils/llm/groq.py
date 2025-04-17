from promplate import Message
from promplate.llm.openai import AsyncChatComplete, AsyncChatGenerate, AsyncChatOpenAI
from promplate.prompt.chat import ensure
from promplate_trace.auto import patch

from .. import prefill
from ..config import env
from .common import client
from .dispatch import link_llm

complete = AsyncChatComplete(http_client=client, base_url=env.groq_base_url, api_key=env.groq_api_key)
generate = AsyncChatGenerate(http_client=client, base_url=env.groq_base_url, api_key=env.groq_api_key)


@link_llm("gemma")
@link_llm("llama3-")
@link_llm("llama-3.1")
@link_llm("llama-3.3-70b-")
@link_llm("meta-llama/llama-4")
@link_llm("qwen-qwq")
@link_llm("deepseek-r1-distill")
class Groq(AsyncChatOpenAI):
    async def complete(self, prompt: str | list[Message], /, **config):
        config = self._run_config | config
        return await complete(prompt, **config)

    async def generate(self, prompt: str | list[Message], /, **config):
        config = self._run_config | config

        if config.get("response_format") == {"type": "json_object"}:
            # streaming json is not supported
            yield await complete(prompt, **config)
            return

        async for token in generate(prompt, **config):
            yield token

    def bind(self, **run_config):
        self._run_config.update(run_config)  # inplace
        return self


groq = Groq()


groq.complete = prefill.patch_async_complete(patch.chat.acomplete(groq.complete))  # type: ignore
groq.generate = prefill.patch_async_generate(patch.chat.agenerate(groq.generate))  # type: ignore
