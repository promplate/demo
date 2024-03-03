from promplate import Message
from promplate.llm.base import AsyncComplete, AsyncGenerate
from promplate.llm.openai import AsyncChatComplete, AsyncChatGenerate, AsyncChatOpenAI
from promplate_trace.auto import patch

from ..config import env
from .common import client
from .dispatch import link_llm

OCTOAI_BASE_URL = "https://text.octoai.run/v1"

complete: AsyncComplete = AsyncChatComplete(http_client=client, base_url=OCTOAI_BASE_URL, api_key=env.octoai_api_key)
generate: AsyncGenerate = AsyncChatGenerate(http_client=client, base_url=OCTOAI_BASE_URL, api_key=env.octoai_api_key)


@link_llm("mixtral")
@link_llm("nous-hermes")
class OctoAI(AsyncChatOpenAI):
    async def complete(self, prompt: str | list[Message], /, **config):
        config = self._run_config | config
        return (await complete(prompt, **config)).removeprefix(" ")

    async def generate(self, prompt: str | list[Message], /, **config):
        config = self._run_config | config

        first_token = True

        async for token in generate(prompt, **config):
            if token and first_token:
                first_token = False
                yield token.removeprefix(" ")
            else:
                yield token

    def bind(self, **run_config):  # type: ignore
        self._run_config.update(run_config)  # inplace
        return self


octoai = OctoAI().bind(model="nous-hermes-2-mixtral-8x7b-dpo")


octoai.complete = patch.chat.acomplete(octoai.complete)  # type: ignore
octoai.generate = patch.chat.agenerate(octoai.generate)  # type: ignore
