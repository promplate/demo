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
        "HTTP-Referer": "https://github.com/promplate",
        "X-Title": "Promplate",
    },
)


@link_llm("z-ai/glm-4.5-air:free")
@link_llm("qwen/qwen3-coder:free")
@link_llm("kwaipilot/kat-coder-pro:free")
@link_llm("alibaba/tongyi-deepresearch-30b-a3b:free")
@link_llm("allenai/olmo-3-32b-think:free")
@link_llm("arcee-ai/trinity-mini:free")
@link_llm("tngtech/tng-r1t-chimera:free")
@link_llm("amazon/nova-2-lite-v1:free")
@link_llm("mistralai/devstral-2512:free")
@link_llm("nex-agi/deepseek-v3.1-nex-n1:free")
@link_llm("nvidia/nemotron-3-nano-30b-a3b:free")
@link_llm("xiaomi/mimo-v2-flash:free")
class OpenRouter(AsyncChatOpenAI):
    complete = staticmethod(patch.chat.acomplete(llm.complete))
    generate = staticmethod(patch.chat.agenerate(llm.generate))


openrouter = OpenRouter()
