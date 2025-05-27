from promplate.llm.openai import AsyncChatComplete, AsyncChatGenerate, AsyncChatOpenAI
from promplate_trace.auto import patch

from .common import client

complete = patch.chat.acomplete(AsyncChatComplete(http_client=client))
generate = patch.chat.agenerate(AsyncChatGenerate(http_client=client))


class OpenAI(AsyncChatOpenAI):
    def generate(self, prompt: str, /, **config):
        config = self._run_config | config
        return generate(prompt, **config)

    def complete(self, prompt: str, /, **config):
        config = self._run_config | config
        return complete(prompt, **config)

    def bind(self, **run_config):
        self._run_config.update(run_config)  # inplace
        return self


openai = OpenAI().bind(model="gpt-4.1-nano", temperature=0.7)
