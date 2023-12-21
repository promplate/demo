from httpx import AsyncClient
from typing import Any
from promplate.llm.openai import AsyncChatComplete, AsyncChatGenerate, AsyncChatOpenAI
from promplate_trace.auto import patch

from .dispatch import link_llm

client = AsyncClient(http2=True)

complete = patch.chat.acomplete(AsyncChatComplete(http_client=client))
generate = patch.chat.agenerate(AsyncChatGenerate(http_client=client))


@link_llm("gpt")
class OpenAI(AsyncChatOpenAI):
    async def generate(self, prompt: str, **config) -> Any:
        """
        Asynchronously generates a response from the OpenAI model based on the given prompt.

        Parameters:
            prompt (str): The input text prompt to guide the model's response generation.
            config (dict): Additional optional keyword arguments to configure the model's response.

        Returns:
            Any: The generated response from the OpenAI model as specified by the input prompt and configuration, as an asynchronous operation.
        """  # type: ignore
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
