from promplate.llm.openai import AsyncChatComplete, AsyncChatGenerate, AsyncChatOpenAI
from promplate_trace.auto import patch

from ..config import env
from .common import client
from .dispatch import link_llm

complete = patch.chat.acomplete(
    AsyncChatComplete(http_client=client, base_url=env.github_models_base_url, api_key=env.github_models_api_key)
)
generate = patch.chat.agenerate(
    AsyncChatGenerate(http_client=client, base_url=env.github_models_base_url, api_key=env.github_models_api_key)
)


@link_llm("azure:o1")
@link_llm("azure:o3")
@link_llm("azure:gpt")
@link_llm("Ministral")
@link_llm("Codestral")
@link_llm("Mistral")
@link_llm("Meta")
@link_llm("Cohere")
@link_llm("AI21")
@link_llm("Phi")
@link_llm("DeepSeek")
class AzureOpenAI(AsyncChatOpenAI):
    @staticmethod
    async def generate(prompt, **kwargs):
        kwargs["model"] = kwargs["model"].replace("azure:", "")
        async for token in generate(prompt, **kwargs):
            yield token

    @staticmethod
    async def complete(prompt, **kwargs):
        kwargs["model"] = kwargs["model"].replace("azure:", "")
        return await complete(prompt, **kwargs)


azure = AzureOpenAI()
