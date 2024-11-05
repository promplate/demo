from promplate import Message
from promplate.llm.openai import AsyncChatComplete, AsyncChatGenerate, AsyncChatOpenAI
from promplate.prompt.chat import ensure
from promplate_trace.auto import patch

from ..config import env
from .common import client
from .dispatch import link_llm

complete = AsyncChatComplete(http_client=client, base_url=env.xai_base_url, api_key=env.xai_api_key)
generate = AsyncChatGenerate(http_client=client, base_url=env.xai_base_url, api_key=env.xai_api_key)


def _patch_roles(prompt: str | list[Message]):
    for message in (messages := ensure(prompt)):
        if "name" in message:
            message["role"] = "user"  # Client specified an invalid argument: Only messages of role 'user' can have a name.

    return messages


@link_llm("grok")
class XAI(AsyncChatOpenAI):
    async def complete(self, prompt: str | list[Message], /, **config):
        config = self._run_config | config
        return await complete(_patch_roles(prompt), **config)

    async def generate(self, prompt: str | list[Message], /, **config):
        config = self._run_config | config

        async for token in generate(_patch_roles(prompt), **config):
            yield token

    def bind(self, **run_config):
        self._run_config.update(run_config)  # inplace
        return self


xai = XAI()


xai.complete = patch.chat.acomplete(xai.complete)  # type: ignore
xai.generate = patch.chat.agenerate(xai.generate)  # type: ignore
