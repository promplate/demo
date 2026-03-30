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
@link_llm("qwen/qwen3.6-plus-preview:free")
@link_llm("stepfun/step-3.5-flash:free")
@link_llm("arcee-ai/trinity-mini:free")
@link_llm("nvidia/nemotron-3-nano-30b-a3b:free")
@link_llm("nvidia/nemotron-3-super-120b-a12b:free")
class OpenRouter(AsyncChatOpenAI):
    complete = staticmethod(patch.chat.acomplete(llm.complete))
    generate = staticmethod(patch.chat.agenerate(llm.generate))


openrouter = OpenRouter()
