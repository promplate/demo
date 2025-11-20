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
@link_llm("z-ai/glm-4.5-air:free")
@link_llm("qwen/qwen3-coder:free")
@link_llm("kwaipilot/kat-coder-pro:free")
@link_llm("alibaba/tongyi-deepresearch-30b-a3b:free")
@link_llm("meituan/longcat-flash-chat:free")
@link_llm("x-ai/grok-4.1-fast:free")
@link_llm("openrouter/")
class OpenRouter(AsyncChatOpenAI):
    complete = staticmethod(patch.chat.acomplete(llm.complete))
    generate = staticmethod(patch.chat.agenerate(llm.generate))


openrouter = OpenRouter()
