from promplate import Message
from promplate.llm.openai import AsyncChatComplete, AsyncChatGenerate, AsyncChatOpenAI
from promplate_trace.auto import patch

from ..config import env
from .common import client
from .dispatch import link_llm

complete = AsyncChatComplete(http_client=client, base_url=env.groq_base_url, api_key=env.groq_api_key)
generate = AsyncChatGenerate(http_client=client, base_url=env.groq_base_url, api_key=env.groq_api_key)


@link_llm("gemma")
@link_llm("llama")
@link_llm("mixtral")
class Groq(AsyncChatOpenAI):
    async def complete(self, prompt: str | list[Message], /, **config):
        config = self._run_config | config
        return (await complete(prompt, **config)).removeprefix(" ")

    async def generate(self, prompt: str | list[Message], /, **config):
        config = self._run_config | config

        async for token in generate(prompt, **config):
            yield token

    def bind(self, **run_config):  # type: ignore
        self._run_config.update(run_config)  # inplace
        return self


groq = Groq().bind(model="mixtral-8x7b-32768")


groq.complete = patch.chat.acomplete(groq.complete)  # type: ignore
groq.generate = patch.chat.agenerate(groq.generate)  # type: ignore
