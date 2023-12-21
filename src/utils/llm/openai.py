from httpx import AsyncClient
from promplate.llm.openai import AsyncChatComplete, AsyncChatGenerate, AsyncChatOpenAI
from promplate_trace.auto import patch

client = AsyncClient(http2=True)

complete = patch.chat.acomplete(AsyncChatComplete(http_client=client))
generate = patch.chat.agenerate(AsyncChatGenerate(http_client=client))

"""This class is a wrapper for the OpenAI API. It provides methods for generating and completing prompts using the OpenAI model."""


class OpenAI(AsyncChatOpenAI):
    def complete(self, prompt, /, **config):  # type: ignore
        config = self._run_config | config
        return complete(prompt, **config)

    def generate(self, prompt: str, /, **config):  # type: ignore
        config = self._run_config | config
        return generate(prompt, **config)


openai = OpenAI().bind(
    model="gpt-3.5-turbo-1106",
    temperature=0.7,
    # response_format={"type": "json_object"},
)
