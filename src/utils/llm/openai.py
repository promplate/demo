from promplate.llm.openai import AsyncChatComplete, AsyncChatGenerate, AsyncChatOpenAI
from promplate_trace.auto import patch

from .common import client
from .dispatch import link_llm

complete = patch.chat.acomplete(AsyncChatComplete(http_client=client))
generate = patch.chat.agenerate(AsyncChatGenerate(http_client=client))


@link_llm("gpt")
class OpenAI(AsyncChatOpenAI):
    def generate(self, prompt: str, /, **config):  # type: ignore
        config = self._run_config | config
        return generate(prompt, **config)

    def bind(self, **run_config):  # type: ignore
        self._run_config.update(run_config)  # inplace
        return self


openai = OpenAI().bind(
    model="gpt-3.5-turbo-1106",
    temperature=0.7,
    # response_format={"type": "json_object"},
)
