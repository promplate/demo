from promplate.llm.openai import AsyncChatOpenAI
from promplate_trace.auto import patch

from ..config import env
from .common import client
from .dispatch import link_llm

llm = AsyncChatOpenAI(
    http_client=client,
    base_url=env.openrouter_base_url,
    api_key=env.openrouter_api_key,
    default_headers={
        # Site information for rankings on openrouter.ai
        "HTTP-Referer": "https://promplate.dev",
        "X-Title": "Promplate",
    },
)


@link_llm("microsoft/mai-ds-r1:free")
@link_llm("deepseek/deepseek-r1-0528:free")
@link_llm("deepseek/deepseek-chat-v3-0324:free")
@link_llm("meta-llama/llama-4-scout:free")
@link_llm("meta-llama/llama-4-maverick:free")
class OpenRouter(AsyncChatOpenAI):
    complete = staticmethod(patch.chat.acomplete(llm.complete))
    generate = staticmethod(patch.chat.agenerate(llm.generate))


openrouter = OpenRouter()
