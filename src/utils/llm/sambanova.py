from promplate.llm.openai import AsyncChatComplete, AsyncChatGenerate, AsyncChatOpenAI
from promplate_trace.auto import patch

from ..config import env
from .common import client
from .dispatch import link_llm


@link_llm("Qwen2.5")
@link_llm("QwQ")
@link_llm("Llama-3")
@link_llm("Meta-Llama-3.2")
@link_llm("Meta-Llama-3.3")
@link_llm("DeepSeek-R1-Distill")
class SambaNova(AsyncChatOpenAI):
    complete = staticmethod(
        patch.chat.acomplete(
            AsyncChatComplete(http_client=client, base_url=env.sambanova_base_url, api_key=env.sambanova_api_key)
        )
    )
    generate = staticmethod(
        patch.chat.agenerate(
            AsyncChatGenerate(http_client=client, base_url=env.sambanova_base_url, api_key=env.sambanova_api_key)
        )
    )


sambanova = SambaNova()
